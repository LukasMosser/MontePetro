import numpy as np

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SeedGenerator(object):
    __metaclass__ = Singleton
    def __init__(self, seed):
        self.seed = seed

    def __call__(self):
        self.set_seed()
        return self.request_seed()

    def set_seed(self):
        np.random.seed(self.seed)

    def request_seed(self):
        return np.random.randint(low=1, high=100000000)