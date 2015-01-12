#!/usr/bin/env python
import scipy.stats
import matplotlib.pyplot as plot

from montepetro import generator


def CalculateTruncatedNormalPorosityParameters():
    sample4 = [0.0749, 0.0964, 0.0908, 0.1112, 0.098, 0.1371, 0.0999, 0.1053]  # Grainstone
    sample2 = [0.0748, 0.0961, 0.0674, 0.0871, 0.0919, 0.1059, 0.0914, 0.1262, 0.09, 0.0984]  # Wackstone
    sample1 = [0.0616, 0.0485, 0.0655, 0.0738, 0.0494, 0.0602]  # Mudstone
    sample3 = [0.0394]  # Packstone
    sample8 = [0.2324]  # Coarse Sandstone
    sample9 = [0.2284]  # Medium Sandstone
    sample10 = [0.213]  # Fine Sandstone
    sample11 = [0.3]  # Marls
    samples = {'mudstone': sample1, 'wackstone': sample2, 'packstone': sample3, 'grainstone': sample4,
               'coarse': sample8, 'medium': sample9, 'fine': sample10, 'marl': sample11}
    result = {}
    debug = True
    for sample in samples:
        a = 0.0
        b = 0.475
        na, nb, nloc, nscale = scipy.stats.truncnorm.fit(samples[sample], fa=0.0, fb=1.0)
        args = {'Distribution': "truncated_normal", 'Min': na, 'Max': nb, 'Mean': nloc, 'StdDev': nscale}
        print "Lower Bound: ", na
        print "Upper Bound: ", nb
        print "Location: ", nloc
        print "Scale: ", nscale
        # R = scipy.stats.truncnorm.rvs(na,nb,nloc,nscale,size=1000)
        gen = generator.RandomGeneratorDics(666, 10000)
        R = gen.GetRandomValues(args)
        plot.hist(R, 50)
        plot.xlabel("Values")
        plot.ylabel("Probability")
        plot.title("Porosity Truncated Normal Distribution Fit Test")
        plot.show()
        dic = {'a': na, 'b': nb, 'loc': nloc, 'scale': nscale}
        result[sample] = dic
    return result