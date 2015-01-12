__author__ = 'lmosser'
import unittest
import numpy as np

from test_utils import mock_random
from montepetro.generators import RandomGenerator
from montepetro.properties import Property, NumericalProperty, RandomProperty

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

        random_prop = RandomProperty(seed=666,n=10, random_number_function=np.random.uniform)
        random_prop.generate_values(low=self.min, high=self.max)
        random_prop_values = list(random_prop.values)

        #reset the mock generator
        self.mock_generator.set_seed()
        mock_random_values = list(self.mock_generator.get_n_random_numbers(low=self.min, high=self.max))
        self.assertEquals(random_prop_values, mock_random_values)

        random_prop.calculate_property_statistics()
        self.assertAlmostEqual(random_prop.mean, np.mean(mock_random_values))

    def tearDown(self):
        pass
