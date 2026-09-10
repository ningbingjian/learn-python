import unittest

from task_tracker.operations import add_task, complete_task, find_task
from task_tracker.validation import parse_priority


class RuleTests(unittest.TestCase):
    def test_add_normalizes_and_returns_next_id(self):
        tasks = []
        task, next_id = add_task(tasks, 1, " Read ", 2, " ")
        self.assertEqual(
            task, {"id": 1, "title": "Read", "priority": 2, "done": False, "note": None}
        )
        self.assertIs(tasks[0], task)
        self.assertEqual(next_id, 2)

    def test_rejected_add_does_not_mutate(self):
        for title, priority in [("", 1), ("x", 0), ("x", 4), ("x", True)]:
            tasks = []
            with self.assertRaises(ValueError):
                add_task(tasks, 1, title, priority)
            self.assertEqual(tasks, [])

    def test_completion_is_idempotent_and_identity_based(self):
        tasks = []
        task, next_id = add_task(tasks, 7, "Read", 1)
        self.assertEqual(next_id, 8)
        self.assertIs(find_task(tasks, 7), task)
        self.assertTrue(complete_task(tasks, 7))
        self.assertFalse(complete_task(tasks, 7))
        with self.assertRaises(ValueError):
            complete_task(tasks, 0)
        self.assertTrue(task["done"])

    def test_priority_parser(self):
        self.assertEqual(parse_priority(" 2 "), 2)
        for text in ["", "2.5", "abc", "0", "4"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_priority(text)

    def test_separate_lists_do_not_share_tasks(self):
        first, second = [], []
        add_task(first, 1, "A", 1)
        self.assertEqual(second, [])


if __name__ == "__main__":
    unittest.main()
