print("CLI Task Tracker")
tasks = []
next_task_id = 1

while True:
    command = input("Command (add/list/complete/quit): ").strip().lower()
    match command:
        case "add":
            title = input("Task title: ").strip()
            if not title:
                print("Error: title cannot be empty.")
                continue
            priority_text = input("Priority (1-3): ").strip()
            try:
                priority = int(priority_text)
            except ValueError:
                print("Error: priority must be an integer from 1 to 3.")
                continue
            if not 1 <= priority <= 3:
                print("Error: priority must be between 1 and 3.")
                continue
            note = input("Note (optional): ").strip() or None
            tasks.append(
                {
                    "id": next_task_id,
                    "title": title,
                    "priority": priority,
                    "done": False,
                    "note": note,
                }
            )
            print(f"Added task #{next_task_id}.")
            next_task_id += 1
        case "list":
            if not tasks:
                print("No tasks.")
            for task in tasks:
                marker = "[x]" if task["done"] else "[ ]"
                note_display = "(none)" if task["note"] is None else task["note"]
                print(
                    f"#{task['id']} {marker} {task['title']} "
                    f"| priority={task['priority']} | note={note_display}"
                )
        case "complete":
            try:
                task_id = int(input("Task id: ").strip())
            except ValueError:
                print("Error: task id must be an integer.")
                continue
            for task in tasks:
                if task["id"] == task_id:
                    if task["done"]:
                        print(f"Task #{task_id} is already complete.")
                    else:
                        task["done"] = True
                        print(f"Completed task #{task_id}.")
                    break
            else:
                print(f"Error: task #{task_id} does not exist.")
        case "quit":
            print("Goodbye.")
            break
        case "":
            print("Enter a command.")
        case _:
            print(f"Unknown command: {command}")
