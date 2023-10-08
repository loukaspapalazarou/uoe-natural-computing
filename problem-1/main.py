import random
import math
from deap import base, creator, tools, algorithms


# Define the Rastrigin function
def rastrigin(x):
    return 10 * len(x) + sum(xi**2 - 10 * math.cos(2 * math.pi * xi) for xi in x)


# Define problem dimensions (d = 1, 2, 3, ...)
problem_dimensions = [1, 2, 3, 4, 5]

# Store optimal population sizes for each problem dimension
optimal_population_sizes = {}

for d in problem_dimensions:
    # Define optimization parameters
    N = 30  # Initial population size
    total_evaluations = 5000  # Total evaluations of the cost function
    generations = total_evaluations // N  # Calculate number of generations

    # Create a fitness function for minimizing the Rastrigin function
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, -5.12, 5.12)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=d
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        return (rastrigin(individual),)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    toolbox.register("select", tools.selBest)

    # Initialize the population
    population = toolbox.population(n=N)

    # Create statistics to track the best fitness values
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", min)

    # Create a logbook to record statistics
    logbook = tools.Logbook()
    logbook.header = ["gen", "evals", "min"]

    # Run the PSO algorithm
    algorithms.eaMuPlusLambda(
        population,
        toolbox,
        mu=N,
        lambda_=N,
        cxpb=0.7,
        mutpb=0.2,
        ngen=generations,
        stats=stats,
        halloffame=None,
    )

    # Store the optimal population size for this problem dimension
    optimal_population_sizes[d] = N

# Print the optimal population sizes for each problem dimension
for d, optimal_size in optimal_population_sizes.items():
    print(f"Optimal Population Size for d={d}: {optimal_size}")
