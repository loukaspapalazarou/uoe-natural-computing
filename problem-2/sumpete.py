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


### TERMINOLOGY ###
#   problem: the entire matrix along with the target sums. For example: 6,3,1,7,9,3,9,5,8;1,12,17;9,9,12
#   matrix: either the problem matrix or solution matrix. For example: 6,3,1,7,9,3,9,5,8 or 0,0,1,0,1,1,1,0,1
#   solution: just the solution matrix. For example 0,0,1,0,1,1,1,0,1
### TERMINOLOGY ###
import math
import random


def load_problem(filename: str):
    pass


def generate_problem(k: int):
    pass


def generate_random_solution(k: int) -> str:
    if k <= 0:
        raise ValueError("k must be greater than 0")
    binary_list = [str(random.randint(0, 1)) for _ in range(k * k)]
    binary_string = ",".join(binary_list)
    return binary_string


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
    return int(k)


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


def fitness_binary(problem: str, candidate: str) -> int:
    # assume fitness matrix format is correct
    args = problem.split(";")
    problem = str_to_matrix(args[0])
    candidate = str_to_matrix(candidate)
    row_sums, col_sums = args[1].split(","), args[2].split(",")
    row_sums = [int(r) for r in row_sums]
    col_sums = [int(c) for c in col_sums]
    k = len(problem)
    for i in range(k):
        row_curr = 0
        col_curr = 0
        for j in range(k):
            row_curr += problem[i][j] * candidate[i][j]
            col_curr += problem[j][i] * candidate[j][i]
        if row_curr != row_sums[i] or col_curr != col_sums[j]:
            return 0
    return 1


def fitness_improved():
    pass


def mutate(candidate):
    pass


def select_parents(population):
    pass


def crossover(parent1, parent2):
    pass


def solver(
    problem, generations=1000, population_size=100, mutation_rate=0.01, fitness="binary"
):
    try:
        k = validate_input(problem)
        print(f"Input is valid, detected size: {int(k)}")
    except ValueError as e:
        print(f"Input is not valid: {e}")

    # print(fitness_binary("6,3,1,7,9,3,9,5,8;1,12,17;9,9,12", "0,0,1,0,1,1,1,0,1"))
    # print(generate_random_solution(10))

    population = [generate_random_solution(k) for _ in range(population_size)]
    for i, p in enumerate(population):
        f = fitness_binary(problem, p)
        print(i, p, f)

    # print(fitness_binary(problem, "0,0,0,0"))


# solver("6,3,1,7,9,3,9,5,8;1,12,17;9,9,12")
solver("0,0,0,0;0,0;0,0")
