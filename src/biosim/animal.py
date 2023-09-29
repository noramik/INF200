import random
import math


class Animal:
    """
    Animal class.

    Contains two subclasses: Herbivore and Carnivore.
    """
    w_birth = 0.0
    sigma_birth = 0.0
    beta = 0.0
    eta = 0.0
    a_half = 0.0
    phi_age = 0.0
    w_half = 0.0
    phi_weight = 0.0
    mu = 0.0
    gamma = 0.0
    zeta = 0.0
    xi = 0.0
    omega = 0.0
    F = 0.0
    DeltaPhiMax = None

    default_params = ({'w_birth': w_birth, 'sigma_birth': sigma_birth, 'beta': beta, 'eta': eta,
                       'a_half': a_half, 'phi_age': phi_age, 'w_half': w_half,
                       'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma, 'zeta': zeta, 'xi': xi,
                       'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax})

    @classmethod
    def set_params(cls, new_params):
        """
        Set class parameters

        Parameters
        ----------
        new_params : dict
            Legal keys: ({'w_birth', 'sigma_birth', 'beta', 'eta', 'a_half', 'phi_age', 'w_half',
                       'phi_weight', 'mu', 'gamma', 'zeta', 'xi', 'omega', 'F'})

        Raises
        -------
        ValueError, KeyError
        """
        valid_keys = [key for key in cls.default_params]

        for key, val in new_params.items():
            if key not in valid_keys:
                raise KeyError(f'This is not a valid key: {key}')
            if val < 0:
                raise ValueError(f'{key} can only be a strictly positive number')
            setattr(cls, key, val)

    def __init__(self, weight=8.0, age=0):
        """
        Parameters
        ----------
        weight : float
            The weight of the animal
        age : int
            The age of the animal
        """
        if weight >= 0:
            self.weight = weight
        else:
            raise ValueError('Weight must be positive number')
        if age >= 0:
            self.age = age
        else:
            raise ValueError(f'Age must be a positive number')
        self._fitness = None
        self.already_moved = False
        self.loc = None

    def _update_fitness(self):
        if self.weight <= 0:
            self._fitness = 0
        else:
            q_plus = 1/(1 + math.exp(self.phi_age * (self.age - self.a_half)))
            q_minus = 1/(1 + math.exp(-self.phi_weight * (self.weight - self.w_half)))
            self._fitness = q_plus*q_minus
        return self._fitness

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self._update_fitness()
        return self._fitness

    def ages(self):
        """
        Animal ages by one year.
        """
        self.age += 1
        self._update_fitness()

    def reset_moved(self):
        """
        Resets the already_moved attribute. The attribute exists to ensure that an animal can't
        move more than once per year.
        """
        self.already_moved = False

    def migrate(self):
        """
        Animal migrate once every year with probability :math:`{\mu \Phi}`.

        """

        if self.already_moved:
            return False
        else:
            p_migration = self.mu * self.fitness
            r = random.random()
            return r <= p_migration

    def set_loc(self, loc):
        """Sets the location of the animal as an attribute."""
        self.loc = loc

    def birth(self, n):
        """
        Animal gives birth with given probability if certain criteria are met. Newborn has an
        initial weight
        :math:`{w \sim \mathcal{N}(w_{birth},\,\sigma_{birth})}`
        the birth weight is drawn from a Gaussian distribution with mean :math:`w_{birth}`
        and standard deviation :math:`\sigma_{birth}`.

        Parameters
        ----------
        n : int
            Number of animals of same species in same location as Animal instance.

        Returns
        -------
            Animal instance or NoneType object
        """
        if self.weight > self.zeta*(self.w_birth + self.sigma_birth):
            norm_dist = random.gauss(self.w_birth, self.sigma_birth)
            nw = norm_dist if norm_dist > 0 else 0
            if self.weight > nw*self.xi:
                if random.random() < min(1.0, self.gamma*self.fitness*(n-1)):
                    self.weight = self.weight - self.xi * nw
                    return type(self)(nw)

    def _weight_gain(self, food_eaten=0.0):
        self.weight += self.beta * food_eaten
        self._update_fitness()

    def weight_loss(self):
        """Animal loses weight and decreases with :math:`{\eta w}`
        """
        self.weight = self.weight - self.eta * self.weight
        self._update_fitness()

    def death(self):
        """
        Decide whether animal dies. An animal dies for certain if  weight: :math:`{w =0}` or
        with probability :math:`{\omega (1- \Phi)}` if :math:`{w >0}` .

        Returns
        -------
        bool
            True if animal dies.
        """
        if self.weight == 0:
            return True
        else:
            return random.random() < self.omega*(1-self.fitness)


class Herbivore(Animal):
    """Subclass of Animal class."""

    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40.0
    phi_age = 0.6
    w_half = 10.0
    phi_weight = 0.1
    mu = 0.25
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10.0

    default_params = ({'w_birth': w_birth, 'sigma_birth': sigma_birth, 'beta': beta, 'eta': eta,
                       'a_half': a_half, 'phi_age': phi_age, 'w_half': w_half,
                       'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma, 'zeta': zeta, 'xi': xi,
                       'omega': omega, 'F': F})

    def feeds_herb(self, food_available=0.0):
        """
        A Herbivore eats an amount F of fodder and gains weight :math:`{\\beta F}`.

        Parameters
        ----------
        food_available: float
            food available in the cell
        """
        if food_available >= self.F:
            self._weight_gain(self.F)
        elif self.F < food_available > 0:
            self._weight_gain(food_available)


class Carnivore(Animal):
    """Subclass of Animal class."""
    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 40.0
    phi_age = 0.3
    w_half = 4.0
    phi_weight = 0.4
    mu = 0.4
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.8
    F = 50.0
    DeltaPhiMax = 10.0

    default_params = ({'w_birth': w_birth, 'sigma_birth': sigma_birth, 'beta': beta, 'eta': eta,
                       'a_half': a_half, 'phi_age': phi_age, 'w_half': w_half,
                       'phi_weight': phi_weight, 'mu': mu, 'gamma': gamma, 'zeta': zeta, 'xi': xi,
                       'omega': omega, 'F': F, 'DeltaPhiMax': DeltaPhiMax})

    def feeds_carn(self, h_fitness, h_weight):
        """
        Carnivore eats herbivore with given probability, and gains weight after eating by
        :math:`{\\beta w_{herb}}`. where :math:`w_{herb}` is the weight of herbivore killed.

        Parameters
        ----------
        h_fitness : float
            The fitness of the herbivore the carnivore wants to eat.
        h_weight : float
            The weight of the herbivore the carnivore wants to eat.
        """

        if self.fitness > h_fitness:
            if (self.fitness - h_fitness) < self.DeltaPhiMax:
                if random.random() < ((self.fitness - h_fitness)/self.DeltaPhiMax):
                    self._weight_gain(h_weight)
            else:
                self._weight_gain(h_weight)
