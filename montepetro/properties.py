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
    def __init__(self, seed_generator=None, n=None, random_number_function=None, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.seed = None
        self.seed_generator = seed_generator
        self.n = n
        self.random_number_function = random_number_function
        self.random_generator = None

        if self.seed_generator is not None:
            self.update_seed(seed_generator)
            self.random_generator = RandomGenerator(self.seed, n, random_number_function)

        self.mean = None

    def update_seed(self, seed_generator):
        self.seed = seed_generator.request_seed()
        self.random_generator = RandomGenerator(self.seed, self.n, self.random_number_function)

    def generate_values(self, *args, **kwargs):
        self.values = self.random_generator.get_n_random_numbers(*args, **kwargs)

    def calculate_property_statistics(self):
        self.mean = np.mean(self.values)


class RegionalProperty(Property):
    def __init__(self, region, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.region = region


class OriginalOilInPlace(RegionalProperty):
    def __init__(self, region, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.region = region

    def calculation(self):
        phi = self.region.properties["Porosity"].values
        area = self.region.properties["Area"].values
        sw = self.region.properties["Sw"].values
        ooip = area*phi*(1.0-sw)
        return ooip

    def calculate_property_statistics(self):
        self.p90 = np.percentile(self.values, 10)
        self.p50 = np.percentile(self.values, 50)
        self.p10 = np.percentile(self.values, 90)
        self.mean = np.mean(self.values)

    def generate_values(self):
        self.values = self.calculation()


class ModelOriginalOilInPlace(RegionalProperty):
    def __init__(self, model, *args, **kwargs):
        Property.__init__(self, *args, **kwargs)
        self.model = model

    def calculation(self):
        ooips = []
        for region_name, region in self.model.regions.iteritems():
            ooips.append(region.properties["ooip"].values)

        # assumes len(arrlist) > 0
        sum = ooips[0].copy()
        for a in ooips[1:]:
            sum += a
        return sum

    def calculate_property_statistics(self):
        self.p90 = np.percentile(self.values, 10)
        self.p50 = np.percentile(self.values, 50)
        self.p10 = np.percentile(self.values, 90)
        self.mean = np.mean(self.values)

    def generate_values(self):
        self.values = self.calculation()
