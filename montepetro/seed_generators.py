import numpy as np
import logging


class SeedGenerator(object):
    def __init__(self, seed):
        self.seed = seed
        np.random.seed(self.seed)
        self.seed_random_function = np.random.randint
        self.seeds = []

    def request_seed(self):
        a = self.create_seed()
        if a in self.seeds:
            logging.log(logging.ERROR, "Duplicate seeds encountered.")
            raise ValueError
        self.seeds.append(a)
        return a

    def create_seed(self, low=1, high=10000000):
        return self.seed_random_function(low=low, high=high)