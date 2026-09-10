from operations import add_task


def run():
    task = add_task("Read")
    return f"Added {task['title']}"
