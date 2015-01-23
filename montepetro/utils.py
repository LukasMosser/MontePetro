__author__ = 'lmosser'
import scipy
import numpy as np


def random_number_from_truncated_normal_distribution(low=0.0, high=1.0, mean=0.5, std=1.0):
    normal = scipy.stats.norm(mean, std)
    u = np.random.uniform(low=0.0, high=1.0)
    x = normal.ppf(normal.cdf(low) + u * (normal.cdf(high) - normal.cdf(low)))
    return x
