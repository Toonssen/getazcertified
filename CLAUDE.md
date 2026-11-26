# getazcertified (prod)

Public repo behind **getazcertified.com**. For now it holds only the static "coming soon" page (`site/`); the app is
developed elsewhere and moves here when the site goes public. GPL-3.0.

- **Deploy**: push to `main` touching `site/**` → workflow `deploy` → environment `production` (main only, required
  reviewer approves each run, no admin bypass) → Azure OIDC → Key Vault → `wrangler pages deploy site` to Pages
  project `getazcertified`. GitHub holds identifiers only (repo variables), **never secrets**.
- **main** is guarded by a ruleset with no bypass: PR only, signed commits, linear history, squash only, required
  checks `check` + CodeQL. Commits are signed with SSH (`gpg.format ssh`).
- **Actions**: only GitHub-owned actions and `azure/login` are allowed, pinned by full commit SHA (tag in a comment);
  every workflow starts with `permissions: {}` and grants per job. No `pull_request_target`, no `${{ github.event.* }}`
  inside `run:`, `persist-credentials: false` on checkout. Fork PRs need approval before any workflow runs.
- **Site rules** (checked by `python3 scripts/check_site.py`, CI job `check`): no JavaScript, no inline styles, nothing loaded
  from another origin (fonts are self-hosted), security headers in `site/_headers`. No Microsoft logos or cert badges;
  keep the "not affiliated with Microsoft" line and the ghcertified credit.
- Report security issues via private vulnerability reporting (`SECURITY.md`). Issues/wiki are off for now.
