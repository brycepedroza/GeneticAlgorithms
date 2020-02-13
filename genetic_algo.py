from richardson import *


class GeneticAlgorithm:
    def __init__(self, population, crossover_rate):
        self.population = []
        self.crossover_rate = crossover_rate
        for i in range(population):
            #
            self.population.append(Richardson())
        best_individuals = []
        average_fitness = []

    def crossover(self):
        """
        apply crossover as per the crossover ratio
        :return:
        """
        pass

    def mutate(self):
        """
        We mutate each individual in the population
        :return:
        """
        pass

    def selection_tournament(self):
        """
        Selection Tournament with Replacement
        :return:
        """
        pass

    def iterate_population(self):
        """
        One iteration is as follows
        Apply Crossover
        Apply Mutations
        Calculate Fitness
        DUEL. Selection Tournament with Replacement
        Keep running total of fittest people across all generations
        :return:
        """
        pass


"""
Th
"""


if __name__ == "__main__":
    g = GeneticAlgorithm(100, 0.4)
    print(len(g.population))

