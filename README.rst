=============================================
MontePetro - Probabilistic Reserves in Python
=============================================
.. image:: https://api.travis-ci.org/z4r/python-coveralls.png?branch=master
    :target: http://travis-ci.org/LukasMosser/MontePetro
.. image:: https://coveralls.io/repos/LukasMosser/MontePetro/badge.png?branch=master
    :target: https://coveralls.io/r/LukasMosser/MontePetro?branch=master

This package provides a library to perform basic monte carlo reserve estimation
from petrophysical data in native python.
The library is mainly intended as an educational resource, but can be applied to a variety
of other monte carlo method applications

INSTALLING THE PKG
==================
Using pip::

    $ pip install montepetro


BASIC USAGE
=============
MontePetro allows to create single and multi-region monte carlo estimates of parameter distributions.
The basic container for all regions is provided by the model class.

.. code-block:: python
    from montepetro.models import Model
    seed = 300
    model = Model("A simple Model", seed)

The model contains regions as well as properties.
It also handles the generation of seed values for all the regional property distributions.
See the Model class documentation for more information.

Regions in MontePetro contain all of the properties of the model
and have their own distributional properties e.g. two different types of bone structure
in a larger bone could be modeled as two regions in a model.

We can perform calculations on the regions themselves or we can pass them to a model
structure and let the model do all the hard work for us!

.. code-block:: python
    from montepetro.regions import Region
    region_a = Region(name="Inner Bone")
    region_b = Region(name="Outer Bone")

    #For simplicity let's add these to our model
    model.add_region(region_a)
    model.add_region(region_b)

MontePetro already comes with a number of properties types that we can define for our model.
RandomProperties are computed contain sets of values that we can sample from probability distributions.
RegionalProperties are properties that we want to calculate based on the defined properties of our model.

For our bone example me way want to estimate the ensemble distribution of the density of the bone.
We define a simple model for the ensemble density of the bone to be:

                Density_Calcite*(1-Porosity)+Density_Bone_Fluid*Porosity

The following code goes into detail on how we create the probability distributions and add them to our model.

.. code-block:: python

    from montepetro.properties import RandomProperty
    import numpy
    #We need a dummy seed generator to initialize the properties, but once we add them to the model
    #The seed of the model will govern the properties behavior.
    s = SeedGenerator(300)

    #Define number of samples we want to take
    n = 10000

    #We pass the RandomProperty our functions from which we sample the probability distributions
    #Here we make use of the numpy libraries built in random number generators
    porosity = RandomProperty(s, name="Porosity", n=n, random_number_function=numpy.random.uniform)
    density_calcite = RandomProperty(s, name="Rho_Calc", n=n, random_number_function=numpy.random.uniform)
    density_bone_fluid = RandomProperty(s, name="Rho_Fluid", n=n, random_number_function=numpy.random.triangular)

    config = {"Inner Bone": {"Porosity": {"low": 0.0, "high": 0.2},
                             "Rho_Calc": {"left": 2.54, "right": 2.7, "mode": 2.58},
                             "Rho_Fluid": {"left": 1.01, "right": 1.5, "mode": 1.2}},
              "Outer Bone": {"Porosity": {"low": 0.1, "high": 0.3},
                           "Rho_Calc": {"left": 2.54, "right": 2.7, "mode": 2.58},
                           "Rho_Fluid": {"left": 1.1, "right": 1.3, "mode": 1.2}}}

    #Let's add these to the model.
    model.add_property(area)
    model.add_property(porosity)
    model.add_property(sw)

    #Some Model container magic! We add all these properties to the regions.
    model.add_defined_properties_to_regions()

    #We pass the model our configuration and run the model
    #This will generate all the sampled distributions for each region
    model.run(config)

We can now perform an operation on these values by creating accessing the values directly.

.. code-block:: python
    for region_name, region in model.regions.iteritems():
        porosity = region.properties["Porosity"].values
        rho_calc = region.properties["Rho_Calc"].values
        rho_bone_fluid = region.properties["Rho_Fluid"].values
        ensemble_density = rho_calc*(1-porosity)+rho_bone_fluid*porosity

        #And we can plot these values of course for our example.
        plot.hist(ensemble_density, bins=50)
    plot.show()

This covers the basic functionality of MontePetro.
You can find the above example in the following ipython notebook.
An application to the estimation of oil and gas reserves using regional properties
is shown in this following ipython notebook.


