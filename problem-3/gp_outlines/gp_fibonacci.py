def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def fib(x, y):
    if x <= 0:
        return 0
    elif x == 1:
        return fib(x-1, y) + fib(x-2, y)

FUNCTIONS = [add, sub, mul, fib]
TERMINALS = ['x', -2, -1, 0, 1, 2]

def target_func(x): # evolution's target
    if x <= 0:
        return 0
    elif x == 1:
        return 1

    return target_func(x - 1) + target_func(x - 2)