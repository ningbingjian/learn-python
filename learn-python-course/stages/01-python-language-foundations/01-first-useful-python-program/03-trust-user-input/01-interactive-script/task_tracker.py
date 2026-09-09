print("CLI Task Tracker — create one task")

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
done = False

print("\nCreated task")
print(f"Title: {title}")
print(f"Priority: {priority}")
print(f"Done: {done}")

if note is None:
    print("Note: (none)")
else:
    print(f"Note: {note}")
