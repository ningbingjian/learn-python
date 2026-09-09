from copy import deepcopy

print("Phase 1 — assignment alias")
tasks = [{"title": "Learn Python", "done": False}]
alias = tasks
alias.append({"title": "Review notes", "done": False})
print(f"same outer list: {alias is tasks}")
print(f"original length after alias append: {len(tasks)}")

print("\nPhase 2 — outer shallow copy")
tasks = [{"title": "Learn Python", "done": False}]
outer_copy = tasks.copy()
outer_copy.append({"title": "Review notes", "done": False})
print(f"same outer list: {outer_copy is tasks}")
print(f"original length after copy append: {len(tasks)}")
print(f"copy length after append: {len(outer_copy)}")
print(f"same inner task: {outer_copy[0] is tasks[0]}")
outer_copy[0]["done"] = True
print(f"original done after copy mutation: {tasks[0]['done']}")

print("\nPhase 3 — record shallow copy")
task = {
    "title": "Learn Python",
    "done": False,
    "tags": ["python"],
}
record_copy = task.copy()
print(f"same record: {record_copy is task}")
record_copy["done"] = True
print(f"original done after record copy rebinding: {task['done']}")
print(f"same nested tags: {record_copy['tags'] is task['tags']}")
record_copy["tags"].append("course")
print(f"original tags after copy mutation: {task['tags']}")

print("\nPhase 4 — deep copy")
task = {
    "title": "Learn Python",
    "done": False,
    "tags": ["python"],
}
deep_snapshot = deepcopy(task)
print(f"same record: {deep_snapshot is task}")
print(f"same nested tags: {deep_snapshot['tags'] is task['tags']}")
deep_snapshot["tags"].append("course")
print(f"original tags after deep copy mutation: {task['tags']}")
print(f"deep copy tags: {deep_snapshot['tags']}")
