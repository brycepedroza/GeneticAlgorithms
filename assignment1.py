from genetic_alogithm.genetic_algo import *
from genetic_alogithm import logger
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Change these as you wish :)
POPULATION = 100
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.9
NUM_GENERATIONS = 100


if __name__ == "__main__":

    # Init Logging
    log_file = "./logs/gen_alg.log"
    logger.create_rotating_log(log_file)
    log = logger.logger
    log.info("----- Starting Genetic Algorithm -----")

    # Perform GA
    g = GeneticAlgorithm(POPULATION, CROSSOVER_RATE, MUTATION_RATE)
    for x in range(NUM_GENERATIONS):
        g.iterate_population()

    # Log average fitness across all generations
    log.info("Average fitness across all generations")
    log.info(g.average_fitness)

    # Ok now so we have the best people and their params. Lets log them
    log.info("Best individuals across all generations")
    for x in g.best_individuals:
        log.info(x.get_county_props())

    best_fitness = g.best_individuals[0].fitness
    average_fitness = np.average(g.average_fitness)

    # Lets study how these params work over time.
    x_no_reset = []
    y_no_reset = []
    z_no_reset = []
    # We will only consider the fittest individual in the calculation
    for x in range(NUM_GENERATIONS):
        x_no_reset.append(g.best_individuals[0].x.curr)
        y_no_reset.append(g.best_individuals[0].y.curr)
        z_no_reset.append(g.best_individuals[0].z.curr)
        g.best_individuals[0].perform_calculations()
    # reset current spending so only 12 params remain.
    g.best_individuals[0].reset_current_spending()
    x_reset = []
    y_reset = []
    z_reset = []
    for x in range(NUM_GENERATIONS):
        x_reset.append(g.best_individuals[0].x.curr)
        y_reset.append(g.best_individuals[0].y.curr)
        z_reset.append(g.best_individuals[0].z.curr)
        g.best_individuals[0].perform_calculations()

    df = pd.DataFrame({'domain': range(NUM_GENERATIONS),
                       'X without Reset': x_no_reset,
                       'Y without Reset': y_no_reset,
                       'Z without Reset': z_no_reset,
                       'X with Reset': x_reset,
                       'Y with Reset': y_reset,
                       'Z with Reset': z_reset})

    # Let's calculate how far off the lines are from eventually coming to a steady state.
    # x_ssd = np.sum(np.square(np.array(x_no_reset) - np.array(x_reset)))
    x_nrmsd = np.sqrt(
        np.mean((np.array(x_reset) - np.array(x_no_reset))) ** 2) \
        / (np.max(x_no_reset))
    # y_ssd = np.sum(np.square(np.array(y_no_reset) - np.array(y_reset)))
    y_nrmsd = np.sqrt(
        np.mean((np.array(y_reset) - np.array(y_no_reset))) ** 2) \
        / (np.max(y_no_reset))
    # z_ssd = np.sum(np.square(np.array(z_no_reset) - np.array(z_reset)))
    z_nrmsd = np.sqrt(
        np.mean((np.array(z_reset) - np.array(z_no_reset))) ** 2) \
        / (np.max(z_no_reset))

    # The larger the ssd, the worse the result
    nrmsd = (x_nrmsd + y_nrmsd + z_nrmsd)/3
    # Final Results
    log.info("Population, Crossover, Mutation, Generations, "
             "Average Fitness, Best Fitness, Average ssd, xssd, yssd, zssd")
    log.info(f"{POPULATION}\t{CROSSOVER_RATE}\t{MUTATION_RATE}\t"
             f"{NUM_GENERATIONS}\t{average_fitness}\t{best_fitness}\t{nrmsd}\t{x_nrmsd}\t{y_nrmsd}\t{z_nrmsd}")
    print(f"{POPULATION},{CROSSOVER_RATE},{MUTATION_RATE},"
          f"{NUM_GENERATIONS},{average_fitness},{best_fitness},{nrmsd},{x_nrmsd},{y_nrmsd},{z_nrmsd}")

    # multiple line plot
    fig, axs = plt.subplots(2, figsize=(12, 8))
    fig.suptitle(f"Population: {POPULATION}\nCrossover: {CROSSOVER_RATE}\nMutation: {MUTATION_RATE}")
    axs[1].set_title('Best Individual')
    axs[1].plot('domain', 'X without Reset', data=df, marker='', color='blue', linewidth=2, linestyle='dotted')
    axs[1].plot('domain', 'Y without Reset', data=df, marker='', color='red', linewidth=2, linestyle='dotted')
    axs[1].plot('domain', 'Z without Reset', data=df, marker='', color='green', linewidth=2, linestyle='dotted')

    axs[1].plot('domain', 'X with Reset', data=df, marker='', color='blue', linewidth=2)
    axs[1].plot('domain', 'Y with Reset', data=df, marker='', color='red', linewidth=2)
    axs[1].plot('domain', 'Z with Reset', data=df, marker='', color='green', linewidth=2)

    axs[1].legend()
    axs[0].set_title('Average Fitness')
    axs[0].plot(range(NUM_GENERATIONS), g.average_fitness, marker='', color='black', linewidth=2)
    plt.show(block=True)

