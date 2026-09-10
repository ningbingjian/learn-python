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

    def edit(self, task_id, title, priority, note=None):
        task = self.find(task_id)
        task.update(title, priority, note)
        return task

    def delete(self, task_id):
        task = self.find(task_id)
        self._tasks.remove(task)
        return task

    def select(self, status="all"):
        if status == "all":
            return self.all_tasks()
        if status == "pending":
            return [task for task in self._tasks if not task.done]
        if status == "done":
            return [task for task in self._tasks if task.done]
        raise ValueError("status must be all, pending, or done.")
