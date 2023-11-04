import numpy as np
import matplotlib.pyplot as plt
import math


def rastrigin(x, d):
    return 10 * d + sum([xi**2 - 10 * math.cos(2 * math.pi * xi) for xi in x])


class Particle:  # all the material that is relavant at the level of the individual particles
    def __init__(self, dim, minx, maxx):
        self.position = np.random.uniform(low=minx, high=maxx, size=dim)
        self.velocity = np.random.uniform(low=-0.1, high=0.1, size=dim)
        self.best_particle_pos = self.position
        self.dim = dim

        self.fitness = rastrigin(self.position, dim)
        self.best_particle_fitness = (
            self.fitness
        )  # we couldd start with very large number here,
        # but the actual value is better in case we are lucky

    def setPos(self, pos):
        self.position = pos
        self.fitness = rastrigin(self.position, self.dim)
        if (
            self.fitness < self.best_particle_fitness
        ):  # to update the personal best both
            # position (for velocity update) and
            # fitness (the new standard) are needed
            # global best is update on swarm leven
            self.best_particle_fitness = self.fitness
            self.best_particle_pos = pos

    def updateVel(self, inertia, a1, a2, best_self_pos, best_swarm_pos):
        # Here we use the canonical version
        # V <- inertia*V + a1r1 (peronal_best - current_pos) + a2r2 (global_best - current_pos)
        cur_vel = self.velocity
        r1 = np.random.uniform(low=0, high=1, size=self.dim)
        r2 = np.random.uniform(low=0, high=1, size=self.dim)
        a1r1 = np.multiply(a1, r1)
        a2r2 = np.multiply(a2, r2)
        best_self_dif = np.subtract(best_self_pos, self.position)
        best_swarm_dif = np.subtract(best_swarm_pos, self.position)
        # the next line is the main equation, namely the velocity update,
        # the velocities are added to the positions at swarm level
        new_vel = (
            inertia * cur_vel
            + np.multiply(a1r1, best_self_dif)
            + np.multiply(a2r2, best_swarm_dif)
        )
        self.velocity = new_vel
        return new_vel


class PSO:  # all the material that is relavant at swarm leveel
    def __init__(self, w, a1, a2, dim, population_size, time_steps, search_range):
        # Here we use values that are (somewhat) known to be good
        # There are no "best" parameters (No Free Lunch), so try using different ones
        # There are several papers online which discuss various different tunings of a1 and a2
        # for different types of problems
        self.w = w  # Inertia
        self.a1 = a1  # Attraction to personal best
        self.a2 = a2  # Attraction to global best
        self.dim = dim

        self.swarm = [
            Particle(dim, -search_range, search_range) for i in range(population_size)
        ]
        self.time_steps = time_steps
        print(f"Initialization - Dimensions: {self.dim}, Population Size: {population_size}")

        # Initialising global best, you can wait until the end of the first time step
        # but creating a random initial best and fitness which is very high will mean you
        # do not have to write an if statement for the one off case
        self.best_swarm_pos = np.random.uniform(low=-500, high=500, size=dim)
        self.best_swarm_fitness = 1e100

    def run(self) -> int:
        for t in range(self.time_steps):
            # if math.isclose(self.best_swarm_fitness, 0):
            #     return t
            if self.best_swarm_fitness == 0:
                return t
            for p in range(len(self.swarm)):
                particle = self.swarm[p]

                new_position = particle.position + particle.updateVel(
                    self.w,
                    self.a1,
                    self.a2,
                    particle.best_particle_pos,
                    self.best_swarm_pos,
                )

                if (
                    new_position @ new_position > 1.0e18
                ):  # The search will be terminated if the distance
                    # of any particle from center is too large
                    print(
                        "Time:",
                        t,
                        "Best Pos:",
                        self.best_swarm_pos,
                        "Best Fit:",
                        self.best_swarm_fitness,
                    )
                    raise SystemExit("Most likely divergent: Decrease parameter values")

                self.swarm[p].setPos(new_position)

                new_fitness = rastrigin(new_position, self.dim)

                if (
                    new_fitness < self.best_swarm_fitness
                ):  # to update the global best both
                    # position (for velocity update) and
                    # fitness (the new group norm) are needed
                    self.best_swarm_fitness = new_fitness
                    self.best_swarm_pos = new_position

            if (
                t % 100 == 0
            ):  # we print only two components even it search space is high-dimensional
                print(
                    "Time: %6d,  Best Fitness: %14.6f,  Best Pos: %9.4f,%9.4f"
                    % (
                        t,
                        self.best_swarm_fitness,
                        self.best_swarm_pos[0],
                        self.best_swarm_pos[1],
                    ),
                    end=" ",
                )
                if self.dim > 2:
                    print("...")
                else:
                    print("")
        return float("inf")
    

MAX_TIME_STEPS = 1000
DIMENSIONS = range(2, 6)
PARTICLE_COUNTS = range(1, 201, 2)
REPETITIONS = 5

results = np.zeros(len(PARTICLE_COUNTS))
for dimension in DIMENSIONS:
    for rep in range(REPETITIONS):
        time_steps_of_run = []
        for particle_count in PARTICLE_COUNTS:
            time_steps = PSO(
                dim=dimension,
                w=0.7,
                a1=2.02,
                a2=2.02,
                population_size=particle_count,
                time_steps=MAX_TIME_STEPS,
                search_range=5.12,
            ).run()
            time_steps_of_run.append(time_steps)
        results += np.array(time_steps_of_run)
    
    time_steps_avg = results / REPETITIONS

    plt.plot(PARTICLE_COUNTS, time_steps_avg)
    plt.grid()
    plt.xlabel("Population size")
    plt.ylabel("Time steps to optimum")
    plt.title(f"PSO - Rastrigin - Dimensions: {dimension}")
    filename = f"pso_rastrigin_dimension_{dimension}.pdf"
    plt.savefig(filename)
    plt.clf()
