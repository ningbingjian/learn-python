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


def run_cli():
    tasks = []
    next_id = 1
    print("CLI Task Tracker")
    while True:
        command = input("Command (add/list/complete/quit): ").strip().lower()
        try:
            match command:
                case "add":
                    title = input("Task title: ").strip()
                    if not title:
                        raise ValueError("title cannot be empty.")
                    priority = parse_priority(input("Priority (1-3): ").strip())
                    note = input("Note (optional): ")
                    task, next_id = add_task(tasks, next_id, title, priority, note)
                    print(f"Added task #{task['id']}.")
                case "list":
                    if not tasks:
                        print("No tasks.")
                    for task in tasks:
                        print(format_task(task))
                case "complete":
                    task_id = parse_task_id(input("Task id: ").strip())
                    changed = complete_task(tasks, task_id)
                    if changed:
                        print(f"Completed task #{task_id}.")
                    else:
                        print(f"Task #{task_id} is already complete.")
                case "quit":
                    print("Goodbye.")
                    break
                case "":
                    print("Enter a command.")
                case _:
                    print(f"Unknown command: {command}")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run_cli()
