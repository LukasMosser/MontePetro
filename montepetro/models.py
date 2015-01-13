import logging
from montepetro.seed_generators import SeedGenerator


class Model(object):
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.seed_generator = SeedGenerator(self.seed)
        self.properties = {}
        self.regions = {}

    def add_region(self, region):
        if self.regions.has_key(region.name):
            logging.log(logging.ERROR, "Encountered duplicate region"+str(region.name)+" in Model "+self.name+".")
            raise KeyError
        else:
            self.regions[region.name] = region

    def add_property(self, prop):
        if self.properties.has_key(prop.name):
            logging.log(logging.ERROR, "Encountered duplicate property"+str(prop.name)+" in Model "+self.name+".")
            raise KeyError
        else:
            prop.update_seed(self.seed_generator)
            self.properties[prop.name] = prop

    def dump(self):
        pass
