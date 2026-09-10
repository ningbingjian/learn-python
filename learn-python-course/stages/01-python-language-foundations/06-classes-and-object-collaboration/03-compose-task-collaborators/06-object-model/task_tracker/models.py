from .validation import clean_fields


class Task:
    def __init__(self, task_id, title, priority, note=None):
        self.id = task_id
        self.title, self.priority, self.note = clean_fields(title, priority, note)
        self.done = False

    def complete(self):
        if self.done:
            return False
        self.done = True
        return True
