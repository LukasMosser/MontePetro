import matplotlib.pyplot as plot
import numpy as np


class Region(object):
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.properties = {}

    def add_property(self, property):
        try:
            self.properties[property.name] = property
        except KeyError:
            pass

    def __str__(self):
        print "-------------------------------------------------------------------------"
        print "Region Name: ", self.region_name
        print "Properties:"
        for property in self.properties:
            print "\tName: ", self.properties[property].name, "\n\tProbability Distribution Function: ", \
                self.properties[property].distribution, "\n\tMean of Samples: ", self.properties[
                property].mean, "\n\tMode of Samples: ", self.properties[property].mode