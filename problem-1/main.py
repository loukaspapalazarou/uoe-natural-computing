import numpy as np
import matplotlib.pyplot as plt
import math
import threading


def rastrigin(x, d):
    return 10 * d + sum([xi**2 - 10 * math.cos(2 * math.pi * xi) for xi in x])


def rosenbrock(pos, dim):  # this serves as a goal function
    # Defined by f(x,y) = (a-x)^2 + b(y-x^2)^2
    # Using here: a = 1, b= 100, optimum 0 at (1,1)
    if dim == 2:
        return (1 - pos[0]) ** 2 + 100 * (pos[1] - pos[0] ** 2) ** 2
    elif dim == 1:
        return (1 - pos[0]) ** 2
    else:
        ros = 0
        for i in range(dim - 1):
            ros = ros + 100 * (pos[i + 1] - pos[i] ** 2) ** 2 * (1 - pos[i]) ** 2
        return ros


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
        self.tid = threading.get_native_id()

        self.swarm = [
            Particle(dim, -search_range, search_range) for i in range(population_size)
        ]
        self.time_steps = time_steps
        print(f"{self.tid}\t| Initialization - Dimensions: {self.dim}")

        # Initialising global best, you can wait until the end of the first time step
        # but creating a random initial best and fitness which is very high will mean you
        # do not have to write an if statement for the one off case
        self.best_swarm_pos = np.random.uniform(low=-500, high=500, size=dim)
        self.best_swarm_fitness = 1e100

    def run(self) -> int:
        for t in range(self.time_steps):
            if math.isclose(self.best_swarm_fitness, 0):
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
                        f"{self.tid}\t| Time:",
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
                    f"{self.tid}\t| Time: %6d,  Best Fitness: %14.6f,  Best Pos: %9.4f,%9.4f"
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


# time_steps_to_optimum = PSO(
#     dim=6,
#     w=0.7,
#     a1=2.02,
#     a2=2.02,
#     population_size=30,
#     time_steps=1000,
#     search_range=5.12,
# ).run()


def test_pso(particles, results, dimension):
    time_steps = PSO(
        dim=dimension,
        w=0.7,
        a1=2.02,
        a2=2.02,
        population_size=particles,
        time_steps=1000,
        search_range=5.12,
    ).run()

    results.append((particles, time_steps))


MAX_PARTICLES = 1001
PARTICLE_STEP = 5
DIMENSIONS = range(2, 8)

for dimension in DIMENSIONS:
    results = []
    threads = []

    for particles in range(5, MAX_PARTICLES, PARTICLE_STEP):
        thread = threading.Thread(target=test_pso, args=(particles, results, dimension))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    results = sorted(results, key=lambda x: x[0])
    x_values, y_values = zip(*results)
    # plt.bar([str(x) for x in x_values], y_values)
    plt.bar(x_values, y_values)
    plt.xlabel("Population size")
    plt.ylabel("Time steps to optimum")
    plt.title(f"PSO - Rastrigin - Dimensions: {dimension}")
    filename = f"pso_rastrigin_dimension_{dimension}.png"
    plt.savefig(filename)
    plt.clf()
