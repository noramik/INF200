import random
import textwrap
import matplotlib.pyplot as plt
import numpy as np

from biosim.graphics import Graphics
from biosim.island import Island



geogr = """\
            WWWWWWWWWWWWWWWWWWWWW
            WHHHHHLLLLWWLLLLLLLWW
            WHHHHHLLLLWWLLLLLLLWW
            WHHHHHLLLLWWLLLLLLLWW
            WWHHLLLLLLLWWLLLLLLLW
            WWHHLLLLLLLWWLLLLLLLW
            WWWWWWWWHWWWWLLLLLLLW
            WHHHHHLLLLWWLLLLLLLWW
            WHHHHHHHHHWWLLLLLLWWW
            WHHHHHDDDDDLLLLLLLWWW
            WHHHHHDDDDDLLLLLLLWWW
            WHHHHHDDDDDLLLLLLLWWW
            WHHHHHDDDDDWWLLLLLWWW
            WHHHHDDDDDDLLLLWWWWWW
            WWHHHHDDDDDDLWWWWWWWW
            WWHHHHDDDDDLLLWWWWWWW
            WHHHHHDDDDDLLLLLLLWWW
            WHHHHDDDDDDLLLLWWWWWW
            WWHHHHDDDDDLLLWWWWWWW
            WWWHHHHLLLLLLLWWWWWWW
            WWWHHHHHHWWWWWWWWWWWW
            WWWWWWWWWWWWWWWWWWWWW"""

ini_herbs = [{'loc': (10, 4),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (10, 4),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

geogr = textwrap.dedent(geogr)


gr = Graphics(r'C:\Users\Eier\inf200\biosim-u01-ilham-nora\data')
isle = Island(geogr, ini_herbs+ini_carns)
herb_line = []
carn_line = []
gr.setup(img_step= 1,final_step=10, ymax=200)
gr._update_island_map(geogr)
for _ in range(10):
    isle.season(1)
    herb_line.append(isle.total_herb_count())
    carn_line.append(isle.total_carn_count())
    gr._update_herb_line(isle.total_herb_count(), _)
    gr._update_carn_line(isle.total_carn_count(), _)
    gr._update_herb_fitness(isle.get_herb_fitness())
    gr._update_carn_fitness(isle.get_carn_fitness())
    gr._update_herb_age(isle.get_herb_age())
    gr._update_carn_age(isle.get_carn_age())
    gr._update_herb_weight(isle.get_herb_weight())
    gr._update_carn_weight(isle.get_carn_weight())
    herb_dist = [cell.herb_count() for cell in isle.isle_map.values()]
    carn_distr = [cell.carn_count() for cell in isle.isle_map.values()]
    herb_distr = np.reshape(herb_dist, (-1, 21))
    carn_distr = np.reshape(carn_distr, (-1, 21))
    gr._update_herb_distr(herb_distr)
    gr._update_carn_distr(carn_distr)
    gr._save_graphics(_)


plt.show()
gr.make_movie('mp4')

print(isle.total_herb_count())

'''
num_steps = 100
final_step = num_steps
gr.setup(img_step=10, final_step=final_step, ymax=300)
step = 0
vis_step = 1
while step < final_step:
    isle.season(1)
    step += 1
    herb_dist = [cell.herb_count() for cell in isle.isle_map.values()]
    carn_distr = [cell.carn_count() for cell in isle.isle_map.values()]
    cells = [cell for cell in isle.isle_map.values()]
    cells_herbpop = [cell.herb_pop for cell in cells]
    #herb_fitness = [herb.fitness for herb in cells_herbpop]
    #fitness = np.random.rand(1000)
    #fitness_c = np.random.rand(1000)
    herb_distr = np.reshape(herb_dist, (-1, 21))
    carn_distr = np.reshape(carn_distr, (-1, 21))
    if step % vis_step == 0:

        gr.update(step, step)
plt.show()'''
