"""The site's Report link (app/src/lib/report.ts, released from dev) prefills the issue form in this repo by field id;
a renamed field or template would silently stop prefilling. python3 -m unittest discover -s scripts"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / ".github" / "ISSUE_TEMPLATE"
REPORT_TS = ROOT / "app" / "src" / "lib" / "report.ts"


def form_ids(path: Path) -> set[str]:
    return set(re.findall(r"^\s+id: ([a-z0-9-]+)$", path.read_text(encoding="utf-8"), re.M))


class IssueFormTests(unittest.TestCase):
    @unittest.skipUnless(REPORT_TS.exists(), "app not released yet")
    def test_report_link_matches_the_form(self):
        ts = REPORT_TS.read_text(encoding="utf-8")
        template = re.search(r'QUESTION_PROBLEM_FORM = "([^"]+)"', ts).group(1)
        form = FORMS / template
        self.assertTrue(form.exists(), f"app/src/lib/report.ts links {template}, which isn't in .github/ISSUE_TEMPLATE/")
        params = set(re.findall(r'"([a-z]+-[a-z-]+)":', ts))
        self.assertTrue(params, "no prefill parameters found in report.ts")
        missing = params - form_ids(form)
        self.assertEqual(missing, set(), f"report.ts prefills {sorted(missing)}, which {template} doesn't have as field ids")

    def test_every_form_sets_a_label(self):
        for form in FORMS.glob("*.yml"):
            if form.name == "config.yml":
                continue
            text = form.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^labels: \[", f"{form.name}: give the form a label")


if __name__ == "__main__":
    unittest.main()
