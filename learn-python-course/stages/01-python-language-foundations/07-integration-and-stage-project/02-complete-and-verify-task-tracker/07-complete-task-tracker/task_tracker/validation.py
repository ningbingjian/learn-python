def clean_fields(title, priority, note=None):
    title = title.strip()
    if not title:
        raise ValueError("title cannot be empty.")
    if type(priority) is not int or not 1 <= priority <= 3:
        raise ValueError("priority must be between 1 and 3.")
    note = note.strip() if note is not None else None
    return title, priority, note or None


def parse_priority(text):
    try:
        priority = int(text)
    except ValueError:
        raise ValueError("priority must be an integer from 1 to 3.") from None
    if not 1 <= priority <= 3:
        raise ValueError("priority must be between 1 and 3.")
    return priority


def parse_task_id(text):
    try:
        return int(text)
    except ValueError:
        raise ValueError("task id must be an integer.") from None
