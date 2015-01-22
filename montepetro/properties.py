import numpy as np
from montepetro.generators import RandomGenerator


class Property(object):
    def __init__(self,  name=None, desc=None):
        self.name = name
        self.desc = desc
        self.values = None

    def generate_values(self):
        pass

    def update_seed(self, *args, **kwargs):
        pass


class RandomProperty(Property):
    def __init__(self, seed_generator, n=None, random_number_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.seed = None
        self.update_seed(seed_generator)
        self.random_generator = RandomGenerator(self.seed, n, random_number_function)
        self.mean = None

    def update_seed(self, seed_generator):
        self.seed = seed_generator.request_seed()

    def generate_values(self, *args, **kwargs):
        self.values = self.random_generator.get_n_random_numbers(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)


class RegionalProperty(Property):
    def __init__(self, region, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.region = region
