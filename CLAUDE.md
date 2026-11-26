# getazcertified (prod)

Public repo behind **getazcertified.com**: the landing page (`site/`) plus the **sneak peek** of the app (`app/`,
`questions/`, AZ-104 practice test + question browser, noindex). GPL-3.0.

- **Ownership** (enforced by `check` › "Who may change which paths"):
  - **Questions are owned here** and open to anyone, also from forks: `questions/**` (incl. `questions/certs/*.json`,
    the cert registry), `docs/question-style/`, `scripts/check_questions.py` + `scripts/test_check_questions.py`,
    `cspell.json`, `CONTRIBUTING.md`. The dev repo pulls them back with its `infra/sync-from-prod.sh`; robertt's own
    questions go through PRs here too.
  - **The app** (`app/`, `.node-version`) arrives only as release PRs `Release dev@<sha>` from `release/*` branches of
    this repo (dev's `infra/release-to-prod.sh`, leak gate first); a release PR may carry nothing else. Dependabot opens
    no npm PRs here (`open-pull-requests-limit: 0`).
  - **Everything else** (`.github/`, `site/`, other `scripts/`, README/CLAUDE/SECURITY) only from branches of this repo.
- **Contributor automation**: issue forms in `.github/ISSUE_TEMPLATE/` (the site's Report link prefills
  `question-problem.yml` via `?question-id=&question-file=`), PR template. Job `questions` checks changed questions
  (rules with inline annotations + job summary, Learn links, cspell `CSPELL_VERSION`) and uploads artifact
  `pr-feedback`; `pr-feedback.yml` (workflow_run, main's code only, `pull-requests: write`) runs
  `scripts/pr_feedback.py`: one sticky comment + labels (`content`, `new-question`, `reword`, `certification`,
  `cert:<id>`, `site`, `deps`). Labels must exist in the repo (`cert:<id>` is only applied when it does).
- **CI** (`.github/workflows/ci.yml`): `check` (paths, landing page, no event expressions, actionlint), `questions`, `unit`, `build` (Next export with
  `NEXT_PUBLIC_SITE_MODE=preview`, then `scripts/assemble.py`: landing page at `/`, challenges removed, `_headers` with a
  CSP whose `script-src` holds the sha256 of every inline script, no `unsafe-inline`), `e2e` (Playwright against the built
  site served by `scripts/serve.py` with those headers, failing on any CSP violation/console error/third-party request).
- **Deploy**: job `deploy` after all checks, on main only → environment `production` (required reviewer approves each
  run, no admin bypass) → Azure OIDC → Key Vault → `wrangler pages deploy dist` to Pages project `getazcertified`.
  GitHub holds identifiers only (repo variables), **never secrets**.
- **Contributors**: be kind and quick (targets, review checklist and reply templates in `MAINTAINING.md`); test any
  contributor-facing change as ToonssenTest (dev repo `infra/contributor-flow-test.py`).
- Run the dev repo's `infra/audit-prod-repo.sh` **before** merging any workflow or settings change here.
- **main** is guarded by a ruleset with no bypass: PR only, signed commits, linear history, squash only, required
  checks (`check`, `questions`, `unit`, `build`, `e2e`, CodeQL). Commits are signed with SSH (`gpg.format ssh`).
- **Actions**: only GitHub-owned actions and `azure/login` are allowed, pinned by full commit SHA (tag in a comment);
  every workflow starts with `permissions: {}` and grants per job. No `pull_request_target`, no `${{ github.event.* }}`
  inside `run:`, `persist-credentials: false` on checkout, `npm ci --ignore-scripts`. Fork PRs from first-time contributors need approval before workflows run.
- **Landing page rules** (`python3 scripts/check_site.py`): no JavaScript, no inline styles, nothing loaded from another
  origin (fonts are self-hosted), security headers in `site/_headers` (also the base for the app's headers). No Microsoft logos or cert badges;
  keep the "not affiliated with Microsoft" line and the ghcertified credit.
- Report security issues via private vulnerability reporting (`SECURITY.md`). Issues are on (forms only, no blank issues); wiki/projects off.
