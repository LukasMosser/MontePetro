import numpy

from montepetro.region import Region
from properties import GlobalProperty, CalculatedPropertyNoLayer
from montepetro.generator import RandomGeneratorDics
from properties import ParameterClass


class Model(object):
    def __init__(self):
        pass

    def __init__(self, name, seed, N, parclass_dict):
        self.model_name = name
        self.seed = seed
        self.N = N
        self.GlobalRandGen = RandomGeneratorDics(self.seed, self.N)
        self.parameter_classes = ParameterClass(parclass_dict)
        self.global_properties = []
        self.regions = {}

    # self.equations = []


    def AddGlobalProperties(self, args):
        for global_prop in args:
            self.AddGlobalProperty(global_prop)

    def AddRegions(self, regions_dict):
        for region in regions_dict:
            self.AddRegion(regions_dict[region])

    def AddGlobalProperty(self, args):
        self.global_properties.append(GlobalProperty(args[0], args[1], args[2], self.randGen))

    def AddRegion(self, region_properties_dict):
        name = region_properties_dict['Name']
        self.regions[name] = Region(self, name, region_properties_dict['RockType'])
        self.regions[name].AddLayerProperties(region_properties_dict['Layer_Properties'])

    def CalculateOOIP(self):
        total_ooip = [0] * self.N
        for key in self.regions:
            self.regions[key].CalculateOOIP()
            values = self.regions[key].calculated_properties['OOIP'].values
            for i in range(len(values)):
                total_ooip[i] += values[i]
        self.ooip_prop = CalculatedPropertyNoLayer('OOIP', total_ooip)

    def AddEquations(self, args):
        for equation in args:
            self.equations.append(equation)

    def AddRegionProperties(self, args):
        i = 0
        for set in args:
            for property in set:
                self.regions[i].AddProperty(property[0], property[1], property[2])
            i += 1

    def AddLocalProperties(self, property_dictionary):
        for property in property_dictionary:
            for region in self.regions:
                pass
            # region.

    def CreateGlobalSamples(self):
        for global_prop in self.global_properties:
            global_prop.GenerateSamples()

    def CreatePropertySamples(self):
        for region in self.regions:
            region.GenerateSamplesOfProperties()

    def CreateDerivedProperties(self):
        for region in self.regions:
            for equation in self.equations:
                print equation
                region.CalculateDerivedProperty(equation[0], equation[1])

    def PrintModelOutput(self):
        for region in self.regions:
            region.PrintProperties()
            region.PrintCalculatedProperties()

    def PlotModelHistograms(self, bins):
        for region in self.regions:
            for property in region.properties:
                property.PlotHistogram(bins)
            for derived_property in region.calculated_properties:
                derived_property.PlotHistogram(bins, False)
            for derived_property in region.calculated_properties:
                derived_property.PlotHistogram(bins, True)

    def DumpModel(self):
        for key in self.regions:
            self.regions[key].Dump_Region()

    def DumpTotalOOIP(self):
        numpy.savetxt("" + str(self.model_name) + "_" + str(self.ooip_prop.name) + ".csv", self.ooip_prop.values,
                      delimiter=",")
