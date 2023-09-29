"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU
import random

from .island import Island
from .cell import Lowland, Highland, Desert, Water
from .animal import Herbivore, Carnivore
from .graphics import Graphics


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        random.seed(seed)
        lines = iter(island_map.splitlines())
        length = len(next(lines))
        if not all(len(line) == length for line in lines):
            raise ValueError('The rows of the island map must all be the same length.')

        self.isle = Island(island_map, ini_pop)
        self._num_animals = None
        self._animal_dict = None
        self._graphics = Graphics(self.isle, island_map, img_dir, img_base, img_fmt)
        self._vis_years = vis_years
        self._step = 0
        self._ymax_animals = ymax_animals
        self._year = 0
        self._img_years = img_years
        self._final_step = None
        self._cmax = cmax_animals
        self._hist_specs = hist_specs
        self._log_file = log_file

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        species_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        species_dict[species].set_params(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        cell_dict = {'L': Lowland, 'H': Highland, 'D': Desert, 'W': Water}
        cell_dict[landscape].set_land_params(params)

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        if self._img_years is None:
            self._img_years = self._vis_years

        if self._vis_years > 0 and self._img_years % self._vis_years != 0:
            raise ValueError('img_steps must be multiple of vis_steps')

        self._final_step = self._step + num_years
        self._graphics.setup(self._final_step, self._img_years, self._ymax_animals, self._cmax,
                             self._hist_specs)

        while self._step < self._final_step:
            self.isle.season()
            self._step += 1
            self._year += 1
            if self._vis_years > 0 and self._step % self._vis_years == 0:
                self._graphics.update(self._step, self._year)
                if self._log_file is not None:
                    with open(self._log_file, 'a') as logfile:
                        logfile.write(f'Year: {self.year}, Number of Animals: {self.num_animals}\n')

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.isle.add_pop(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        herb = self.isle.total_herb_count()
        carn = self.isle.total_carn_count()
        self._num_animals = herb + carn
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        self._animal_dict = ({'Herbivore': self.isle.total_herb_count(),
                             'Carnivore': self.isle.total_carn_count()})
        return self._animal_dict

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        self._graphics.make_movie()
