from .animal import Herbivore, Carnivore
import random


class Cell:
    """
    Class representing one single square for the animals to live in.
    Contains four subclasses: Lowland, Highland, Desert and Water.

    Parameters
    ----------
    f_max : float
        Available fodder in the cell.
    """

    f_max = 0.0
    habitable = True

    default_params = {'f_max': f_max}

    @classmethod
    def set_land_params(cls, new_params):
        """
        Parameters
        ----------
        new_params : dict
            Legal keys = {'f_max'}

        Raises
        -------
        ValueError, KeyError
        """
        valid_key = ['f_max']
        for key, val in new_params.items():
            if key not in valid_key:
                raise KeyError(f'This is not a valid key: {key}')
            if val < 0:
                raise ValueError('f_max must be greater than or equal to 0')
            setattr(cls, key, val)

    def __init__(self, ini_pop=None):
        """

        Parameters
        ----------
        ini_pop: list of dictionaries
            The initial animal population.
        """
        self.herb_pop = []
        self.carn_pop = []
        if ini_pop is not None:
            for animal in ini_pop:
                if animal['species'] == 'Herbivore':
                    self.herb_pop.append(Herbivore(age=animal['age'], weight=animal['weight']))
                elif animal['species'] == 'Carnivore':
                    self.carn_pop.append(Carnivore(age=animal['age'], weight=animal['weight']))
        self.herb_migrating = []
        self.carn_migrating = []

    def aging(self):
        """All animals in the populations age by one year. """
        if self.habitable:
            for herb in self.herb_pop:
                herb.ages()
            for carn in self.carn_pop:
                carn.ages()

    def migrating(self):
        """
        Decide which animals can migrate.

        Returns
        -------
        herb_migrating : list
            List of herbivore objects wanting to migrate
        carn_migrating : list
            List of carnivore objects wanting to migrate
        """
        herb_migrating = [herb for herb in self.herb_pop if herb.migrate()]
        carn_migrating = [carn for carn in self.carn_pop if carn.migrate()]

        return herb_migrating, carn_migrating

    def move_to(self, herb_list=None, carn_list=None):
        """
        Animals moving to cell.

        Parameters
        ----------
        herb_list : list
            List of herbivore objects moving to the cell
        carn_list :
            List of carnivore objects moving to the cell
        """
        if herb_list is not None:
            self.herb_pop.extend([herb for herb in herb_list if herb.already_moved is False])
        if carn_list is not None:
            self.carn_pop.extend([carn for carn in carn_list if carn.already_moved is False])

    def remove_animal(self, h_pop=None, c_pop=None):
        """
        Animals that have migrated need to be removed from the population.

        Parameters
        ----------
        h_pop : list
            List of herbivore objects that have moved away from the cell
        c_pop : list
            List of carnivore objects that have moved away from the cell
        """
        if h_pop is not None:
            self.herb_pop = [herb for herb in self.herb_pop if herb not in h_pop]
        if c_pop is not None:
            self.carn_pop = [carn for carn in self.carn_pop if carn not in c_pop]

    def reset_moved(self):
        """Resets the animals having moved."""
        for herb in self.herb_pop:
            herb.reset_moved()
        for carn in self.carn_pop:
            carn.reset_moved()

    def set_loc(self, loc):
        """
        Sets the location of the populations.

        Parameters
        ----------
        loc : tuple
            The location of the animals
        """
        for herb in self.herb_pop:
            herb.set_loc(loc)
        for carn in self.carn_pop:
            carn.set_loc(loc)

    def mating(self):
        """The animals in the cell mate with given probability. New animals are born and appended
         to population lists."""
        if self.habitable:
            n = len(self.herb_pop)
            new_herbs = [nb for herb in self.herb_pop if (nb := herb.birth(n))]
            self.herb_pop.extend(new_herbs)

            n = len(self.carn_pop)
            new_carns = [nb for carn in self.carn_pop if (nb := carn.birth(n))]
            self.carn_pop.extend(new_carns)

    def feeding_herbs(self):
        """The herbivores in the cell feed in order of fitness. The fittest animals eat first."""
        if self.habitable:
            self.herb_pop.sort(key=lambda h: h.fitness, reverse=True)
            ([(ix, herb.feeds_herb(self.f_max - herb.F * ix)) for ix, herb in
              enumerate(self.herb_pop)])

    def feeding_carnivores(self):
        """
        The carnivores in the cell eat in random order. Each carnivore starts by trying to eat
        the least fit herbivore, then pass through the herbivore population until it has either
        eaten enough or until there are no more herbivores left to try to kill. Then the next
        carnivore tries to eat in the same way.
        """
        random.shuffle(self.carn_pop)
        self.herb_pop.sort(key=lambda h: h.fitness)
        if self.habitable:
            for carn in self.carn_pop:
                food_eaten = 0
                for herb in self.herb_pop:
                    if food_eaten < carn.F:
                        ini_weight = carn.weight
                        carn.feeds_carn(herb.fitness, min(herb.weight, Carnivore.F - food_eaten))
                        if carn.weight > ini_weight:
                            food_eaten += herb.weight
                            herb.weight = 0

    def losing_weight(self):
        """The animals in the populations lose weight."""
        if self.habitable:
            for herb in self.herb_pop:
                herb.weight_loss()
            for carn in self.carn_pop:
                carn.weight_loss()

    def dying(self):
        """ The animals in the populations die with given probabilities."""
        if self.habitable:
            self.herb_pop = [herb for herb in self.herb_pop if herb.death() is False]
            self.carn_pop = [car for car in self.carn_pop if car.death() is False]

    def herb_count(self):
        """
        Counts the number of herbivores in the cell.

        Returns
        -------
        num_herbs : int
            Number of herbivores in the cell
        """
        return len(self.herb_pop)

    def carn_count(self):
        """
        Counts the number of carnivores in the cell.

        Returns
        -------
        num_carns : int
            Number of carnivores in the cell
        """
        return len(self.carn_pop)

    def add_pop(self, pop=None):
        """
        Adds additional populations to the cell.

        Parameters
        ----------
        pop : list of dictionaries
            Additional animals to be added
        """
        if self.habitable:
            if pop is not None:
                new_herbs = ([Herbivore(animal['weight'], animal['age']) for animal in pop if
                             animal['species'] == 'Herbivore'])
                new_carns = ([Carnivore(animal['weight'], animal['age']) for animal in pop if
                             animal['species'] == 'Carnivore'])
                self.herb_pop.extend(new_herbs)
                self.carn_pop.extend(new_carns)


class Lowland(Cell):
    """Lowland type cell."""
    f_max = 800.0
    habitable = True

    default_params = {'f_max': f_max}


class Highland(Cell):
    """
    Highland type cell
    """
    f_max = 300.0
    habitable = True
    default_params = {'f_max': f_max}


class Desert(Cell):
    """
    Desert type cell.
    All methods from Cell class are available, except the herbivore population
    can't eat because there is no fodder present.
    """
    f_max = 0
    habitable = True
    default_params = {'f_max': f_max}

    def feeding_herbs(self):
        pass


class Water(Cell):
    """
    Water type cell.
    Water cell is an inactive cell, where no animals can live.
    """
    f_max = 0
    habitable = False
    default_params = {'f_max': f_max}

    def __init__(self, ini_pop):
        super().__init__()
        self.herb_pop = []
        self.carn_pop = []
