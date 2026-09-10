from operations import add_task


def success_message(title):
    return f"Added {title}"


def run():
    return add_task("Read")
