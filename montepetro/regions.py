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


    def calculate_ranked_correlation_matrix(self, target):
        for property in self.properties:
            rho = self.randGen.CalculatePearson(target.values, property.samples)
            print "Property Name:\t" + str(property.name) + "\tPearson rank:\t" + str(rho[0]) + ""

    def __str__(self):
        print "-------------------------------------------------------------------------"
        print "Region Name: ", self.region_name
        print "Properties:"
        for property in self.properties:
            print "\tName: ", self.properties[property].name, "\n\tProbability Distribution Function: ", \
                self.properties[property].distribution, "\n\tMean of Samples: ", self.properties[
                property].mean, "\n\tMode of Samples: ", self.properties[property].mode

    def PrintCalculatedProperties(self):
        print "Calculated Properties:"
        for property in self.calculated_properties:
            print "\tName: ", property.name, "\n\tMean of values: ", property.mean, "\n\tMode of Samples: ", property.mode  # ,"\n Mode of values: ", property.mode


    def PlotPropertyHistograms(self):
        for property in self.properties:
            if property.show:
                plot.hist(property.samples, bins=25, histtype='stepfilled', normed=True, alpha=0.2, label=property.name)
        plot.title("" + str(self.region_name) + " Property Histograms")
        plot.ylabel("Probability")
        plot.xlabel("Value")
        plot.legend()
        plot.show()

    def Dump_Region(self):
        for key in self.properties:
            np.savetxt("" + str(self.region_name) + "_" + str(self.properties[key].name) + ".csv",
                          self.properties[key].samples, delimiter=",")
        for key in self.calculated_properties:
            np.savetxt("" + str(self.region_name) + "_" + str(self.calculated_properties[key].name) + ".csv",
                          self.calculated_properties[key].values, delimiter=",")

    def Assemble_Values(self):
        output = []
        for key in self.properties:
            values = list(self.properties[key].samples)
            values.insert(0, str(self.properties[key].name))
            output.append(self.properties[key].samples)
        for key in self.calculated_properties:
            values = list(self.calculated_properties[key].values)
            values.insert(0, str(self.calculated_properties[key].name))
            output.append(self.calculated_properties[key].values)
        return output