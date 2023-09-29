from biosim.island import Island
from biosim.cell import Lowland
from biosim.animal import Carnivore
import random
import textwrap
import matplotlib.pyplot as plt

geogr = """\
           L
           """

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (1, 1),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]
ini_carns = [{'loc': (1, 1),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

'''
isle = Island(geogr, ini_herbs)

isle.season(50)
isle.add_pop(ini_carns)
c = []
y = []
h =[]
print([carn for carn in isle.isle_map[(1, 1)].carn_pop])
for _ in range(100):
    isle.season(1)
    c.append(isle.total_carn_count())
    h.append(isle.total_herb_count())
    y.append(_)

    print([carn.weight for carn in isle.isle_map[(1, 1)].carn_pop])

plt.plot(y, c, label='carns')
plt.plot(y, h, label='herbs')
plt.legend()
plt.show()
'''
ini_carns = [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]

ini_herbs = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]

cell = Lowland(ini_herbs+ini_carns)
c = []
x = []
h =[]
for _ in range(50):
    cell.feeding_herbs()
    cell.feeding_carnivores()
    cell.mating()
    cell.aging()
    cell.losing_weight()
    cell.dying()
    c.append(cell.carn_count())
    h.append(cell.herb_count())
    x.append(_)

    print([carn.weight for carn in cell.carn_pop])

#print([carn.food_eaten for carn in cell.carn_pop])
#plt.plot(x, c, label='carns')
#plt.plot(x, h, label='herbs')
#plt.legend()
#plt.show()