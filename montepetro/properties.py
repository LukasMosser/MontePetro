import numpy as np
import matplotlib.pyplot as plot

from montepetro.generators import RandomGenerator


class Property(object):
    def __init__(self,  name=None, desc=None):
        self.name = name
        self.desc = desc
        self.values = None

    def plot(self):
        pass


class RandomProperty(Property):
    def __init__(self, seed=None, n=None, random_number_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.random_generator = RandomGenerator(seed, n, random_number_function)
        self.mean = None

    def generate_values(self, *args, **kwargs):
        self.values = self.random_generator.get_n_random_numbers(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)

    def plot(self, bins=50):
        plot.hist(self.values, bins)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(self.name)
        plot.show()


class NumericalProperty(Property):
    def __init__(self, numerical_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.numerical_function = numerical_function
        self.mean = None

    def generate_values(self, *args, **kwargs):
        self.values = self.numerical_function(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)

    def plot(self, bins=50):
        plot.hist(self.values, bins)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(self.name)
        plot.show()


class OriginalOilInPlace(NumericalProperty):
    def __init__(self):
        NumericalProperty.__init__(name="OOIP", desc="Original Oil in Place Property")
        self.numerical_function = self.original_oil_in_place

    def original_oil_in_place(self, *args, **kwargs):
        area = kwargs['regions'].properties['area']
        phi = kwargs['regions'].properties['porosity']
        sw = kwargs['regions'].properties['sw']
        result = []

        for i in range(len(area)):
            result.append(area[i]*phi[i]*(1-sw[i]))

        return np.array(result)