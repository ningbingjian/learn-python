"""Black-box tests for the first interactive Task Tracker state."""

import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "task_tracker.py"


def run_tracker(user_input: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI with deterministic terminal input."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=user_input,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )


class TaskTrackerCliTests(unittest.TestCase):
    def assert_no_traceback(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_creates_valid_task_and_normalizes_text(self) -> None:
        result = run_tracker("  Learn Python  \n2\n  Finish Module 01  \n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Created task", result.stdout)
        self.assertIn("Title: Learn Python", result.stdout)
        self.assertIn("Priority: 2", result.stdout)
        self.assertIn("Done: False", result.stdout)
        self.assertIn("Note: Finish Module 01", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_normalizes_blank_note_to_none(self) -> None:
        result = run_tracker("Learn Python\n1\n   \n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Note: (none)", result.stdout)

    def test_rejects_blank_title(self) -> None:
        result = run_tracker("   \n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: title cannot be empty.", result.stdout)
        self.assert_no_traceback(result)

    def test_rejects_non_integer_priority(self) -> None:
        result = run_tracker("Learn Python\nhigh\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Error: priority must be an integer from 1 to 3.",
            result.stdout,
        )
        self.assert_no_traceback(result)

    def test_rejects_priority_outside_allowed_range(self) -> None:
        result = run_tracker("Learn Python\n4\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: priority must be between 1 and 3.", result.stdout)
        self.assert_no_traceback(result)


if __name__ == "__main__":
    unittest.main()
