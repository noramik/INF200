from biosim.simulation import BioSim
from biosim.animal import Herbivore
import textwrap

geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WLLLW
           WWWWW"""
geogr = textwrap.dedent(geogr)

Herbivore.set_params({'mu': 1.9})
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 2000}
                      for _ in range(1000]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

sim = BioSim(geogr, ini_herbs)

