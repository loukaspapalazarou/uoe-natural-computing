from sumplete import solver, generate_problem
import matplotlib.pyplot as plt

average_gens = []

PROB_DIMS = range(3,7)
REPS = range(5)

max_generations = 5000
fitness = "scalar"

for prob_dim in PROB_DIMS:
    gens = []
    for _ in REPS:
        gens.append(solver(
                problem=generate_problem(prob_dim),
                generations=max_generations,
                population_size=200,
                fitness=fitness,
                n_best=0.1,
                breeding_rate=0.3, 
                crossover_rate=0.4,
                mutation_rate=0.05,
                output_graph_name="output.pdf",
            )[1])
    average_gens.append(sum(gens)/len(gens))

# Create a list of dimension labels
dimension_labels = [str(dim) for dim in PROB_DIMS]
plt.bar(dimension_labels, average_gens)
plt.xlabel('Dimensions')
plt.ylabel('Average Generations to Solution')
plt.tight_layout()
# Add values or "no solution found" on top of the bars
for i, (dim, avg_gen) in enumerate(zip(PROB_DIMS, average_gens)):
    label = f'{avg_gen:.2f}' if avg_gen < max_generations else 'No solution found'
    plt.text(i, avg_gen, label, ha='center', va='bottom')
plt.savefig(f"{fitness}_fitness.pdf")