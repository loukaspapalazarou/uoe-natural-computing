import itertools
import json
import logging
from sumplete import solver, generate_problem

# Configure the logging module to write logs to a file named "out.log"
logging.basicConfig(filename='out.log', level=logging.INFO)

PROBLEM_SIZE = 5
NUM_PROBLEMS = 3

# Define the parameter grid for the grid search
population_size_list = [10, 20, 50, 100, 150, 200]
fitness_list = ["binary", "scalar"]
n_best_list = [0.01, 0.05, 0.1, 0.2, 0.4]
breeding_rate_list = [0.1, 0.2, 0.3, 0.4]
crossover_rate_list = [0.1, 0.3, 0.5]
mutation_rate_list = [0.01, 0.05, 0.1]
problems = [generate_problem(PROBLEM_SIZE)] * NUM_PROBLEMS

best_solution = None
best_params = {}
best_generation = float('inf')
generations = 10_000
for (
    population_size,
    fitness,
    n_best,
    breeding_rate,
    crossover_rate,
    mutation_rate,
) in itertools.product(
    population_size_list,
    fitness_list,
    n_best_list,
    breeding_rate_list,
    crossover_rate_list,
    mutation_rate_list,
):
    # Use the logging module to log information
    logging.info(f"Testing parameters: population_size={population_size}, fitness={fitness}, n_best={n_best}, breeding_rate={breeding_rate}, crossover_rate={crossover_rate}, mutation_rate={mutation_rate}")
    sols = []
    for problem in problems:
        sol = solver(
            problem=problem,
            generations=generations,
            population_size=population_size,
            fitness=fitness,
            n_best=n_best,
            breeding_rate=breeding_rate,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            verbose=False,
            output_graph_name=None
        )
        sols.append(sol[1])
    
    sol = int(sum(sols) / len(sols))

    if sol < best_generation:
        best_params = {
            "generations": generations,
            "population_size": population_size,
            "fitness": fitness,
            "n_best": n_best,
            "breeding_rate": breeding_rate,
            "crossover_rate": crossover_rate,
            "mutation_rate": mutation_rate,
        }
        best_generation = sol

with open("best_params.txt", "w") as f:
    json.dump(best_params, f)

print()
print("Best Parameters:", best_params)
