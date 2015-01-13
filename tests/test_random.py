__author__ = 'lmosser'
import unittest
import os

import numpy as np

from tests.test_utils import mock_random, mock_numerical_function
from montepetro.generators import RandomGenerator
from montepetro.properties import Property, NumericalProperty, RandomProperty
from montepetro.json_parser import JSONParser


class RandomGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.N = 10
        self.seed = 666

    def test_random_generator(self):
        # mock the random number function to test trivial behavior
        gen = RandomGenerator(self.seed, self.N, mock_random)

        self.assertEqual(gen.N, self.N)
        self.assertEqual(gen.seed, self.seed)

        self.assertEqual(gen.get_random_number(), np.array([1.0]))
        self.assertListEqual(list(gen.get_n_random_numbers()), list(np.ones(self.N)))

        # test passing a list of arguments to the random number function
        gen.random_number_function = np.random.uniform
        self.assertAlmostEqual(gen.get_random_number(low=0.0, high=1.0), np.array(0.7004371218578347), places=5)
        # How to test get N random numbers?

class TestRegions(unittest.TestCase):

    def setUp(self):
        pass

    def test_region(self):
        pass

    def tearDown(self):
        pass

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

        random_prop = RandomProperty(seed=666,
                                     n=10,
                                     random_number_function=np.random.uniform,
                                     name="Random Property",
                                     desc="Test the random property")

        random_prop.generate_values(low=self.min, high=self.max)
        random_prop_values = list(random_prop.values)

        #reset the mock generator
        self.mock_generator.set_seed()
        mock_random_values = list(self.mock_generator.get_n_random_numbers(low=self.min, high=self.max))
        self.assertEquals(random_prop_values, mock_random_values)

        random_prop.calculate_property_statistics()
        self.assertAlmostEqual(random_prop.mean, np.mean(mock_random_values))

        numerical_prop = NumericalProperty(numerical_function=mock_numerical_function,
                                           name="Numerical Property",
                                           desc="A numerical property")

        numerical_prop.generate_values()
        self.assertEquals(numerical_prop.values, 1.0)

        numerical_prop.calculate_property_statistics()
        self.assertEquals(numerical_prop.mean, 1.0)


    def tearDown(self):
        pass

class TestJSONConfigLoader(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_config.json"
        self.bad_file_name = "test_config_bad.json"
        self.cwd = os.getcwd()
        os.chdir(self.cwd+"/tests/test_data/")

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

    def tearDown(self):
        os.chdir(self.cwd)