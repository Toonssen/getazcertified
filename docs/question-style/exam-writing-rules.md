# Exam writing rules

The rules every getazcertified question follows, for any certification. A per-exam style guide (for example
[`az-104.md`](az-104.md)) adds that exam's voice, archetypes and skill areas on top. The file format is in
[`questions/README.md`](../../questions/README.md).

## What Microsoft publishes about its exams

These rules are based on what Microsoft says publicly. Microsoft doesn't publish item-writing guidelines. Everything
beyond the points below is our own practice and is labeled as such.

- **Blueprint first.** Experts define the critical tasks of the job role, then the distribution of skills on the
  exam. Questions are written to that blueprint, reviewed by a panel for technical accuracy, relevance and alignment
  to the skill domain, beta tested, and kept only if they meet psychometric criteria such as difficulty and the
  ability to tell high and low performers apart.
  ([Exam development](https://learn.microsoft.com/en-us/credentials/certifications/exam-development))
- **Question types.** Microsoft doesn't say in advance which formats an exam uses. Its sample videos show multiple
  choice, build list, drag and drop, hot area, active screen, case studies and labs, plus problem-solution sets
  ("you are presented a problem and asked if the solution provided would solve the problem").
  ([Exam duration and exam experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience))
- **Length by level.** Most exams have 40–60 questions. Fundamentals exams take 45 minutes. Associate and expert
  role-based exams take 100 minutes, or 120 when they may contain labs. (Same page.)
- **Scoring.** Scores are scaled from 1 to 1,000, with 700 to pass. Multi-part questions earn one point per correct
  part, and there's no penalty for guessing. Alternate scoring is stated in the question text.
  ([Exam scoring](https://learn.microsoft.com/en-us/credentials/certifications/exam-scoring-reports))
- **Practice assessments** give "insight into the style, wording, and difficulty" of exam questions, but they aren't
  the exam's questions.
  ([Practice Assessments](https://learn.microsoft.com/en-us/credentials/certifications/practice-assessments-for-microsoft-certifications))
  They are a style reference only. Never use them, or any other question set, as a source of questions.

## Rules for every question

1. **Start from the blueprint.** Each question tests one skill from the cert's study guide (`skill_area`), and the
   set follows the study guide's weights. Pick the skill first, then invent the scenario.
2. **One job task, from the role's point of view.** The scenario is something a person in that role really does.
   No trivia that the role never needs ("which year did…").
3. **Exactly one defensible key.** An expert who reads only the cited Learn pages gets the same answer. If a second
   answer could be argued, change the scenario until it can't.
4. **Plausible distractors.** Every wrong answer is something a partly prepared candidate might pick: a real feature
   that solves a neighboring problem, the right feature at the wrong scope or SKU, or the number you get by making
   the classic mistake.
5. **No cues.** The key is not the longest option, the only one that repeats the stem's wording, or the only one
   that fits the grammar of the stem. Options are parallel in form and length.
6. **Answers stand alone.** The site shuffles answers, so no option may say "all/none of the above" or refer to
   another option. *(Checked.)*
7. **The qualifier carries weight.** A requirement like *"must minimize costs"* is there because a distractor would
   work without it.
8. **No tricks.** No double negatives, no hidden "not". When one word decides the answer, put it in plain sight.
9. **Current and true.** Every fact behind the key and behind each explanation is on a cited Learn page, checked
   today. Name the assumed value when a limit or a date may change. Don't make a claim stronger than the page: no *only*,
   *always* or *never* unless it says so. When the key depends on something being absent (no resource lock, no
   other role assignment), the stem says so.
10. **Original.** Invented scenario, our own words, our own object names. See
    [Originality](../../questions/README.md#originality).

## Difficulty profiles

Each cert has a `level` in `questions/certs/<id>.json` that picks its profile. The levels are Microsoft's; the
profiles are **our own practice**, a calibration of what each level asks, not something Microsoft publishes.

| | fundamentals | associate | expert | specialty |
|---|---|---|---|---|
| Examples | AZ-900, SC-900, AI-900 | AZ-104, AZ-700 | AZ-305, AZ-400 | product-specific certs |
| Asks the candidate to | recognize a concept, pick the right service | configure, troubleshoot, calculate | design, compare trade-offs across services | apply one product deeply |
| Scenario | 0–2 sentences | 2–6 sentences, named objects, one requirement list | longer scenario or a series sharing one case, several competing requirements | like associate, deep in one product |
| Exhibits | rare | common (tables, settings, templates) | common, often more than one | common |
| Main archetypes | `fact-recall`, `best-choice` | `best-choice`, `exhibit-*`, `calculate`, `complete-*` | `best-choice` with trade-offs, `goal-solution` series, `choose-n` | as associate |
| Sources per question | 1 Learn page is usually enough | 1–3 Learn pages | usually 2–3 pages, since the answer combines services | 1–3 pages, product docs first |
| Distractors | other services in the same family | right feature, wrong scope or SKU; the off-by-one number | a design that meets most requirements but breaks one | a near-miss setting of the same product |

When the profiles and the per-exam style guide disagree, the style guide wins for that exam.

## Sources

- **Allowed:** Microsoft Learn documentation and training modules, the official study guide, and product
  documentation that Learn links to. A question can combine several of them, as the profile asks.
- **Not allowed:** real exam items, braindumps, practice tests or courses (Microsoft's own practice assessments
  included), and other question sites. Remembered questions count as copied.
- Cite what proves the answer: 1–3 links in `documentation`, main page first.
- Write explanations in your own words. Exact names of settings and commands are fine; copied sentences are not.

## Checks and review

| What | How |
|---|---|
| Format, keys, closed sets, links | `scripts/check_questions.py` (CI job `questions`) |
| Answers stand alone, 3–6 options, lead-in ends with a question, goal-solution shape | `scripts/check_questions.py` |
| Spelling | cspell (`cspell.json`) |
| Rules 1–5 and 7–10 | review: the rubric below, by a maintainer (and by an AI reviewer when one drafts questions) |

**Review rubric.** Each item passes or fails. A question merges only when all of them pass.

1. *Skill:* tests the `skill_area` it claims, at the cert's level.
2. *Key:* exactly one defensible answer, provable from the cited pages.
3. *Explanations:* every claim is on a cited page, in our own words and no stronger than the page. Wrong answers
   say why they fail *here*.
4. *Distractors:* each one is plausible for a partly prepared candidate. None is a joke option.
5. *Cues:* no length, wording or grammar cue points at the key.
6. *Profile:* scenario size, exhibit and number of sources match the level.
7. *Original:* new scenario and wording, not recognizably someone else's question.
