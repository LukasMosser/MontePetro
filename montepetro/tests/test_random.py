__author__ = 'lmosser'
import unittest
import numpy as np

from montepetro.generators import RandomGenerator


class RandomGeneratorTests(unittest.TestCase):
    def mock_random(self):
        return 1.0

    def setUp(self):
        self.N = 10
        self.seed = 666

    def test_random_generator(self):
        gen = RandomGenerator(self.seed, self.N)

        self.assertEqual(gen.N, self.N)
        self.assertEqual(gen.seed, self.seed)

        # mock the random number function to test trivial behavior
        gen.random_number_function = self.mock_random
        self.assertEqual(gen.get_random_number(), np.array([1.0]))
        self.assertListEqual(list(gen.get_n_random_numbers()), list(np.ones(self.N)))

        # test passing a list of arguments to the random number function
        gen.random_number_function = np.random.uniform
        self.assertAlmostEqual(gen.get_random_number(low=0.0, high=1.0), np.array(0.7004371218578347), places=5)
        # How to test get N random numbers?