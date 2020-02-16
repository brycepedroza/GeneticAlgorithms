from genetic_alogithm.genetic_algo import *
from genetic_alogithm import logger
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import argparse

# Change these as you wish :)
POPULATION = 100
CROSSOVER_RATE = 0.4
MUTATION_RATE = 0.8
NUM_GENERATIONS = 100


def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hide',
                        default=False,
                        action='store_true',
                        help='If true, hides graph output')
    parser.add_argument('-normalize',
                        default=False,
                        action='store_true',
                        help='If true, normalize fitness function')
    parser.add_argument('-population',
                        type=int,
                        default=POPULATION,
                        help='Population Size')
    parser.add_argument('-generations',
                        type=int,
                        default=NUM_GENERATIONS,
                        help='Number of Generations')
    parser.add_argument('-crossover',
                        type=float,
                        default=CROSSOVER_RATE,
                        help='Crossover Rate')
    parser.add_argument('-mutation',
                        type=float,
                        default=MUTATION_RATE,
                        help='Mutation Rate')
    return parser.parse_args()


if __name__ == "__main__":

    # Init Logging and args
    args = parse_my_args()
    log_file = "./logs/gen_alg.log"
    logger.create_rotating_log(log_file)
    log = logger.logger
    log.info("----- Starting Genetic Algorithm -----")

    # Perform GA
    g = GeneticAlgorithm(args.population, args.crossover, args.mutation, args.normalize)
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
    fitness_no_reset = []

    # We will only consider the fittest individual in the calculation
    for x in range(NUM_GENERATIONS):
        x_no_reset.append(g.best_individuals[0].x.curr)
        y_no_reset.append(g.best_individuals[0].y.curr)
        z_no_reset.append(g.best_individuals[0].z.curr)
        fitness_no_reset.append(g.best_individuals[0].fitness)
        g.best_individuals[0].perform_calculations()

    # reset current spending so only 12 params remain.
    g.best_individuals[0].reset_current_spending()
    x_reset = []
    y_reset = []
    z_reset = []
    fitness_reset = []
    for x in range(NUM_GENERATIONS):
        x_reset.append(g.best_individuals[0].x.curr)
        y_reset.append(g.best_individuals[0].y.curr)
        z_reset.append(g.best_individuals[0].z.curr)
        fitness_reset.append(g.best_individuals[0].fitness)
        g.best_individuals[0].perform_calculations()

    # Let's calculate how far off the lines are from eventually coming to a steady state.
    x_nrmsd = np.sqrt(
        np.mean((np.array(x_reset) - np.array(x_no_reset))) ** 2) \
        / (np.max(x_no_reset))
    y_nrmsd = np.sqrt(
        np.mean((np.array(y_reset) - np.array(y_no_reset))) ** 2) \
        / (np.max(y_no_reset))
    z_nrmsd = np.sqrt(
        np.mean((np.array(z_reset) - np.array(z_no_reset))) ** 2) \
        / (np.max(z_no_reset))
    fitness_nrmsd = np.sqrt(
        np.mean((np.array(fitness_reset) - np.array(fitness_no_reset))) ** 2) \
        / (np.max(fitness_reset))

    # The larger the ssd, the worse the result
    country_nrmsd = (x_nrmsd + y_nrmsd + z_nrmsd)/3
    # Final Results
    log.info("Population, Crossover, Mutation, Generations, "
             "Average Fitness, Best Fitness, Country rmsd, Fitness rmsd, Normalized")
    log.info(f"{args.population}\t{args.crossover}\t{args.mutation}\t"
             f"{args.generations}\t{average_fitness}\t{best_fitness}\t"
             f"{country_nrmsd}\t{fitness_nrmsd}\t{args.normalize}")
    print(f"{args.population},{args.crossover},{args.mutation},"
          f"{args.generations},{average_fitness},{best_fitness},"
          f"{country_nrmsd},{fitness_nrmsd},{args.normalize}")

    # Display results
    if not args.hide:
        df = pd.DataFrame({'domain': range(NUM_GENERATIONS),
                           'X without Reset': x_no_reset,
                           'Y without Reset': y_no_reset,
                           'Z without Reset': z_no_reset,
                           'X with Reset': x_reset,
                           'Y with Reset': y_reset,
                           'Z with Reset': z_reset})

        # multiple line plot
        fig, axs = plt.subplots(2, figsize=(12, 8))
        fig.suptitle(f"Population: {args.population}\nCrossover: {args.crossover}\nMutation: {args.mutation}")
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

