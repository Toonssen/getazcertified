# Question writing guide

Questions are Markdown files parsed by [mdquiz](https://github.com/v-fidelusaleksander/mdquiz). This is the format
inherited from [ghcertified](https://github.com/FidelusAleksander/ghcertified), plus the rules getazcertified adds
for Azure exams. **How the questions should read** (voice, archetypes, exhibits, distractors) is in the per-exam
style guide, e.g. [`docs/question-style/az-104.md`](../docs/question-style/az-104.md).

## Files

- One question per file, `questions/en/<cert>/question-NNN.md` (zero-padded: `question-042.md`). Numbers run on without
  gaps: use the next free number (CI prints it, and tells you if a file needs renaming).
- Each certification is described by `questions/certs/<cert>.json` (title, study-guide date, skill areas, colour,
  icon, `draft` or `live`); the site builds its catalog from these files. Certs: `az-104`. How to add one:
  [CONTRIBUTING.md › Propose a new certification](../CONTRIBUTING.md#propose-a-new-certification).

## Template

````markdown
---
question: |-
  You have an Azure subscription that contains the virtual networks shown in the following table.

  You need to deploy a virtual machine named VM1 to West Europe.

  To which virtual networks can you connect VM1?
documentation:
  - title: "Virtual networks and VMs"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/network-overview"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name    Location      Resource group
VNet1   West Europe   RG-Net
VNet2   North Europe  RG-Net
VNet3   West Europe   RG-App
```

- [x] VNet1 and VNet3 only
  > A VM can only join a virtual network in its own region. The resource group doesn't matter.
- [ ] VNet1 only
  > VNet3 is also in West Europe; being in another resource group doesn't stop it.
- [ ] VNet1, VNet2, and VNet3
  > VNet2 is in North Europe. A virtual network can't span regions.
````

## Frontmatter

Only these keys, in this exact form (the checker accepts this subset of YAML and nothing else):

| key | required | value |
|---|---|---|
| `question` | yes | `\|-` block indented two spaces: **one line per paragraph** (line breaks are shown as-is), a blank line between paragraphs, `- ` for requirement lists; or a one-line `"…"` string |
| `documentation` | yes | one to three Microsoft Learn pages that back the answer and the explanations, each a `title` + `url` pair, main page first. See [Documentation links](#documentation-links) |
| `skill_area` | yes | one of the study guide's skill areas, see below |
| `study_guide` | yes | the skills-measured date the question was written against (`"2026-04-17"` for AZ-104) |
| `archetype` | yes | `best-choice`, `exhibit-select`, `exhibit-statement`, `complete-statement`, `complete-code`, `calculate`, `goal-solution`, `choose-n`, `fact-recall` |
| `series` | no | slug shared by questions that reuse one scenario |

### Documentation links

Every question lists the Microsoft Learn pages that back its answer. Readers see them in the **Learn more in the docs**
menu above the question, by their title. Write each entry as two lines: the title, then the URL, indented exactly like this:

```yaml
documentation:
  - title: "Azure Files share permissions"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions"
  - title: "Azure Files identity auth"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-active-directory-overview"
```

- **One to three entries.** The first is the main page: the one that settles the answer.
- **`url`**: a `https://learn.microsoft.com/` page that states the facts in your explanations. Copy it from the browser;
  the `en-us/` part is fine.
- **`title`**: a short label for that page, **at most 40 characters** (counting spaces). Name the page's topic, in
  sentence case, as plain text: `"Azure Storage redundancy"`, `"What is a private endpoint?"`, `"Steps to assign an Azure role"`.
  - Start from the page's own heading and shorten it; drop the product suffix Learn adds (`"... - Azure Monitor"`).
  - Don't add words the menu already says: no "docs", "documentation" or "Microsoft Learn".
  - No period at the end, no Markdown, no quotes.
  - **Main page: at most 30 characters** when a question lists two or three pages. The first entry shares its menu
    line with a "Main page" tag; a longer title wraps on phones. With one page there's no tag and 40 applies.
  - The same page gets the same title in every question: search the folder for the URL before inventing one. The
    checker fails on a second title for a page and names the file that has the first one. So a main-page title (≤ 30)
    is that page's title everywhere.
- Two entries in one question can't share a URL or a title.

The checker tells you what to fix, for example
`documentation[2].title 'Overview of the Azure Monitor alert types' is 41 characters; keep it to 40 (e.g. "Share-level permissions")`.

The skill areas per functional group, with the study guide's weights, are in the cert's file, e.g.
[`questions/certs/az-104.json`](certs/az-104.json) › `domains`. For AZ-104:

| functional group | weight | `skill_area` |
|---|---|---|
| Manage Azure identities and governance | 20–25% | `entra-users-groups`, `access-azure-resources`, `subscriptions-governance` |
| Implement and manage storage | 15–20% | `storage-access`, `storage-accounts`, `files-blob` |
| Deploy and manage Azure compute resources | 20–25% | `arm-bicep`, `virtual-machines`, `containers`, `app-service` |
| Implement and manage virtual networking | 15–20% | `virtual-networks`, `secure-vnet-access`, `name-resolution-load-balancing` |
| Monitor and maintain Azure resources | 10–15% | `monitor-resources`, `backup-recovery` |

## Body

- **Exhibits:** fenced blocks between the frontmatter and the answers. They render under the question text, in
  order. Prose outside a fence is dropped by the parser, so all scenario text goes in `question`.
- **Answers:** `- [x]` for correct and `- [ ]` for wrong. Answers are shuffled in the app. Several `[x]` make it
  multi-select, and then the stem must say how many (*"Which two…"*).
- **Explanations:** every answer gets an indented blockquote (`  > …`) on the lines right after it. Inline code,
  `[links](https://learn.microsoft.com/...)` and bare URLs render.

## Rules (enforced by `scripts/check_questions.py`)

- All required keys are present, the values come from the closed sets above, and `documentation` holds one to three `title` + `url` entries with distinct Learn URLs and titles of at most 40 characters (30 for the main page of a multi-link question), one title per page across all questions (see [Documentation links](#documentation-links)).
- There are at least 2 answers and at least one correct, with no duplicates, and every answer has an explanation.
- "Which two/three…" matches the number of correct answers, and multi-select always says how many.
- `exhibit-statement` and `goal-solution` answers are exactly `Yes` and `No`. `exhibit-*` questions have an exhibit block.
- Question numbers have no gaps; certification files in `questions/certs/` are valid, every question folder has one,
  and a `live` cert has at least 20 questions.
- Once every functional group has questions, the share of each should fall inside the study-guide weights. This
  only **warns** (one new question can tip a percentage); maintainers balance the set.
- With `--links`: every Learn URL in the file answers 200.

```bash
python3 scripts/check_questions.py            # rules
python3 scripts/check_questions.py --links    # rules + live links
python3 -m unittest discover -s scripts       # the checker's own tests
```

In a pull request, CI runs these on the files you changed: problems show **inline on your diff** ("Files changed"
tab) and in a comment on the PR, with the fix and the next free file name. Spelling is checked by cspell (`cspell.json`): add real Azure terms
there, don't misspell around it.

## Originality

Questions are original. Write each scenario yourself from the Microsoft Learn documentation and the official study
guide. Never copy or reconstruct real exam items, braindumps or another site's or course's questions. If you remember
a question, don't write it down: write a new scenario that tests the skill.
<!-- probe 1 -->
<!-- probe 2 -->
<!-- probe 3 -->
