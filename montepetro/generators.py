import numpy as np


class RandomGenerator(object):
    def __init__(self, seed, n):
        self.seed = seed
        self.set_seed()
        self.N = n
        self.random_number_function = None

    def set_seed(self):
        np.random.seed(self.seed)

    def get_random_number(self, *args, **kwargs):
        return np.array(self.random_number_function(*args, **kwargs))

    def get_n_random_numbers(self, *args, **kwargs):
        return np.array([self.random_number_function(*args, **kwargs) for r in range(self.N)])
