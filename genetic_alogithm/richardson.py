import random
import logging
logger = logging.getLogger()


class Country:
    def __init__(self, dominant=False, **kwargs):
        self.dominant = dominant
        self.curr = 0
        self.__dict__.update(kwargs)


class Richardson:
    def __init__(self, new=True, x=None, y=None, z=None, mutation_rate=0.9, normalize=False):
        if new:
            self.x = Richardson.new_country(dominant=True)
            self.y = Richardson.new_country()
            self.z = Richardson.new_country()
        else:
            self.x = x
            self.y = y
            self.z = z
        self.fitness = -1
        self.mutation_rate = mutation_rate
        self.normalize = normalize

    def mutate(self, individual=-1):
        """
        We mutate one of the fields if a random number from 0-1 that we pick
        is less than the mutation rate. ie. if our mutation rate is .9,
        and the random is less or equal then we mutate, thus simulating a
        90% mutation rate.
        :return:
        """
        if random.uniform(0, 1) <= self.mutation_rate:
            # Then we mutate one of the fields!
            temp_name = random.choice(['x', 'y', 'z'])
            random_country = self.__getattribute__(temp_name)
            random_value = random.choice(
                ['expend', 'econ_rest', 'k_self', 'k_others'])
            temp_value1 = random_country.__getattribute__(random_value)

            # Mutate value by 5% Either add or subtract.
            if random.randint(0, 1) == 1:
                temp_value2 = temp_value1 + temp_value1 * .05
            else:
                temp_value2 = temp_value1 - temp_value1 * .05

            # Make sure the value is in between 0 and 1
            if temp_value2 > 1:
                temp_value2 = 1
            elif temp_value2 < 0:
                temp_value2 = 0

            random_country.__setattr__(random_value, temp_value2)
            logger.debug(f"Mutating individual {individual}'s {random_value} "
                         f"from country {temp_name} to {temp_value2}, from {temp_value1}")

    def perform_calculations(self):

        if self.x.dominant:
            Richardson.calculate_spending(self.x, self.y, self.z)
        elif self.y.dominant:
            Richardson.calculate_spending(self.y, self.x, self.z)
        elif self.z.dominant:
            Richardson.calculate_spending(self.z, self.y, self.x)

        # Is x the biggest?
        if self.x.curr > self.y.curr and self.x.curr > self.z.curr:
            self.x.dominant = True
            self.y.dominant = False
            self.z.dominant = False
        # Is y the biggest?
        if self.y.curr > self.x.curr and self.y.curr > self.z.curr:
            self.y.dominant = True
            self.x.dominant = False
            self.z.dominant = False
        # Is z the biggest?
        if self.z.curr > self.y.curr and self.z.curr > self.x.curr:
            self.z.dominant = True
            self.y.dominant = False
            self.x.dominant = False

        if self.x.dominant:
            self.fitness = Richardson.calculate_fitness(self.x, self.y, self.z, self.normalize)
        elif self.y.dominant:
            self.fitness = Richardson.calculate_fitness(self.y, self.x, self.z, self.normalize)
        elif self.z.dominant:
            self.fitness = Richardson.calculate_fitness(self.z, self.y, self.x, self.normalize)

    def reset_current_spending(self):
        self.x.curr = 0
        self.y.curr = 0
        self.z.curr = 0
        # reset who is dominating too, x is default
        self.x.dominant = True
        self.y.dominant = False
        self.z.dominant = False

    @staticmethod
    def calculate_fitness(dominant, a, b, normalize):

        fitness = abs(dominant.curr - (a.curr + b.curr))
        if normalize:
            fitness = fitness/abs(dominant.curr-min(a.curr, b.curr))
        return fitness

    @staticmethod
    def calculate_spending(dominant: Country, a: Country, b: Country):
        dominant.curr = dominant.curr + (
                dominant.k_self * (dominant.expend-dominant.curr) +
                dominant.k_others * (a.curr+b.curr)) * \
            (dominant.econ_rest-dominant.curr)
        a.curr = a.curr + (
                a.k_self * (a.expend-a.curr) +
                a.k_others * (dominant.curr-b.curr)) * \
            (a.econ_rest-a.curr)
        b.curr = b.curr + (
                b.k_self * (b.expend-b.curr) +
                b.k_others * (dominant.curr-a.curr)) * \
            (b.econ_rest-b.curr)

    @staticmethod
    def new_country(dominant=False):
        return Country(
            dominant=dominant,
            expend=random.uniform(0, 1),
            econ_rest=random.uniform(0, 1),
            k_self=random.uniform(0, 1),
            k_others=random.uniform(0, 1)
        )

    def get_county_props(self):
        return {
            'x': self.x.__dict__,
            'y': self.y.__dict__,
            'z': self.z.__dict__
        }

    def __lt__(self, other):
        return self.fitness < other.fitness

