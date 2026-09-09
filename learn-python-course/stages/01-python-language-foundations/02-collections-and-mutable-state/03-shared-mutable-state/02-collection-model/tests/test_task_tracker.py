"""Black-box tests for the Task Tracker collection model."""

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


class TaskTrackerCollectionTests(unittest.TestCase):
    def assert_no_traceback(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_adds_normalized_task_to_collection(self) -> None:
        result = run_tracker("  Review collections  \n3\n  Practice nested data  \n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Task count: 2", result.stdout)
        self.assertIn(
            "First task: #1 Learn Python | priority=2 | done=True",
            result.stdout,
        )
        self.assertIn(
            "Newest task: #2 Review collections | priority=3 | done=False",
            result.stdout,
        )
        self.assertIn("Newest note: Practice nested data", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_normalizes_blank_note_to_none(self) -> None:
        result = run_tracker("Review collections\n1\n   \n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Task count: 2", result.stdout)
        self.assertIn("Newest note: (none)", result.stdout)

    def test_rejects_blank_title_before_collection_changes(self) -> None:
        result = run_tracker("   \n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: title cannot be empty.", result.stdout)
        self.assertNotIn("Task count:", result.stdout)
        self.assert_no_traceback(result)

    def test_rejects_non_integer_priority(self) -> None:
        result = run_tracker("Review collections\nhigh\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Error: priority must be an integer from 1 to 3.",
            result.stdout,
        )
        self.assertNotIn("Task count:", result.stdout)
        self.assert_no_traceback(result)

    def test_rejects_priority_outside_allowed_range(self) -> None:
        result = run_tracker("Review collections\n0\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: priority must be between 1 and 3.", result.stdout)
        self.assertNotIn("Task count:", result.stdout)
        self.assert_no_traceback(result)


if __name__ == "__main__":
    unittest.main()
