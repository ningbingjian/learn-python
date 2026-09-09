import math

total = 0.1 + 0.2
expected = 0.3
difference = abs(total - expected)

print(f"total repr: {total!r}")
print(f"expected repr: {expected!r}")
print(f"exactly equal: {total == expected}")
print(f"difference: {difference!r}")
print(f"close enough: {math.isclose(total, expected)}")
