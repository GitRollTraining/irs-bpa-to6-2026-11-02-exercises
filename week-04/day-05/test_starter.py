"""Checks on the starter itself. They stay true while you work: they do not check your solution."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ("README.md", "START_HERE.md", "CHALLENGE.md", "SUBMISSION.md", "OPTIONAL_TOOLS.md", "SESSION_RECORD.md")


class StarterTests(unittest.TestCase):
    def test_notebook_is_valid_python_source(self):
        source = (ROOT / "notebook.py").read_text(encoding="utf-8")
        self.assertTrue(source.startswith("# Databricks notebook source\n"))
        compile(source, "notebook.py", "exec")

    def test_local_links_resolve(self):
        for page in PAGES:
            text = (ROOT / page).read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", text):
                if target.startswith("http"):
                    continue
                self.assertTrue((ROOT / target).exists(), f"{page} links to missing {target}")

    def test_report_keeps_its_headings(self):
        text = (ROOT / "SUBMISSION.md").read_text(encoding="utf-8")
        for heading in ("## The group's result", "## Which error costs more for this group, and the list",
                        "## Groups A and B", "## Two tasks: trained model or prompting",
                        "### The cover-sheet summary", "### Letters about paying over time",
                        "## Files and limits"):
            self.assertIn(heading, text)
        self.assertNotIn("retrained", text)  # cut on 2026-11-24 to fit the day

    def test_brief_asks_for_two_tasks_and_written_reasons(self):
        text = " ".join((ROOT / "CHALLENGE.md").read_text(encoding="utf-8").split())
        self.assertIn("Our mail room keeps 6,000 past letters of this kind", text)
        self.assertIn("**Choose the technique for two tasks.**", text)
        self.assertNotIn("retrained", text)  # cut on 2026-11-24 to fit the day
        self.assertIn("never your user name or a notebook path", text)
        self.assertIn("explain one choice aloud for 2 to 3 minutes", text)

    def test_brief_keeps_the_tie_rule(self):
        # The tie rule is the Checkpoint's: the list never holds more than the capacity; when
        # returns tie at the cut, the learner breaks the tie and writes how the group chooses.
        text = " ".join((ROOT / "CHALLENGE.md").read_text(encoding="utf-8").split())
        self.assertIn("The list never holds more returns than the capacity", text)
        self.assertIn("you break the tie, and you write down how the group chooses between them", text)
        self.assertNotIn("both go on the list", text)
        report = " ".join((ROOT / "SUBMISSION.md").read_text(encoding="utf-8").split())
        self.assertIn("how the group chooses between them so that the list holds no more than the capacity", report)
        self.assertNotIn("both go on the list", report)


if __name__ == "__main__":
    unittest.main()
