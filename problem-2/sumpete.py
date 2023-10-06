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
    problem,
    generations=1000,
    population_size=100,
    fitness="binary",
    k_best_rate=0.1,
    breeding_rate=0.5,
    crossover_point_rate=0.3,
    mutation_rate=0.01,
):
    """function(a, b) -> list""" """
    Solve a binary matrix optimization problem using a genetic algorithm.

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    - generations (int, optional): The number of generations for the genetic algorithm. Default is 1000.
    - population_size (int, optional): The size of the population in each generation. Default is 100.
    - fitness (str, optional): The fitness function to use ("binary" or "improved"). Default is "binary".
    - k_best_rate (float, optional): The rate of selecting the top-performing candidates as parents. Default is 0.1.
    - breeding_rate (float, optional): The rate of candidates that will be bred in each generation. Default is 0.5.
    - crossover_point_rate (float, optional): The rate of crossover points when performing crossover. Default is 0.3.
    - mutation_rate (float, optional): The rate of mutation in candidate solutions. Default is 0.01.

    Returns:
    ?
    """
    try:
        k = validate_input(problem)
        print(f"Input is valid, detected size: {int(k)}")
    except ValueError as e:
        print(f"Input is not valid: {e}")

    # print(fitness_binary("6,3,1,7,9,3,9,5,8;1,12,17;9,9,12", "0,0,1,0,1,1,1,0,1"))
    # print(generate_random_solution(10))

    population = [generate_random_solution(k) for _ in range(population_size)]

    for generation in range(generations):
        # Calculate fitness of each candidate solution
        # Place the result in a list of tuples like so: [(candidate_1, fitness_1), ..., (candidate_N, fitness_N)]
        # This is done to keep a reference to the original population matrix after sorting by the fitness score
        if fitness == "binary":
            fitness_scores = [
                (i, fitness_binary(problem, candidate))
                for i, candidate in enumerate(population)
            ]
        elif fitness == "improved":
            fitness_scores = [
                (i, fitness_improved(problem, candidate))
                for i, candidate in enumerate(population)
            ]
        else:
            raise ValueError(f"The '{fitness}' fitness function does not exist.")

        fitness_scores = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
        print(fitness_scores)
        print()
        # print(fitness_binary(problem, "1,0,0,0"))


# solver("6,3,1,7,9,3,9,5,8;1,12,17;9,9,12")
solver("1,0,0,0;1,0;1,0")
