#!/usr/bin/env python3
"""Check question files against the getazcertified question rules.

    python3 scripts/check_questions.py            # rules only (fast, offline)
    python3 scripts/check_questions.py --links    # also check every Learn link answers 200

Standard library only. The frontmatter reader accepts a deliberately small YAML subset
(see questions/README.md): `key: "value"` lines, `question: |-` blocks and a
`documentation:` list of `  - "url"` lines. Anything
else is reported instead of guessed at. Parsing compatibility with mdquiz itself is
covered separately by app/src/lib/__tests__/questions.test.ts.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "questions"

STUDY_GUIDES = {"az-104": "2026-04-17"}

# AZ-104 skills measured (study guide 2026-04-17): functional group -> skill areas.
SKILL_AREAS = {
    "az-104": {
        "identity-governance": [
            "entra-users-groups",
            "access-azure-resources",
            "subscriptions-governance",
        ],
        "storage": [
            "storage-access",
            "storage-accounts",
            "files-blob",
        ],
        "compute": [
            "arm-bicep",
            "virtual-machines",
            "containers",
            "app-service",
        ],
        "virtual-networking": [
            "virtual-networks",
            "secure-vnet-access",
            "name-resolution-load-balancing",
        ],
        "monitor-maintain": [
            "monitor-resources",
            "backup-recovery",
        ],
    }
}

# Study-guide weight ranges per functional group, in percent.
WEIGHTS = {
    "az-104": {
        "identity-governance": (20, 25),
        "storage": (15, 20),
        "compute": (20, 25),
        "virtual-networking": (15, 20),
        "monitor-maintain": (10, 15),
    }
}

ARCHETYPES = {
    "best-choice",         # requirements, then "What should you use / do first?"
    "exhibit-select",      # exhibit, then pick the item or set that qualifies
    "exhibit-statement",   # exhibit, then one statement to judge Yes / No
    "complete-statement",  # exhibit, then complete a sentence with the right value
    "complete-code",       # complete a command, template or rule
    "calculate",           # work out a number from the scenario
    "goal-solution",       # proposed solution: does it meet the goal?
    "choose-n",            # "Which two ...?" multi-select
    "fact-recall",         # one fact, no scenario
}

REQUIRED_KEYS = ("question", "documentation", "skill_area", "study_guide", "archetype")
OPTIONAL_KEYS = ("series",)
LEARN_PREFIX = "https://learn.microsoft.com/"
MAX_DOC_LINKS = 3
NUMBER_WORDS = {"two": 2, "three": 3, "four": 4}
COUNT_RE = re.compile(r"\b(?:Which|What)\s+(two|three|four)\b", re.IGNORECASE)
ANSWER_RE = re.compile(r"^(?:\d+\.|-) \[([xX ]?)\] (.*)$")
LINK_RE = re.compile(r"https://learn\.microsoft\.com/[^\s)\]>\"']+")


@dataclass
class Question:
    path: Path
    cert: str
    meta: dict[str, str | list[str]] = field(default_factory=dict)
    answers: list[tuple[bool, str, str]] = field(default_factory=list)  # correct, text, explanation
    body: str = ""


class FormatError(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str | list[str]], str]:
    if not text.startswith("---\n"):
        raise FormatError("file must start with a '---' frontmatter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise FormatError("frontmatter is not closed by a '---' line")
    lines = text[4:end].split("\n")
    body = text[end + 5 :]
    meta: dict[str, str | list[str]] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.fullmatch(r'([a-z_]+): "(.*)"', line)
        if m:
            key, value = m.groups()
            if '"' in value.replace('\\"', ""):
                raise FormatError(f"line {i + 2}: unescaped quote in {key}")
            meta[key] = value.replace('\\"', '"')
            i += 1
            continue
        m = re.fullmatch(r"([a-z_]+):", line)
        if m:
            key = m.group(1)
            items: list[str] = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                im = re.fullmatch(r'  - "([^"]*)"', lines[i])
                if not im:
                    raise FormatError(f'line {i + 2}: list items must be  - "value": {lines[i]!r}')
                items.append(im.group(1))
                i += 1
            meta[key] = items
            continue
        m = re.fullmatch(r"([a-z_]+): \|-", line)
        if m:
            key = m.group(1)
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""):
                block.append(lines[i][2:] if lines[i] else "")
                i += 1
            meta[key] = "\n".join(block).strip("\n")
            continue
        raise FormatError(
            f"frontmatter line {i + 2} is outside the allowed subset "
            f'(key: "value", key: |- or a key: list): {line!r}'
        )
    return meta, body


def parse_answers(body: str) -> list[tuple[bool, str, str]]:
    answers: list[list] = []
    in_fence = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ANSWER_RE.match(line)
        if m:
            answers.append([m.group(1).lower() == "x", m.group(2).strip(), []])
        elif answers and line.strip().startswith(">"):
            answers[-1][2].append(line.strip()[1:].strip())
    return [(c, t, " ".join(e).strip()) for c, t, e in answers]


def load(path: Path) -> Question:
    cert = path.parent.name
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    return Question(path=path, cert=cert, meta=meta, answers=parse_answers(body), body=body)


def domain_of(cert: str, skill_area: str) -> str | None:
    for domain, areas in SKILL_AREAS.get(cert, {}).items():
        if skill_area in areas:
            return domain
    return None


def check(q: Question) -> list[str]:
    errs: list[str] = []
    m = q.meta
    for key in REQUIRED_KEYS:
        if not m.get(key):
            errs.append(f"missing {key}")
    for key in m:
        if key not in REQUIRED_KEYS + OPTIONAL_KEYS:
            errs.append(f"unknown frontmatter key {key}")
    for key, value in m.items():
        if isinstance(value, list) and key != "documentation":
            errs.append(f"{key} must be a single value, not a list")
    if errs:
        return errs
    doc = m.get("documentation", "")
    docs = doc if isinstance(doc, list) else [doc] if doc else []
    if len(docs) > MAX_DOC_LINKS:
        errs.append(f"documentation has {len(docs)} links, at most {MAX_DOC_LINKS}")
    if len(set(docs)) != len(docs):
        errs.append("documentation lists the same link twice")
    for url in docs:
        if not url.startswith(LEARN_PREFIX):
            errs.append(f"documentation must be a {LEARN_PREFIX} URL: {url}")
    if m.get("skill_area") and domain_of(q.cert, m["skill_area"]) is None:
        errs.append(f"unknown skill_area {m['skill_area']!r} for {q.cert}")
    if m.get("archetype") and m["archetype"] not in ARCHETYPES:
        errs.append(f"unknown archetype {m['archetype']!r}")
    expected_guide = STUDY_GUIDES.get(q.cert)
    if expected_guide and m.get("study_guide") and m["study_guide"] != expected_guide:
        errs.append(f"study_guide must be {expected_guide!r}")

    if len(q.answers) < 2:
        errs.append("needs at least 2 answers")
    correct = sum(1 for c, _, _ in q.answers if c)
    if correct == 0:
        errs.append("has no correct answer")
    for n, (_, text, expl) in enumerate(q.answers, 1):
        if not expl:
            errs.append(f"answer {n} ({text[:40]!r}) has no explanation")
    texts = [t for _, t, _ in q.answers]
    if len(set(texts)) != len(texts):
        errs.append("duplicate answer text")

    stem = m.get("question", "")
    stem_lines = stem.split("\n")
    for a, b in zip(stem_lines, stem_lines[1:]):
        if a.strip() and b.strip() and not b.startswith("- "):
            errs.append(f"question text is hard-wrapped (one line per paragraph): {b[:40]!r}")
            break
    cm = COUNT_RE.search(stem)
    if cm:
        want = NUMBER_WORDS[cm.group(1).lower()]
        if correct != want:
            errs.append(f"stem asks for {cm.group(1)} answers but {correct} are marked correct")
    elif correct > 1:
        errs.append("several answers are correct but the stem doesn't say 'Which two/three ...'")
    if m.get("archetype") == "choose-n" and not cm:
        errs.append("choose-n question must ask 'Which two/three ...'")
    if m.get("archetype") in ("exhibit-statement", "goal-solution") and sorted(texts) != ["No", "Yes"]:
        errs.append(f"{m['archetype']} answers must be exactly Yes and No")
    if m.get("archetype", "").startswith("exhibit") and "```" not in q.body:
        errs.append("exhibit question has no exhibit block")
    return errs


def check_weights(questions: list[Question]) -> list[str]:
    errs: list[str] = []
    by_cert: dict[str, list[Question]] = {}
    for q in questions:
        by_cert.setdefault(q.cert, []).append(q)
    for cert, qs in by_cert.items():
        if cert not in WEIGHTS:
            continue
        counts: dict[str, int] = {}
        for q in qs:
            d = domain_of(cert, q.meta.get("skill_area", ""))
            if d:
                counts[d] = counts.get(d, 0) + 1
        if any(counts.get(d, 0) == 0 for d in WEIGHTS[cert]):
            continue  # a set still being built domain by domain: weights apply once every group has questions
        for domain, (lo, hi) in WEIGHTS[cert].items():
            pct = 100 * counts.get(domain, 0) / len(qs)
            if not lo <= pct <= hi:
                errs.append(f"{cert}: {domain} is {pct:.1f}% of {len(qs)} questions, study guide says {lo}-{hi}%")
    return errs


def check_links(questions: list[Question]) -> list[str]:
    urls: dict[str, list[str]] = {}
    for q in questions:
        found = set(LINK_RE.findall(q.path.read_text(encoding="utf-8")))
        for u in found:
            urls.setdefault(u.rstrip(".,"), []).append(q.path.name)
    errs: list[str] = []
    for url, files in sorted(urls.items()):
        page = url.split("#", 1)[0]
        req = urllib.request.Request(page, headers={"User-Agent": "getazcertified-link-check"})
        status = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    status = resp.status
                break
            except urllib.error.HTTPError as e:
                status = e.code
                if e.code < 500 and e.code != 429:
                    break
            except (urllib.error.URLError, TimeoutError) as e:
                status = f"error {e}"
            time.sleep(2 * (attempt + 1))
        if status != 200:
            errs.append(f"{url} -> {status} (in {', '.join(sorted(set(files)))})")
        time.sleep(0.2)
    print(f"checked {len(urls)} Learn links")
    return errs


def find_files(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths]
    return sorted(QUESTIONS.glob("*/*/question-*.md"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("files", nargs="*", help="question files (default: all)")
    ap.add_argument("--links", action="store_true", help="also check that every Learn link answers 200")
    args = ap.parse_args(argv)

    files = find_files(args.files)
    problems: list[str] = []
    questions: list[Question] = []
    for path in files:
        try:
            q = load(path)
        except FormatError as e:
            problems.append(f"{path.relative_to(ROOT)}: {e}")
            continue
        questions.append(q)
        if q.cert not in SKILL_AREAS:
            continue  # rules apply to certs with a study guide; others are parse-checked only
        for err in check(q):
            problems.append(f"{path.relative_to(ROOT)}: {err}")
    if not args.files:
        problems += check_weights([q for q in questions if q.cert in SKILL_AREAS])
    if args.links:
        problems += check_links([q for q in questions if q.cert in SKILL_AREAS])

    for p in problems:
        print(p)
    print(f"{len(files)} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
