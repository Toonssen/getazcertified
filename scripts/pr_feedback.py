#!/usr/bin/env python3
"""PR feedback bot, stage 2: one sticky comment + labels on a pull request after the ci workflow ran.

    python3 scripts/pr_feedback.py <artifact-dir>        (in .github/workflows/pr-feedback.yml, GH_TOKEN set)

Runs from main in a workflow_run job (write token), never on pull-request code. Stage 1 (ci.yml, job `questions`) ran on
the PR's code and left an artifact: pr.txt (PR number), report.json (scripts/check_questions.py --report) and
spelling.txt (cspell). All of that is untrusted:
- the PR number is only used after the API confirms that PR's head is the commit the ci run checked;
- labels come from the PR's file list as the API returns it, from a fixed allowlist (cert:<id> only if that label exists);
- report text is shown inside a code fence longer than any backtick run in it, capped in count and length, so it
  can't format, mention or link anything.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

MARKER = "<!-- pr-feedback -->"
API = "https://api.github.com"
MAX_ITEMS = 40
MAX_ITEM_CHARS = 600
MAX_FILE_BYTES = 512 * 1024
FIRST_TIME = {"FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE"}
CERT_ID_RE = re.compile(r"[a-z]{2,4}-\d{3}")
QUESTION_RE = re.compile(r"questions/en/([a-z]{2,4}-\d{3})/question-\d+\.md")
CONTENT_PREFIXES = ("questions/", "docs/question-style/", "cspell.json", "CONTRIBUTING.md")


def labels_for(files: list[dict], existing: set[str]) -> list[str]:
    """Labels from the PR's changed files (API objects with filename/status)."""
    labels: set[str] = set()
    for f in files:
        name, status = f.get("filename", ""), f.get("status", "")
        if name.startswith(CONTENT_PREFIXES):
            labels.add("content")
        m = QUESTION_RE.fullmatch(name)
        if m:
            labels.add("new-question" if status == "added" else "reword")
            labels.add(f"cert:{m.group(1)}")
        m = re.fullmatch(r"questions/certs/([a-z0-9-]+)\.json", name)
        if m and CERT_ID_RE.fullmatch(m.group(1)):
            labels.add("certification")
            labels.add(f"cert:{m.group(1)}")
        if name.startswith(("app/", "site/")):
            labels.add("site")
        if name in ("app/package.json", "app/package-lock.json"):
            labels.add("deps")
    return sorted(l for l in labels if not l.startswith("cert:") or l in existing)


def touches_content(files: list[dict]) -> bool:
    return any(f.get("filename", "").startswith(CONTENT_PREFIXES) for f in files)


def clean(item: object) -> str:
    """One line of untrusted text: no control characters, capped."""
    text = re.sub(r"[\x00-\x1f\x7f]+", " ", str(item)).strip()
    return text if len(text) <= MAX_ITEM_CHARS else text[: MAX_ITEM_CHARS - 1] + "…"


def fenced(lines: list[str]) -> str:
    """A code block that its content can't close: the fence is longer than any run of backticks inside."""
    longest = max((len(r) for line in lines for r in re.findall(r"`+", line)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n" + "\n".join(lines) + f"\n{fence}"


def capped(items: list[str]) -> list[str]:
    out = [clean(i) for i in items[:MAX_ITEMS]]
    if len(items) > MAX_ITEMS:
        out.append(f"… and {len(items) - MAX_ITEMS} more (see the checks)")
    return out


def render(
    report: dict | None,
    spelling: list[str],
    conclusion: str,
    first_time: bool,
    run_url: str,
    certs: set[str] | None = None,
    other_failed: list[str] | None = None,
) -> str:
    """The comment. certs: show next numbers only for these (the PR's); other_failed: failed jobs besides `questions`."""
    parts = [MARKER]
    if first_time:
        parts.append(
            "👋 Thanks for your first contribution to getazcertified! The checks below run on every push; "
            "a maintainer reviews the content once they pass. Guide: "
            "[CONTRIBUTING.md](https://github.com/Toonssen/getazcertified/blob/main/CONTRIBUTING.md)."
        )
    problems: list[str] = []
    warnings: list[str] = []
    nexts: dict = {}
    if report is not None:
        for f in report.get("files", [])[:1000]:
            for p in f.get("problems", [])[:20]:
                problems.append(f"{f.get('file', '?')}: {p}")
        problems += [str(p) for p in report.get("other_problems", [])[:1000]]
        warnings = [str(w) for w in report.get("warnings", [])[:20]]
        nexts = report.get("next_numbers", {}) if isinstance(report.get("next_numbers"), dict) else {}

    if report is None and not other_failed:
        parts.append(f"### ⚠️ The question checks didn't finish\nSee [the checks]({run_url}) for what went wrong.")
    elif problems or spelling:
        parts.append("### ❌ Some things to fix")
        if problems:
            parts.append("Question rules (also shown inline under *Files changed*):\n\n" + fenced(capped(problems)))
        if spelling:
            parts.append(
                "Spelling: fix the word, or if it's a real Azure term add it to `cspell.json` in this PR.\n\n"
                + fenced(capped(spelling))
            )
        parts.append("Edit the file in this pull request to fix them; the checks run again and this comment updates.")
    if other_failed:
        hint = (
            " `check` fails when a pull request from a fork changes files outside the questions and their docs; "
            "for those please open an issue."
            if "check" in other_failed else ""
        )
        parts.append(f"Also failed: {', '.join(f'`{j}`' for j in other_failed)} (see [the checks]({run_url})).{hint}")
    elif report is not None and not (problems or spelling) and conclusion != "success":
        parts.append(f"### ⚠️ The question rules pass, but another check failed\nSee [the checks]({run_url}).")
    else:
        parts.append("### ✅ All checks passed\nA maintainer will review the content (correct, original, clear, fair).")
    if warnings:
        parts.append("For the maintainer (no action needed):\n\n" + fenced(capped(warnings)))
    good = {
        c: n for c, n in nexts.items()
        if isinstance(c, str) and CERT_ID_RE.fullmatch(c) and isinstance(n, int) and 0 < n < 1000
        and (not certs or c in certs)
    }
    if good:
        parts.append(
            "Next free file name: "
            + ", ".join(f"`questions/en/{c}/question-{n:03d}.md`" for c, n in sorted(good.items()))
        )
    parts.append(f"<sub>[Checks]({run_url}) · updated for every push</sub>")
    return "\n\n".join(parts)


def read_small(path: Path) -> str | None:
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        return None
    return path.read_text(encoding="utf-8", errors="replace")


class GitHub:
    def __init__(self, repo: str, token: str):
        self.repo, self.token = repo, token

    def call(self, method: str, path: str, body: dict | None = None):
        req = urllib.request.Request(
            f"{API}/repos/{self.repo}{path}",
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "getazcertified-pr-feedback",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        return json.loads(data) if data else None

    def pages(self, path: str, limit: int = 5) -> list:
        out: list = []
        for page in range(1, limit + 1):
            sep = "&" if "?" in path else "?"
            batch = self.call("GET", f"{path}{sep}per_page=100&page={page}")
            out += batch
            if len(batch) < 100:
                break
        return out


def run(gh, event: dict, artifact: Path, log=print) -> str:
    wr = event.get("workflow_run") or {}
    if wr.get("event") != "pull_request":
        return "skip: not a pull_request run"
    raw = (read_small(artifact / "pr.txt") or "").strip()
    if not re.fullmatch(r"\d{1,7}", raw):
        return "skip: no PR number in the artifact"
    number = int(raw)
    pr = gh.call("GET", f"/pulls/{number}")
    if pr.get("state") != "open" or pr.get("head", {}).get("sha") != wr.get("head_sha"):
        return f"skip: PR #{number} is closed or has moved on from {wr.get('head_sha')}"
    files = gh.pages(f"/pulls/{number}/files", limit=3)
    existing = {l["name"] for l in gh.pages("/labels", limit=3)}
    labels = labels_for(files, existing)
    if labels:
        gh.call("POST", f"/issues/{number}/labels", {"labels": labels})

    comments = gh.pages(f"/issues/{number}/comments", limit=5)
    mine = next(
        (c for c in comments if c.get("user", {}).get("login") == "github-actions[bot]" and c.get("body", "").startswith(MARKER)),
        None,
    )
    if not touches_content(files) and mine is None:
        return f"PR #{number}: labels {labels}, no question changes, no comment"

    report = None
    text = read_small(artifact / "report.json")
    if text:
        try:
            report = json.loads(text)
            if not isinstance(report, dict):
                report = None
        except ValueError:
            report = None
    spelling = [l for l in (read_small(artifact / "spelling.txt") or "").splitlines() if l.strip()]
    certs = {m.group(1) for f in files if (m := re.match(r"questions/(?:en|certs)/([a-z]{2,4}-\d{3})", f.get("filename", "")))}
    other_failed: list[str] = []
    run_id = wr.get("id")
    if isinstance(run_id, int):
        jobs = gh.call("GET", f"/actions/runs/{run_id}/jobs?per_page=50") or {}
        other_failed = sorted(
            clean(j.get("name", "?")) for j in jobs.get("jobs", [])
            if j.get("conclusion") == "failure" and j.get("name") != "questions"
        )
    body = render(
        report,
        spelling,
        str(wr.get("conclusion")),
        pr.get("author_association") in FIRST_TIME,
        str(wr.get("html_url", "")),
        certs,
        other_failed,
    )
    if mine:
        gh.call("PATCH", f"/issues/comments/{mine['id']}", {"body": body})
    else:
        gh.call("POST", f"/issues/{number}/comments", {"body": body})
    return f"PR #{number}: labels {labels}, comment {'updated' if mine else 'posted'}"


def main(argv: list[str]) -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    gh = GitHub(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"])
    try:
        print(run(gh, event, Path(argv[1])))
    except urllib.error.HTTPError as e:
        print(f"::error::GitHub API {e.code} on {e.url}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
