# Contributing to getazcertified

Thanks for helping! getazcertified is a free set of **original** practice questions for Azure certifications, each
backed by Microsoft Learn. You don't need to install anything: everything below works in the browser.

| I want to… | Do this | Takes |
|---|---|---|
| Report a wrong or unclear question | Click **Report** on the question on getazcertified.com, or [open the form](https://github.com/Toonssen/getazcertified/issues/new?template=question-problem.yml) | 2 min |
| Suggest a topic that needs questions | [Suggest a topic](https://github.com/Toonssen/getazcertified/issues/new?template=question-topic.yml) | 2 min |
| Write a new question | [Add a question](#add-a-question) | 15–30 min |
| Improve or reword a question | [Edit a question](#improve-or-reword-a-question) | 5–10 min |
| Add a whole certification | [Propose a new certification](#propose-a-new-certification) | an issue first |
| Report a website bug | [Site bug](https://github.com/Toonssen/getazcertified/issues/new?template=site-bug.yml) | 2 min |

## The rules (short)

1. **Original only.** Write your own scenario from the Microsoft Learn docs and the official study guide. Never copy or
   rebuild real exam questions, braindumps, or questions from other sites or courses.
2. **Backed by Learn.** Every explanation must follow from the one to three Learn pages you cite.
3. **Explain every answer**, the wrong ones too: why it's wrong is where people learn.

How a good question reads (voice, scenario types, distractors): the style guide,
[`docs/question-style/az-104.md`](docs/question-style/az-104.md). The full file format: [`questions/README.md`](questions/README.md).

## Add a question

1. Open [`questions/en/az-104/`](questions/en/az-104), click **Add file › Create new file**.
2. Name it `question-NNN.md` with the next free number (the highest number in the folder + 1). Not sure? Pick any
   number; CI tells you the right one.
3. Paste this template and fill it in:

````markdown
---
question: |-
  You have an Azure subscription that contains a storage account named st1.

  You need to ensure that users can access st1 only from a virtual network named VNet1.

  What should you configure?
documentation:
  - title: "Storage firewall and network access"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A virtual network rule on st1 for VNet1, with public network access limited to selected networks
  > With access limited to selected networks, only the listed networks reach st1. VNet1's subnet needs the
  > Microsoft.Storage service endpoint for the rule.
- [ ] A shared access signature for VNet1
  > A SAS grants access to anyone who holds it, wherever they connect from.
- [ ] A private DNS zone for st1
  > DNS only resolves names; it doesn't block access from other networks.
````

   - `question`: one line per paragraph, blank line between paragraphs, indented two spaces.
   - `documentation`: one to three Learn pages, each a short `title` (max 40 characters; 30 for the first when you list
     several) and its `url`. Use the same title as other questions that cite the same page.
   - `skill_area`, `archetype`: pick from the lists in [`questions/README.md`](questions/README.md#frontmatter).
   - Answers: `- [x]` correct, `- [ ]` wrong, each followed by an explanation line starting with `  > `.
4. Click **Commit changes… › Propose changes**, then **Create pull request**. GitHub makes the fork for you.

## Improve or reword a question

Found a clearer way to say it, an outdated fact or a weak distractor? Open the question's file (the **Report** form on
the site links it), click the pencil, edit in place and propose the change.

- Keep the file name: it's the question's id, and people's progress is tied to it.
- Explanations must still follow from the cited pages; add or swap a Learn link if the facts come from elsewhere.
- Say **why** in the pull request ("Basic SKU retired", "two answers were both right", "stem was ambiguous").

## Propose a new certification

1. [Open a certification proposal](https://github.com/Toonssen/getazcertified/issues/new?template=certification.yml)
   first, so we can agree on it before you write questions.
2. Then, in a pull request:
   - Add `questions/certs/<exam>.json`, copied from [`questions/certs/az-104.json`](questions/certs/az-104.json):
     exam code as `id` (e.g. `sc-500`), title, one-sentence description, the study guide's date and skill groups
     (with their weights and your skill-area names), a colour slot 1–8 and an icon from the list CI gives you.
     Keep `"status": "draft"`: draft certifications aren't shown on the site yet.
   - Add questions in `questions/en/<exam>/`, starting at `question-001.md`.
3. Once the set is big enough (at least 20 questions, spread over the skill groups) the maintainer switches it to
   `"live"`.

## What happens after you open a pull request

- **Checks run automatically.** First-time contributors wait for a maintainer to start them (one click, a GitHub
  safety rule). Problems show **inline on your changes** (the *Files changed* tab) and in a bot comment that says what
  to fix and the next free file name. Fix them by editing the file in your pull request; the checks run again.
- The checks cover the format, the rules above, the Learn links (they must load) and spelling (add real Azure terms to
  [`cspell.json`](cspell.json)).
- A maintainer then reviews the **content**: is it correct, original, clear and fair? Expect a reply within a week.

Want to run the checks yourself? `python3 scripts/check_questions.py` (Python 3 only, no packages).

## The website

The site's code isn't open for pull requests yet: please [open an issue](https://github.com/Toonssen/getazcertified/issues/new?template=site-bug.yml)
for bugs and ideas.

## License

By contributing you agree that your contribution is licensed under the project's [GPL-3.0 license](LICENSE).
getazcertified is not affiliated with or endorsed by Microsoft.
