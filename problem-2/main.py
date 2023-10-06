from sumplete import solver, generate_problem

if __name__ == "__main__":
    solver(
        generate_problem(4),
        generations=10000,
        population_size=500,
        fitness="scalar",
        n_best=0.05,
        breeding_rate=0.01,
        crossover_rate=0.01,
        mutation_rate=0.01,
        verbose=True,
    )
