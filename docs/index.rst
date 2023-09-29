.. biosim documentation master file, created by
   sphinx-quickstart on Tue Jun  7 17:28:03 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BioSim's documentation!
==================================

BioSim is a package for population dynamics on an island. The package allows the user to simulate
and visualise the population dynamics between herbivores and carnivores on an island with four
different landscape types.

The key points:

* Contains two animal species: herbivores and carnivores.
* Contains four different landscapes: lowland, highland, desert and water.
* Herbivores eat fodder while carnivores eat and kill herbivores.
* Animals can move to a new cell once per year.
* Visualisation of population dynamics over time. Visualisation includes a line plot over total\
  number of animals per species, animal distributions, the island map and histograms of the \
  animals' fitness, weight and age.

.. toctree::
   :maxdepth: 5
   :caption: Contents:

   user_interface
   graphics
   animal
   cell
   island



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
