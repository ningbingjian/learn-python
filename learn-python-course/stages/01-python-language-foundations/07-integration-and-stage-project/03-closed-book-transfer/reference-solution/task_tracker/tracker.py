from .models import Task


def priority_key(task):
    return task.priority


class TaskTracker:
    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def add(self, title, priority, note=None, due_in_days=None):
        task = Task(self._next_id, title, priority, note, due_in_days)
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

    def edit(self, task_id, title, priority, note=None, due_in_days=None):
        task = self.find(task_id)
        task.update(title, priority, note, due_in_days)
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

    def by_priority(self):
        return sorted(self._tasks, key=priority_key)

    def due_today(self):
        return [task for task in self._tasks if not task.done and task.due_in_days == 0]
