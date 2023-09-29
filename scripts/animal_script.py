from biosim.animal import Herbivore, Carnivore

herb_pop = [Herbivore(25, 5) for _ in range(50)]

#print(len([nb for herb in herb_pop if (nb := herb.birth())]))


herb = Herbivore(10, 5)

#herb.set_params({'zeta': 0.05})

#print(herb.birth(10))
#print(herb.weight)


c = Carnivore(1000, 2)
#print(c.fitness)
print(c.sigma_birth)
print(Carnivore.sigma_birth)