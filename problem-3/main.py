import operator
import math
import random
import numpy as np
import deap
from deap import gp, base, creator, tools, algorithms


# Define the problem: Approximating the Fibonacci sequence
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# Define functions and terminals for the genetic program
pset = gp.PrimitiveSet("MAIN", arity=1)
pset.addPrimitive(operator.add, arity=2)
pset.addPrimitive(operator.sub, arity=2)
pset.addPrimitive(operator.mul, arity=2)
pset.addPrimitive(operator.neg, arity=1)
pset.addPrimitive(max, arity=2)
pset.addTerminal(1.0, "1")
pset.addEphemeralConstant("rand", lambda: random.randint(1, 10))


# Define the fitness function
def evalFibTree(individual):
    func = gp.compile(expr=individual, pset=pset)
    error = 0.0
    for i in range(10):
        error += abs(fib(i) - func(i))
    return (error,)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalFibTree)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def main():
    random.seed(42)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)

    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    pop, log = algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=0.7,
        mutpb=0.3,
        ngen=100,
        stats=mstats,
        halloffame=hof,
        verbose=True,
    )

    return pop, log, hof


if __name__ == "__main__":
    pop, log, hof = main()
    best_individual = hof[0]
    print("Best Individual:", best_individual)
    print("Best Fitness:", best_individual.fitness.values[0])
    func = gp.compile(expr=best_individual, pset=pset)
    for i in range(10):
        print(f"Fib({i}) = {fib(i)}, Approximation = {func(i)}")
