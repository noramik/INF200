from collections import defaultdict
import random

from .cell import Lowland, Highland, Desert, Water


class Island:
    """
    Class representing the entire island.
    """
    cell_dict = {'W': Water, 'H': Highland, 'D': Desert, 'L': Lowland}

    def __init__(self, island_map, ini_pop=None):
        """

        Parameters
        ----------
        island_map : str
            Map of the island with a letter representing each cell.
            Legal letters: {'W', 'H', 'D', 'L'}
        ini_pop : list of dictionaries
            The initial population
        """
        self.isle_map = {}

        pop = defaultdict(list)
        if ini_pop is not None:
            for elm in ini_pop:
                pop[elm['loc']] += elm['pop']

        lines = [i.strip() for i in island_map.splitlines()]
        types = [list(j) for j in lines]

        is_edges_water = (types[0] + types[-1] + [c[0] for c in types[1:-1]] + [c[-1] for c in
                                                                                types[1:-1]])

        if is_edges_water.count('W') != len(is_edges_water):
            raise ValueError('Island is not surrounded by water')

        for i, row in enumerate(island_map.splitlines()):
            for j, col in enumerate(list(row)):
                if col in self.cell_dict:
                    self.isle_map[(i+1, j+1)] = self.cell_dict[col](pop.get((i+1, j+1)))
                else:
                    raise ValueError(f'This is not a valid landscape type: {col}')

    def _set_loc(self):
        """Sets the location of the animals. Helper method to handle_migration."""
        for loc, cell in self.isle_map.items():
            if cell.habitable:
                cell.set_loc(loc)

    def _move(self, moving_to_herb, moving_to_carn):
        """
        Moves the herbivore and carnivore instances to a new cell. Helper method to
        handle_migration.

        Parameters
        ----------
        moving_to_herb: dict
            Dictionary mapping lists of herbivore instances that should be moved to their new
            locations
        moving_to_carn
            Dictionary mapping lists of carnivore instances that should be moved to their new
            locations
        Returns
        -------
        remove_dict_herb : dict
            Dictionary mapping lists of herbivores that are to be removed from their previous
            location to their old cell.
        remove_dict_carn : dict
             Dictionary mapping lists of herbivores that are to be removed from their previous
            location to their old cell.
        """
        remove_dict_herb = {cell: [] for cell in self.isle_map.values()}
        remove_dict_carn = {cell: [] for cell in self.isle_map.values()}
        for new_loc, h_pop in moving_to_herb.items():
            if self.isle_map[new_loc].habitable:
                self.isle_map[new_loc].move_to(herb_list=h_pop)
                for herb in h_pop:
                    remove_dict_herb[self.isle_map[herb.loc]] += [herb]

        for new_loc, c_pop in moving_to_carn.items():
            if self.isle_map[new_loc].habitable:
                self.isle_map[new_loc].move_to(carn_list=c_pop)
                for carn in c_pop:
                    remove_dict_carn[self.isle_map[carn.loc]] += c_pop

        return remove_dict_herb, remove_dict_carn

    @staticmethod
    def _remove_herb(remove_dict_herb):
        """
        Removes herbivore instances from cells. Helper method to handle_migration.

        Parameters
        ----------
        remove_dict_herb : dict
            Dictionary mapping list of herbivore instances to the cells from which they should be
            removed.
        """
        for cell, h_pop in remove_dict_herb.items():
            if cell.habitable:
                cell.remove_animal(h_pop=h_pop)
                for herb in h_pop:
                    herb.already_moved = True

    @staticmethod
    def _remove_carn(remove_dict_carn):
        """
        Removes carnivore instances from cells. Helper method to handle_migration.

        Parameters
        ----------
        remove_dict_carn : dict
            Dictionary of carnivore instances to be removed
        """
        for cell, c_pop in remove_dict_carn.items():
            if cell.habitable:
                cell.remove_animal(c_pop=c_pop)
                for carn in c_pop:
                    carn.already_moved = True

    def handle_migration(self):
        """
        Animal migrates with given probability each year. An animal can only migrate to habitable
        cells. If an animal wants to migrate to a watertype cell, it remains put.
        """
        self._set_loc()
        self._reset_moved()
        moving_to_herb = {key: [] for key in self.isle_map}
        moving_to_carn = {key: [] for key in self.isle_map}
        for loc, cell in self.isle_map.items():
            if cell.habitable:
                herb_migr, carn_migr = cell.migrating()
                north = (loc[0] - 1, loc[1])
                south = (loc[0]+1, loc[1])
                west = (loc[0], loc[1]-1)
                east = (loc[0], loc[1]+1)
                for herb in herb_migr:
                    new_location = random.choice([west, east, north, south])
                    moving_to_herb[new_location] += [herb]
                for carn in carn_migr:
                    new_location = random.choice([west, east, north, south])
                    moving_to_carn[new_location] += [carn]

        self._set_loc()
        remove_herb, remove_carn = self._move(moving_to_herb, moving_to_carn)
        self._remove_herb(remove_herb)
        self._remove_carn(remove_carn)

    def _reset_moved(self):
        """Resets the animal having moved. Helper method to handle_migration"""
        for cell in self.isle_map.values():
            cell.reset_moved()

    def season(self):
        """
        Represents a year passing.
        """
        for cell in self.isle_map.values():
            if cell.habitable:
                cell.feeding_herbs()
                cell.feeding_carnivores()
                cell.mating()
        self.handle_migration()

        for cell in self.isle_map.values():
            if cell.habitable:
                cell.aging()
                cell.losing_weight()
                cell.dying()

    def total_herb_count(self):
        """
        Counts total amount of Herbivores across the whole island.

        Returns
        -------
        num : int
            number of herbivores
        """
        num = 0
        for cell in self.isle_map.values():
            try:
                num += cell.herb_count()
            except AttributeError:
                continue
        return num

    def total_carn_count(self):
        """
        Counts total amount of Carnivores across the whole island.

        Returns
        -------
        num : int
            number of carnivores
        """
        num = 0
        for cell in self.isle_map.values():
            try:
                num += cell.carn_count()
            except AttributeError:
                continue
        return num

    def add_pop(self, pop):
        """
        Add population to island.

        Parameters
        ----------
        pop : list of dictionaries
            The population to be added.
        """
        for pop_dict in pop:
            self.isle_map[pop_dict['loc']].add_pop(pop_dict['pop'])

    def get_herb_fitness(self):
        """
        Gets fitness for all herbivores in the cell.

        Returns
        -------
        fitness : list
            A list with all the herbivore's fitness.
        """
        fitness = []
        for cell in self.isle_map.values():
            fitness.extend([h.fitness for h in cell.herb_pop])
        return fitness

    def get_carn_fitness(self):
        """
        Gets fitness for all carnivores in the cell.

        Returns
        -------
        fitness : list
            A list with all the carnivores's fitness.
        """
        fitness = []
        for cell in self.isle_map.values():
            fitness.extend([c.fitness for c in cell.carn_pop])
        return fitness

    def get_herb_age(self):
        """
        Gets age for all herbivores in the cell.

        Returns
        -------
        age : list
            A list with all the herbivore's age.
        """
        age = []
        for cell in self.isle_map.values():
            age.extend([h.age for h in cell.herb_pop])
        return age

    def get_carn_age(self):
        """
        Gets age for all carnivores in the cell.

        Returns
        -------
        age : list
            A list with all the herbivore's age.
        """
        age = []
        for cell in self.isle_map.values():
            age.extend([c.age for c in cell.carn_pop])
        return age

    def get_herb_weight(self):
        """
        Gets weight for all herbivores in cell.

        Returns
        -------
        weight : list
            A list with all the herbivore's weight.
        """
        weight = []
        for cell in self.isle_map.values():
            weight.extend([h.weight for h in cell.herb_pop])
        return weight

    def get_carn_weight(self):
        """
        Gets weight for all carnivores in cell.

        Returns
        -------
        weight : list
            A list with all the herbivore's weight.
        """
        weight = []
        for cell in self.isle_map.values():
            weight.extend([c.weight for c in cell.carn_pop])
        return weight
