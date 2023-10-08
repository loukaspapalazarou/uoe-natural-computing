import math
import random


def generate_problem(k: int, max_num: int = 100):
    """
    Generate a random problem string.

    Parameters:
    - k (int): The size of the square matrix.
    - max_num (int, optional): The maximum value for random integers in the matrix. Default is 100.

    Returns:
    - str: A problem string containing the matrix and target sums.
    """
    matrix = []
    for _ in range(k):
        row = [random.randint(1, max_num) for _ in range(k)]
        matrix.append(row)
    solution = []
    for _ in range(k):
        row = [
            random.choices([0, 1], weights=[1 / 3, 2 / 3])[0] for _ in range(k)
        ]  # Use random.choices with weights
        solution.append(row)

    row_sums = []
    col_sums = []
    for i in range(k):
        row_curr = 0
        col_curr = 0
        for j in range(k):
            row_curr += matrix[i][j] * solution[i][j]
            col_curr += matrix[j][i] * solution[j][i]
        row_sums.append(row_curr)
        col_sums.append(col_curr)

    s = ""
    matrix = [str(item) for row in matrix for item in row]
    row_sums = [str(num) for num in row_sums]
    col_sums = [str(num) for num in col_sums]
    s += ",".join(matrix) + ";"
    s += ",".join(row_sums) + ";"
    s += ",".join(col_sums)
    return s


def print_problem(problem: str):
    """
    Print a problem in a formatted way.

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    """
    args = problem.split(";")
    row_sums = args[1].split(",")
    col_sums = args[2].split(",")
    m = str_to_matrix(args[0])

    # Print the matrix with row sums
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(f"{m[i][j]:2}", end=" ")
        print("|", row_sums[i])

    # Print the separator line
    print("-" * (len(m[0]) * 3 + len(row_sums[0]) + 1))

    # Print column sums
    for j in range(len(col_sums)):
        print(f"{col_sums[j]:2}", end=" ")
    print()


def generate_random_solution(k: int) -> str:
    """
    Generate a random solution.

    Parameters:
    - k (int): The size of the square matrix.

    Returns:
    - str: A randomly generated solution string.
    """
    if k <= 0:
        raise ValueError("k must be greater than 0")
    binary_list = [str(random.randint(0, 1)) for _ in range(k * k)]
    binary_string = ",".join(binary_list)
    return binary_string


def validate_input(input: str) -> int:
    """
    Validate the input string and return the size of the square matrix.

    Parameters:
    - input (str): A formatted problem string containing the matrix and target sums.

    Returns:
    - int: The size of the square matrix.
    """
    if not input.__contains__(";"):
        raise ValueError("Input must contain semicolons.")
    args = input.split(";")
    if len(args) != 3:
        raise ValueError("Input must be divided into 3 sections separated by ';'.")
    input_matrix = args[0]
    input_matrix = input_matrix.split(",")
    k = math.sqrt(len(input_matrix))
    if not k.is_integer():
        raise ValueError("Input matrix must be square.")
    if len(args[1].split(",")) != k or len(args[2].split(",")) != k:
        raise ValueError("Amount of target sums is incorrect.")
    return int(k)


def str_to_matrix(input_str: str) -> list[list[int]]:
    """
    Convert a string representation of a matrix to a 2D list of integers.

    Parameters:
    - input_str (str): A string representation of a matrix.

    Returns:
    - list[list[int]]: A 2D list of integers representing the matrix.
    """
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
    """
    Calculate the fitness of a candidate solution using a binary fitness function.

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    - candidate (str): A candidate solution string.

    Returns:
    - int: The fitness score (1 if the solution is valid, 0 otherwise).
    """
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
    """
    Calculate the fitness of a candidate solution using a scalar fitness function.

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    - candidate (str): A candidate solution string.

    Returns:
    - float: The fitness score (a value between 0 and 1).
    """
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
    """
    Apply mutation to a candidate solution.

    Parameters:
    - candidate (str): A candidate solution string.
    - mutation_rate (float): The rate of mutation in candidate solutions.
    """
    candidate = candidate.split(",")
    for i in range(len(candidate)):
        if random.random() < mutation_rate:
            if candidate[i] == "0":
                candidate[i] = "1"
            else:
                candidate[i] = "0"


def crossover(parent1: str, parent2: str, crossover_point_rate: float) -> (str, str):
    """
    Perform crossover between two parent solutions to produce two offspring solutions.

    Parameters:
    - parent1 (str): The first parent solution string.
    - parent2 (str): The second parent solution string.
    - crossover_point_rate (float): The percentage of genes to be taken from parent 1 during crossover.

    Returns:
    - Tuple[str, str]: Two offspring solution strings.
    """
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
    verbose=True,
    output_graph_name="output.png",
    tid=None,
):
    """
    Sumplete game solver using a genetic algorithm

    Parameters:
    - problem (str): A formatted problem string containing the matrix and target sums.
    - generations (int, optional): The number of generations for the genetic algorithm. Default is 1000.
    - population_size (int, optional): The size of the population in each generation. Default is 100.
    - fitness (str, optional): The fitness function to use ("binary" or "scalar"). Default is "binary".
    - n_best (float, optional): The percentage of the selected top-performing candidates as parents. Default is 0.1.
    - breeding_rate (float, optional): The percentage of candidates that will be bred in each generation. Default is 0.5.
    - crossover_rate (float, optional): The percentage of the genes that will be taken from parent 1 when performing crossover. Default is 0.5.
    - mutation_rate (float, optional): The rate of mutation in candidate solutions. Default is 0.01.
    - verbose (bool, optional): Whether to print debug information. Default is True.
    - output_graph_name (str, optional): The name of the generated graph of the best fitness in terms of the generation. Default is "output.png".
    - tid (int, optional): If a thread id is given it will be displayed in the log messages. Default is None

    Returns:
    - The solution if it is found, otherwise -1
    """
    # k is the detected dimension of the matrix
    k = validate_input(problem)
    if verbose:
        print(f"Input is valid, detected size: {int(k)}")

    if not 0 <= n_best <= 1:
        raise ValueError("k_best should be between 0 and 1")
    if not 0 <= breeding_rate <= 1:
        raise ValueError("breeding should be between 0 and 1")
    if not 0 <= crossover_rate <= 1:
        raise ValueError("crossover should be between 0 and 1")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("mutation should be between 0 and 1")

    population = [generate_random_solution(k) for _ in range(population_size)]
    best_fitness = 0

    for generation in range(generations):
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
                if verbose:
                    print("\n")
                    print_problem(problem)
                    if tid:
                        print(f"TID:{tid} | ", end="")
                    print(f"Solution found in generation {generation}: {population[i]}")
                return population[i]
            population[i] = (population[i], fitness_val)
            best_fitness = max(best_fitness, fitness_val)

        if verbose and generation % 100 == 0:
            if tid:
                print(f"TID:{tid} | ", end="")
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
    if verbose:
        if tid:
            print(f"TID:{tid} | ", end="")
        print(f"No solution found.")
    return -1
