__author__ = 'lmosser'
import scipy.stats
import numpy as np


def truncated_normal_rvs(low=0.0, high=1.0, mean=0.5, std=1.0, size=1):
    normal = scipy.stats.norm(mean, std)
    u = np.random.uniform(low=0.0, high=1.0, size=size)
    x = normal.ppf(normal.cdf(low) + u * (normal.cdf(high) - normal.cdf(low)))
    return x

def constant_value(*args, **kwargs):
    value = kwargs.get("value")
    return value
