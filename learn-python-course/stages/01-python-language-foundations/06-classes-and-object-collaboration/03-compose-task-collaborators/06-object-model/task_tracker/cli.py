from .validation import parse_priority, parse_task_id


def format_task(task):
    marker = "x" if task.done else " "
    note = task.note if task.note is not None else "(none)"
    return (
        f"#{task.id} [{marker}] {task.title} | priority={task.priority} | note={note}"
    )


def run_cli(tracker, read=input, write=print):
    write("CLI Task Tracker")
    while True:
        command = read("Command (add/list/complete/quit): ").strip().lower()
        try:
            match command:
                case "add":
                    title = read("Task title: ").strip()
                    if not title:
                        raise ValueError("title cannot be empty.")
                    priority = parse_priority(read("Priority (1-3): ").strip())
                    note = read("Note (optional): ")
                    task = tracker.add(title, priority, note)
                    write(f"Added task #{task.id}.")
                case "list":
                    tasks = tracker.all_tasks()
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
                case "quit":
                    write("Goodbye.")
                    break
                case "":
                    write("Enter a command.")
                case _:
                    write(f"Unknown command: {command}")
        except ValueError as error:
            write(f"Error: {error}")
