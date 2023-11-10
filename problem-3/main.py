from gp_outlines.gp_hexagonal import FUNCTIONS, TERMINALS, DOMAIN, target_func
from gp import run

POP_SIZE = 60  # population size
MIN_DEPTH = 2  # minimal initial random tree depth
MAX_DEPTH = 5  # maximal initial random tree depth
GENERATIONS = 200  # maximal number of generations to run evolution
TOURNAMENT_SIZE = 5  # size of tournament for tournament selection
XO_RATE = 0.8  # crossover rate
PROB_MUTATION = 0.2  # per-node mutation probability

if __name__ == "__main__":
    run(
        functions=FUNCTIONS,
        terminals=TERMINALS,
        target_func=target_func,
        pop_size=POP_SIZE,
        min_depth=MIN_DEPTH,
        max_depth=MAX_DEPTH,
        generations=GENERATIONS,
        tournament_size=TOURNAMENT_SIZE,
        xo_rate=XO_RATE,
        prob_mutation=PROB_MUTATION,
        domain=DOMAIN,
        outputfile="test.pdf",
    )
