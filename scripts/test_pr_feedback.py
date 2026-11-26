"""Tests for pr_feedback.py: python3 -m unittest discover -s scripts"""

import json
import tempfile
import unittest
from pathlib import Path

import pr_feedback as pf

SHA = "a" * 40
EVENT = {"workflow_run": {"id": 99, "event": "pull_request", "head_sha": SHA, "conclusion": "failure", "html_url": "https://x/run/1"}}


class FakeGitHub:
    def __init__(self, files, comments=(), sha=SHA, association="FIRST_TIME_CONTRIBUTOR", labels=("cert:az-104",)):
        self.files, self.comments, self.sha, self.association = list(files), list(comments), sha, association
        self.labels = [{"name": l} for l in labels]
        self.calls = []

    jobs = ()

    def call(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == "GET" and path.startswith("/actions/runs/"):
            return {"jobs": [{"name": n, "conclusion": c} for n, c in self.jobs]}
        if method == "GET" and path.startswith("/pulls/"):
            return {"state": "open", "head": {"sha": self.sha}, "author_association": self.association}
        return {}

    def pages(self, path, limit=5):
        if path.endswith("/files"):
            return self.files
        if path == "/labels":
            return self.labels
        return self.comments


def artifact(tmp, pr="7", report=None, spelling=""):
    d = Path(tmp)
    (d / "pr.txt").write_text(pr)
    if report is not None:
        (d / "report.json").write_text(json.dumps(report))
    (d / "spelling.txt").write_text(spelling)
    return d


REPORT = {
    "files": [{"file": "questions/en/az-104/question-110.md", "ok": False, "problems": ["skill_area 'x' unknown"]}],
    "other_problems": [],
    "warnings": ["weights: storage 30% > 20%"],
    "next_numbers": {"az-104": 110},
}


class LabelTests(unittest.TestCase):
    def test_new_reword_cert_site(self):
        files = [
            {"filename": "questions/en/az-104/question-110.md", "status": "added"},
            {"filename": "questions/en/az-104/question-003.md", "status": "modified"},
            {"filename": "questions/certs/sc-500.json", "status": "added"},
            {"filename": "app/package-lock.json", "status": "modified"},
        ]
        self.assertEqual(
            pf.labels_for(files, {"cert:az-104"}),
            ["cert:az-104", "certification", "content", "deps", "new-question", "reword", "site"],
        )

    def test_unknown_cert_label_and_odd_names_are_dropped(self):
        files = [{"filename": "questions/certs/Evil Label.json", "status": "added"}]
        self.assertEqual(pf.labels_for(files, set()), ["content"])


class RenderTests(unittest.TestCase):
    def test_untrusted_text_stays_inside_the_fence(self):
        evil = "x ```` @Toonssen [click](https://evil) <img src=x>\n## heading"
        body = pf.render({"files": [], "other_problems": [evil], "next_numbers": {}}, [], "failure", False, "u")
        fence_line = next(l for l in body.splitlines() if l.startswith("`") and l.endswith("text"))
        self.assertEqual(fence_line, "`````text")  # longer than the 4-backtick run
        self.assertIn("x ```` @Toonssen", body)
        self.assertNotIn("\n## heading", body)  # newline flattened

    def test_caps_and_next_numbers(self):
        report = {"files": [], "other_problems": [f"p{i}" for i in range(100)], "next_numbers": {"az-104": 5, "../x": 3}}
        body = pf.render(report, [], "failure", False, "u")
        self.assertIn("… and 60 more", body)
        self.assertIn("`questions/en/az-104/question-005.md`", body)
        self.assertNotIn("../x", body)

    def test_exactly_one_verdict(self):
        verdicts = ("Some things to fix", "All checks passed", "didn't finish", "another check failed")
        cases = [
            ({"files": [], "other_problems": ["p"], "next_numbers": {}}, [], "failure", [], "Some things to fix"),
            ({"files": [], "other_problems": [], "next_numbers": {}}, ["q.md:1: Unknown word (x)"], "failure", [], "Some things to fix"),
            ({"files": [], "other_problems": [], "next_numbers": {}}, [], "success", [], "All checks passed"),
            ({"files": [], "other_problems": [], "next_numbers": {}}, [], "failure", [], "another check failed"),
            (None, [], "failure", [], "didn't finish"),
        ]
        for report, spelling, conclusion, other, want in cases:
            body = pf.render(report, spelling, conclusion, False, "u", None, other)
            self.assertEqual([v for v in verdicts if v in body], [want], (report, spelling, conclusion))
        body = pf.render({"files": [], "other_problems": ["p"], "next_numbers": {}}, [], "failure", False, "u", None, ["check"])
        self.assertIn("Also failed: `check`", body)
        self.assertNotIn("All checks passed", body)

    def test_pass_and_welcome(self):
        body = pf.render({"files": [], "other_problems": [], "next_numbers": {}}, [], "success", True, "u")
        self.assertIn("All checks passed", body)
        self.assertIn("first contribution", body)
        self.assertTrue(body.startswith(pf.MARKER))


class RunTests(unittest.TestCase):
    def test_names_other_failed_jobs_and_only_the_prs_certs(self):
        gh = FakeGitHub([{"filename": "questions/en/az-900/question-001.md", "status": "added"}])
        gh.jobs = (("check", "failure"), ("questions", "failure"), ("unit", "success"))
        report = dict(REPORT, next_numbers={"az-104": 110, "az-900": 2})
        with tempfile.TemporaryDirectory() as tmp:
            pf.run(gh, EVENT, artifact(tmp, report=report))
        body = next(b for m, p, b in gh.calls if m == "POST" and p.endswith("/comments"))["body"]
        self.assertIn("Also failed: `check`", body)
        self.assertIn("from a fork", body)
        nexts = next(l for l in body.splitlines() if l.startswith("Next free file name"))
        self.assertEqual(nexts, "Next free file name: `questions/en/az-900/question-002.md`")

    def test_posts_comment_and_labels(self):
        gh = FakeGitHub([{"filename": "questions/en/az-104/question-110.md", "status": "added"}])
        with tempfile.TemporaryDirectory() as tmp:
            out = pf.run(gh, EVENT, artifact(tmp, report=REPORT, spelling="q.md:3:1 - Unknown word (Azre)"))
        self.assertIn("comment posted", out)
        posts = {p: b for m, p, b in gh.calls if m == "POST"}
        self.assertEqual(posts["/issues/7/labels"]["labels"], ["cert:az-104", "content", "new-question"])
        body = posts["/issues/7/comments"]["body"]
        self.assertIn("skill_area 'x' unknown", body)
        self.assertIn("Azre", body)
        self.assertIn("question-110.md", body)

    def test_updates_own_sticky_comment_only(self):
        comments = [
            {"id": 1, "user": {"login": "someone"}, "body": pf.MARKER + " fake"},
            {"id": 2, "user": {"login": "github-actions[bot]"}, "body": pf.MARKER + " old"},
        ]
        gh = FakeGitHub([{"filename": "questions/en/az-104/question-003.md", "status": "modified"}], comments)
        with tempfile.TemporaryDirectory() as tmp:
            pf.run(gh, EVENT, artifact(tmp, report=REPORT))
        self.assertIn(("PATCH", "/issues/comments/2"), [(m, p) for m, p, _ in gh.calls])
        self.assertNotIn("/issues/7/comments", [p for m, p, _ in gh.calls if m == "POST"])

    def test_stale_sha_or_bad_number_does_nothing(self):
        for gh, pr in ((FakeGitHub([], sha="b" * 40), "7"), (FakeGitHub([]), "7; rm -rf /")):
            with tempfile.TemporaryDirectory() as tmp:
                out = pf.run(gh, EVENT, artifact(tmp, pr=pr, report=REPORT))
            self.assertTrue(out.startswith("skip"), out)
            self.assertEqual([m for m, *_ in gh.calls if m != "GET"], [])

    def test_site_only_pr_gets_labels_but_no_comment(self):
        gh = FakeGitHub([{"filename": "site/index.html", "status": "modified"}])
        with tempfile.TemporaryDirectory() as tmp:
            out = pf.run(gh, EVENT, artifact(tmp, report=REPORT))
        self.assertIn("no comment", out)

    def test_missing_report_says_checks_did_not_finish(self):
        gh = FakeGitHub([{"filename": "questions/en/az-104/question-110.md", "status": "added"}])
        with tempfile.TemporaryDirectory() as tmp:
            pf.run(gh, EVENT, artifact(tmp))
        body = next(b for m, p, b in gh.calls if m == "POST" and p.endswith("/comments"))["body"]
        self.assertIn("didn't finish", body)


if __name__ == "__main__":
    unittest.main()
