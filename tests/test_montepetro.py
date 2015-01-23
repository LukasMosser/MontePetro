__author__ = 'lmosser'
import unittest
import os

import numpy as np

from tests.test_utils import mock_random, mock_numerical_function, MockRegion, MockRandomProperty
from tests.test_utils import MockProperty, mock_random_seed_function, MockSeedGenerator

from montepetro.generators import RandomGenerator
from montepetro.properties import Property, RandomProperty, RegionalProperty
from montepetro.properties import ModelOriginalOilInPlace, OriginalOilInPlace
from montepetro.json_parser import JSONParser
from montepetro.regions import Region
from montepetro.seed_generators import SeedGenerator
from montepetro.models import Model


class TestRandomGenerators(unittest.TestCase):
    def setUp(self):
        self.N = 10
        self.seed = 666
        self.value = 1.0

    def test_random_generator(self):
        # mock the random number function to test trivial behavior
        gen = RandomGenerator(self.seed, self.N, mock_random)

        self.assertEqual(gen.N, self.N)
        self.assertEqual(gen.seed, self.seed)

        self.assertEqual(gen.get_random_number(value=self.value), np.array([self.value]))
        self.assertListEqual(list(gen.get_n_random_numbers(value=self.value)), list(np.ones(self.N)))

        # test passing a list of arguments to the random number function
        gen.random_number_function = np.random.uniform
        self.assertAlmostEqual(gen.get_random_number(low=0.0, high=1.0), np.array(0.7004371218578347), places=5)
        # How to test get N random numbers?


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.name = "Test Property"
        self.desc = "This is a simple property."
        self.random_number_function = np.random.uniform
        self.min = 0.0
        self.max = 1.0
        self.seed = 666
        self.n = 10
        self.mock_generator = RandomGenerator(seed=self.seed,
                                              n=self.n,
                                              random_number_function=self.random_number_function)

    def test_properties(self):
        prop = Property(name="Test Property", desc="This is a simple property.")

        self.assertEquals(prop.name, self.name)
        self.assertEquals(prop.desc, self.desc)

        self.assertEqual(prop.generate_values(), None)
        self.assertEqual(prop.update_seed(), None)

        mock_seed_generator = MockSeedGenerator(self.seed)
        random_prop = RandomProperty(seed_generator=mock_seed_generator,
                                     n=10,
                                     random_number_function=np.random.uniform,
                                     name="Random Property",
                                     desc="Test the random property")

        random_prop.generate_values(low=self.min, high=self.max)
        random_prop_values = list(random_prop.values)

        # reset the mock generator
        self.mock_generator.set_seed()
        mock_random_values = list(self.mock_generator.get_n_random_numbers(low=self.min, high=self.max))
        self.assertEquals(random_prop_values, mock_random_values)

        random_prop.calculate_property_statistics()
        self.assertAlmostEqual(random_prop.mean, np.mean(mock_random_values))

        regional_property = RegionalProperty(MockRegion(name="MockRegion"))
        self.assertEqual(regional_property.region.name, "MockRegion")

    def tearDown(self):
        pass


class TestJSONConfigLoader(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_config.json"
        self.bad_file_name = "test_config_bad.json"
        self.cwd = os.getcwd()
        os.chdir(self.cwd + "/tests/test_data/")

    def test_json_loader(self):
        json = JSONParser(self.file_name)
        json_bad = JSONParser(self.bad_file_name)

        self.assertTrue(json.validate_json())
        self.assertFalse(json_bad.validate_json())

        self.assertEquals(json.data["Name"], "Test Run")
        self.assertEquals(json.data["Version"], "0.01")
        self.assertEquals(json.data["Author"], "LukasMosser")

        self.assertEquals(len(json.data["Regions"]), 1)
        json_regions = [region for region in json.data["Regions"]]

        self.assertEquals(len(json_regions), 1)

        self.assertEquals(len(json.data["Properties"]), 1)

    def tearDown(self):
        os.chdir(self.cwd)


class TestRegions(unittest.TestCase):
    def setUp(self):
        pass

    def test_region(self):
        # Test Basic Functionality
        parent_a = Region(parent=None, name="Test Region")
        self.assertEquals(parent_a.name, "Test Region")
        self.assertEquals(parent_a.parent, None)

        child = Region(parent=parent_a, name="Child Region")
        self.assertEquals(child.parent, parent_a)

        parent_b = Region(parent=None, name="Test Region B")
        child.parent = parent_b
        self.assertNotEqual(child.parent, parent_a)
        self.assertEqual(child.parent, parent_b)

    def test_region_properties(self):
        region = Region(parent=None, name="Test Region")
        property = MockProperty()

        region.add_property(property)
        self.assertEqual(len(region.properties), 1)
        self.assertRaises(KeyError, region.add_property, property)

    def test_region_output(self):
        region = Region(parent=None, name="Test Region")
        self.assertEqual(region.__str__(), "Region Name: Test Region")

    def tearDown(self):
        pass


class TestSeedGenerator(unittest.TestCase):
    def setUp(self):
        self.seed = 300

    def test_seed_generator(self):
        # This fails here: seed_generator_a = SeedGenerator(self.seed)
        np.random.seed(self.seed)
        seed1 = np.random.randint(low=1, high=10000000)
        seed2 = np.random.randint(low=1, high=10000000)

        # And works only here:
        seed_generator_a = SeedGenerator(self.seed)
        seed_generator_a.seed_random_function = mock_random_seed_function

        print seed_generator_a.request_seed()
        print seed_generator_a.seeds
        self.assertRaises(ValueError, seed_generator_a.request_seed)

        seed_generator_a = SeedGenerator(self.seed)
        self.assertEqual(seed_generator_a.request_seed(), seed1)
        self.assertEqual(seed_generator_a.request_seed(), seed2)

        # Therefore SeedGenerator instance will need to be hard coded into the Model class

    def tearDown(self):
        pass


class TestModel(unittest.TestCase):
    def setUp(self):
        self.name = "Test Model"
        self.seed = 200

    def test_model(self):
        model = Model(self.name, self.seed)
        self.assertEqual(model.seed, self.seed)

        model.seed_generator = MockSeedGenerator(self.seed)
        self.assertEqual(model.name, self.name)
        self.assertEqual(model.seed, self.seed)

        mock_property = MockProperty()

        model.add_property(mock_property)
        self.assertEquals(len(model.properties), 1)
        self.assertRaises(KeyError, model.add_property, mock_property)

        mock_random_property = MockRandomProperty(seed_generator=MockSeedGenerator(self.seed - 1),
                                                  name="MockRandomProperty")
        mock_random_property.name = "MockRandomProperty"

        # assigning the property should reset the seed using the models seed generator
        model.add_property(mock_random_property)

        self.assertEqual(model.properties[mock_random_property.name].seed, self.seed)
        self.assertEqual(len(model.properties), 2)

        mock_region = MockRegion(name="MockRegion")
        mock_region.add_property(MockRandomProperty(seed_generator=MockSeedGenerator(self.seed - 1),
                                                    name="RegionRandomMockProperty"))
        model.add_region(mock_region)
        self.assertEquals(len(model.regions), 1)
        self.assertEqual(model.regions[mock_region.name].properties["RegionRandomMockProperty"].seed, self.seed)
        self.assertRaises(KeyError, model.add_region, mock_region)

        #Test Regional Property Addition
        model.add_regional_property("MockRegionalProperty", RegionalProperty)
        for region_name, region in model.regions.iteritems():
            self.assertEqual(len(region.properties), 2)

        # Test filling a model
        # Reinitialize model to get a clean slate
        model = Model(self.name, self.seed)
        mock_random_property_a = MockRandomProperty(seed_generator=MockSeedGenerator(self.seed),
                                                    name="MockRandomProperty")
        mock_region_a = MockRegion(name="MockRegion")

        model.add_region(mock_region_a)
        model.add_property(mock_random_property_a)

        model.add_defined_properties_to_regions()
        for key, region in model.regions.iteritems():
            self.assertEqual(len(region.properties), 1)

        mock_random_property_b = MockRandomProperty(seed_generator=MockSeedGenerator(self.seed - 1),
                                                    name="MockRandomPropertyB")
        model.add_property(mock_random_property_b)

        for region_name, region in model.regions.iteritems():
            self.assertEqual(len(region.properties), 1)

        mock_region_b = MockRegion(name="MockRegionB")

        model.add_region(mock_region_b)
        model.add_defined_properties_to_regions()
        for region_name_a, region_a in model.regions.iteritems():
            for region_name_b, region_b in model.regions.iteritems():
                for property_name, property in model.properties.iteritems():
                    self.assertNotEqual(model.properties[property_name], region_a.properties[property_name])
                    if region_a is not region_b:
                        self.assertNotEqual(region_a.properties[property_name], region_b.properties[property_name])
            self.assertEqual(len(region_a.properties), 2)



        #Test runnning a model from a configuration dictionary
        config = {"MockRegionA": {"MockRandomPropertyA": {"low": 100.0, "high": 1000.0},
                           "MockRandomPropertyB": {"low": 100.0, "high": 1000.0}}
                 }

        n = 10
        model = Model(self.name, self.seed)
        mock_random_property_a = MockRandomProperty(seed_generator=MockSeedGenerator(self.seed),
                                                    name="MockRandomPropertyA", n=n,
                                                    random_number_function=np.random.uniform)
        mock_random_property_b = MockRandomProperty(seed_generator=MockSeedGenerator(self.seed),
                                                    name="MockRandomPropertyB", n=n,
                                                    random_number_function=np.random.uniform)
        mock_region_a = MockRegion(name="MockRegionA")
        model.add_property(mock_random_property_a)
        model.add_property(mock_random_property_b)
        model.add_region(mock_region_a)
        model.run(config)

        for region_name, region in model.regions.iteritems():
            for property_name, property in region.properties.iteritems():
                self.assertEqual(len(property.values), 10)

    def tearDown(self):
        pass


class TestOilInPlaceCalculation(unittest.TestCase):
    def setUp(self):
        pass

    def test_oil_in_place_calculation(self):
        seed = 300
        n = 1
        model = Model("Simple Model", 666)

        area = RandomProperty(name="Area", n=n, random_number_function=mock_random)
        porosity = RandomProperty(name="Porosity", n=n, random_number_function=mock_random)
        sw = RandomProperty(name="Sw", n=n, random_number_function=mock_random)

        config = {"Region A": {"Area": {"value": 2.0},
                               "Porosity": {"value": 0.5},
                               "Sw": {"value": 0.1}},
                  "Region B": {"Area": {"value": 1.0},
                               "Porosity": {"value": 0.5},
                               "Sw": {"value": 0.1}}}

        #oil in place region a should be 2.0*0.5*(1-0.1) = 1.0*0.9 = 0.9
        #oil in place region b should be 1.0*0.5*(1-0.1) = 0.5*0.9 = 0.45

        model.add_property(area)
        model.add_property(porosity)
        model.add_property(sw)

        region_a = Region(name="Region A")
        region_b = Region(name="Region B")

        model.add_region(region_a)
        model.add_region(region_b)

        model.add_defined_properties_to_regions()

        model.run(config)

        model.add_regional_property("ooip", OriginalOilInPlace)
        for region_name, region in model.regions.iteritems():
            if region_name is "Region A":
                self.assertAlmostEqual(np.sum(region.properties["ooip"].values), n*0.9, 4)

            else:
                self.assertAlmostEqual(np.sum(region.properties["ooip"].values), n*0.45, 4)


        ooip = ModelOriginalOilInPlace(model)
        ooip.generate_values()

        self.assertAlmostEqual(np.sum(ooip.values), n*(0.9+0.45), 4)

    def tearDown(self):
        pass