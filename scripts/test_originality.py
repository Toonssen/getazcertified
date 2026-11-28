"""Tests for originality.py: python3 -m unittest discover -s scripts"""

import tempfile
import unittest
from pathlib import Path

import check_questions as cq
import originality as og
from test_check_questions import GOOD


def load(tmp: Path, name: str, text: str) -> cq.Question:
    d = tmp / "az-104"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(text, encoding="utf-8")
    return cq.load(d / name)


class OriginalityTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_copy_is_flagged_and_series_is_not(self):
        a = load(self.tmp, "question-001.md", GOOD)
        b = load(self.tmp, "question-002.md", GOOD.replace("stfab01", "stfab02"))
        self.assertEqual(len(og.within_set([a, b], set())), 1)
        series = GOOD.replace('archetype: "choose-n"', 'archetype: "choose-n"\nseries: "s1"')
        c = load(self.tmp, "question-003.md", series)
        d = load(self.tmp, "question-004.md", series.replace("stfab01", "stfab02"))
        self.assertEqual(og.within_set([c, d], set()), [])

    def test_different_question_passes(self):
        a = load(self.tmp, "question-001.md", GOOD)
        other = (GOOD.replace("You have an Azure subscription that contains a storage account named stfab01.",
                              "Your company plans to move twelve on-premises file servers to Azure Files next month.")
                 .replace("- [x] First", "- [x] Alpha").replace("- [x] Second", "- [x] Beta"))
        b = load(self.tmp, "question-002.md", other)
        self.assertEqual(og.within_set([a, b], set()), [])

    def test_learn_run_found(self):
        a = load(self.tmp, "question-001.md", GOOD.replace("Why third is wrong.",
                 "Locks prevent other users from accidentally deleting or modifying critical resources in your subscription."))
        docs = self.tmp / "docs"
        docs.mkdir()
        (docs / "lock.md").write_text("As an administrator, locks prevent other users from accidentally deleting or "
                                      "modifying critical resources in your subscription.", encoding="utf-8")
        runs = og.learn_runs([a], docs, set())
        self.assertTrue(runs and "lock.md" in runs[0], runs)


if __name__ == "__main__":
    unittest.main()
