import random
import string

# Target string to evolve towards
target = "Hello, Genetic Algorithm!"

# Genetic algorithm parameters
population_size = 100
mutation_rate = 0.01


def generate_random_string(length):
    return "".join(random.choice(string.printable) for _ in range(length))


def calculate_fitness(candidate):
    return sum(c1 == c2 for c1, c2 in zip(candidate, target))


def mutate(candidate):
    return "".join(
        c if random.random() > mutation_rate else random.choice(string.printable)
        for c in candidate
    )


def select_parents(population):
    return random.choices(
        population,
        weights=[calculate_fitness(candidate) for candidate in population],
        k=2,
    )


def crossover(parent1, parent2):
    pivot = random.randint(1, len(parent1) - 1)
    child1 = parent1[:pivot] + parent2[pivot:]
    child2 = parent2[:pivot] + parent1[pivot:]
    return child1, child2


# Initialize a population of random strings
population = [generate_random_string(len(target)) for _ in range(population_size)]

generation = 0
while True:
    generation += 1

    # Calculate fitness for each candidate
    fitness_scores = [calculate_fitness(candidate) for candidate in population]

    # Check for a perfect match
    if max(fitness_scores) == len(target):
        print(f"Generation {generation}: Found a perfect match!")
        break

    # Select two parents
    parent1, parent2 = select_parents(population)

    # Create two children through crossover
    child1, child2 = crossover(parent1, parent2)

    # Mutate the children
    child1 = mutate(child1)
    child2 = mutate(child2)

    # Replace two weakest candidates with the children
    weakest_indices = sorted(
        range(len(fitness_scores)), key=lambda i: fitness_scores[i]
    )[:2]
    population[weakest_indices[0]] = child1
    population[weakest_indices[1]] = child2

    if generation % 10 == 0:
        best_fitness = max(fitness_scores)
        best_candidate = population[fitness_scores.index(best_fitness)]
        print(f"Generation {generation}: {best_candidate} (Fitness: {best_fitness})")
