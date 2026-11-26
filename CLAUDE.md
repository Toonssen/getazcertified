# getazcertified (prod)

Public repo behind **getazcertified.com**: the landing page (`site/`) plus the **sneak peek** of the app (`app/`,
`questions/`, AZ-104 practice test + question browser, noindex). GPL-3.0.

- **app/ and questions/ are release snapshots** from the development repo, arriving as PRs titled "Release dev@<sha>"
  (made by a release script that runs a leak gate first). Don't edit them here; change them upstream and release again.
  `check` enforces it: a PR touching `app/`, `questions/`, `scripts/check_questions.py`, `cspell.json` or `.node-version`
  must come from a `release/*` branch of this repo. Dependabot opens no npm PRs here (`open-pull-requests-limit: 0`):
  dependency bumps happen upstream and arrive by release.
  This repo owns `.github/`, `site/`, `scripts/check_site.py`, `scripts/assemble.py`, `scripts/serve.py` and the docs.
- **CI** (`.github/workflows/ci.yml`): `check` (landing page + actionlint), `questions`, `unit`, `build` (Next export with
  `NEXT_PUBLIC_SITE_MODE=preview`, then `scripts/assemble.py`: landing page at `/`, challenges removed, `_headers` with a
  CSP whose `script-src` holds the sha256 of every inline script, no `unsafe-inline`), `e2e` (Playwright against the built
  site served by `scripts/serve.py` with those headers, failing on any CSP violation/console error/third-party request).
- **Deploy**: job `deploy` after all checks, on main only → environment `production` (required reviewer approves each
  run, no admin bypass) → Azure OIDC → Key Vault → `wrangler pages deploy dist` to Pages project `getazcertified`.
  GitHub holds identifiers only (repo variables), **never secrets**.
- **main** is guarded by a ruleset with no bypass: PR only, signed commits, linear history, squash only, required
  checks (`check`, `questions`, `unit`, `build`, `e2e`, CodeQL). Commits are signed with SSH (`gpg.format ssh`).
- **Actions**: only GitHub-owned actions and `azure/login` are allowed, pinned by full commit SHA (tag in a comment);
  every workflow starts with `permissions: {}` and grants per job. No `pull_request_target`, no `${{ github.event.* }}`
  inside `run:`, `persist-credentials: false` on checkout, `npm ci --ignore-scripts`. Fork PRs need approval before any workflow runs.
- **Landing page rules** (`python3 scripts/check_site.py`): no JavaScript, no inline styles, nothing loaded from another
  origin (fonts are self-hosted), security headers in `site/_headers` (also the base for the app's headers). No Microsoft logos or cert badges;
  keep the "not affiliated with Microsoft" line and the ghcertified credit.
- Report security issues via private vulnerability reporting (`SECURITY.md`). Issues/wiki are off for now.
