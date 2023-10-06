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
import time


def load_problem(filename: str):
    pass


def generate_problem(k: int):
    pass


def print_problem(problem: str):
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
    flat_matrix = input_str.split(",")
    n = int(len(flat_matrix) ** 0.5)
    if n * n != len(flat_matrix):
        raise ValueError("Input list length is not a perfect square.")
    matrix = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = int(flat_matrix[i * n + j])
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
        if row_curr != row_sums[i] or col_curr != col_sums[i]:
            return 0
    return 1


def fitness_scalar(problem: str, candidate: str) -> float:
    # assume fitness matrix format is correct
    args = problem.split(";")
    problem = str_to_matrix(args[0])
    candidate = str_to_matrix(candidate)
    row_sums, col_sums = args[1].split(","), args[2].split(",")
    row_sums = [int(r) for r in row_sums]
    col_sums = [int(c) for c in col_sums]
    k = len(problem)
    distance = 0
    max_distance = 0
    for i in range(k):
        row_curr = 0
        col_curr = 0
        for j in range(k):
            row_curr += problem[i][j] * candidate[i][j]
            col_curr += problem[j][i] * candidate[j][i]
        distance += abs(row_curr - row_sums[i])
        distance += abs(col_curr - col_sums[i])
        max_distance += row_sums[i] + col_sums[i]
    return (max_distance - distance) / (max_distance)


def mutate(candidate: str, mutation_rate: float):
    candidate = candidate.split(",")
    for i in range(len(candidate)):
        if random.random() < mutation_rate:
            if candidate[i] == "0":
                candidate[i] = "1"
            else:
                candidate[i] = "0"


def crossover(parent1: str, parent2: str, crossover_point_rate: float) -> (str, str):
    parent1 = parent1.split(",")
    parent2 = parent2.split(",")
    if len(parent1) != len(parent1):
        raise ValueError("Parent sizes should be the same.")
    pivot = int(crossover_point_rate * len(parent1))
    child1 = parent1[:pivot] + parent2[pivot:]
    child2 = parent2[:pivot] + parent1[pivot:]
    return child1, child2


def solver(
    problem,
    generations=1000,
    population_size=10,
    fitness="binary",
    n_best=0.4,
    breeding_rate=0.1,
    crossover_rate=0.1,
    mutation_rate=0.01,
):
    """function(a, b) -> list""" """
    Solve a binary matrix optimization problem using a genetic algorithm.

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    - generations (int, optional): The number of generations for the genetic algorithm. Default is 1000.
    - population_size (int, optional): The size of the population in each generation. Default is 100.
    - fitness (str, optional): The fitness function to use ("binary" or "scalar"). Default is "binary".
    - n_best (float, optional): The percentage of the selected top-performing candidates as parents. Default is 0.1.
    - breeding_rate (float, optional): The percentage of candidates that will be bred in each generation. Default is 0.5.
    - crossover_rate (float, optional): The percentage of the genes that will be taken from parent 1 when performing crossover. Default is 0.5.
    - mutation_rate (float, optional): The rate of mutation in candidate solutions. Default is 0.01.

    Returns:
    ?
    """
    # k is the detected dimension of the matrix
    k = validate_input(problem)
    print(f"Input is valid, detected size: {int(k)}")

    if not 0 <= n_best <= population_size:
        raise ValueError("k_best should be between 0 and K")
    if not 0 <= breeding_rate <= 1:
        raise ValueError("breeding should be between 0 and 1")
    if not 0 <= crossover_rate <= 1:
        raise ValueError("crossover should be between 0 and 1")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("mutation should be between 0 and 1")

    population = [generate_random_solution(k) for _ in range(population_size)]
    best_fitness = 0

    for generation in range(generations):
        # time.sleep(0.1)
        # Calculate fitness of each candidate solution
        # For each candidate solution in the population,
        # replace the candidate string with a tuple like this: (candidate_str, candidate_fitness)
        if fitness == "binary":
            fitness_fn = lambda ind: fitness_binary(problem, ind)
        elif fitness == "scalar":
            fitness_fn = lambda ind: fitness_scalar(problem, ind)
        else:
            raise ValueError(f"The '{fitness}' fitness function does not exist.")

        for i in range(population_size):
            fitness_val = fitness_fn(population[i])
            if fitness_val == 1:
                print(f"Solution found: {population[i]}")
                return population[i]
            population[i] = (population[i], fitness_val)
            best_fitness = max(best_fitness, fitness_val)

        print(f"Generation {generation}. Best fitness: {best_fitness}")

        # We now can sort the population based on fitness
        population.sort(key=lambda x: x[1], reverse=True)
        # Now go through the evolution steps
        new_population = []
        # 1: Pick the n best solutions to move to the next population unchanged
        for i in range(int(n_best * population_size)):
            new_population.append(population[i][0])
        # 2: Find the parents for the next population
        #    Breed them and move their offspring to the new population
        num_of_candidates_to_reproduce = int(breeding_rate * population_size)
        for i in range(num_of_candidates_to_reproduce):
            parent1 = random.choice(population)[0]
            parent2 = random.choice(population)[0]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            new_population.append(",".join(child1))
            new_population.append(",".join(child2))
        # 3: Mutate
        for c in new_population:
            mutate(c, mutation_rate)
        # 4: If not enough solutions, fill population with new random solutions
        while len(new_population) < population_size:
            new_population.append(generate_random_solution(k))
        population = new_population[:population_size]


problem = "1,0,0,0;1,0;1,0"
problem = "1,7,1,8;8,0;1,7"
problem = "6,3,1,7,9,3,9,5,8;1,12,17;9,9,12"
solver(problem, fitness="scalar")
