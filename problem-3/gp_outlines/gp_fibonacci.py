def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y

FUNCTIONS = [add, sub, mul]
TERMINALS = ['x', -2, -1, 0, 1, 2]

def target_func(x): # evolution's target
    return x*x + 2*x