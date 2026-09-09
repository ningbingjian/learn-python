print("CLI Task Tracker — collection model")

tasks = [
    {
        "id": 1,
        "title": "Learn Python",
        "priority": 2,
        "done": False,
        "note": "Finish Module 01",
    }
]

title = input("Task title: ").strip()
if not title:
    print("Error: title cannot be empty.")
    raise SystemExit(1)

priority_text = input("Priority (1-3): ").strip()
try:
    priority = int(priority_text)
except ValueError:
    print("Error: priority must be an integer from 1 to 3.")
    raise SystemExit(1)

if not 1 <= priority <= 3:
    print("Error: priority must be between 1 and 3.")
    raise SystemExit(1)

note_text = input("Note (optional): ").strip()
note = note_text or None

new_task = {
    "id": 2,
    "title": title,
    "priority": priority,
    "done": False,
    "note": note,
}
tasks.append(new_task)

tasks[0]["done"] = True

first_task = tasks[0]
latest_task = tasks[-1]

print(f"\nTask count: {len(tasks)}")
print(
    f"First task: #{first_task['id']} {first_task['title']} "
    f"| priority={first_task['priority']} | done={first_task['done']}"
)
print(
    f"Newest task: #{latest_task['id']} {latest_task['title']} "
    f"| priority={latest_task['priority']} | done={latest_task['done']}"
)

if latest_task["note"] is None:
    print("Newest note: (none)")
else:
    print(f"Newest note: {latest_task['note']}")
