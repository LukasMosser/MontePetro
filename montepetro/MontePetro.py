#!/usr/bin/python
import sys
import getopt
import string
import random

from montepetro.models import Model


def main(argv):
    inputfile = ''
    visual = False
    verbose = False
    N = 0
    N_Bool = False
    Seed = 0
    Seed_Bool = False
    try:
        opts, args = getopt.getopt(argv, "hi:pvs:n:", ["ifile=", "plot=", "verbose=", "seed=", "number="])
    except getopt.GetoptError:
        print 'MontePetro.py -i <inputfile> -p <Visualisation> -v <Verbose> -s <Seed> -n <Number of Samples>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'MontePetro.py -i <inputfile> -p <Visualisation> -v <Verbose> -s <Seed> -n <Number of Samples>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-p", "--plot"):
            visual = True
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-s", "--seed"):
            Seed = int(arg)
            Seed_Bool = True
        elif opt in ("-n", "--number"):
            N = int(arg)
            N_Bool = True
        else:
            assert False, "unhandled option"
    config_module = __import__(inputfile)

    dump = config_module.Dump
    if N_Bool == False:
        N = config_module.N
    if not Seed_Bool:
        Seed = config_module.Seed

    Model_1 = Model(config_module.Model_Name, Seed, N, config_module.Parameter_Classes)
    Model_1.AddRegions(config_module.Regions)
    Model_1.CalculateOOIP()
    Model_1.DumpModel()
    Model_1.DumpTotalOOIP()


#
# if verbose:
# Model_1.PrintModelOutput()
#
# if visual:
# Model_1.PlotModelHistograms(25)
#
# if dump:
# Model_1.DumpModel()

def SeedGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


if (__name__ == "__main__"):
    main(sys.argv[1:])