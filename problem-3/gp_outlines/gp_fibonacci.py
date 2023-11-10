def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def pow(x, y):
    return x**y


def fib(x, y):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, int(x) + 1):
            a, b = b, a + b
        return b


FUNCTIONS = [add, sub, mul, fib]
TERMINALS = ["x", *[i for i in range(10)], *[2 ** (-i) for i in range(4)]]
DOMAIN = (1, 100, 1)


# Target Function: Fibonacci Sequence
def target_func(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, int(x) + 1):
            a, b = b, a + b
        return b
