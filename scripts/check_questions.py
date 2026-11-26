#!/usr/bin/env python3
"""Check question files against the getazcertified question rules.

    python3 scripts/check_questions.py            # rules only (fast, offline)
    python3 scripts/check_questions.py --links    # also check every Learn link answers 200

Standard library only. The frontmatter reader accepts a deliberately small YAML subset
(see questions/README.md): `key: "value"` lines, `question: |-` blocks and a
`documentation:` list of `  - title: "…"` / `    url: "…"` pairs. Anything
else is reported instead of guessed at. Parsing compatibility with mdquiz itself is
covered separately by app/src/lib/__tests__/questions.test.ts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "questions"

CERTS_DIR = QUESTIONS / "certs"
LEARN_PREFIX = "https://learn.microsoft.com/"

# Certifications are data: one questions/certs/<cert>.json each (see CONTRIBUTING.md › Propose a new certification).
# The app builds its catalog from the same files.
CERT_STATUSES = ("draft", "live")
CERT_COLORS = range(1, 9)  # palette slots --cert-1..8 in app/src/app/globals.css (the CSP forbids inline colours)
CERT_ICONS = (  # lucide icons the app maps (app/src/lib/cert-meta.tsx); generic glyphs, never Microsoft logos
    "server-cog", "shield-check", "network", "database", "brain", "cloud", "code", "lock",
    "workflow", "chart-line", "key-round", "boxes",
)
CERT_ID_RE = re.compile(r"^[a-z]{2,4}-\d{3}$")  # exam code, e.g. az-104, sc-500
MIN_LIVE_QUESTIONS = 20
CERT_EXAMPLE = "questions/certs/az-104.json"


def load_certs(certs_dir: Path | None = None) -> tuple[dict[str, dict], list[str]]:
    """Read every questions/certs/*.json; return {id: cert} and the problems found (with how to fix them)."""
    certs_dir = certs_dir or CERTS_DIR
    certs: dict[str, dict] = {}
    errs: list[str] = []
    for path in sorted(certs_dir.glob("*.json")):
        where = f"questions/certs/{path.name}"
        try:
            c = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errs.append(f"{where}: not valid JSON ({e.msg} at line {e.lineno}); compare with {CERT_EXAMPLE}")
            continue
        if not isinstance(c, dict):
            errs.append(f"{where}: must be a JSON object like {CERT_EXAMPLE}")
            continue
        missing = [k for k in ("id", "title", "description", "status", "study_guide", "color", "icon", "domains") if k not in c]
        if missing:
            errs.append(f"{where}: missing {', '.join(missing)}; copy the shape of {CERT_EXAMPLE}")
            continue
        cid = c["id"]
        if cid != path.stem:
            errs.append(f"{where}: id {cid!r} must match the file name ({path.stem!r})")
        if not isinstance(cid, str) or not CERT_ID_RE.match(cid):
            errs.append(f"{where}: id {cid!r} must be the lowercase exam code, e.g. \"az-104\" or \"sc-500\"")
        if c["status"] not in CERT_STATUSES:
            errs.append(f"{where}: status must be \"draft\" (new, hidden on the site) or \"live\" (maintainers only)")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c["study_guide"])):
            errs.append(f"{where}: study_guide must be the date of the official study guide's skills list, YYYY-MM-DD")
        if c["color"] not in CERT_COLORS:
            errs.append(f"{where}: color must be a palette slot from 1 to 8 (see app/src/app/globals.css)")
        if c["icon"] not in CERT_ICONS:
            errs.append(f"{where}: icon {c['icon']!r} isn't available; pick one of: {', '.join(CERT_ICONS)}")
        if not 10 <= len(str(c["title"])) <= 60:
            errs.append(f"{where}: title should read like \"Azure Administrator (AZ-104)\" (10-60 characters)")
        if not 20 <= len(str(c["description"])) <= 200:
            errs.append(f"{where}: description is one sentence about what the exam covers (20-200 characters)")
        url = c.get("study_guide_url", "")
        if url and not str(url).startswith(LEARN_PREFIX):
            errs.append(f"{where}: study_guide_url must be a {LEARN_PREFIX} page")
        domains = c["domains"] if isinstance(c["domains"], list) else []
        if not domains:
            errs.append(f"{where}: domains lists the study guide's skill groups, each with id, name, weight and skill_areas")
        seen_areas: set[str] = set()
        for n, d in enumerate(domains, 1):
            if not isinstance(d, dict) or not {"id", "name", "weight", "skill_areas"} <= set(d):
                errs.append(f"{where}: domains[{n}] needs id, name, weight [min, max] and skill_areas")
                continue
            w = d["weight"]
            if not (isinstance(w, list) and len(w) == 2 and all(isinstance(x, int) for x in w) and 0 < w[0] <= w[1] <= 100):
                errs.append(f"{where}: domains[{n}].weight must be [min, max] percent from the study guide, e.g. [15, 20]")
            for area in d["skill_areas"] if isinstance(d["skill_areas"], list) else []:
                if area in seen_areas:
                    errs.append(f"{where}: skill area {area!r} appears in two domains")
                seen_areas.add(area)
        if not errs or not any(e.startswith(where) for e in errs):
            certs[cid] = c
    return certs, errs


CERTS, CERT_ERRORS = load_certs()
STUDY_GUIDES = {cid: c["study_guide"] for cid, c in CERTS.items()}
SKILL_AREAS = {cid: {d["id"]: list(d["skill_areas"]) for d in c["domains"]} for cid, c in CERTS.items()}
WEIGHTS = {cid: {d["id"]: tuple(d["weight"]) for d in c["domains"]} for cid, c in CERTS.items()}

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
MAX_DOC_LINKS = 3
DOC_TITLE_MIN = 3
DOC_TITLE_MAX = 40  # fits one line of the "Learn more in the docs" menu, also on a phone
DOC_MAIN_TITLE_MAX = 30  # the main page shares its menu line with the "Main page" tag (only shown with 2+ links)
DOC_EXAMPLE = '  - title: "Share-level permissions"\n    url: "https://learn.microsoft.com/en-us/azure/..."'
# Words that only repeat what the menu already says, or leftovers of a Learn page title ("... - Azure Monitor").
DOC_TITLE_FILLER = re.compile(r"microsoft learn|\bdocs?\b|\bdocumentation\b|\s-\s|\|", re.IGNORECASE)
NUMBER_WORDS = {"two": 2, "three": 3, "four": 4}
COUNT_RE = re.compile(r"\b(?:Which|What)\s+(two|three|four)\b", re.IGNORECASE)
ANSWER_RE = re.compile(r"^(?:\d+\.|-) \[([xX ]?)\] (.*)$")
LINK_RE = re.compile(r"https://learn\.microsoft\.com/[^\s)\]>\"']+")


@dataclass
class Question:
    path: Path
    cert: str
    meta: dict[str, str | list] = field(default_factory=dict)
    answers: list[tuple[bool, str, str]] = field(default_factory=list)  # correct, text, explanation
    body: str = ""


class FormatError(Exception):
    pass


def parse_documentation(lines: list[str], i: int) -> tuple[list[dict[str, str]], int]:
    """Read `  - title: "…"` + `    url: "…"` pairs starting at lines[i]; return the entries and the next index."""
    entries: list[dict[str, str]] = []
    while i < len(lines) and lines[i].startswith("  "):
        n = len(entries) + 1
        tm = re.fullmatch(r'  - title: "([^"]*)"', lines[i])
        if not tm:
            raise FormatError(
                f"line {i + 2}: documentation entry {n} must start with a title line, then a url line:\n{DOC_EXAMPLE}\n"
                f"got: {lines[i]!r}"
            )
        um = re.fullmatch(r'    url: "([^"]*)"', lines[i + 1]) if i + 1 < len(lines) else None
        if not um:
            raise FormatError(
                f"line {i + 3}: documentation entry {n} needs a url line right under its title "
                f'(4 spaces, then url: "https://learn.microsoft.com/...")'
            )
        entries.append({"title": tm.group(1), "url": um.group(1)})
        i += 2
    return entries, i


def parse_frontmatter(text: str) -> tuple[dict[str, str | list], str]:
    if not text.startswith("---\n"):
        raise FormatError("file must start with a '---' frontmatter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise FormatError("frontmatter is not closed by a '---' line")
    lines = text[4:end].split("\n")
    body = text[end + 5 :]
    meta: dict[str, str | list] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.fullmatch(r'([a-z_]+): "(.*)"', line)
        if m:
            key, value = m.groups()
            if '"' in value.replace('\\"', ""):
                raise FormatError(f"line {i + 2}: unescaped quote in {key}")
            if key == "documentation":
                raise FormatError(
                    f"line {i + 2}: documentation is a list of title + url entries, not a single URL:\n"
                    f"documentation:\n{DOC_EXAMPLE}"
                )
            meta[key] = value.replace('\\"', '"')
            i += 1
            continue
        if line == "documentation:":
            meta["documentation"], i = parse_documentation(lines, i + 1)
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


def check_documentation(docs: list) -> list[str]:
    errs: list[str] = []
    if len(docs) > MAX_DOC_LINKS:
        errs.append(f"documentation has {len(docs)} links, at most {MAX_DOC_LINKS}: keep the pages that back the answer")
    urls = [d["url"] for d in docs]
    titles = [d["title"].casefold() for d in docs]
    if len(set(urls)) != len(urls):
        errs.append("documentation lists the same link twice")
    if len(set(titles)) != len(titles):
        errs.append("documentation uses the same title twice: each title should say what that page is about")
    for n, d in enumerate(docs, 1):
        title, url = d["title"], d["url"]
        if not url.startswith(LEARN_PREFIX):
            errs.append(f"documentation must be a {LEARN_PREFIX} URL: {url}")
        where = f"documentation[{n}].title {title!r}"
        if n == 1 and len(docs) > 1 and len(title) > DOC_MAIN_TITLE_MAX:
            errs.append(
                f"{where} is {len(title)} characters; the main page shares its line with the \"Main page\" tag, "
                f"keep it to {DOC_MAIN_TITLE_MAX} (e.g. \"Azure Files share permissions\"). The same page keeps "
                f"that title in every question"
            )
        elif len(title) > DOC_TITLE_MAX:
            errs.append(f"{where} is {len(title)} characters; keep it to {DOC_TITLE_MAX} (e.g. \"Share-level permissions\")")
        elif len(title.strip()) < DOC_TITLE_MIN:
            errs.append(f"{where} is empty or too short: name the page's topic in a few words")
        if title != title.strip() or "  " in title:
            errs.append(f"{where} has extra spaces")
        if title.endswith("."):
            errs.append(f"{where} ends with a period; titles are labels, not sentences")
        if re.search(r"[\[\]`*_<>#]", title):
            errs.append(f"{where} contains Markdown or HTML; use plain text")
        if DOC_TITLE_FILLER.search(title):
            errs.append(f"{where} repeats filler (\"docs\", \"Microsoft Learn\", \" - Product\"): name only the topic")
        if title[:1].islower():
            errs.append(f"{where} should start with a capital letter (sentence case)")
    return errs


def rel(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def check_doc_titles(questions: list[Question], report: set[Path] | None = None) -> list[str]:
    """One page, one title: every question that links a URL uses the same title for it (first one seen wins)."""
    seen: dict[str, tuple[str, Path]] = {}
    errs: list[str] = []
    for q in sorted(questions, key=lambda q: str(q.path)):
        docs = q.meta.get("documentation", [])
        for n, d in enumerate(docs if isinstance(docs, list) else [], 1):
            if not isinstance(d, dict):
                continue
            first = seen.setdefault(d["url"], (d["title"], q.path))
            if d["title"] != first[0] and (report is None or q.path in report):
                errs.append(
                    f"{rel(q.path)}: documentation[{n}].title {d['title']!r} differs from "
                    f"{rel(first[1])}, which calls this page {first[0]!r}; use one title per page"
                )
    return errs


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
    errs += check_documentation(m.get("documentation", []))
    if m.get("skill_area") and domain_of(q.cert, m["skill_area"]) is None:
        areas = ", ".join(a for d in SKILL_AREAS.get(q.cert, {}).values() for a in d)
        errs.append(f"unknown skill_area {m['skill_area']!r} for {q.cert}; use one of: {areas}")
    if m.get("archetype") and m["archetype"] not in ARCHETYPES:
        errs.append(f"unknown archetype {m['archetype']!r}; use one of: {', '.join(sorted(ARCHETYPES))} (see questions/README.md)")
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


def load_quiet(path: Path) -> Question | None:
    try:
        return load(path)
    except FormatError:
        return None


def check_certs(everyone: list[Question]) -> list[str]:
    """Registry problems, question folders without a registry entry, and live certs that are still too small."""
    errs = list(CERT_ERRORS)
    counts: dict[str, int] = {}
    for q in everyone:
        counts[q.cert] = counts.get(q.cert, 0) + 1
    for cert in sorted(counts):
        if cert not in CERTS and not any(e.startswith(f"questions/certs/{cert}.json") for e in errs):
            errs.append(
                f"questions/certs/{cert}.json: missing; every folder under questions/<locale>/ needs a certification "
                f"file (copy {CERT_EXAMPLE}, set status \"draft\")"
            )
    for cid, c in CERTS.items():
        if c["status"] == "live" and counts.get(cid, 0) < MIN_LIVE_QUESTIONS:
            errs.append(
                f"questions/certs/{cid}.json: status \"live\" needs at least {MIN_LIVE_QUESTIONS} questions "
                f"({counts.get(cid, 0)} now); keep it \"draft\" until then"
            )
    return errs


def check_numbering(everyone: list[Question], report: set[Path] | None = None) -> list[str]:
    """Question numbers per certification run 001, 002, … without gaps, so the next free number is obvious."""
    errs: list[str] = []
    by_cert: dict[str, list[tuple[int, Question]]] = {}
    for q in everyone:
        m = re.fullmatch(r"question-(\d+)", q.path.stem)
        if m:
            by_cert.setdefault(q.cert, []).append((int(m.group(1)), q))
    for cert, items in by_cert.items():
        used = {n for n, _ in items}
        free = [n for n in range(1, len(items) + 1) if n not in used]
        for n, q in sorted(items, key=lambda t: t[0]):
            if n > len(items) and (report is None or q.path in report):
                target = free.pop(0) if free else len(items) + 1
                errs.append(
                    f"{rel_path(q.path)}: question numbers run on without gaps; rename this file to "
                    f"question-{target:03d}.md (the next free number)"
                )
            if not re.fullmatch(r"question-\d{3,}", q.path.stem):
                errs.append(f"{rel_path(q.path)}: use three digits, e.g. question-{n:03d}.md")
    return errs


def check_readme_tables(readme: Path | None = None) -> list[str]:
    """questions/README.md repeats each cert's domains as a table for readers; it must match questions/certs/*.json."""
    readme = readme or QUESTIONS / "README.md"
    if not readme.exists():
        return []
    rows = [l for l in readme.read_text(encoding="utf-8").split("\n") if l.startswith("| ")]
    errs = []
    for cid, c in CERTS.items():
        for d in c["domains"]:
            row = next((r for r in rows if r.startswith(f"| {d['name']} |")), None)
            want = f"{d['weight'][0]}–{d['weight'][1]}%"
            if row is None or want not in row or any(f"`{a}`" not in row for a in d["skill_areas"]):
                errs.append(
                    f"questions/README.md: the skill-area table row for {d['name']!r} ({cid}) must read "
                    f"{want} and list {', '.join(d['skill_areas'])}, as in questions/certs/{cid}.json"
                )
    return errs


def next_numbers(everyone: list[Question]) -> dict[str, int]:
    """The next free question number per certification: the first gap, else one past the last."""
    used: dict[str, set[int]] = {}
    for q in everyone:
        m = re.fullmatch(r"question-(\d+)", q.path.stem)
        if m:
            used.setdefault(q.cert, set()).add(int(m.group(1)))
    out = {cid: 1 for cid in CERTS}
    for cert, nums in used.items():
        out[cert] = next(n for n in range(1, len(nums) + 2) if n not in nums)
    return out


def split_problem(problem: str) -> tuple[str | None, str]:
    """'questions/en/az-104/question-001.md: msg' -> (path, msg); link errors name their files in '(in a, b)'."""
    m = re.match(r"^((?:questions|scripts)/[^\s:]+\.(?:md|json)): (.*)$", problem, re.S)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r"\(in ([^,)]+)", problem)
    return (m.group(1) if m else None), problem


def line_for(path: str, msg: str) -> int:
    """Best line for an annotation: the frontmatter key or documentation entry the message is about, else 1."""
    try:
        lines = (ROOT / path).read_text(encoding="utf-8").split("\n")
    except OSError:
        return 1
    m = re.match(r"documentation\[(\d+)\]", msg)
    if m:
        hits = [i for i, l in enumerate(lines, 1) if l.startswith("  - title:")]
        n = int(m.group(1))
        return hits[n - 1] if 0 < n <= len(hits) else 1
    m = re.match(r"line (\d+)", msg) or re.match(r"frontmatter line (\d+)", msg)
    if m:
        return int(m.group(1))
    url = re.search(r"https://\S+", msg)
    for key in ([url.group(0)] if url else []) + [
        f"{k}:" for k in REQUIRED_KEYS + OPTIONAL_KEYS if k in msg
    ] + (["- ["] if "answer" in msg else []):
        for i, l in enumerate(lines, 1):
            if key in l:
                return i
    return 1


def gh_escape(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def write_outputs(files: list[Path], problems: list[str], warnings: list[str], nexts: dict[str, int], report: str | None) -> None:
    """GitHub annotations + job summary in Actions, and a JSON report for the PR feedback comment."""
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for level, items in (("error", problems), ("warning", warnings)):
        for p in items:
            path, msg = split_problem(p)
            if in_actions and path:
                print(f"::{level} file={path},line={line_for(path, msg)},title=Question check::{gh_escape(msg)}")
    rows = []
    for f in files:
        rel = str(rel_path(f))
        mine = [split_problem(p)[1] for p in problems if split_problem(p)[0] == rel]
        rows.append({"file": rel, "ok": not mine, "problems": mine})
    data = {
        "files": rows,
        "other_problems": [p for p in problems if split_problem(p)[0] not in {r["file"] for r in rows}],
        "warnings": warnings,
        "next_numbers": nexts,
    }
    if report:
        Path(report).write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    repo = os.environ.get("GITHUB_REPOSITORY", "Toonssen/getazcertified")
    base = f"https://github.com/{repo}/blob/main"
    if summary:
        out = ["## Question checks", ""]
        if rows:
            out += ["| File | Result |", "|---|---|"]
            for r in rows:
                result = "✅ ok" if r["ok"] else "❌ " + "<br>".join(x.replace("|", "\\|") for x in r["problems"])
                out.append(f"| `{r['file']}` | {result} |")
        for p in data["other_problems"]:
            out.append(f"- ❌ {p}")
        for w in warnings:
            out.append(f"- ⚠️ {w}")
        out += ["", "**Next free file names:** " + ", ".join(f"`questions/en/{c}/question-{n:03d}.md`" for c, n in sorted(nexts.items())),
                "", f"How to fix: [question guide]({base}/questions/README.md) · [contributing]({base}/CONTRIBUTING.md)"]
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")


def rel_path(path: Path) -> Path:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("files", nargs="*", help="question files (default: all); missing files (deleted in a PR) are skipped")
    ap.add_argument("--links", action="store_true", help="also check that every Learn link answers 200")
    ap.add_argument("--report", metavar="PATH", help="write a JSON report (used by the PR feedback comment)")
    args = ap.parse_args(argv)

    if args.files:
        files = [p for p in find_files(args.files) if p.exists() and re.fullmatch(r"question-\d+\.md", p.name)]
    else:
        files = find_files([])
    problems: list[str] = []
    questions: list[Question] = []
    for path in files:
        try:
            q = load(path)
        except FormatError as e:
            problems.append(f"{rel_path(path)}: {e}")
            continue
        questions.append(q)
        if q.cert not in CERTS:
            continue  # reported once by check_certs
        for err in check(q):
            problems.append(f"{rel_path(path)}: {err}")
    # Rules across questions use every file, also when only some files are checked.
    everyone = [q for q in (questions if not args.files else [load_quiet(p) for p in find_files([])]) if q is not None]
    problems += check_certs(everyone)
    problems += check_readme_tables()
    problems += check_numbering(everyone, report=None if not args.files else {q.path for q in questions})
    problems += check_doc_titles(
        [q for q in everyone if q.cert in CERTS],
        report=None if not args.files else {q.path for q in questions},
    )
    # Exam weights guide the set as a whole; a single contribution shouldn't fail on them, so they only warn.
    warnings = check_weights([q for q in everyone if q.cert in CERTS])
    if args.links:
        problems += check_links([q for q in questions if q.cert in CERTS])

    nexts = next_numbers(everyone)
    write_outputs(files, problems, warnings, nexts, args.report)
    for p in problems:
        print(p)
    for w in warnings:
        print(f"warning: {w}")
    print(f"{len(files)} files, {len(problems)} problems" + (f", {len(warnings)} warnings" if warnings else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
