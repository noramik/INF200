"""
This module is based on randvis.graphics

url: (https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/blob/main/june_block/\
examples/randvis_project/src/randvis/graphics.py)

Some parts of the module are based on plotting example.

url: (https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/tree/main/june_block/\
examples/plotting)

:mod:`biosim.graphics` provides graphics support for BioSim.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for BioSim."""

    def __init__(self, island, geogr, img_dir=None, img_name=None, img_fmt=None):
        """
        Parameters
        ----------
        island : instance
            An Island instance
        geogr : str
            multiline string specifying the map layout
        img_dir : str
            directory for image files; no images if None
        img_name : str
            beginning of name for image files
        img_fmt : str
            image file format suffix
        """
        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._herb_img_axis = None
        self._carn_img_axis = None
        self._mean_ax = None
        self._mean_line = None
        self._pop_ax = None
        self._herb_line = None
        self._carn_line = None
        self._herb_distr_ax = None
        self._carn_distr_ax = None
        self._fitness_ax = None
        self._age_ax = None
        self._weight_ax = None
        self._axt = None
        self._txt = None
        self._fitness_hist_herb = None
        self._fitness_hist_carn = None
        self._age_hist_herb = None
        self._age_hist_carn = None
        self._weight_hist_herb = None
        self._weight_hist_carn = None
        self._spec = None
        self._island = island
        self._geogr = geogr
        self._cmax = None
        self._ymax = None
        self._hist_specs = None
        self._final_step = None

    def update(self, step, year):
        """
        Updates graphics with current data and save to file if necessary.
        Parameters
        ----------
        step : int
            current timestep
        year : int
            current year
        """

        herb_distr = [cell.herb_count() for cell in self._island.isle_map.values()]
        map_dims = ((len(self._geogr.splitlines())), len(list(self._geogr.splitlines()[0])))
        herb_distr = np.reshape(herb_distr, map_dims)
        carn_distr = [cell.carn_count() for cell in self._island.isle_map.values()]
        carn_distr = np.reshape(carn_distr, map_dims)
        self._update_island_map(self._geogr)
        self._update_animal_lines(self._island.total_herb_count(), self._island.total_carn_count(),
                                  step)
        self._update_herb_distr(herb_distr)
        self._update_carn_distr(carn_distr)
        self._update_year(year)
        self._update_fitness(self._island.get_herb_fitness(), self._island.get_carn_fitness())
        self._update_age(self._island.get_herb_age(), self._island.get_carn_age())
        self._update_weight(self._island.get_herb_weight(), self._island.get_carn_weight())
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(step)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_step=0, img_step=0, ymax=None, cmax=None, hist_specs=None):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        Parameters
        ----------
        final_step : int
            last time step to be visualised (upper limit of x-axis)
        img_step : int
            interval between saving image to file
        ymax : int
            limit of y-axis for Animal Count plot
        cmax : dict
            Dict specifying color-code limits for animal densities
        hist_specs: dict
            Specifications for histograms.
        """

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()
            self._spec = gridspec.GridSpec(ncols=3, nrows=3,
                                           width_ratios=[1, 1, 1], wspace=0.5,
                                           hspace=0.5, height_ratios=[2, 2, 1])

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(self._spec[0])
            self._map_ax.set_title('Island', fontsize='small')
            self._map_ax.locator_params(nbins=5)
            self._img_axis = None

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(self._spec[2])
            self._pop_ax.set_title('Animal count', fontsize='small')
            self._pop_ax.locator_params(nbins=5)
            if ymax is None:
                self._ymax = 500
                self._pop_ax.set_ylim(0, self._ymax)
            else:
                self._pop_ax.set_ylim(0, ymax)
            self._pop_ax.set_xlim(0, final_step + 1)

        if self._herb_line is None:
            herb_plot = self._pop_ax.plot(np.arange(0, final_step + 1),
                                          np.full(final_step + 1, np.nan))
            self._herb_line = herb_plot[0]
        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._carn_line is None:
            carn_plot = self._pop_ax.plot(np.arange(0, final_step + 1),
                                          np.full(final_step + 1, np.nan))
            self._carn_line = carn_plot[0]
        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._herb_distr_ax is None:
            self._herb_distr_ax = self._fig.add_subplot(self._spec[3])
            self._herb_distr_ax.set_title('Herbivore distribution', fontsize='small')
            self._herb_distr_ax.locator_params(nbins=5)
            self._herb_img_axis = None

        if self._carn_distr_ax is None:
            self._carn_distr_ax = self._fig.add_subplot(self._spec[5])
            self._carn_distr_ax.set_title('Carnivore distribution', fontsize='small')
            self._carn_distr_ax.locator_params(nbins=5)
            self._carn_img_axis = None

        if cmax is None:
            self._cmax = {'Herbivore': 200, 'Carnivore': 50}
        else:
            self._cmax = cmax

        if self._axt is None:
            self._axt = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])
            self._axt.axis('off')

        if self._txt is None:
            template = 'Year: {:5d}'
            self._txt = self._axt.text(0.5, 0.5, template.format(0),
                                       horizontalalignment='center',
                                       verticalalignment='center',
                                       transform=self._axt.transAxes)  # relative coordinates
        if hist_specs is None:
            self._hist_specs = {'weight': {'max': 100, 'delta': 2}, 'age': {'max': 100, 'delta': 2},
                                'fitness': {'max': 1.0, 'delta': 0.05}}
        else:
            self._hist_specs = hist_specs

        if self._fitness_ax is None:
            self._fitness_ax = self._fig.add_subplot(self._spec[6])
            self._fitness_ax.locator_params(nbins=5)
            self._fitness_ax.set_title('Fitness', fontsize='small')
            self._fitness_ax.set_ylim(0, 2000)

        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(self._spec[7])
            self._age_ax.set_title('Age', fontsize='small')
            self._age_ax.locator_params(nbins=5)
            self._age_ax.set_ylim(0, 2000)

        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(self._spec[8])
            self._weight_ax.set_title('Weight', fontsize='small')
            self._weight_ax.locator_params(nbins=5)
            self._weight_ax.set_ylim(0, 2000)

        if self._final_step is None:
            self._final_step = final_step

    def _update_island_map(self, geogr):
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in geogr.splitlines()]

        if self._img_axis is not None:
            self._img_axis.set_data(map_rgb)
        else:
            self._img_axis = self._map_ax.imshow(map_rgb)

    def _update_herb_distr(self, distr_map):
        if self._herb_img_axis is not None:
            self._herb_img_axis.set_data(distr_map)
        else:
            self._herb_img_axis = self._herb_distr_ax.imshow(distr_map,
                                                             interpolation='nearest',
                                                             vmin=0, vmax=self._cmax['Herbivore'])
            plt.colorbar(self._herb_img_axis, ax=self._herb_distr_ax,
                         orientation='vertical')

    def _update_carn_distr(self, distr_map):
        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(distr_map)
        else:
            self._carn_img_axis = self._carn_distr_ax.imshow(distr_map,
                                                             interpolation='nearest',
                                                             vmin=0, vmax=self._cmax['Carnivore'])
            plt.colorbar(self._carn_img_axis, ax=self._carn_distr_ax,
                         orientation='vertical')

    def _update_animal_lines(self, num_herbs, num_carns, step):
        y_data_h = self._herb_line.get_ydata()
        y_data_h[step] = num_herbs
        self._herb_line.set_ydata(y_data_h)

        y_data_c = self._carn_line.get_ydata()
        y_data_c[step] = num_carns
        self._carn_line.set_ydata(y_data_c)

        if self._ymax < max(num_herbs, num_carns):
            self._ymax = max(num_herbs, num_carns)*1.2
            self._pop_ax.set_ylim(0, self._ymax)
        if step > self._final_step:
            self._pop_ax.set_xlim(0, step+10)

    def _update_fitness(self, herb_fitness, carn_fitness):
        bins = (np.arange(0, self._hist_specs['fitness']['max'], self._hist_specs['fitness']
                ['delta']))

        if self._fitness_hist_herb is not None:
            self._fitness_hist_herb[0].remove()
        _, _, self._fitness_hist_herb = (self._fitness_ax.hist(herb_fitness, bins=bins,
                                         histtype='step', color='blue'))

        if self._fitness_hist_carn is not None:
            self._fitness_hist_carn[0].remove()
        _, _, self._fitness_hist_carn = (self._fitness_ax.hist(carn_fitness, bins=bins,
                                         histtype='step', color='red'))

    def _update_age(self, herb_age, carn_age):
        bins = (np.arange(0, self._hist_specs['age']['max'], self._hist_specs['age']['delta']))
        if self._age_hist_herb is not None:
            self._age_hist_herb[0].remove()
        _, _, self._age_hist_herb = (self._age_ax.hist(herb_age, bins=bins, histtype='step',
                                     color='blue'))

        if self._age_hist_carn is not None:
            self._age_hist_carn[0].remove()
        _, _, self._age_hist_carn = (self._age_ax.hist(carn_age, bins=bins, histtype='step',
                                                       color='red'))

    def _update_weight(self, herb_weight, carn_weight):
        bins = np.arange(0, self._hist_specs['weight']['max'], self._hist_specs['weight']['delta'])
        if self._weight_hist_herb is not None:
            self._weight_hist_herb[0].remove()
        _, _, self._weight_hist_herb = (self._weight_ax.hist(herb_weight, bins=bins,
                                                             histtype='step', color='blue'))

        if self._weight_hist_carn is not None:
            self._weight_hist_carn[0].remove()
        _, _, self._weight_hist_carn = (self._weight_ax.hist(carn_weight, bins=bins,
                                                             histtype='step', color='red'))

    def _update_year(self, year):
        template = 'Year: {:5d}'
        plt.pause(0.01)  # pause required to make figure visible
        self._txt.set_text(template.format(year))
        self._fig.canvas.flush_events()

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return
        self._fig.canvas.flush_events()
        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
