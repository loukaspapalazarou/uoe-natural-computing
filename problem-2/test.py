from sumplete import solver, generate_problem
import threading


def solve_problem(
    problem,
    generations,
    population_size,
    fitness,
    n_best,
    breeding_rate,
    crossover_rate,
    mutation_rate,
    verbose,
    output_graph_name,
    tid,
):
    solver(
        problem=problem,
        generations=generations,
        population_size=population_size,
        fitness=fitness,
        n_best=n_best,
        breeding_rate=breeding_rate,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        verbose=verbose,
        output_graph_name=output_graph_name,
        tid=tid,
    )


if __name__ == "__main__":
    problem = generate_problem(4)

    # Define different sets of parameters
    parameter_sets = [
        {
            "generations": 10000,
            "population_size": 100,
            "fitness": "scalar",
            "n_best": 0.07,
            "breeding_rate": 0.01,
            "crossover_rate": 0.3,
            "mutation_rate": 0.05,
            "verbose": True,
            "output_graph_name": "output1.png",
            "tid": 1,
        },
        {
            "generations": 5000,
            "population_size": 50,
            "fitness": "scalar",
            "n_best": 0.1,
            "breeding_rate": 0.02,
            "crossover_rate": 0.4,
            "mutation_rate": 0.1,
            "verbose": True,
            "output_graph_name": "output2.png",
            "tid": 2,
        },
    ]

    # Create a thread for each parameter set
    threads = [
        threading.Thread(target=solve_problem, args=(problem,), kwargs=params)
        for params in parameter_sets
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
