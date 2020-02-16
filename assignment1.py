from code.genetic_algo import *
from code import logger
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == "__main__":

    log_file = "./logs/gen_alg.log"
    logger.create_rotating_log(log_file)
    log = logger.logger
    log.info("----- Starting Genetic Algorithm -----")

    g = GeneticAlgorithm(100, 0.3)
    num_generations = 50
    for x in range(num_generations):
        g.iterate_population()

    # Log average fitness across all generations
    log.info("Average fitness across all generations")
    log.info(g.average_fitness)

    # Ok now so we have the best people and their params. Lets log them
    log.info("Best individuals across all generations")
    for x in g.best_individuals:
        log.info(x.get_county_props())

    # Lets study how these params work over time.
    num_iterations = 100
    x_res = []
    y_res = []
    z_res = []
    # reset current spending so only 12 params remain
    g.best_individuals[0].reset_current_spending()
    for x in range(num_iterations):
        g.best_individuals[0].perform_calculations()
        x_res.append(g.best_individuals[0].x.curr)
        y_res.append(g.best_individuals[0].y.curr)
        z_res.append(g.best_individuals[0].z.curr)

    df = pd.DataFrame({'domain': range(num_iterations),
                       'x_res': x_res,
                       'y_res': y_res,
                       'z_res': z_res})

    # multiple line plot
    plt.plot('domain', 'x_res', data=df, marker='', color='blue', linewidth=2)
    plt.plot('domain', 'y_res', data=df, marker='', color='red', linewidth=2)
    plt.plot('domain', 'z_res', data=df, marker='', color='green', linewidth=2)
    plt.legend()
    plt.show(block=True)