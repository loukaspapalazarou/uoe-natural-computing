from gp_outlines.gp_func import FUNCTIONS, TERMINALS, target_func
from gp import run

POP_SIZE        = 60   # population size
MIN_DEPTH       = 2    # minimal initial random tree depth
MAX_DEPTH       = 5    # maximal initial random tree depth
GENERATIONS     = 250  # maximal number of generations to run evolution
TOURNAMENT_SIZE = 5    # size of tournament for tournament selection
XO_RATE         = 0.8  # crossover rate 
PROB_MUTATION   = 0.2  # per-node mutation probability 

if __name__ == '__main__':
    run(
        FUNCTIONS,
        TERMINALS,
        target_func,
        POP_SIZE,
        MIN_DEPTH,
        MAX_DEPTH,
        GENERATIONS,
        TOURNAMENT_SIZE,
        XO_RATE,
        PROB_MUTATION
        )