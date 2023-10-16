import random
import operator

# Define the set of possible operators and operands
operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}
operands = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Define the target value
target = 24

# Define the population size and number of generations
population_size = 100
generations = 100

# Define the mutation rate
mutation_rate = 0.2


# Define the fitness function
def evaluate_expression(expression):
    try:
        result = eval(expression)
        return 1 / (abs(target - result) + 1)
    except ZeroDivisionError:
        return 0  # Avoid division by zero


# Generate random individuals (expressions)
def generate_individual(length):
    individual = []
    for _ in range(length):
        if random.random() < 0.5:
            individual.append(random.choice(list(operators.keys())))
        else:
            individual.append(str(random.choice(operands)))
    return "".join(individual)


# Create an initial population
population = [generate_individual(5) for _ in range(population_size)]

# Evolution loop
for generation in range(generations):
    # Evaluate the fitness of each individual
    fitness_scores = [evaluate_expression(individual) for individual in population]

    # Select parents for reproduction
    parents = random.choices(population, weights=fitness_scores, k=population_size)

    # Create a new generation through crossover and mutation
    new_population = []
    for _ in range(population_size):
        parent1, parent2 = random.choices(parents, k=2)
        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(child) - 1)
            child = (
                child[:mutation_point]
                + generate_individual(1)
                + child[mutation_point + 1 :]
            )
        new_population.append(child)

    # Replace the old population with the new generation
    population = new_population

    # Check for a perfect solution
    best_fit = max(fitness_scores)
    if best_fit == 1.0:
        print(
            f"Generation {generation}: Found a perfect solution: {population[fitness_scores.index(best_fit)]}"
        )
        break

# Find the best solution in the final population
best_solution = population[fitness_scores.index(max(fitness_scores))]
print(f"Best solution: {best_solution}")
