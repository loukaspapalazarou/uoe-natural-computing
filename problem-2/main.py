from sumplete import solver, generate_problem

if __name__ == "__main__":
    solver(
        problem=generate_problem(5),
        generations=10000,
        population_size=100,
        fitness="scalar",
        n_best=0.1,
        breeding_rate=0.3,
        crossover_rate=0.5,
        mutation_rate=0.05,
        verbose=True,
        output_graph_name="output.pdf",
    )
