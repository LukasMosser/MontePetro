__author__ = 'lmosser'
from montepetro.properties import Property, RandomProperty
from montepetro.regions import Region
from montepetro.seed_generators import SeedGenerator


def mock_random():
    return 1.0


def mock_numerical_function():
    return 1.0


def mock_random_seed_function(*args, **kwargs):
    return int(1)


class MockSeedGenerator(SeedGenerator):
    def __init__(self, seed):
        SeedGenerator.__init__(self, seed=seed)

    def request_seed(self):
        return self.seed


class MockProperty(Property):
    def __init__(self):
        Property.__init__(self, name="MockProperty", desc="A Mock Property")

    def generate_values(self):
        return True


class MockRandomProperty(RandomProperty):
    def __init__(self, seed_generator, *args, **kwargs):
        RandomProperty.__init__(self, seed_generator, *args, **kwargs)


class MockRegion(Region):
    def __init__(self, *args, **kwargs):
        Region.__init__(self, *args, **kwargs)
