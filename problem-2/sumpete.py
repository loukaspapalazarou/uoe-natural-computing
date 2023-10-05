# 90744:6,3,1,7,9,3,9,5,8;1,12,17;9,9,12;2,2,1,2,1,1,1,2,1;90744;1;0;1

# 6,3,1,7,9,3,9,5,8;1,12,17;9,9,12;2,2,1,2,1,1,1,2,1;1;0;1

# [6,3,1,7,9,3,9,5,8];[1,12,17];[9,9,12];[2,2,1,2,1,1,1,2,1];1;0;1
# [matrix];[row sums];[col sums];[solution matrix];dunno

# 6 3 1 | 1
# 7 9 3 | 12
# 9 5 8 |17
# - - -
# 9 9 12

# 0 0 1
# 0 1 1
# 1 0 1
import math


def generate_problem():
    pass


def validate_input(input: str) -> int:
    if not input.__contains__(";"):
        raise ValueError("Input must contain semicolons.")
    args = input.split(";")
    if len(args) != 3:
        raise ValueError("Input must be divided in 3 sections separated by ';'.")
    input_matrix = args[0]
    input_matrix = input_matrix.split(",")
    k = math.sqrt(len(input_matrix))
    if not k.is_integer():
        raise ValueError("Input matrix must be square.")
    if len(args[1].split(",")) != k or len(args[2].split(",")) != k:
        raise ValueError("Amount of target sums is incorrect.")
    return k


def str_to_matrix(input_str: str) -> list[list[int]]:
    k = int(math.sqrt(len(input_str)))
    flat_matrix = input_str.split(",")
    ptr = 0
    matrix = []
    for i in range(k - 1):
        matrix.append([])
        for _ in range(k - 1):
            matrix[i].append(int(flat_matrix[ptr]))
            ptr += 1
    return matrix


def fitness_binary(candidate: str) -> int:
    # assume fitness matrix format is correct
    pass
    solution = "0,0,1,0,1,0,1,0,1"


def fitness_improved():
    pass


def solver(problem, generations=1000, population_size=100, mutation_rate=0.01):
    try:
        n = validate_input(problem)
        print(f"Input is valid, detected dimension: {int(n)}")
    except ValueError as e:
        print(f"Input is not valid: {e}")
