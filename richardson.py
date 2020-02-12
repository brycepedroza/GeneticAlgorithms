import random


class Rates:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Country:
    def __init__(self, dominant=False, **kwargs):
        self.__dict__.update(kwargs)
        self.dominant = dominant
        self.curr = 0
        self.next = -1


class Richardson:
    def __init__(self, new=True, x=None, y=None, z=None):
        if new:
            self.x = Richardson.new_country(dominant=True)
            self.y = Richardson.new_country()
            self.z = Richardson.new_country()
        else:
            self.x = x
            self.y = y
            self.z = z
        self.fitness = -1

    def calculate_spending(self):
        if self.x.dominant:
            self.x.next = self.x.curr + \
                (self.x.k_self*(self.x.expend-self.x.curr) +
                    self.x.k_others*(self.y.curr+self.z.curr)) * \
                (self.x.econ_rest-self.x.curr)
            self.y.next = self.y.curr + \
                (self.y.k_self * (self.y.expend - self.y.curr) +
                    self.y.k_others * (self.x.curr - self.z.curr)) * \
                (self.y.econ_rest - self.y.curr)
            self.z.next = self.z.curr + \
                (self.z.k_self * (self.z.expend - self.z.curr) +
                    self.z.k_others * (self.x.curr - self.y.curr)) * \
                (self.z.econ_rest - self.z.curr)
        elif self.y.dominant:
            pass
        elif self.z.dominant:
            pass

    def calculate_fitness(self):
        self.fitness = abs(self.x.next - (self.y.next + self.z.next))

    @staticmethod
    def new_country(dominant=False):
        return Country(
            dominant=dominant,
            expend=random.uniform(0, 1),
            econ_rest=random.uniform(0, 1),
            k_self=random.uniform(0, 1),
            k_others=random.uniform(0, 1)
        )


if __name__ == "__main__":
    r = Richardson()
    r.calculate_spending()
    r.calculate_fitness()

    print(r.fitness)

