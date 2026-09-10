"""Regression tests for the author-side structure gate, not learner exercises."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from verify_stage import EXPECTED_UNITS, check_structure


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="stage01-gate-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write_status(self.root, "BUILT")
        for module, units in EXPECTED_UNITS.items():
            self.write_status(self.root / module, "BUILT")
            for unit in units:
                self.write_status(self.root / module / unit, "BUILT")
        self.module = self.root / next(iter(EXPECTED_UNITS))
        self.unit = self.module / EXPECTED_UNITS[self.module.name][0]

    def write_status(self, directory, status):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "README.md").write_text(
            f"# Fixture\n\n> 状态：`{status}`<br>\n\nBUILT is discussed here.\n",
            encoding="utf-8",
        )

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            check_structure(self.root)

    def test_valid_tree(self):
        self.check()

    def test_extra_numbered_module_is_rejected(self):
        for name in ["08-extra", "100-extra", "01-duplicate"]:
            with self.subTest(name=name):
                directory = self.root / name
                directory.mkdir()
                with self.assertRaises(AssertionError):
                    self.check()
                directory.rmdir()

    def test_extra_numbered_unit_is_rejected(self):
        for name in ["04-extra", "99-extra", "01-duplicate"]:
            with self.subTest(name=name):
                directory = self.module / name
                directory.mkdir()
                with self.assertRaises(AssertionError):
                    self.check()
                directory.rmdir()

    def test_renamed_unit_is_rejected(self):
        self.unit.rename(self.module / "01-wrong-name")
        with self.assertRaises(AssertionError):
            self.check()

    def test_substring_status_is_rejected_at_every_level(self):
        for directory in [self.root, self.module, self.unit]:
            for status in ["NOT BUILT", "UNBUILT", "DESIGNED"]:
                with self.subTest(directory=directory.name, status=status):
                    self.write_status(directory, status)
                    with self.assertRaises(AssertionError):
                        self.check()
            self.write_status(directory, "BUILT")

    def test_missing_status_is_rejected(self):
        (self.unit / "README.md").write_text(
            "# BUILT is not a status field\n", encoding="utf-8"
        )
        with self.assertRaises(AssertionError):
            self.check()

    def test_missing_readme_is_rejected(self):
        (self.unit / "README.md").unlink()
        with self.assertRaises(AssertionError):
            self.check()

    def test_expected_non_numbered_support_directory_is_allowed(self):
        (self.module / "support").mkdir()
        self.check()


if __name__ == "__main__":
    unittest.main()
