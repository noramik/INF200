import pytest
import scipy.stats as stats
import math
import random
import statistics

from biosim.animal import Herbivore, Carnivore

SEED = 12345678
alpha = 0.1


class TestCarnivore:
    @pytest.fixture(autouse=True)
    def create_carn(self):
        """Test if Carnivore instance can be created."""
        self.carn = Carnivore(30, 5)

    @pytest.fixture()
    def reset_carn_defaults(self):
        yield
        Carnivore.set_params(Carnivore.default_params)

    def test_carn_cls_attr(self):
        """
        Tests if Carnivore class attribute is set to default value.

        Note: This test passes in Pycharm, but fails in tox. Unclear why.
        """
        carn = Carnivore()
        assert carn.sigma_birth == 1.0

    def test_set_params_carn(self, reset_carn_defaults):
        """Tests if Carnivore parameters can be set."""
        Carnivore.set_params({'w_birth': 10.0})
        assert Carnivore.w_birth == 10.0

    def test_carn_feeds(self):
        """Tests if Carnivore object can eat."""
        carn = Carnivore(100, 5)
        for _ in range(100):
            carn.feeds_carn(0, 50)
        assert carn.weight > 100


@pytest.fixture()
def set_params_herbs(request):
    Herbivore.set_params(request.param)
    yield
    Herbivore.set_params(Herbivore.default_params)


@pytest.mark.parametrize('set_params_herbs', [{'w_birth': 10}], indirect=True)
def test_set_params_herb(set_params_herbs):
    """Tests if Herbivore parameters can be set."""
    assert Herbivore.w_birth == 10


def test_create_herb():
    """
    Test for creating a Herbivore object.
    """
    herb = Herbivore()
    assert herb.age == 0


def test_fitness_attr():
    """
    Tests if the fitness attribute is calculated correctly.
    """
    herb = Herbivore(Herbivore.w_half, Herbivore.a_half)
    # If weight = w_half and age = a_half, the fitness of the herbivore will be 1/2*1/2 = 1/4
    assert herb.fitness == 0.25


def test_ages():
    """
    Test for ages method.
    """
    herb = Herbivore()
    n = 100
    for i in range(n):
        herb.ages()
        assert herb.age == i + 1


@pytest.mark.parametrize('set_params_herbs', [{'zeta': 1.0, 'w_birth': 10.0, 'sigma_birth': 2.0}],
                         indirect=True)
def test_no_birth(set_params_herbs):
    """
    Deterministic test of birth method, where the herbivore should never give birth.
    Animal won't give birth if the weight is less than zeta*(w_birth+sigma_birth)
    """
    weight = 1.0*(10.0+2.0)
    herb = Herbivore(weight)
    n = 50
    for _ in range(n):
        assert herb.birth(100) is None


def test_birth():
    """
    Deterministic test of birth method, where the herbivore should always give birth.
    """
    herb = Herbivore(weight=40)
    assert herb.birth(100) is not None


def test_weight_attr():
    """
    Test to verify that weight can't be set to less than 0.
    Regression test.
    """
    with pytest.raises(ValueError):
        Herbivore(-3)


@pytest.mark.parametrize('set_params_herbs', [{'gamma': 10.0, 'zeta': 0.0}], indirect=True)
def test_birth_lose_weight(set_params_herbs):
    """
    Test to verify that the animal loses weight when giving birth.

    Regression test.
    """
    herb = Herbivore(50)
    ini_weight = herb.weight
    herb.birth(100)
    assert herb.weight < ini_weight


# noinspection PyPep8Naming
def test_birthweight():
    """
    Tests if the birthweight of the herbivore follows a Gaussian distribution, with mean w_birth.
    If test passes null hypothesis is true

    H0: Observed mean = w_birth
    HA: Observed mean != w_birth
    """
    random.seed(SEED)
    herb_pop = [Herbivore(400, 5) for _ in range(100)]
    n = 200
    newborns = [nb.weight for herb in herb_pop if (nb := herb.birth(n))]
    mu = Herbivore.w_birth
    sigma = Herbivore.sigma_birth
    mean = statistics.mean(newborns)
    Z = (mean-mu)/sigma
    p_val = 2 * stats.norm.cdf(-abs(Z))
    assert p_val > alpha


def test_feeds():
    herb = Herbivore(10, 2)
    ini_weight = herb.weight
    herb.feeds_herb(10)
    assert herb.weight > ini_weight


def test_feeds_gains_weight():
    """Tests if herbivore gains weight when eating food."""
    herb = Herbivore(5)
    herb.feeds_herb(10)
    new_weight = 5 + 0.9*10  # current_weight + beta*F
    assert herb.weight == new_weight


def test_weight_loss():
    """
    Tests if the weight_loss method works. If it works, the animal should weigh less after the
    method is called.
    """
    herb = Herbivore(30, 5)
    ini_weight = herb.weight
    herb.weight_loss()
    assert herb.weight < ini_weight


def test_certain_death():
    """
    Deterministic test of death method, where the herbivore should always die.
    """
    herb = Herbivore(weight=0)
    n = 100
    for n in range(n):
        assert herb.death()


# noinspection PyPep8Naming
def test_dies_stats():
    """
    Statistical test of death method.
    """
    random.seed(SEED)
    num_tries = 100
    herb = Herbivore(Herbivore.w_half, Herbivore.a_half)
    p = herb.omega*(1-herb.fitness)
    num_survivors = sum(herb.death() for _ in range(num_tries))
    mean = num_tries*p
    std = math.sqrt(num_tries*p*(1 - p))
    Z = (num_survivors - mean)/std
    p_val = 2*stats.norm.cdf(-abs(Z))
    assert p_val > alpha


# noinspection PyPep8Naming
@pytest.mark.parametrize('set_params_herbs', [{'mu': 1.0}], indirect=True)
def test_migrate(set_params_herbs):
    """
    Statistical test of migrate method. If test passes the null hypothesis is true.

    H0: Observed number of animals migrating is equal to expected number.
        Since mu is set to 1, the probability of migrating is equal to the animals fitness.
        That means the number of animals expected to migrate is num*p
    HA: Observed number of animals migrating is different from the number we expected.
    """
    random.seed(SEED)
    num = 100
    herb = Herbivore(40, 5)
    p = herb.fitness
    num_migrate = sum(herb.migrate() for _ in range(num))
    expected = num*p
    std = math.sqrt(num*p*(1 - p))
    Z = (num_migrate - expected)/std
    p_val = 2 * stats.norm.cdf(-abs(Z))
    assert p_val > alpha
