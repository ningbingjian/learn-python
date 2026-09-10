def broken(title, tasks=[]):
    tasks.append(title)
    return tasks


def fixed(title, tasks=None):
    if tasks is None:
        tasks = []
    tasks.append(title)
    return tasks


first = broken("Read")
second = broken("Test")
print("shared default:", first is second, first)
assert first is second and first == ["Read", "Test"]
first = fixed("Read")
second = fixed("Test")
print("fresh defaults:", first is second, first, second)
assert first is not second and first == ["Read"] and second == ["Test"]
owned = []
assert fixed("Owned", owned) is owned
print("explicit owner:", owned)
