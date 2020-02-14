from richardson import *
import copy
from heapq import heappushpop, heappush, nsmallest

class GeneticAlgorithm:
    def __init__(self, population, crossover_rate):
        self.population = []
        self.crossover_rate = crossover_rate
        for i in range(population):
            #
            self.population.append(Richardson())
        self.best_individuals = []
        self.average_fitness = []

    def crossover(self):
        """
        Apply crossover as per the crossover ratio.
        Some possible ways to change the crossover:
        1. apply average of both values to each attribute
        2. only allow individuals to crossover one.
        :return:
        """
        pass
        for i in range(len(self.population)):
            # Check if we perform crossover
            if random.uniform(0, 1) <= self.crossover_rate:
                # Make sure that we don't select current individual
                index = random.randint(0, len(self.population)-1)
                while index == i:
                    index = random.randint(0, len(self.population)-1)

                # Then we swap attributes of two individuals
                temp_name1 = random.choice(['x', 'y', 'z'])
                random_country1 = self.population[i].__getattribute__(temp_name1)
                random_value1 = random.choice(
                    ['expend', 'econ_rest', 'k_self', 'k_others'])
                value1 = random_country1.__getattribute__(random_value1)
                temp_name2 = random.choice(['x', 'y', 'z'])
                random_country2 = self.population[index].__getattribute__(temp_name2)
                random_value2 = random.choice(
                    ['expend', 'econ_rest', 'k_self', 'k_others'])
                value2 = random_country2.__getattribute__(random_value2)

                # swap the two values
                temp = value1
                value1 = value2
                value2 = temp

                # set them back to the right individual
                random_country1.__setattr__(random_value1, value1)
                random_country2.__setattr__(random_value2, value2)

    def mutate(self):
        """
        We mutate each individual in the population
        :return:
        """
        for i in self.population:
            i.mutate()

    def selection_tournament(self):
        """
        Selection Tournament with Replacement
        :return:
        """
        for i in self.population:
            i.perform_calculations()

        new_generation = []
        # Currently only 1v1 selection
        for i in range(len(self.population)):
            # Make sure that we don't select current individual
            index = random.randint(0, len(self.population)-1)
            while index == i:
                index = random.randint(0, len(self.population)-1)
            # WE WANT TO ADD LOWER FITNESS. LOWER IS MORE STABLE
            if self.population[i].fitness <= self.population[index].fitness:
                new_generation.append(copy.deepcopy(self.population[i]))
            else:
                new_generation.append(copy.deepcopy(self.population[i]))
        self.population = new_generation

    def calculate_best(self):
        avg_fitness = 0
        for i in self.population:
            avg_fitness += i.fitness
        self.average_fitness.append(avg_fitness/len(self.population))

        self.best_individuals += self.population[:10]
        self.best_individuals.sort(key=lambda x: x.fitness)


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
        g.crossover()
        g.mutate()
        g.selection_tournament()
        g.calculate_best()
        print(len(g.population))


if __name__ == "__main__":
    g = GeneticAlgorithm(100, 0.4)
    for x in range(50):
        g.iterate_population()
    pass
    print()
