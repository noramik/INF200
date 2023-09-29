import random
from biosim.cell import Lowland, Highland, Desert, Water
from biosim.animal import Carnivore

SEED = 101
random.seed(SEED)

herb_pop = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 40}
                      for _ in range(5)]

ini_carns =  [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(5)]
'''
print(herb_pop)

Carnivore.set_params({'DeltaPhiMax': 1.0})
low = Lowland(herb_pop)

w = Water()
#print(w.mating())

for _ in range(50):

    low.feeding_herbs()

    #print([herb.weight for herb in low.herb_pop])
    #print(len(low.herb_pop))

low.add_pop(ini_carns)
print(low.carn_pop)

for _ in range(50):
    low.feeding_carnivores()
    print([carn.weight for carn in low.carn_pop])
'''

low = Lowland(ini_pop=ini_carns+herb_pop)
print([herb for herb in low.herb_pop])
print([carn for carn in low.carn_pop])