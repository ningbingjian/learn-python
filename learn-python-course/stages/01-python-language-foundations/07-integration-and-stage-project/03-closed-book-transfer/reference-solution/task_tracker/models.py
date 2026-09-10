from .validation import clean_due, clean_fields


class Task:
    def __init__(self, task_id, title, priority, note=None, due_in_days=None):
        self.id = task_id
        self.title, self.priority, self.note = clean_fields(title, priority, note)
        self.due_in_days = clean_due(due_in_days)
        self.done = False

    def complete(self):
        if self.done:
            return False
        self.done = True
        return True

    def update(self, title, priority, note=None, due_in_days=None):
        title, priority, note = clean_fields(title, priority, note)
        due_in_days = clean_due(due_in_days)
        self.title = title
        self.priority = priority
        self.note = note
        self.due_in_days = due_in_days
