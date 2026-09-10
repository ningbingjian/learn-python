import subprocess
import sys
import unittest
from pathlib import Path

from task_tracker.cli import main
from task_tracker.tracker import TaskTracker
from task_tracker.validation import parse_due

ROOT = Path(__file__).resolve().parents[1]


class TransferTests(unittest.TestCase):
    def test_parser_preserves_zero_and_none(self):
        self.assertIsNone(parse_due(" "))
        self.assertEqual(parse_due("0"), 0)
        self.assertEqual(parse_due(" 2 "), 2)
        for text in ["-1", "2.5", "abc"]:
            with self.assertRaises(ValueError):
                parse_due(text)

    def test_model_rejects_invalid_due_without_consuming_id(self):
        tracker = TaskTracker()
        for due in [-1, True, False, 2.5, "0"]:
            with self.assertRaises(ValueError):
                tracker.add("A", 1, due_in_days=due)
        self.assertEqual(tracker.all_tasks(), [])
        self.assertEqual(tracker.add("A", 1).id, 1)

    def test_edit_is_atomic_and_can_clear_due(self):
        tracker = TaskTracker()
        task = tracker.add("A", 2, "old", 0)
        task.complete()
        with self.assertRaises(ValueError):
            tracker.edit(1, "B", 1, "new", -1)
        self.assertEqual(
            (task.title, task.priority, task.note, task.due_in_days), ("A", 2, "old", 0)
        )
        tracker.edit(1, "B", 1, None, None)
        self.assertIsNone(task.due_in_days)
        self.assertTrue(task.done)
        self.assertEqual(task.id, 1)

    def test_sort_is_stable_and_does_not_mutate_storage(self):
        tracker = TaskTracker()
        tracker.add("A", 2)
        tracker.add("B", 1)
        tracker.add("C", 1)
        self.assertEqual([t.id for t in tracker.by_priority()], [2, 3, 1])
        self.assertEqual([t.id for t in tracker.all_tasks()], [1, 2, 3])
        self.assertIs(tracker.by_priority()[0], tracker.find(2))

    def test_due_filter_distinguishes_none_zero_and_done(self):
        tracker = TaskTracker()
        a = tracker.add("today", 1, due_in_days=0)
        b = tracker.add("done", 1, due_in_days=0)
        tracker.add("later", 1, due_in_days=2)
        tracker.add("none", 1)
        b.complete()
        self.assertEqual(tracker.due_today(), [a])
        self.assertEqual(len(tracker.all_tasks()), 4)

    def test_new_and_existing_commands_in_one_session(self):
        result = subprocess.run(
            [sys.executable, "-m", "task_tracker"],
            cwd=ROOT,
            input="add\nA\n2\n\n0\nadd\nB\n1\n\n\n"
            "list --priority\nlist --due\nedit\n2\nB2\n1\n\n0\n"
            "complete\n1\nlist --pending\nlist --done\nlist --due\n"
            "delete\n1\nadd\nC\n3\n\n2\nlist\nquit\n",
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("#1 [x] A | priority=2 | note=(none) | due=0", result.stdout)
        self.assertIn("#2 [ ] B2 | priority=1 | note=(none) | due=0", result.stdout)
        tail = result.stdout.split("Added task #3.")[-1]
        self.assertNotIn("#1 [", tail)
        self.assertIn("#3 [ ] C | priority=3 | note=(none) | due=2", tail)

    def test_eof_at_new_add_and_edit_prompt_does_not_commit(self):
        for lines in [["add", "A", "2", ""], ["edit", "1", "B", "3", "new"]]:
            pending = list(lines)

            def read(prompt):
                if not pending:
                    raise EOFError
                return pending.pop(0)

            tracker = TaskTracker()
            task = tracker.add("old", 1, "keep", 0)
            self.assertEqual(main(tracker, read, lambda text: None), 0)
            self.assertEqual(len(tracker.all_tasks()), 1)
            self.assertEqual(
                (task.title, task.priority, task.note, task.due_in_days),
                ("old", 1, "keep", 0),
            )
            self.assertEqual(tracker.add("next", 2).id, 2)

    def test_invalid_due_recovers_and_preserves_old_data(self):
        pending = [
            "add",
            "Bad",
            "1",
            "",
            "-1",
            "edit",
            "1",
            "New",
            "3",
            "new note",
            "2.5",
            "complete",
            "99",
            "",
            "unknown",
            "quit",
        ]
        tracker, output = TaskTracker(), []
        task = tracker.add("A", 2, "keep", 0)
        self.assertEqual(main(tracker, lambda prompt: pending.pop(0), output.append), 0)
        self.assertEqual(
            (task.title, task.priority, task.note, task.due_in_days),
            ("A", 2, "keep", 0),
        )
        self.assertEqual(len(tracker.all_tasks()), 1)
        self.assertIn("Error: task #99 does not exist.", output)
        self.assertIn("Enter a command.", output)

    def test_empty_new_filters_and_repeat_complete(self):
        pending = [
            "list --due",
            "list --priority",
            "add",
            "A",
            "2",
            "",
            "0",
            "complete",
            "1",
            "complete",
            "1",
            "list --due",
            "quit",
        ]
        output = []
        self.assertEqual(
            main(read=lambda prompt: pending.pop(0), write=output.append), 0
        )
        self.assertEqual(output.count("No tasks."), 3)
        self.assertIn("Task #1 is already complete.", output)


if __name__ == "__main__":
    unittest.main()
