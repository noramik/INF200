import textwrap
from biosim.island import Island
import random

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
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]
h = []
c = []
for seed in range(100, 200):
    random.seed(seed)
    isle= Island(geogr, ini_herbs)
    isle.season(50)
    isle.add_pop(ini_carns)
    isle.season(250)
    h.append(isle.total_herb_count())
    c.append(isle.total_carn_count())

print(h)
print(c)