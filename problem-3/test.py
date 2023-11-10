expr = "(((((1 add -4) div (4 div -1)) mul (-2 div 1)) mul (3 mul 0)) sub (((((((-1 add -3) mul 1) add ((x sub 1) mul x)) sub ((((-2 add (x mul x)) add ((x sub -3) mul x)) div (1 div -1)) sub ((((((3 mul 2) add (-3 sub -3)) add ((x sub 2) mul x)) sub ((((((-1 mul (-4 add (-1 add 3))) add (x add ((x sub 2) mul x))) sub 1) add ((x sub 3) mul x)) div (1 div -1)) sub x)) sub 1) sub 3))) sub 3) div (3 div -1)) sub 2))"
expr = expr.replace("mul", "*")
expr = expr.replace("add", "+")
expr = expr.replace("sub", "-")
expr = expr.replace("div", "/")


def target_func(x):  # evolution's target
    return x * (2 * x - 1)


for i in range(5, 20):
    r1, r2 = (eval(expr.replace("x", str(i))), target_func(i))
    print(i, r1, r2)
