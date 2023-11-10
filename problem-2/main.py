from sumplete import solver, generate_problem

if __name__ == "__main__":
    sol = solver(
        problem=generate_problem(3),
        generations=1_000,
        population_size=300,
        fitness="scalar",
        n_best=0.1,
        breeding_rate=0.3, 
        crossover_rate=0.5,
        mutation_rate=0.05,
        output_graph_name="output.pdf",
    )
# INFO:root:Best so far: {'generations': 5000, 'population_size': 200, 'fitness': 'scalar', 'n_best': 0.1, 'breeding_rate': 0.3, 'crossover_rate': 0.5, 'mutation_rate': 0.1}
