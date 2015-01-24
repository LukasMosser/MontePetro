=============================================
MontePetro
=============================================
Probabilistic Reserve Estimation in Python
=============================================
.. image:: https://api.travis-ci.org/z4r/python-coveralls.png?branch=master
    :target: http://travis-ci.org/LukasMosser/MontePetro
.. image:: https://coveralls.io/repos/LukasMosser/MontePetro/badge.png?branch=master
    :target: https://coveralls.io/r/LukasMosser/MontePetro?branch=master
.. image:: http://img.shields.io/pypi/dm/montepetro.svg?style=flat
        :target: https://pypi.python.org/pypi/montepetro/
.. image:: http://img.shields.io/pypi/v/montepetro.svg?style=flat
        :target: https://pypi.python.org/pypi/montepetro/
.. image:: http://img.shields.io/badge/license-GPL-blue.svg?style=flat
        :target: https://github.com/LukasMosser/MontePetro/blob/master/LICENSE

This package provides a library to perform basic monte carlo estimation of property distributions in native python.
The package was originaly intended to estimate oil and gas reserves in multi-regional domains
from petrophysical datasets, but can be applied to a variety of problems such as the example problems shown here.

An IPython Notebook showing the Libraries application to oil and gas reserve estimation can be found here.

Installation
==================
Using pip::

    $ pip install montepetro

This will install MontePetro from the Python Package Index.

Basic use of the MontePetro package
==================================
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

    ensemble_density = calcite_density*(1-porosity) + bone_fluid_density * porosity

The following code goes into detail on how we create the probability distributions and add them to our model.

.. code-block:: python

    #Define number of samples we want to take
    n = 10000

    #We pass the RandomProperty our functions from which we sample the probability distributions
    #Here we make use of the numpy libraries built in random number generators
    porosity = RandomProperty(name="Porosity", n=n, random_number_function=numpy.random.uniform)
    density_calcite = RandomProperty(name="Rho_Calc", n=n, random_number_function=numpy.random.triangular)
    density_bone_fluid = RandomProperty(name="Rho_Fluid", n=n, random_number_function=numpy.random.triangular)

    config = {"Inner Bone": {"Porosity": {"low": 0.0, "high": 0.2},
                             "Rho_Calc": {"left": 2.54, "right": 2.7, "mode": 2.58},
                             "Rho_Fluid": {"left": 1.01, "right": 1.5, "mode": 1.2}},
              "Outer Bone": {"Porosity": {"low": 0.1, "high": 0.2},
                           "Rho_Calc": {"left": 2.50, "right": 3.0, "mode": 2.8},
                           "Rho_Fluid": {"left": 1.1, "right": 1.3, "mode": 1.2}}}

    #Let's add these to the model.
    model.add_property(porosity)
    model.add_property(density_calcite)
    model.add_property(density_bone_fluid)

    #Some Model container magic! We add all these properties to the regions.
    model.add_defined_properties_to_regions()

    #We pass the model our configuration and run the model
    #This will generate all the sampled distributions for each region
    model.run(config)

We can now perform an operation on these values by accessing the values directly.

.. code-block:: python

    import matplotlib.pyplot as plot
    densities = []
    for region_name, region in model.regions.iteritems():
        porosity = region.properties["Porosity"].values
        rho_calc = region.properties["Rho_Calc"].values
        rho_bone_fluid = region.properties["Rho_Fluid"].values
        ensemble_density = rho_calc*(1-porosity)+rho_bone_fluid*porosity
        densities.append(ensemble_density)

    total_density = numpy.add(densities[0], densities[1])
    plot.hist(total_density, bins=500)
    plot.show()

This covers the basic functionality of MontePetro.
You can find the above example in the following ipython notebook `here
<http://nbviewer.ipython.org/gist/LukasMosser/c40fb62427ab0b966dca>`_.
An application to the estimation of oil and gas reserves using regional properties
is shown in this following ipython notebook `here
<http://nbviewer.ipython.org/gist/LukasMosser/0a1a4fd85c1ae54c0f85>`_

Citation
--------

To cite MontePetro in publications use::

    MontePetro Development Team (2015). MontePetro: Python library for probabilistic reserve estimates
    URL http://www.github.com/lukasmosser/MontePetro

A BibTeX entry for LaTeX users is::

    @Manual{,
    title = {MontePetro: Python library for probabilistic reserve estimates},
    author = {{MontePetro Development Team}},
    year = {2015},
    url = {http://www.github.com/lukasmosser/MontePetro},
    }

Copyright (C) <2015>  <Lukas Mosser>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


