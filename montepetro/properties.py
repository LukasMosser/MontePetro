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

class OOIP(object):
    def __init__(self, layer):
        self.area = layer.properties['Area']()
        self.poro = layer.properties['Porosity']()
        self.sw = layer.properties['Sw']()
        self.values = []
        for i in range(len(self.area)):
            self.values.append(self.area[i] * self.poro[i] * (1 - self.sw[i]))
        self.ooip = CalculatedProperty('OOIP', self.values, layer)

    def __call__(self):
        return self.ooip