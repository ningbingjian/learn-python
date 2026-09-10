counter = 0


def broken():
    counter += 1  # noqa: F823 - intentional failure observed by this lab
    return counter


def change(items):
    items.append("visible")
    items = ["local"]
    return items


try:
    broken()
except UnboundLocalError:
    print("rebinding before local value: UnboundLocalError")
else:
    raise AssertionError("expected UnboundLocalError")

original = []
returned = change(original)
print("caller:", original)
print("returned:", returned)
assert original == ["visible"] and returned == ["local"]
assert original is not returned and counter == 0
