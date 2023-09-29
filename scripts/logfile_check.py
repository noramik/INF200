from biosim.simulation import BioSim

import textwrap

geogr = """\
           WWW
           WLW
           WWW"""
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

for seed in range(100, 103):
    sim = BioSim(geogr, ini_herbs, seed=seed,
                 img_dir='results', img_base=f'mono_hc_{seed:05d}', img_years=300)
    sim.simulate(5)
    sim.add_population(ini_carns)
    sim.simulate(25)

