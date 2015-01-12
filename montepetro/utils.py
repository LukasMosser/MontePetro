__author__ = 'lmosser'
import numpy as np
import scipy.stats as st


def random_number_from_truncated_normal_distribution(min=0.0, max=1.0, mean=0.5, std=1.0):
    normal = st.norm(mean, std)
    u = np.random.uniform(low=0.0, high=1.0)
    x = normal.ppf(normal.cdf(min) + u * (normal.cdf(max) - normal.cdf(min)))
    return x