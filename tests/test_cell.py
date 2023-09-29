import pytest
import random
import math
import scipy.stats as stats

from biosim.cell import Cell, Lowland, Highland, Desert, Water
from biosim.animal import Herbivore, Carnivore
HERBIVORE_DEFAULT_WEIGHT = 50
ini_pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': HERBIVORE_DEFAULT_WEIGHT}
           for _ in range(50)]

SEED = 1234567
alpha = 0.1


@pytest.fixture()
def set_params_carn(request):
    Carnivore.set_params(request.param)
    yield
    Carnivore.set_params(Herbivore.default_params)


@pytest.fixture()
def set_params_low(request):
    Lowland.set_land_params(request.param)
    yield
    Lowland.set_land_params(Lowland.default_params)


@pytest.mark.parametrize('set_params_low', [{'f_max': 600.0}], indirect=True)
def test_set_landscape_params(set_params_low):
    """Tests if landscape parameters can be set."""
    assert Lowland.f_max == 600.0


@pytest.mark.parametrize('cell, expected_fmax, expected_herb ', [
    (Lowland(ini_pop), 800.0, 50),
    (Highland(ini_pop), 300.0, 50),
    (Desert(ini_pop), 0.0, 50),
    (Water(ini_pop), 0.0,  0)

])
def test_create_herb(cell, expected_fmax, expected_herb):
    """
    Testing if a Cell object can be created
    :return:
    """
    assert cell.f_max == expected_fmax
    assert cell.herb_count() == expected_herb


@pytest.mark.parametrize('cell, expected_carn ', [
    (Lowland(ini_pop), 0),
    (Highland(ini_pop), 0),
    (Desert(ini_pop),  0),
    (Water(ini_pop),  0)
])
def test_create_carn(cell, expected_carn):
    """
    Testing if a Cell object can be created
    :return:
    """
    assert cell.carn_count() == expected_carn


def test_aging_herb():
    """
    Test of aging method.
    :return:
    """
    h = Cell(ini_pop)
    h.aging()
    for herb in h.herb_pop:
        assert herb.age == 6


def test_aging_carn():
    """
    Test of aging method.
    :return:
    """
    c = Cell(ini_pop)
    c.aging()
    for carn in c.carn_pop:
        assert carn.age == 6


@pytest.mark.parametrize('cell ', [
    (Lowland(ini_pop)),
    (Highland(ini_pop)),
    (Desert(ini_pop))

])
def test_mating_herb(cell):
    """
    This tests whether mating method works. Since it is very unlikely that no herbivores are born
    if the mating method runs a hundred times, we check for length of herb_pop list before and
    after.
    """
    random.seed(SEED)
    num = 100
    pop_before = cell.herb_count()
    for _ in range(num):
        cell.mating()
    assert cell.herb_count() > pop_before


CARNIVORE_DEFAULT_WEIGHT = 50


ini_carns = [{'species': 'Carnivore',
             'age': 5,
              'weight': CARNIVORE_DEFAULT_WEIGHT}
             for _ in range(50)]


@pytest.mark.parametrize('cell ', [
    (Lowland(ini_carns)),
    (Highland(ini_carns)),
    (Desert(ini_carns))

])
def test_mating_carn(cell):
    """
    This tests whether mating method works. Since it is very unlikely that no herbivores are born
    if the mating method runs a hundred times, we check for length of herb_pop list before and
    after.
    """
    random.seed(SEED)
    num = 100
    pop_before = cell.carn_count()
    for _ in range(num):
        cell.mating()
    assert cell.carn_count() > pop_before


HERBIVORE_DEFAULT_WEIGHT = 20

ini_pop_alone = [{'species': 'Herbivore',
                  'age': 5,
                  'weight': HERBIVORE_DEFAULT_WEIGHT}]
ini_pop_many = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': HERBIVORE_DEFAULT_WEIGHT}
                for _ in range(200)]


@pytest.mark.parametrize('cell, expected_feeding', [
    (Lowland(ini_pop_many), 80),
    (Highland(ini_pop_many), 30),
    (Desert(ini_pop_many), 0),
    (Lowland(ini_pop_alone), 1),
    (Highland(ini_pop_alone), 1),
    (Desert(ini_pop_alone), 0)
])
def test_feeding_herb(cell, expected_feeding):
    """
    Test to see if food is being eaten
    """

    cell.feeding_herbs()
    count_feeding = [herb.weight > HERBIVORE_DEFAULT_WEIGHT for herb in cell.herb_pop].count(True)
    assert count_feeding == expected_feeding


@pytest.mark.parametrize('set_params_carn', [{'DeltaPhiMax': 1.0, 'F': 10000, 'beta': 1.0}],
                         indirect=True)
def test_feeding_carns_stats(set_params_carn):
    """
    Statistical test of feeding_carnivores method.
    With these parameters the carnivore should eat 3/4 of the herbivores.

    H0: The carnivore eats 3/4 of the herbivore population
    HA: The herbivore doesn't eat 3/4 of the herbivore population

    If the test passes, the null hypothesis is true.
    """
    num = 100
    ini_herbs = [{'species': 'Herbivore',
                 'age': Herbivore.a_half,
                  'weight': Herbivore.w_half}
                 for _ in range(num)]
    # The herbivores' fitness will be 1/4 for these values
    ini_carn = [{'species': 'Carnivore',
                'age': 2,
                 'weight': 1000}]
    # With this age and weight the carnivore's fitness will be very close to 1.
    low = Lowland(ini_herbs+ini_carn)
    low.feeding_carnivores()
    # If the herbivore is eaten its weight will be set to 0.
    herbs_killed = len([herb for herb in low.herb_pop if herb.weight == 0])
    expected = 75
    p = 3/4
    std = math.sqrt(num*p*(1 - p))
    z1 = (herbs_killed - expected)/std
    p_val = 2 * stats.norm.cdf(-abs(z1))
    assert p_val > alpha


def test_losing_weight():
    """
    Test that checks if animals actually lose weight.
    """
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 30}
           for _ in range(10)]
    l_cell = Lowland(pop)
    ini_weights = [herb.weight for herb in l_cell.herb_pop]
    l_cell.losing_weight()
    weight_after = [herb.weight for herb in l_cell.herb_pop]
    assert all([w_a < w_b for w_a in weight_after for w_b in ini_weights])


def test_dying():
    pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(50)]
    n = 10
    cell = Cell(pop)
    ini_count = len(cell.herb_pop)
    for _ in range(n):
        cell.dying()

    assert len(cell.herb_pop) < ini_count


def test_add_pop():
    """Test for add_pop method."""
    pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(50)]
    high = Highland(pop)
    ini_count = len(high.herb_pop)
    high.add_pop(pop)
    assert len(high.herb_pop) == 2*ini_count


def test_migrating():
    """Test to check that migrating method works, and it returns a list with animals wanting to
    migrate."""
    random.seed(SEED)
    pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(500)]
    low = Lowland(pop)
    herb_migr, carn_migr = low.migrating()
    assert len(herb_migr) != 0


def test_move_to():
    """Tests whether animal objects can be moved to cell."""
    random.seed(SEED)
    n = 10
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(n)]
    low = Lowland(pop)
    new_carns = [Carnivore(20, 5) for _ in range(n)]
    low.move_to(carn_list=new_carns)
    assert len(low.carn_pop) == 2*n


def test_remove_animal():
    """Tests if animal objects can be removed from cells."""
    random.seed(SEED)
    n = 10
    pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(n)]
    low = Lowland(pop)
    herbs_migr = [herb for herb in low.herb_pop]
    low.remove_animal(herbs_migr)
    assert len(low.herb_pop) == 0
