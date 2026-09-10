import subprocess
import sys
import unittest
from pathlib import Path

from task_tracker.cli import main
from task_tracker.tracker import TaskTracker

ROOT = Path(__file__).resolve().parents[1]


class DeliveryTests(unittest.TestCase):
    def test_edit_is_atomic_and_preserves_identity_and_done(self):
        tracker = TaskTracker()
        task = tracker.add("A", 2, "old")
        task.complete()
        for title, priority in [("", 1), ("B", 0), ("B", True)]:
            with self.assertRaises(ValueError):
                tracker.edit(1, title, priority, "changed")
            self.assertEqual((task.title, task.priority, task.note), ("A", 2, "old"))
        self.assertIs(tracker.edit(1, " B ", 3, ""), task)
        self.assertEqual(
            (task.id, task.title, task.priority, task.note, task.done),
            (1, "B", 3, None, True),
        )

    def test_delete_never_renumbers_or_reuses_ids(self):
        tracker = TaskTracker()
        tracker.add("A", 1)
        second = tracker.add("B", 2)
        tracker.delete(1)
        self.assertIs(tracker.find(2), second)
        self.assertEqual(tracker.add("C", 3).id, 3)
        with self.assertRaises(ValueError):
            tracker.delete(1)
        self.assertEqual([t.id for t in tracker.all_tasks()], [2, 3])

    def test_filters_preserve_order_and_canonical_collection(self):
        tracker = TaskTracker()
        a, b, c = tracker.add("A", 1), tracker.add("B", 2), tracker.add("C", 3)
        b.complete()
        self.assertEqual(tracker.select("pending"), [a, c])
        self.assertEqual(tracker.select("done"), [b])
        tracker.select("pending").clear()
        self.assertEqual(tracker.select(), [a, b, c])
        with self.assertRaises(ValueError):
            tracker.select("unknown")

    def test_edit_delete_and_filter_transcript(self):
        result = subprocess.run(
            [sys.executable, "-m", "task_tracker"],
            cwd=ROOT,
            input="add\nA\n1\nold\nadd\nB\n2\n\ncomplete\n2\n"
            "list --pending\nlist --done\nedit\n1\nNew\n3\n\n"
            "delete\n2\nadd\nC\n2\n\nlist\nquit\n",
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("#1 [ ] A |", result.stdout)
        self.assertIn("#2 [x] B |", result.stdout)
        final_list = result.stdout.split("Added task #3.")[-1]
        self.assertIn("#1 [ ] New | priority=3 | note=(none)", final_list)
        self.assertIn("#3 [ ] C |", final_list)
        self.assertNotIn("#2 [x]", final_list)

    def test_eof_at_every_add_prompt_does_not_commit(self):
        for lines in [[], ["add"], ["add", "A"], ["add", "A", "2"]]:
            remaining = list(lines)

            def read(prompt):
                if not remaining:
                    raise EOFError
                return remaining.pop(0)

            tracker, output = TaskTracker(), []
            self.assertEqual(main(tracker, read, output.append), 0)
            self.assertEqual(tracker.all_tasks(), [])
            self.assertIn("Input ended.", output[-1])

    def test_eof_at_every_edit_prompt_preserves_task(self):
        for lines in [
            ["edit"],
            ["edit", "1"],
            ["edit", "1", "B"],
            ["edit", "1", "B", "3"],
        ]:
            remaining = list(lines)

            def read(prompt):
                if not remaining:
                    raise EOFError
                return remaining.pop(0)

            tracker = TaskTracker()
            task = tracker.add("A", 2, "old")
            self.assertEqual(main(tracker, read, lambda text: None), 0)
            self.assertEqual((task.title, task.priority, task.note), ("A", 2, "old"))

    def test_interrupt_has_distinct_exit_code(self):
        def read(prompt):
            raise KeyboardInterrupt

        self.assertEqual(main(read=read, write=lambda text: None), 130)

    def test_unexpected_bug_is_not_swallowed(self):
        def read(prompt):
            raise RuntimeError("broken adapter")

        with self.assertRaises(RuntimeError):
            main(read=read, write=lambda text: None)

    def test_bad_edit_recovers_without_partial_change(self):
        remaining = [
            "edit",
            "1",
            "B",
            "4",
            "edit",
            "99",
            "delete",
            "bad",
            "list --everything",
            "quit",
        ]
        tracker, output = TaskTracker(), []
        task = tracker.add("A", 1, "keep")
        self.assertEqual(
            main(tracker, lambda prompt: remaining.pop(0), output.append), 0
        )
        self.assertEqual((task.title, task.priority, task.note), ("A", 1, "keep"))
        self.assertIn("Error: task #99 does not exist.", output)
        self.assertIn("Unknown command: list --everything", output)

    def test_real_process_eof(self):
        result = subprocess.run(
            [sys.executable, "-m", "task_tracker"],
            cwd=ROOT,
            input="add\nA\n2\n",
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertNotIn("Added task", result.stdout)
        self.assertIn("Input ended.", result.stdout)


if __name__ == "__main__":
    unittest.main()
