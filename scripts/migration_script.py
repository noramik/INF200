import textwrap

from biosim.island import Island

geogr = """\
           WWWW
           WLWW
           WLHW
           WWWW"""
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

isle = Island(geogr, (ini_herbs+ ini_carns))

geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WLLLW
           WWWWW"""
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]

geogr = textwrap.dedent(geogr)
isle = Island(geogr, ini_herbs)

for _ in range(1):
    isle.handle_migration()
print([len(cell.herb_pop) for cell in isle.isle_map.values()])


