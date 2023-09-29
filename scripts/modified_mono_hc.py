import textwrap
from biosim.island import Island
from biosim.animal import Carnivore
import matplotlib.pyplot as plt
import statistics
import random

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)
Carnivore.set_params({'DeltaPhiMax': 0.05})
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]}]
''''
for seed in range(100, 103):
    random.seed(seed)
    sim = Island(geogr, ini_herbs)
    x = []
    y = []
    for _ in range(301):
        sim.season(1)
        #print(f'Year {_}: {sim.total_animal_count()}')
        x.append(_)
        y.append(sim.total_animal_count())

    print(statistics.mean(y[100:]), statistics.stdev(y[100:]))

    plt.plot(x, y)
    plt.show()
'''
Carnivore.set_params({'DeltaPhiMax': 0.05})
for seed in range(100, 110):
    random.seed(seed)
    sim = Island(geogr, ini_herbs)
    x = []
    y = []
    #print([cell.carn_pop for cell in sim.isle_map.values()])

    for _ in range(50):
        sim.season(1)
        x.append(_)
        y.append(sim.total_herb_count())


    #Carnivore.set_params({'DeltaPhiMax': 0.5})
    sim.add_pop(ini_carns)
    #print([cell.carn_pop for cell in sim.isle_map.values()])




    c = []
    yc = []
    for _ in range(250):
        sim.season(1)
        x.append(_+50)
        y.append(sim.total_herb_count())
        c.append(sim.total_carn_count())
        yc.append(_+50)
        print([carn.weight for carn in sim.isle_map[(2, 2)].carn_pop])

    plt.plot(x, y, label='herbs')
    plt.plot(yc, c, label='carns')
    plt.legend()
    plt.show()
