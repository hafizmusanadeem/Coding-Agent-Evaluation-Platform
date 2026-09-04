def sum_range(a, b):
    """Return the sum of integers from a to b, INCLUSIVE of b."""
    total = 0
    for i in range(a, b):  # BUG: excludes b, should be range(a, b + 1)
        total += i
    return total


def double(x):
    return x * 2


def is_even(x):
    return x % 2 == 0