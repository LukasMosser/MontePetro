=============================================
MontePetro - Probabilistic Reserves in Python
=============================================
.. image:: https://api.travis-ci.org/z4r/python-coveralls.png?branch=master
    :target: http://travis-ci.org/LukasMosser/MontePetro
.. image:: https://coveralls.io/repos/LukasMosser/MontePetro/badge.png?branch=master
    :target: https://coveralls.io/r/LukasMosser/MontePetro?branch=master

This package provides a library to do basic monte carlo reserve estimation
from petrophysical data in native python.
The library is mainly intended as an educational resource, but can be applied to a variety
of other monte carlo method applications

INSTALLING THE PKG
==================
Using pip::

    $ pip install montepetro


BASIC USAGE
=============


.. code-block:: python

    s = SeedGenerator(300)
    n = 10000
    model = Model("Simple Model", 666)

    area = RandomProperty(s, name="Area", n=n, random_number_function=np.random.uniform)
    porosity = RandomProperty(s, name="Porosity", n=n, random_number_function=np.random.triangular)
    sw = RandomProperty(s, name="Sw", n=n, random_number_function=np.random.triangular)

    config = {"Region A": {"Area": {"low": 100.0, "high": 1000.0},
                           "Porosity": {"left": 0.01, "right": 0.10, "mode": 0.05},
                           "Sw": {"left": 0.00, "right": 0.15, "mode": 0.05}},
              "Region B": {"Area": {"low": 20.0, "high": 200.0},
                           "Porosity": {"left": 0.05, "right": 0.15, "mode": 0.10},
                           "Sw": {"left": 0.00, "right": 0.20, "mode": 0.10}}}

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
        print region.properties["ooip"].values

    ooip = ModelOriginalOilInPlace(model)
    ooip.generate_values()
    plot.hist(ooip.values, bins=50)
    plot.show()


