from biosim.cell import Lowland
import statistics
seed = 100

ini_herbs = [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]

low = Lowland(ini_herbs)

num_herbs = []

print(low.f_max)

for _ in range(301):
    low.feeding_herbs()
    low.mating()
    low.aging()
    low.losing_weight()
    low.dying()
    print(low.herb_count())
