from .models import Task


class TaskTracker:
    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def add(self, title, priority, note=None):
        task = Task(self._next_id, title, priority, note)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def all_tasks(self):
        return self._tasks.copy()

    def find(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"task #{task_id} does not exist.")

    def complete(self, task_id):
        return self.find(task_id).complete()
