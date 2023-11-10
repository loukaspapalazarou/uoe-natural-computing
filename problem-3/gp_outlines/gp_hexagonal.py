def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    if y == 0:
        return float("inf")
    return x / y


FUNCTIONS = [add, sub, mul, div]
TERMINALS = ["x", *range(-4, 5)]
DOMAIN = (0, 100, 1)


def target_func(x):  # evolution's target
    return x * (2 * x - 1)
