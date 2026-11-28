"""Tests for scripts/assemble.py: the landing page's contributor section. Run: python -m unittest discover -s scripts"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import assemble  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "assemble.py"


def fake_out(root: Path, people: list[dict] | str | None) -> Path:
    """A minimal built app: en.html plus, optionally, contributors.json and an avatar file per valid entry."""
    out = root / "out"
    (out / "contributors").mkdir(parents=True)
    (out / "en.html").write_text("<!doctype html><html lang=en><title>x</title></html>", encoding="utf-8")
    if people is not None:
        raw = people if isinstance(people, str) else json.dumps(people)
        (out / "contributors" / "contributors.json").write_text(raw, encoding="utf-8")
        if isinstance(people, list):
            for c in people:
                if isinstance(c, dict) and isinstance(c.get("avatar"), str) and c["avatar"].startswith("/contributors/"):
                    (out / c["avatar"].lstrip("/")).write_bytes(b"png")
    return out


def run(out: Path, dist: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), str(out), str(dist)], capture_output=True, text=True)


class LoadContributors(unittest.TestCase):
    def test_valid_entries_only(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            out = fake_out(Path(d), [
                {"login": "octocat", "avatar": "/contributors/octocat.png", "contributions": 3},
                {"login": "<script>", "avatar": "/contributors/x.png", "contributions": 1},
                {"login": "evil", "avatar": "https://example.com/e.png", "contributions": 1},
                {"login": "dots", "avatar": "/contributors/../../etc.png", "contributions": 1},
                "not-a-dict",
            ])
            (out / "contributors" / "nofile.png").unlink(missing_ok=True)
            people = assemble.load_contributors(out)
            self.assertEqual([c["login"] for c in people], ["octocat"])

    def test_avatar_file_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            out = fake_out(Path(d), [{"login": "ghost", "avatar": "/contributors/ghost.png", "contributions": 1}])
            (out / "contributors" / "ghost.png").unlink()
            self.assertEqual(assemble.load_contributors(out), [])

    def test_missing_or_broken_file(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(assemble.load_contributors(fake_out(Path(d) / "a", None)), [])
            self.assertEqual(assemble.load_contributors(fake_out(Path(d) / "b", "{not json")), [])
            self.assertEqual(assemble.load_contributors(fake_out(Path(d) / "c", '{"login": "x"}')), [])


class Render(unittest.TestCase):
    def test_empty_renders_nothing(self) -> None:
        self.assertEqual(assemble.render_contributors([]), "")

    def test_singular_and_plural(self) -> None:
        one = [{"login": "a", "avatar": "/contributors/a.png", "contributions": 1}]
        self.assertIn("1 person has helped", assemble.render_contributors(one))
        self.assertIn('title="a: 1 contribution"', assemble.render_contributors(one))
        two = one + [{"login": "b", "avatar": "/contributors/b.png", "contributions": 5}]
        html = assemble.render_contributors(two)
        self.assertIn("2 people have helped", html)
        self.assertIn('href="https://github.com/b"', html)
        self.assertIn('src="/contributors/b.png"', html)
        self.assertNotIn("style=", html)


class EndToEnd(unittest.TestCase):
    def test_landing_page_gets_contributors(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            out = fake_out(Path(d), [
                {"login": "octocat", "avatar": "/contributors/octocat.png", "contributions": 26},
                {"login": "hubot", "avatar": "/contributors/hubot.jpg", "contributions": 2},
            ])
            dist = Path(d) / "dist"
            r = run(out, dist)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("2 contributors", r.stdout)
            page = (dist / "index.html").read_text(encoding="utf-8")
            self.assertNotIn(assemble.CONTRIBUTORS_MARKER, page)
            self.assertIn("2 people have helped build getazcertified", page)
            self.assertIn('<img src="/contributors/hubot.jpg"', page)
            self.assertIn("CONTRIBUTING.md", page)

    def test_no_contributors_hides_list_and_warns(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            dist = Path(d) / "dist"
            r = run(fake_out(Path(d), None), dist)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("::warning::", r.stderr)
            page = (dist / "index.html").read_text(encoding="utf-8")
            self.assertNotIn(assemble.CONTRIBUTORS_MARKER, page)
            self.assertNotIn('class="avatars"', page)
            self.assertIn("Contribute on GitHub", page)

    def test_site_keeps_the_marker(self) -> None:
        text = (assemble.SITE / "index.html").read_text(encoding="utf-8")
        self.assertEqual(text.count(assemble.CONTRIBUTORS_MARKER), 1, "site/index.html lost the contributors marker")


if __name__ == "__main__":
    unittest.main()
