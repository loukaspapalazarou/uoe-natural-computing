import random
import numpy as np


# Define the target sequence (Fibonacci numbers)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Define the fitness function to measure the similarity of a generated sequence to the target
def fitness(program):
    error = 0
    for n in range(20):  # Compare the first 20 Fibonacci numbers
        if program(n) != fibonacci(n):
            error += 1
    return -error  # We want to minimize the error


# Define genetic programming operations (e.g., addition, subtraction, conditionals, etc.)
def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b


def if_then_else(condition, if_branch, else_branch):
    if condition:
        return if_branch
    else:
        return else_branch


# Initialize a random program as the starting point
def random_program(max_depth=5):
    if max_depth == 0 or random.random() < 0.5:
        return random.randint(0, 1)  # Randomly return 0 or 1
    else:
        operation = random.choice([addition, subtraction, if_then_else])
        if operation == if_then_else:
            condition = random_program(max_depth - 1)
            if_branch = random_program(max_depth - 1)
            else_branch = random_program(max_depth - 1)
            return lambda n: operation(condition(n), if_branch(n), else_branch(n))
        else:
            left_operand = random_program(max_depth - 1)
            right_operand = random_program(max_depth - 1)
            return lambda n: operation(left_operand(n), right_operand(n))


# Genetic programming loop
population_size = 100
generations = 100

best_program = None
best_fitness = float("-inf")

for _ in range(generations):
    population = [random_program() for _ in range(population_size)]
    fitness_scores = [fitness(program) for program in population]
    best_index = np.argmax(fitness_scores)
    if fitness_scores[best_index] > best_fitness:
        best_fitness = fitness_scores[best_index]
        best_program = population[best_index]

# Display the best program and its fitness score
print("Best Program:", best_program)
print("Fitness Score:", best_fitness)

# Test the best program with Fibonacci numbers up to 20
for n in range(20):
    print(f"F({n}) =", best_program(n))
