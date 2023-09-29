from biosim.cell import Lowland

ini_herbs = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]

low = Lowland(ini_herbs)

print([anim for anim in low.herb_pop])
print(low.species_dict)
low.remove_animal([anim for anim in low.herb_pop], 'Herbivore')
print([anim for anim in low.herb_pop])
print(low.species_dict)