import matplotlib.pyplot as plot
import numpy as np
import logging


class Region(object):
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.properties = {}

    def add_property(self, prop):
        if prop.name in self.properties.keys():
            logging.log(logging.ERROR,
                        "Encountered duplicate property" + str(prop.name) + " in region " + str(self.name) + ".")
            raise KeyError
        else:
            self.properties[prop.name] = prop

    def __str__(self):
        str = ""
        str += "Region Name: " + self.name
        return str