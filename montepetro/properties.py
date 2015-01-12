import numpy
import matplotlib.pyplot as plot

from montepetro.generators import RandomGeneratorDics


class Property(object):
    def __init__(self, args, seed, N):
        self.name = args['Name']  # name of property
        self.args = args  # arguments for distribution
        self.randGen = RandomGeneratorDics(seed, N)  # Random Number Generator
        self.show = True
        self.GenerateSamples()

    def __call__(self):
        return self.samples

    def GenerateSamples(self):
        self.samples = self.randGen.GetRandomValues(self.args)
        self.mean = numpy.mean(self.samples)

    # self.mode = numpy.bincount(list(self.samples)).argmax()
    def PlotHistogram(self, bins):
        plot.hist(self.samples, bins)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(self.name)
        plot.show()


class GlobalProperty(object):
    def __init__(self, name, dist, args, randGen):
        self.name = name
        self.args = args
        self.distribution = dist
        self.randGen = randGen
        self.show = True

    def GenerateSamples(self):
        self.samples = self.randGen.GetRandomValues(self.distribution, self.args)
        self.mean = numpy.mean(self.samples)

    # self.mode = numpy.bincount(list(self.samples)).argmax()
    def PlotHistogram(self, bins):
        plot.hist(self.samples, bins)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(self.name)
        plot.show()


class CalculatedProperty(object):
    def __init__(self, name, values, parentRegion):
        self.name = name
        self.values = values
        self.parentRegion = parentRegion
        self.CalculateStatisticalProperties()

    def __call__(self):
        return self.values

    def CalculateStatisticalProperties(self):
        self.mean = numpy.mean(self.values)

    # self.mode = numpy.bincount(list(self.values)).argmax()

    def PlotHistogram(self, bins, c_bool):
        plot.hist(self.values, bins, cumulative=c_bool, normed=True)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(''.join([self.name, self.parentRegion.region_name]))
        plot.show()


class CalculatedPropertyNoLayer(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.CalculateStatisticalProperties()

    def __call__(self):
        return self.values

    def CalculateStatisticalProperties(self):
        self.mean = numpy.mean(self.values)

    # self.mode = numpy.bincount(list(self.values)).argmax()

    def PlotHistogram(self, bins, c_bool):
        plot.hist(self.values, bins, cumulative=c_bool, normed=True)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title(self.name)
        plot.show()


class ParameterClass(object):
    def __init__(self):
        pass

    def __init__(self, paramclass_dict):
        self.classes = paramclass_dict

    def __call__(self, class_id):
        return self.classes[class_id]


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