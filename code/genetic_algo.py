from code.richardson import *
import copy

logger = logging.getLogger()


class GeneticAlgorithm:
    def __init__(self, population, crossover_rate):
        logger.info(f"Population: {population} Crossover: {crossover_rate}")
        self.population = []
        self.crossover_rate = crossover_rate
        for i in range(population):
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

                logger.debug(f"Crossing individual {i}'s {random_value1} from country {temp_name1}: {value1} "
                            f"to individual {index}'s {random_value2} from country {temp_name2}: {value2}")

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
        for i in range(len(self.population)):
            self.population[i].mutate(individual=i)

    def selection_tournament(self):
        """
        Selection Tournament with Replacement
        :return:
        """
        for i in range(len(self.population)):
            self.population[i].perform_calculations(individual=i)
        fitness_vals = ",".join([str(i.fitness) for i in self.population])
        logger.info(f"New fitness values: {fitness_vals}")

        new_generation = []
        # Currently only 1v1 selection
        for i in range(len(self.population)):
            # Make sure that we don't select current individual
            individual1 = random.randint(0, len(self.population)-1)
            while individual1 == i:
                individual1 = random.randint(0, len(self.population)-1)
            individual2 = random.randint(0, len(self.population)-1)
            # while individual2 == i or individual1 != individual2:
            #     individual2 = random.randint(0, len(self.population)-1)

            # WE WANT TO ADD LOWER FITNESS. LOWER IS MORE STABLE
            if self.population[i].fitness <= self.population[individual1].fitness:
                new_generation.append(copy.deepcopy(self.population[i]))

            else:
                new_generation.append(copy.deepcopy(self.population[individual1]))

        self.population = new_generation

    def calculate_best(self):
        avg_fitness = 0
        for i in self.population:
            avg_fitness += i.fitness
        self.average_fitness.append(avg_fitness/len(self.population))
        logger.info(f"Average Fitness: {self.average_fitness[-1]}")

        self.best_individuals += self.population
        self.best_individuals.sort(key=lambda x: x.fitness)
        self.best_individuals = self.best_individuals[:10]
        fitness_vals = ",".join([str(i.fitness) for i in self.best_individuals])
        logger.info(f"Best Fitness: {fitness_vals}")

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
        self.crossover()
        self.mutate()
        self.selection_tournament()
        self.calculate_best()


