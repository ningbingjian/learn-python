from .operations import add_task, complete_task, format_task
from .validation import parse_priority, parse_task_id


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
