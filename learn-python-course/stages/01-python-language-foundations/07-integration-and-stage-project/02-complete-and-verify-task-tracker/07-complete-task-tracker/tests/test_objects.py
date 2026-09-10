import unittest

from task_tracker.models import Task
from task_tracker.tracker import TaskTracker


class ObjectTests(unittest.TestCase):
    def test_normalization_and_instance_independence(self):
        first, second = Task(1, " A ", 1, " "), Task(2, "B", 2)
        self.assertEqual(first.title, "A")
        self.assertIsNone(first.note)
        self.assertTrue(first.complete())
        self.assertFalse(first.complete())
        self.assertFalse(second.done)

    def test_failed_add_does_not_consume_id(self):
        tracker = TaskTracker()
        for title, priority in [("", 1), ("A", 0), ("A", 4), ("A", True)]:
            with self.assertRaises(ValueError):
                tracker.add(title, priority)
        self.assertEqual(tracker.all_tasks(), [])
        self.assertEqual(tracker.add("OK", 3).id, 1)

    def test_trackers_do_not_share_state(self):
        first, second = TaskTracker(), TaskTracker()
        first.add("A", 1)
        self.assertEqual(second.all_tasks(), [])
        self.assertEqual(second.add("B", 2).id, 1)

    def test_list_copy_protects_membership_not_objects(self):
        tracker = TaskTracker()
        task = tracker.add("A", 1)
        view = tracker.all_tasks()
        self.assertIs(view[0], task)
        view.clear()
        self.assertEqual(len(tracker.all_tasks()), 1)
        tracker.all_tasks()[0].complete()
        self.assertTrue(tracker.find(1).done)

    def test_completion_and_missing_ids(self):
        tracker = TaskTracker()
        tracker.add("A", 2)
        self.assertTrue(tracker.complete(1))
        self.assertFalse(tracker.complete(1))
        for task_id in [0, -1, 2]:
            with self.assertRaises(ValueError):
                tracker.complete(task_id)


if __name__ == "__main__":
    unittest.main()
