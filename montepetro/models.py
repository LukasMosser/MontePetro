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
        if region.name in self.regions.keys():
            logging.log(logging.ERROR,
                        "Encountered duplicate region" + str(region.name) + " in Model " + self.name + ".")
            raise KeyError
        else:
            for key in region.properties.keys():
                # update the regional property seed
                region.properties[key].update_seed(self.seed_generator)
                # delete any values
                region.properties[key].values = None
            self.regions[region.name] = region

    def add_property(self, prop):
        if prop.name in self.properties.keys():
            logging.log(logging.ERROR,
                        "Encountered duplicate property" + str(prop.name) + " in Model " + self.name + ".")
            raise KeyError
        else:
            prop.update_seed(self.seed_generator)
            self.properties[prop.name] = prop

    def add_defined_properties_to_regions(self):
        for region_name, region in self.regions.iteritems():
            for property_name, property in self.properties.iteritems():
                if property_name not in region.properties.keys():
                    region.add_property(property)

    def add_regional_property(self, prop_name, prop):
        for region_name, region in self.regions.iteritems():
            region.properties[prop_name] = prop(region)
            region.properties[prop_name].generate_values()

    def run(self, config):
        for region_name, region in self.regions.iteritems():
            region_config = config[region_name]
            for property_name, property in region.properties.iteritems():
                regional_property_config = region_config[property_name]
                property.generate_values(**regional_property_config)
