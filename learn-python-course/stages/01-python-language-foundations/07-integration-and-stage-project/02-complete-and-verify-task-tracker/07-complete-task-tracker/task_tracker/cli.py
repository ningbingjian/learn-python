from .tracker import TaskTracker
from .validation import parse_priority, parse_task_id


def format_task(task):
    marker = "x" if task.done else " "
    note = task.note if task.note is not None else "(none)"
    return (
        f"#{task.id} [{marker}] {task.title} | priority={task.priority} | note={note}"
    )


def read_fields(read, editing=False):
    title = read("New title: " if editing else "Task title: ").strip()
    if not title:
        raise ValueError("title cannot be empty.")
    priority = parse_priority(read("Priority (1-3): ").strip())
    note = read("Note (optional; blank clears): " if editing else "Note (optional): ")
    return title, priority, note


def run_cli(tracker, read=input, write=print):
    write("CLI Task Tracker")
    while True:
        command = (
            read(
                "Command (add/list/complete/edit/delete/quit; list --pending/--done): "
            )
            .strip()
            .lower()
        )
        try:
            match command:
                case "add":
                    title, priority, note = read_fields(read)
                    task = tracker.add(title, priority, note)
                    write(f"Added task #{task.id}.")
                case "list" | "list --pending" | "list --done":
                    status = "all" if command == "list" else command.split("--")[1]
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
                    title, priority, note = read_fields(read, editing=True)
                    tracker.edit(task_id, title, priority, note)
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
