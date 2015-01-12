import matplotlib.pyplot as plot
import numpy

from montepetro.properties import Property, CalculatedProperty, OOIP


class Region(object):
    def __init__(self):
        pass

    def __init__(self, parent, name, parameter_class):
        self.model = parent
        self.region_name = name
        self.properties = []
        self.calculated_properties = {}
        self.parameter_class = parameter_class
        self.AddPropertiesFromParameterClass()

    def AddPropertiesFromParameterClass(self):
        prop_list = []
        parcls_dict = self.model.parameter_classes
        param_cls = self.model.parameter_classes(self.parameter_class)
        self.properties = dict([(param, Property(param_cls[param],
                                                 self.model.GlobalRandGen.GetRandomInteger(10000, 1000000, 1),
                                                 self.model.N)) for param in parcls_dict(self.parameter_class)])

    def AddLayerProperties(self, layer_prop_dict):
        for prop_key in layer_prop_dict:
            self.properties[prop_key] = Property(layer_prop_dict[prop_key],
                                                 self.model.GlobalRandGen.GetRandomInteger(10000, 1000000, 1),
                                                 self.model.N)

    def AddProperty(self, param, args):
        self.properties[param] = Property(args, self.model.GlobalRandGen.GetRandomInteger(10000, 1000000, 1),
                                          self.model.N)

    def CalculateDerivedProperty(self, name, equation):
        values = eval(equation)
        self.calculated_properties.append(CalculatedProperty(name, values, self))

    def CalculateOOIP(self):
        ooip = OOIP(self)
        self.calculated_properties['OOIP'] = ooip.ooip

    def CalculateRankedCorrelationMatrix(self, target):
        for property in self.properties:
            rho = self.randGen.CalculatePearson(target.values, property.samples)
            print "Property Name:\t" + str(property.name) + "\tPearson rank:\t" + str(rho[0]) + ""

    def GenerateSamplesOfProperties(self):
        for property in self.properties:
            property.GenerateSamples()

    def PrintProperties(self):
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
            numpy.savetxt("" + str(self.region_name) + "_" + str(self.properties[key].name) + ".csv",
                          self.properties[key].samples, delimiter=",")
        for key in self.calculated_properties:
            numpy.savetxt("" + str(self.region_name) + "_" + str(self.calculated_properties[key].name) + ".csv",
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