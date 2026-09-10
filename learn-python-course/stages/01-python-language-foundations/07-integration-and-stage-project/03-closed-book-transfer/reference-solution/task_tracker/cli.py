from .tracker import TaskTracker
from .validation import parse_due, parse_priority, parse_task_id


def format_task(task):
    marker = "x" if task.done else " "
    note = task.note if task.note is not None else "(none)"
    due = "none" if task.due_in_days is None else str(task.due_in_days)
    return (
        f"#{task.id} [{marker}] {task.title} | "
        f"priority={task.priority} | note={note} | due={due}"
    )


def read_fields(read, editing=False):
    title = read("New title: " if editing else "Task title: ").strip()
    if not title:
        raise ValueError("title cannot be empty.")
    priority = parse_priority(read("Priority (1-3): ").strip())
    note = read("Note (optional; blank clears): " if editing else "Note (optional): ")
    due = parse_due(read("Due in days (blank for none): "))
    return title, priority, note, due


def run_cli(tracker, read=input, write=print):
    write("CLI Task Tracker")
    while True:
        command = (
            read(
                "Command (add/list/complete/edit/delete/quit; list --pending/--done/--priority/--due): "
            )
            .strip()
            .lower()
        )
        try:
            match command:
                case "add":
                    title, priority, note, due = read_fields(read)
                    task = tracker.add(title, priority, note, due)
                    write(f"Added task #{task.id}.")
                case (
                    "list"
                    | "list --pending"
                    | "list --done"
                    | "list --priority"
                    | "list --due"
                ):
                    status = "all" if command == "list" else command.split("--")[1]
                    if status == "priority":
                        tasks = tracker.by_priority()
                    elif status == "due":
                        tasks = tracker.due_today()
                    else:
                        tasks = tracker.select(status)
                    if not tasks:
                        write("No tasks.")
                    for task in tasks:
                        write(format_task(task))
                case "complete":
                    task_id = parse_task_id(read("Task id: ").strip())
                    if tracker.complete(task_id):
                        write(f"Completed task #{task_id}.")
                    else:
                        write(f"Task #{task_id} is already complete.")
                case "edit":
                    task_id = parse_task_id(read("Task id: ").strip())
                    tracker.find(task_id)
                    title, priority, note, due = read_fields(read, editing=True)
                    tracker.edit(task_id, title, priority, note, due)
                    write(f"Updated task #{task_id}.")
                case "delete":
                    task_id = parse_task_id(read("Task id: ").strip())
                    tracker.delete(task_id)
                    write(f"Deleted task #{task_id}.")
                case "quit":
                    write("Goodbye.")
                    return 0
                case "":
                    write("Enter a command.")
                case _:
                    write(f"Unknown command: {command}")
        except ValueError as error:
            write(f"Error: {error}")


def main(tracker=None, read=input, write=print):
    if tracker is None:
        tracker = TaskTracker()
    try:
        return run_cli(tracker, read, write)
    except EOFError:
        write("\nInput ended. Goodbye.")
        return 0
    except KeyboardInterrupt:
        write("\nCancelled. Goodbye.")
        return 130
