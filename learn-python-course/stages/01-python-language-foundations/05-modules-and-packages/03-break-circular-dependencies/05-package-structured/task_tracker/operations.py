from .validation import clean_fields


def add_task(tasks, next_id, title, priority, note=None):
    title, priority, note = clean_fields(title, priority, note)
    task = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "done": False,
        "note": note,
    }
    tasks.append(task)
    return task, next_id + 1


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError(f"task #{task_id} does not exist.")


def complete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task["done"]:
        return False
    task["done"] = True
    return True


def format_task(task):
    marker = "x" if task["done"] else " "
    note = task["note"] if task["note"] is not None else "(none)"
    return (
        f"#{task['id']} [{marker}] {task['title']} | "
        f"priority={task['priority']} | note={note}"
    )
