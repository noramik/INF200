import scipy.stats as stats
import random

import pytest
from biosim.island import Island
from biosim.cell import Cell
from biosim.animal import Herbivore, Carnivore
import textwrap

SEED = 1234567
alpha = 0.1
geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)
num_herbs = 10
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(num_herbs)]}]
num_carns = 5
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(num_carns)]}]


def test_create():
    isle = Island(geogr, ini_carns)
    assert isle.total_carn_count() == num_carns


def test_season(mocker):
    """
    Tests if season method works, by checking if season calls on aging method in Cell class the
    expected number of times.
    """
    isle = Island(island_map=geogr, ini_pop=ini_herbs)
    mocker.spy(Cell, 'aging')
    years = 10
    for _ in range(years):
        isle.season()
    assert Cell.aging.call_count == years


def test_empty():
    """
    Tests if an 'empty' island can be created.
    """
    island = Island(island_map="W")
    assert island.total_herb_count() == 0


def test_add_pop():
    """Tests if add_pop method works as expected."""
    island = Island(island_map=geogr, ini_pop=ini_herbs)
    island.add_pop(ini_carns)
    assert island.total_carn_count() == num_carns


def test_multi_pop():
    """
    Tests if both herbivores and carnivores can be added at the same time.
    """
    land = Island(island_map=geogr, ini_pop=ini_herbs + ini_carns)
    assert land.total_herb_count() == num_herbs


def test_add_pop_water():
    """
    Test to check that populations can't be added to Water cells.
    """
    new_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(num_herbs)]}]
    isle = Island(island_map=geogr, ini_pop=ini_herbs)
    isle.add_pop(new_herbs)
    assert isle.total_herb_count() == num_herbs


@pytest.fixture
def set_herb_params(request):
    Herbivore.set_params(request.param)
    yield
    Herbivore.set_params(Herbivore.default_params)


@pytest.mark.parametrize('set_herb_params', [{'mu': 1.0}], indirect=True)
def test_handle_migration(set_herb_params):
    """
    Statistical test of handle_migration method using chi-square. We set mu to 1.0, and set weight
    very large to get the animals' fitness as close to 1 as possible. Then we know that the animals
    will migrate in almost every case.

    H0: The observed number of migrants is as expected, only differences due to natural variation.
    HA: The observed number of migrants isn't as expected.

    If the test passes, that means the null hypothesis is true.
    """
    random.seed(SEED)
    geo = """\
               WWWWW
               WLLLW
               WLLLW
               WLLLW
               WWWWW"""
    herbs = [{'loc': (3, 3),
             'pop': [{'species': 'Herbivore',
                     'age': 5,
                      'weight': 2000}
                     for _ in range(1000)]}]
    north = (2, 3)
    west = (3, 2)
    east = (3, 4)
    south = (4, 3)

    geo = textwrap.dedent(geo)
    isle = Island(geo, herbs)
    isle.handle_migration()
    expected = 250
    observed = [isle.isle_map[north].herb_count(), isle.isle_map[west].herb_count(),
                isle.isle_map[east].herb_count(), isle.isle_map[south].herb_count()]
    chi_square = 0
    for obs in observed:
        chi_square += (obs - expected)**2/expected

    df = 4
    p = 1 - stats.chi2.cdf(chi_square, df)
    assert p > alpha


def test_remove_animal():
    """Tests if carnivores are being removed from the cell when _remove_carn method is called"""
    geo = """\
               WWWWW
               WLLLW
               WLLLW
               WLLLW
               WWWWW"""
    geo = textwrap.dedent(geo)
    isle = Island(geo, ini_herbs+ini_carns)
    carn_pop = isle.isle_map[(2, 2)].carn_pop
    cell = isle.isle_map[(2, 2)]
    isle._remove_carn({cell: carn_pop})
    assert len(cell.carn_pop) == 0


def test_edges():
    """Tests if having non-water cell as the edge raises a ValueError."""
    geo = """\
               WLW
               WWW
               WWW"""
    geo = textwrap.dedent(geo)
    with pytest.raises(ValueError):
        Island(geo)


def test_get_weight_herb():
    """
    Test if the weight list is returned correctly from the function get_herb_weight() in Island
    class.
    """
    isle = Island(island_map=geogr, ini_pop=ini_herbs)
    weight = isle.get_herb_weight()
    ref_weight = [h['weight'] for h in ini_herbs[0]['pop']]
    assert weight == ref_weight


def test_get_weight_carn():
    """
    Test if the weight list is returned correctly from the function get_carn_weight() in Island
    class
    """
    isle = Island(island_map=geogr, ini_pop=ini_carns)
    weight = isle.get_carn_weight()
    ref_weight = [c['weight'] for c in ini_carns[0]['pop']]
    assert weight == ref_weight


def test_get_age_herb():
    """
    Test if the age list is returned correctly from the function get_herb_age() in Island class.
    """
    isle = Island(island_map=geogr, ini_pop=ini_herbs)
    age = isle.get_herb_age()
    ref_age = [h['age'] for h in ini_herbs[0]['pop']]
    assert age == ref_age


def test_get_age_carn():
    """
    Test if the age list is returned correctly from the function get_carn_age() in Island class
    """
    isle = Island(island_map=geogr, ini_pop=ini_carns)
    age = isle.get_carn_age()
    ref_age = [c['age'] for c in ini_carns[0]['pop']]
    assert age == ref_age


def test_get_herb_fitness():
    """
    Test if the fitness list is returned correctly from the function get_herb_fitness() in
    Island class
    """
    isle = Island(island_map=geogr, ini_pop=ini_herbs)
    fitness = isle.get_herb_fitness()
    ref_fitness = [Herbivore(h['weight'], h['age']).fitness for h in ini_herbs[0]['pop']]
    assert fitness == ref_fitness


def test_get_carn_fitness():
    """
    Test if the fitness list is returned correctly from the function get_carn_fitness() in Island
    class.
    """
    isle = Island(island_map=geogr, ini_pop=ini_carns)
    fitness = isle.get_carn_fitness()
    ref_fitness = [Carnivore(c['weight'], c['age']).fitness for c in ini_carns[0]['pop']]
    assert fitness == ref_fitness
