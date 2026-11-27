"""Tests for check_questions.py: python3 -m unittest discover -s scripts"""

import re
import tempfile
import unittest
from pathlib import Path

import check_questions as cq

GOOD = '''---
question: |-
  You have an Azure subscription that contains a storage account named stfab01.

  Which two actions can you perform?
documentation:
  - title: "Storage account overview"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] First
  > Why first is right.
- [x] Second
  > Why second is right.
- [ ] Third
  > Why third is wrong.
'''


def write(tmp: Path, text: str, cert: str = "az-104") -> Path:
    d = tmp / cert
    d.mkdir(parents=True, exist_ok=True)
    p = d / "question-001.md"
    p.write_text(text, encoding="utf-8")
    return p


class CheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def errors(self, text: str) -> list[str]:
        return cq.check(cq.load(write(self.tmp, text)))

    def test_good_question_passes(self):
        self.assertEqual(self.errors(GOOD), [])

    def test_block_question_keeps_paragraphs(self):
        q = cq.load(write(self.tmp, GOOD))
        self.assertIn("stfab01.\n\nWhich two", q.meta["question"])

    def test_hard_wrapped_stem(self):
        bad = GOOD.replace("named stfab01.", "named\n  stfab01.")
        self.assertTrue(any("hard-wrapped" in e for e in self.errors(bad)))

    DOC_BLOCK = (
        'documentation:\n'
        '  - title: "Storage account overview"\n'
        '    url: "https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview"\n'
    )

    def with_docs(self, *entries: tuple[str, str]) -> str:
        items = "".join(f'  - title: "{t}"\n    url: "{u}"\n' for t, u in entries)
        return GOOD.replace(self.DOC_BLOCK, "documentation:\n" + items)

    def load_error(self, text: str) -> str:
        with self.assertRaises(cq.FormatError) as ctx:
            cq.load(write(self.tmp, text))
        return str(ctx.exception)

    def test_missing_documentation(self):
        self.assertIn("missing documentation", self.errors(GOOD.replace(self.DOC_BLOCK, "")))

    def test_empty_documentation_list(self):
        self.assertIn("missing documentation", self.errors(self.with_docs()))

    def test_documentation_entries_parse(self):
        text = self.with_docs(
            ("Storage account overview", "https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview"),
            ("Azure Storage redundancy", "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy"),
        )
        q = cq.load(write(self.tmp, text))
        self.assertEqual(
            [d["title"] for d in q.meta["documentation"]], ["Storage account overview", "Azure Storage redundancy"]
        )
        self.assertEqual(cq.check(q), [])

    def test_old_single_url_form_is_rejected_with_example(self):
        msg = self.load_error(GOOD.replace(self.DOC_BLOCK, 'documentation: "https://learn.microsoft.com/en-us/azure/"\n'))
        self.assertIn("title + url", msg)
        self.assertIn('title: "', msg)

    def test_old_url_list_form_is_rejected(self):
        msg = self.load_error(GOOD.replace(self.DOC_BLOCK, 'documentation:\n  - "https://learn.microsoft.com/en-us/azure/"\n'))
        self.assertIn("must start with a title line", msg)

    def test_title_without_url_line(self):
        msg = self.load_error(GOOD.replace(self.DOC_BLOCK, 'documentation:\n  - title: "Storage account overview"\n'))
        self.assertIn("needs a url line", msg)

    def test_url_before_title_is_rejected(self):
        self.load_error(GOOD.replace(
            self.DOC_BLOCK, 'documentation:\n  - url: "https://learn.microsoft.com/en-us/azure/"\n    title: "Overview"\n'
        ))

    def test_title_length_limit(self):
        u = "https://learn.microsoft.com/en-us/azure/"
        ok = "A" + "b" * 39
        self.assertEqual(self.errors(self.with_docs((ok, u))), [])
        errs = self.errors(self.with_docs((ok + "c", u)))
        self.assertTrue(any("is 41 characters; keep it to 40" in e for e in errs), errs)
        self.assertTrue(any("too short" in e for e in self.errors(self.with_docs(("", u)))))

    def test_title_style_rules(self):
        u = "https://learn.microsoft.com/en-us/azure/"
        cases = {
            "Storage overview.": "ends with a period",
            "[Storage](x)": "Markdown",
            "Storage docs": "filler",
            "Alerts - Azure Monitor": "filler",
            "storage overview": "capital letter",
            " Storage": "extra spaces",
        }
        for title, expected in cases.items():
            errs = self.errors(self.with_docs((title, u)))
            self.assertTrue(any(expected in e for e in errs), (title, errs))

    def test_main_title_limit_with_several_links(self):
        u = "https://learn.microsoft.com/en-us/azure/"
        main31 = "Share-level permissions for Az" + "x"
        self.assertEqual(len(main31), 31)
        errs = self.errors(self.with_docs((main31, u + "a"), ("Second page", u + "b")))
        self.assertTrue(any("keep it to 30" in e and "Main page" in e for e in errs), errs)
        # one link: no tag, so the 40 limit applies; later entries too
        self.assertEqual(self.errors(self.with_docs((main31, u + "a"))), [])
        self.assertEqual(self.errors(self.with_docs(("Main", u + "a"), (main31, u + "b"))), [])

    def test_one_title_per_page_across_questions(self):
        u = "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy"
        qs = []
        for i, title in enumerate(["Azure Storage redundancy", "Storage redundancy"], 1):
            p = write(self.tmp, self.with_docs((title, u)))
            p = p.rename(p.with_name(f"question-00{i}.md"))
            qs.append(cq.load(p))
        errs = cq.check_doc_titles(qs)
        self.assertEqual(len(errs), 1, errs)
        self.assertIn("question-002.md", errs[0])
        self.assertIn("'Azure Storage redundancy'", errs[0])
        self.assertEqual(cq.check_doc_titles(qs, report={qs[0].path}), [])

    def test_foreign_host_in_documentation(self):
        errs = self.errors(self.with_docs(
            ("Overview", "https://learn.microsoft.com/en-us/azure/"), ("Elsewhere", "https://example.com/x")
        ))
        self.assertTrue(any("documentation must be" in e for e in errs))

    def test_duplicate_links_titles_and_too_many(self):
        u = "https://learn.microsoft.com/en-us/azure/"
        self.assertTrue(any("same link twice" in e for e in self.errors(self.with_docs(("One", u), ("Two", u)))))
        dup_title = self.with_docs(("Same", u + "a"), ("same", u + "b"))
        self.assertTrue(any("same title twice" in e for e in self.errors(dup_title)))
        many = [(f"Page {n}", f"{u}page-{n}") for n in range(4)]
        self.assertTrue(any("at most 3" in e for e in self.errors(self.with_docs(*many))))

    def test_list_only_allowed_for_documentation(self):
        text = GOOD.replace('archetype: "choose-n"\n', 'archetype:\n  - "choose-n"\n')
        self.assertTrue(any("archetype must be a single value" in e for e in self.errors(text)))

    def test_unknown_skill_area_and_archetype(self):
        bad = GOOD.replace('"storage-accounts"', '"storage-stuff"').replace('"choose-n"', '"trivia"')
        errs = self.errors(bad)
        self.assertTrue(any("unknown skill_area" in e for e in errs))
        self.assertTrue(any("unknown archetype" in e for e in errs))

    def test_wrong_study_guide(self):
        self.assertTrue(any("study_guide" in e for e in self.errors(GOOD.replace("2026-04-17", "2025-01-01"))))

    def test_answer_without_explanation(self):
        bad = GOOD.replace("  > Why third is wrong.\n", "")
        self.assertTrue(any("has no explanation" in e for e in self.errors(bad)))

    def test_choose_count_mismatch(self):
        bad = GOOD.replace("- [ ] Third", "- [x] Third")
        self.assertTrue(any("asks for two" in e for e in self.errors(bad)))

    def test_multi_correct_without_count(self):
        bad = GOOD.replace("Which two actions", "Which actions").replace('"choose-n"', '"best-choice"')
        self.assertTrue(any("doesn't say" in e for e in self.errors(bad)))

    def test_yes_no_archetype_needs_yes_no(self):
        bad = GOOD.replace('"choose-n"', '"exhibit-statement"')
        self.assertTrue(any("exactly Yes and No" in e for e in self.errors(bad)))

    def test_exhibit_needs_block(self):
        text = (GOOD.replace("Which two actions can you perform?", "Is the statement true?")
                .replace('"choose-n"', '"exhibit-statement"')
                .split("\n---\n")[0]
                + "\n---\n\n- [x] Yes\n  > Because.\n- [ ] No\n  > Because not.\n")
        errs = self.errors(text)
        self.assertIn("exhibit question has no exhibit block", errs)
        fixed = text.replace("\n---\n\n", "\n---\n\n```text\nName  Kind\nst1   StorageV2\n```\n\n")
        self.assertEqual(self.errors(fixed), [])

    def test_answers_must_not_point_at_other_answers(self):
        for text in ("All of the above", "None of the following", "Both of the above", "Answers A and B", "Option 2"):
            bad = GOOD.replace("- [ ] Third", f"- [ ] {text}")
            self.assertTrue(any("refers to other answers" in e for e in self.errors(bad)), text)
        # Ordinary words must not trip it.
        ok = GOOD.replace("- [ ] Third", "- [ ] Assign the Reader role to all of the users")
        self.assertEqual(self.errors(ok), [])

    def test_option_count(self):
        two = GOOD.replace("- [ ] Third\n  > Why third is wrong.\n", "")
        self.assertTrue(any("use 3 to 6" in e for e in self.errors(two.replace('"choose-n"', '"best-choice"')
                                                                    .replace("Which two actions", "Which action")
                                                                    .replace("- [x] Second", "- [ ] Second"))))
        seven = GOOD + "".join(f"- [ ] Extra {n}\n  > Why not.\n" for n in range(5))
        self.assertTrue(any("has 8 answers" in e for e in self.errors(seven)))

    def test_lead_in_archetypes_end_with_a_question(self):
        bad = GOOD.replace("Which two actions can you perform?", "Select two actions.")
        self.assertTrue(any("must end with its question" in e for e in self.errors(bad)))

    def test_goal_solution_shape(self):
        head = (GOOD.replace("Which two actions can you perform?", "You need to block public access.\n\n  Solution: You set X.\n\n  Is that enough?")
                .replace('"choose-n"', '"goal-solution"').split("\n---\n")[0])
        text = head + "\n---\n\n- [x] Yes\n  > Because.\n- [ ] No\n  > Because not.\n"
        self.assertTrue(any("Does this meet the goal?" in e for e in self.errors(text)))
        fixed = text.replace("Is that enough?", "Does this meet the goal?")
        self.assertEqual(self.errors(fixed), [])

    def test_unknown_key_and_unsupported_yaml(self):
        self.assertTrue(any("unknown frontmatter key" in e for e in self.errors(GOOD.replace("---\n\n-", 'extra: "x"\n---\n\n-'))))
        with self.assertRaises(cq.FormatError):
            cq.parse_frontmatter("---\ntags: [a, b]\n---\n")

    def test_answers_inside_fence_are_ignored(self):
        text = GOOD.replace("---\n\n- [x] First", "---\n\n```text\n- [x] not an answer\n```\n\n- [x] First")
        self.assertEqual(len(cq.load(write(self.tmp, text)).answers), 3)

    def test_weights_skip_partial_set(self):
        qs = [cq.load(write(self.tmp, GOOD))] * 40
        self.assertEqual(cq.check_weights(qs), [])

    def test_weights_flag_lopsided_full_set(self):
        base = cq.load(write(self.tmp, GOOD))
        areas = ["storage-accounts"] * 36 + ["entra-users-groups", "arm-bicep", "virtual-networks", "backup-recovery"]
        qs = [cq.Question(path=base.path, cert="az-104", meta={**base.meta, "skill_area": a}) for a in areas]
        errs = cq.check_weights(qs)
        self.assertTrue(any("storage is 90.0%" in e for e in errs))


if __name__ == "__main__":
    unittest.main()


GOOD_CERT = {
    "id": "sc-500",
    "title": "Security Operations Analyst (SC-500)",
    "description": "Threat detection and response with Microsoft security tools for a test certification.",
    "status": "draft",
    "level": "associate",
    "study_guide": "2026-05-01",
    "color": 2,
    "icon": "shield-check",
    "domains": [{"id": "detect", "name": "Detect threats", "weight": [20, 30], "skill_areas": ["alerts"]}],
}


class CertRegistryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def certs(self, **changes) -> tuple[dict, list[str]]:
        import json
        c = dict(GOOD_CERT, **changes)
        (self.dir / f"{c['id'] if isinstance(c['id'], str) else 'x'}.json").write_text(json.dumps(c), encoding="utf-8")
        return cq.load_certs(self.dir)

    def test_good_cert_loads(self):
        certs, errs = self.certs()
        self.assertEqual(errs, [])
        self.assertIn("sc-500", certs)

    def test_real_registry_is_clean(self):
        self.assertEqual(cq.CERT_ERRORS, [])
        self.assertEqual(cq.CERTS["az-104"]["status"], "live")
        self.assertIn("storage-accounts", cq.SKILL_AREAS["az-104"]["storage"])

    def test_bad_values_say_how_to_fix(self):
        cases = {
            "icon": ("microsoft-logo", "pick one of"),
            "color": (12, "palette slot from 1 to 8"),
            "status": ("published", '"draft"'),
            "study_guide": ("May 2026", "YYYY-MM-DD"),
            "level": ("hard", "level must be one of"),
        }
        for key, (value, expected) in cases.items():
            _, errs = self.certs(**{key: value})
            self.assertTrue(any(expected in e for e in errs), (key, errs))
            for f in self.dir.glob("*.json"):
                f.unlink()

    def test_id_must_match_file_and_be_an_exam_code(self):
        (self.dir / "sc-500.json").write_text('{"id": "security"}', encoding="utf-8")
        _, errs = cq.load_certs(self.dir)
        self.assertTrue(any("missing" in e for e in errs))
        import json
        (self.dir / "sc-500.json").write_text(json.dumps(dict(GOOD_CERT, id="SC500")), encoding="utf-8")
        _, errs = cq.load_certs(self.dir)
        self.assertTrue(any("match the file name" in e for e in errs))
        self.assertTrue(any("exam code" in e for e in errs))

    def test_invalid_json(self):
        (self.dir / "sc-500.json").write_text('{"id": "sc-500",}', encoding="utf-8")
        _, errs = cq.load_certs(self.dir)
        self.assertTrue(any("not valid JSON" in e for e in errs), errs)

    def test_bad_weight(self):
        _, errs = self.certs(domains=[{"id": "d", "name": "D", "weight": [30, 20], "skill_areas": ["a"]}])
        self.assertTrue(any("weight must be [min, max]" in e for e in errs), errs)


class CrossFileTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def q(self, cert: str, number: str) -> cq.Question:
        return cq.Question(path=self.tmp / "en" / cert / f"question-{number}.md", cert=cert)

    def test_live_cert_needs_enough_questions(self):
        errs = cq.check_certs([self.q("az-104", f"{n:03d}") for n in range(1, 5)])
        self.assertTrue(any("needs at least 20 questions" in e for e in errs), errs)

    def test_folder_without_registry_entry(self):
        qs = [self.q("az-104", f"{n:03d}") for n in range(1, 21)] + [self.q("zz-999", "001")]
        errs = cq.check_certs(qs)
        self.assertTrue(any("questions/certs/zz-999.json: missing" in e for e in errs), errs)

    def test_numbering_gap_names_the_free_number(self):
        qs = [self.q("az-104", "001"), self.q("az-104", "002"), self.q("az-104", "009")]
        errs = cq.check_numbering(qs)
        self.assertEqual(len(errs), 1)
        self.assertIn("rename this file to question-003.md", errs[0])
        self.assertEqual(cq.next_numbers(qs[:2])["az-104"], 3)
        self.assertEqual(cq.next_numbers([qs[0], qs[2]])["az-104"], 2)

    def test_annotation_lines(self):
        path = "questions/en/az-104/question-025.md"
        text = (cq.ROOT / path).read_text(encoding="utf-8").split("\n")
        line = cq.line_for(path, "documentation[2].title 'x' is too long")
        self.assertTrue(text[line - 1].startswith("  - title:"))
        self.assertEqual(cq.split_problem(f"{path}: unknown archetype 'x'"), (path, "unknown archetype 'x'"))
        self.assertTrue(text[cq.line_for(path, "unknown archetype 'x'") - 1].startswith("archetype:"))


class MainOutputTests(unittest.TestCase):
    def test_actions_mode_writes_annotations_summary_and_report(self):
        import contextlib
        import io
        import json
        import os
        from unittest import mock

        with tempfile.TemporaryDirectory() as tmp:
            summary, report = Path(tmp) / "summary.md", Path(tmp) / "report.json"
            out = io.StringIO()
            env = {"GITHUB_ACTIONS": "true", "GITHUB_STEP_SUMMARY": str(summary), "GITHUB_REPOSITORY": "o/r"}
            with mock.patch.dict(os.environ, env), contextlib.redirect_stdout(out):
                code = cq.main([str(cq.ROOT / "questions/en/az-104/question-025.md"), "--report", str(report)])
            self.assertEqual(code, 0)
            data = json.loads(report.read_text())
            self.assertEqual(data["files"][0], {"file": "questions/en/az-104/question-025.md", "ok": True, "problems": []})
            self.assertGreater(data["next_numbers"]["az-104"], 100)
            self.assertIn("https://github.com/o/r/blob/main/CONTRIBUTING.md", summary.read_text())
            self.assertNotIn("::error", out.getvalue())


class ReadmeTableTests(unittest.TestCase):
    def test_real_readme_matches_registry(self):
        self.assertEqual(cq.check_readme_tables(), [])

    def test_draft_cert_needs_no_table(self):
        draft = {"az-900": {"status": "draft", "domains": [{"name": "Describe cloud concepts", "weight": [25, 30], "skill_areas": ["cloud"]}]}}
        self.assertEqual(cq.check_readme_tables(certs=draft), [])
        live = {"az-900": dict(draft["az-900"], status="live")}
        self.assertEqual(len(cq.check_readme_tables(certs=live)), 1)

    def test_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            text = (cq.QUESTIONS / "README.md").read_text(encoding="utf-8").replace("15–20% | `storage-access`", "10–20% | `storage-access`")
            readme.write_text(text, encoding="utf-8")
            errs = cq.check_readme_tables(readme)
            self.assertEqual(len(errs), 1, errs)
            self.assertIn("Implement and manage storage", errs[0])


class DocTemplateTests(unittest.TestCase):
    """The templates contributors copy must pass the checker as they are."""

    def templates(self, doc: str) -> list[str]:
        text = (cq.ROOT / doc).read_text(encoding="utf-8")
        return re.findall(r"````markdown\n(---\n.*?)````", text, re.S)

    def test_doc_templates_pass(self):
        found = 0
        for doc in ("CONTRIBUTING.md", "questions/README.md"):
            for n, tpl in enumerate(self.templates(doc), 1):
                found += 1
                with tempfile.TemporaryDirectory() as tmp:
                    q = cq.load(write(Path(tmp), tpl))
                    self.assertEqual(cq.check(q), [], f"{doc} template {n}")
        self.assertGreaterEqual(found, 2)
