import statistics
import random

SEED = 100
random.seed(SEED)

from biosim.cell import Lowland, Water

ini_herbs = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]

ini_carns =[{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]

low = Lowland(ini_herbs)
'''
print([carn.fitness for carn in low.carn_pop])
print([herb.fitness for herb in low.herb_pop])
for _ in range(20):
    low.feeding_carnivores()

print([carn.weight for carn in low.carn_pop])


print([herb.weight for herb in low.herb_pop])
print([herb.fitness for herb in low.herb_pop])

for _ in range(30):
    low.feeding_herbs()
    low.feeding_carnivores()
    print(f'Year {_}: Herbivores: {low.herb_count()}')
    print(f'Year {_}: Carnivores: {low.carn_count()}')
    low.add_pop([{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}])
print([herb.age for herb in low.herb_pop])
print([herb.weight for herb in low.herb_pop])
print([herb.fitness for herb in low.herb_pop])
'''

w = Water(ini_carns+ini_herbs)

print(w.herb_pop)

w.add_pop(ini_carns)
print(w.carn_pop)