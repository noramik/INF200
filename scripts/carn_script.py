from biosim.animal import Carnivore


carn = Carnivore(30, 3)
carn.ages()
'''
for _ in range(10):
    print(carn.birth())

carn.weight_loss()
print(carn.weight)


print(Carnivore.DeltaPhiMax)

carn.feeds(10)
print(carn.weight)
for _ in range(20):
    carn.weight_loss()
    carn.ages()
print(carn.fitness, carn.weight)
'''
tup = (1, 2)

print(tup[0])