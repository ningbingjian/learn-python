"""Verify the command contract independently of the implementation structure."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND = [sys.executable, "task_tracker.py"]


class CliTests(unittest.TestCase):
    def run_cli(self, transcript):
        result = subprocess.run(
            COMMAND,
            cwd=ROOT,
            input=transcript,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertNotIn("Traceback", result.stdout)
        self.assertIn("Goodbye.", result.stdout)
        return result.stdout

    def test_empty_list_and_quit(self):
        output = self.run_cli("list\nquit\nadd\n")
        self.assertIn("No tasks.", output)
        self.assertNotIn("Added task", output)

    def test_two_tasks_keep_input_order_and_distinct_states(self):
        output = self.run_cli(
            " ADD \n  First task  \n 1 \n   \n"
            "add\nSecond task\n3\n  Read notes  \nlist\nquit\n"
        )
        first = "#1 [ ] First task | priority=1 | note=(none)"
        second = "#2 [ ] Second task | priority=3 | note=Read notes"
        self.assertIn(first, output)
        self.assertIn(second, output)
        self.assertLess(output.index(first), output.index(second))

    def test_failed_add_does_not_consume_an_id(self):
        cases = [
            ("add\n   \n", "title cannot be empty"),
            ("add\nBad\nhigh\n", "priority must be an integer"),
            ("add\nBad\n2.5\n", "priority must be an integer"),
            ("add\nBad\n0\n", "priority must be between"),
            ("add\nBad\n4\n", "priority must be between"),
        ]
        for failed_input, message in cases:
            with self.subTest(failed_input=failed_input):
                output = self.run_cli(
                    failed_input + "list\nadd\nGood\n2\n\nlist\nquit\n"
                )
                self.assertIn(message, output)
                self.assertIn("No tasks.", output)
                self.assertEqual(output.count("Added task #1."), 1)
                self.assertNotIn("Added task #2.", output)
                self.assertIn("#1 [ ] Good", output)
                self.assertNotIn("[ ] Bad", output)

    def test_complete_uses_business_id_and_keeps_session_alive(self):
        output = self.run_cli(
            "add\nFirst\n1\n\nadd\nSecond\n2\n\ncomplete\n2\nlist\nquit\n"
        )
        self.assertIn("Completed task #2.", output)
        self.assertIn("#1 [ ] First", output)
        self.assertIn("#2 [x] Second", output)
        self.assertNotIn("does not exist", output)

    def test_repeated_completion_is_idempotent(self):
        output = self.run_cli("add\nFirst\n2\n\ncomplete\n1\ncomplete\n1\nlist\nquit\n")
        self.assertEqual(output.count("Completed task #1."), 1)
        self.assertEqual(output.count("Task #1 is already complete."), 1)
        self.assertIn("#1 [x] First", output)

    def test_missing_and_invalid_ids_do_not_modify_tasks(self):
        for task_id in ["abc", "0", "-1", "99"]:
            with self.subTest(task_id=task_id):
                output = self.run_cli(
                    f"add\nFirst\n2\n\ncomplete\n{task_id}\nlist\nquit\n"
                )
                self.assertIn("Error:", output)
                self.assertIn("#1 [ ] First", output)
                self.assertNotIn("Completed task", output)

    def test_search_in_empty_collection(self):
        output = self.run_cli("complete\n1\nlist\nquit\n")
        self.assertIn("Error: task #1 does not exist.", output)
        self.assertIn("No tasks.", output)

    def test_unknown_and_blank_commands_recover(self):
        output = self.run_cli("\n  mystery  \nlist\n QUIT \n")
        self.assertIn("Enter a command.", output)
        self.assertIn("Unknown command: mystery", output)
        self.assertIn("No tasks.", output)


if __name__ == "__main__":
    unittest.main()
