#!/usr/bin/env python3
"""Originality checks that need no outside data. Reports only; never edits.

    python3 scripts/originality.py az-104                         # near-duplicates within the cert's set
    python3 scripts/originality.py az-104 --learn ~/azure-docs     # also: 12-word runs copied from a docs clone
    python3 scripts/originality.py az-104 --only question-110.md  # just these files against the rest

Within the set, a pair is flagged when the stems are very close (ratio >= 0.80) or when two questions share both the
whole answer set and the key. Questions in the same `series` share a scenario on purpose and are skipped.

With --learn DIR (a local clone of a Microsoft Learn docs repo, e.g. MicrosoftDocs/azure-docs), every run of 12 or
more words that a stem or explanation shares with a docs page is listed. Exact setting and page names are fine; whole
copied sentences should be rewritten in our own words.

Exit status 1 when anything is flagged. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import check_questions as cq

STEM_MAX = 0.80
RUN = 12


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def grams(w: list[str], n: int = RUN) -> set[tuple[str, ...]]:
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def within_set(qs: list[cq.Question], only: set[str]) -> list[str]:
    out = []
    for i, a in enumerate(qs):
        for b in qs[i + 1:]:
            if only and a.path.name not in only and b.path.name not in only:
                continue
            if a.meta.get("series") and a.meta.get("series") == b.meta.get("series"):
                continue
            sm = SequenceMatcher(None, norm(a.meta["question"]), norm(b.meta["question"]), autojunk=False)
            r = sm.ratio() if sm.quick_ratio() >= STEM_MAX else 0.0
            same_set = {norm(t) for _, t, _ in a.answers} == {norm(t) for _, t, _ in b.answers}
            same_key = {norm(t) for c, t, _ in a.answers if c} == {norm(t) for c, t, _ in b.answers if c}
            yes_no = {norm(t) for _, t, _ in a.answers} == {"yes", "no"}
            if r >= STEM_MAX or (same_set and same_key and not yes_no):
                why = f"stem {r:.2f}" + (", same answers and key" if same_set and same_key and not yes_no else "")
                out.append(f"{a.path.name} ~ {b.path.name}: {why}")
    return out


def learn_runs(qs: list[cq.Question], docs: Path, only: set[str]) -> list[str]:
    want: dict[tuple[str, ...], set[str]] = {}
    for q in qs:
        if only and q.path.name not in only:
            continue
        for text in [q.meta["question"]] + [e for _, _, e in q.answers]:
            for g in grams(words(text)):
                want.setdefault(g, set()).add(q.path.name)
    hits: dict[str, dict[str, str]] = {}
    for page in docs.rglob("*.md"):
        try:
            w = words(page.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        for i in range(len(w) - RUN + 1):
            g = tuple(w[i:i + RUN])
            for name in want.get(g, ()):
                hits.setdefault(name, {}).setdefault(" ".join(g), str(page.relative_to(docs)))
    return [f"{name}: '{run}' <- {page}" for name in sorted(hits) for run, page in list(hits[name].items())[:3]]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cert")
    ap.add_argument("--learn", type=Path, help="local clone of a Learn docs repo")
    ap.add_argument("--only", nargs="*", default=[], help="file names to check against the rest")
    args = ap.parse_args(argv)
    folder = cq.QUESTIONS / "en" / args.cert
    qs = [cq.load(p) for p in sorted(folder.glob("question-*.md"))]
    only = set(args.only)
    flagged = within_set(qs, only)
    print(f"{len(qs)} {args.cert} questions; {len(flagged)} near-duplicate pair(s)")
    for line in flagged:
        print("  " + line)
    if args.learn:
        runs = learn_runs(qs, args.learn.expanduser(), only)
        print(f"{len(runs)} run(s) of {RUN}+ words shared with {args.learn}")
        for line in runs:
            print("  " + line)
        flagged += runs
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
