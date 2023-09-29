import textwrap
import matplotlib.pyplot as plt
from biosim.simulation import BioSim
from biosim.cell import Lowland
from biosim.animal import Herbivore

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]


sim = BioSim(geogr, ini_herbs, seed=1, cmax_animals={'Herbivore': 1000, 'Carnivore': 200})
sim.simulate(10)

sim.set_animal_parameters('Herbivore', {'mu': 40})

print(sim.num_animals_per_species)
plt.show()
