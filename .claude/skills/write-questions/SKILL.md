---
name: write-questions
description: Use when asked to write, draft or generate new practice questions for a certification in this repo (e.g. "write 5 AZ-104 questions on storage", "draft questions from these Learn pages"). Plans from the cert's blueprint, drafts from the given sources at the cert's difficulty level, runs every gate, has an independent reviewer score each question, and stops before the PR for the maintainer's review.
---

# Write questions

A pipeline for new questions that follow [`docs/question-style/exam-writing-rules.md`](../../../docs/question-style/exam-writing-rules.md)
and the cert's style guide. Read both before starting, plus [`questions/README.md`](../../../questions/README.md)
for the file format.

**Inputs** (ask only for what's missing): the cert id, how many questions, and optionally a skill area and sources
(Learn URLs, local files). Without a skill area, the blueprint step picks one.

Keep everything for a run in `.claude/local/runs/<YYYY-MM-DD>-<cert>-<slug>/` (gitignored): `plan.md`,
`sources.md`, `drafts/`, `gates.txt`, `review.md`. A run that dies can resume from these files.

## 1. Blueprint

1. Read `questions/certs/<cert>.json`: `level` (the difficulty profile), domains, weights, skill areas.
2. Count the existing questions per skill area and archetype
   (`grep -h '^skill_area\|^archetype' questions/en/<cert>/*.md | sort | uniq -c`).
3. Choose the skill areas that are furthest below their domain weight, unless the user named one.
4. For each question, write one line in `plan.md`: skill area, the job task it tests, the archetype (from the
   profile's mix), and the concept the key turns on. Check existing questions on the same concept
   (`grep -il '<concept words>' questions/en/<cert>/*.md`) and pick a different decision point than they use.

## 2. Sources

- Use the user's sources first. Otherwise find the Learn pages for each concept: a local docs clone or search, then
  read **today's** page (a docs clone can be months old).
- The profile sets how many sources a question needs. An expert question that combines services cites every page it
  relies on (max 3).
- In `sources.md`, for each question, record the URL and the exact sentences that prove the key and each
  explanation. A claim without a quoted sentence doesn't go in a question.
- Never use another question set (exam items, braindumps, practice tests, courses, other sites) as a source.

## 3. Draft

Draft in a **writer subagent** (Agent tool, general-purpose) per batch of up to 5 questions. Give it: the
exam-writing rules, the style guide, `questions/README.md`, the plan lines, `sources.md`, and the next free file
numbers (`python3 scripts/check_questions.py` prints them). Ask it to write the files into the run's `drafts/`
folder and to obey:

- invented scenario and object names, the cert's voice, the profile's scenario size and exhibits;
- one defensible key; distractors from rule 4; no cues; options that stand alone (answers are shuffled);
- every explanation sentence backed by a quoted sentence in `sources.md`.

## 4. Gates

Copy the drafts into `questions/en/<cert>/` and run, saving the output to `gates.txt`:

```bash
python3 scripts/check_questions.py questions/en/<cert>/question-NNN.md ...   # rules
python3 scripts/check_questions.py --links questions/en/<cert>/question-NNN.md ...
python3 scripts/originality.py <cert> --only question-NNN.md ...             # add --learn <docs clone> if there is one
npx --yes cspell@10.4.1 --no-progress --config cspell.json questions/en/<cert>/question-NNN.md ...
```

If `.claude/local/originality-hook` exists and is executable, run it with the new file paths as arguments. It's
a maintainer's local extra check: a non-zero exit means **stop**, show its output and rewrite. Don't read it or
describe it anywhere.

Fix and re-run until all gates pass. A fix to a rule that could happen again becomes a checker rule (with a test)
in `scripts/check_questions.py`.

## 5. Review

Hand the passing files to a **reviewer subagent** that didn't write them. Give it only the exam-writing rules
(including the review rubric), the style guide, the files and `sources.md`. It must open each cited page itself and
score every rubric item pass/fail with a one-line reason, writing everything to `review.md`. Rewrite each failed
item, then re-run the gates and the review for that question. Two failed rounds on one question → drop it and say so.

## 6. Hand-off

Stop before committing. Show the maintainer, per question: file, skill area, archetype, the key in one line, and
the review result, with the run folder path. After their spot-check: a branch `content/<cert>-<slug>`, a signed
commit, and a PR whose body lists the questions and the gate results. Never mention local hooks in the PR.
