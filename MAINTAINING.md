# Maintaining getazcertified

How contributions are handled, written down so contributors know what to expect and so it stays consistent. Short on
purpose; [CONTRIBUTING.md](CONTRIBUTING.md) is the contributor's side.

## Response times

| | Target |
|---|---|
| First reply on an issue or pull request | within 3 days |
| Decision (merge, changes requested, or declined) | within a week of the checks passing |

A quick "Thanks, I'll look at this on the weekend" counts as a reply. Nothing is closed automatically for being quiet.

## Starting the checks for a first-time contributor

GitHub holds the workflows of someone without a merged PR until you click **Approve and run workflows** on the PR, on
every push. If they pushed several commits within seconds, GitHub sometimes creates no checks for the newest commit
(seen 2026-11-26), and no button shows up. Close and reopen the PR: that starts the checks for the latest commit.

## Reviewing a question

The checks already cover the format, links, spelling and numbering. The review is about the content:

- [ ] **Correct**: the marked answer is right *today*, according to the cited Learn page(s).
- [ ] **Backed**: every explanation follows from a cited page (open them; don't trust memory).
- [ ] **Original**: an own scenario, not a copied or rebuilt exam item, course or other site's question.
- [ ] **Clear**: one reading only; the stem says how many answers to pick; names and numbers are consistent.
- [ ] **Fair distractors**: wrong answers are plausible, and each explanation says why it's wrong.
- [ ] **Fits the set**: right `skill_area`; not a near-duplicate of an existing question.

A reword PR: the meaning stays the same (or the PR says why the facts changed), and the file name stays (it's the
question's id).

## Merging

- Squash merge. The contributor stays the author and shows up on the site's contributors list.
- Small fixes (a typo, a title): suggest them with GitHub's "Suggested change" so the contributor can apply them in one
  click, or push to their branch if they allowed edits, rather than asking for another round.
- A new certification stays `draft` until it has at least 20 questions over its skill groups. Going `live` is a
  maintainer PR that also adds its skill-area table to `questions/README.md`.

## Replies

Be kind and specific. Thank people, say what happens next, and explain every "no".

**Merged**
> Thanks a lot, @name! Merged. It'll be on getazcertified.com with the next deploy, and you're now on the contributors
> list. 🎉

**Needs changes**
> Thanks for this! It's nearly there: <what and why, with the Learn page>. Edit the file in this PR and the checks run
> again. Shout if anything is unclear.

**Declined**
> Thank you for taking the time. I'm not merging this one because <reason>. <What would be accepted instead, or
> "an issue first next time saves you work">. I hope to see you again!

**Duplicate**
> Thanks! This is already covered by <link>, so I'm closing this one. If yours adds something, please say so and I'll
> reopen it.

**Looks copied from an exam or another site**
> Thanks for contributing. This looks very close to <source or "a real exam item">, and we only take original scenarios
> (CONTRIBUTING › The rules). Could you write a new scenario that tests the same skill? Happy to help.

## Starter issues

Keep a few issues labelled **`good first issue`** + **`help wanted`** open: small, well-described tasks (a topic that
needs a question, with the skill area and the Learn page to start from). When someone comments "I'd like to take
this", assign them and reply within a few days; if it goes quiet for a month, ask kindly before giving it to someone
else.
