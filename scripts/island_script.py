import textwrap

from biosim.island import Island

geogr = """\
        WWW
        WLW
        WWW"""
geogr = textwrap.dedent(geogr)



ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(5)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(5)]}]

#isle = Island(geogr, ini_herbs)


'''
isle.season(200)

for cell in isle.land_dict.values():
    print(cell.herb_pop)
    print(len(cell.herb_pop))


isle = Island(geogr, ini_herbs)
for _ in range(100):
    isle.season(1)
    print(isle.total_animal_count())

'''

#isle.season(301)
#print(isle.total_herb_count())

#print(ini_herbs+ini_carns)
isle = Island(geogr,ini_herbs+ini_carns)
print([len(cell.herb_pop) for cell in isle.isle_map.values()])
print([len(cell.carn_pop) for cell in isle.isle_map.values()])

print(isle.isle_map)

isle.add_pop(ini_carns)
print([len(cell.carn_pop) for cell in isle.isle_map.values()])