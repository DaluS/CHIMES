from .filter import Filter, FilterType

import numpy as np
import plotly.offline as pyo


# Used below to exclude the time variable from plots
EXCLUDE_TIME_FILTER = Filter(include=False, type=FilterType.KEY, field='time')


# Abstract base plot for other plots to inherit from
class Plot:
    """
    Base abstract plot. Plots are containers for figures, with rules to select variables from a CHIMES hub and display them
    in a figure or set of figures with specified configuration rules.

    Attributes
    ----------
    _name : str
        (metadata) Plot name.
    _description : str
        (metadata) Detailed plot description.
    filters: [Filter]
        List of variables filters. Filters are used to select which hub variables will be shown in the plot.
    config: object
        Set of config options to control the plot format and style.
    variables: Dict
        The set of variables to plot. These are drawn from a hub via the configured filters above.
    figure: Figure
        The most recent generated figure for the plot.

    Examples
    --------
    >>> plot = Plot()
    Create a new plot

    >>> plot.set_filters([IncludeKeyFilter(field='omega')])
    Filter to include the "omega" variables

    >>> plot.load_variables(hub)
    Load the "omega" variable from the hub

    >>> plot.generate()
    >>> plot.show()
    Generate and then display the resulting plot
    """

    def __init__(self):
        self._name = 'Plot'
        self._description = 'Base abstract plot.'

        self.filters = []    # List of filters. These will be used to select which variables from the run will be plot.
        self.config = {}     # Set of configuration items for the plot

        self.variables = {}  # Variables to plot. These will be loaded by the load_variables function below.

        self.figure = None
        self._hub = None

    # Getters
    def get_filters(self):
        return self.filters

    def get_config(self):
        return self.config

    # Setters
    def set_filters(self, filters: [Filter] = []):
        """
        Replace the filters with a new filter list.

        Parameters
        ----------
        filters : [Filter]
            List of filters for the plot to use when loading variables from the hub.
        """
        self.filters = filters

    def set_config(self, config={}):
        """
        Replace the plot configuration.

        Parameters
        ----------
        config : object
            Configuration object for the plot.
        """
        self.config = config

    def add_filter(self, filter):
        """
        Add a new filter to the filters list.

        Parameters
        ----------
        filter : Filter
            Filter to be applied to the plot when selecting variables.
        """
        self.filters.append(filter)

    # Load variables from the run. These will be filtered by the configured filter rules.
    def load_variables(self, hub):
        """
        Load variables from a CHIMES hub into the variables list so they can be rendered.

        The variables list starts out empty. From there the filtering proceeds in 2 stages:

        1. Includes
            All include filters are run in order. These filters copy matching variables into the
            variables list. If there are no include filters all variables are copied in by default.

        2. Excludes
            All exclude filters are run in order. Matching variables are removed from the variables
            list if they are found.

        The default behavior is to include all variables if there are no configured filters.

        Parameters
        ----------
        hub : CHIMESHub
            Hub to plot.
        """
        self._hub = hub

        # Reset any previously loaded variables
        # Make a copy of the d_params so that any modifications made by the filters don't
        # impact the hub itself
        dfields = hub.get_dfields()
        self.variables = {}

        # Scan the filters list for include filters and run any we find
        has_include = False
        for filter in self.filters:
            if filter._include is True:
                has_include = True
                for key, value in dfields.items():
                    filter.fn(key, value, self.variables)

        # If there were no include filters, copy each variable into the variable set
        if has_include is False:
            for key, value in dfields.items():
                self.variables[key] = value
                self.variables[key]['value'] = np.copy(value['value'])

        # Finally, run any exclude filters if they are present
        for filter in self.filters:
            if filter._include is False:
                for key, value in dfields.items():
                    filter.fn(key, value, self.variables)

        # Exclude time from all plots by default as it is redundant
        for key, value in dfields.items():
            EXCLUDE_TIME_FILTER.fn(key, value, self.variables)

    def generate(self):
        """
        Use the loaded variables to generate the corresponding plot.
        """
        pass

    def show(self):
        """
        Display the latest generated figure.
        """
        pass


class CalculateIndicesPlot(Plot):
    def _calculate_idx(self, hub, idx):
        # idx input
        if isinstance(idx, int):
            pass
        elif isinstance(idx, str):
            try:
                idx = hub.dfields['nx']['list'].index(idx)
            except BaseException:
                liste = hub.dfields['nx']['list']
                raise Exception(f'the parrallel system cannot be found !\n you gave {idx} in {liste}')
        else:
            raise Exception(f'the parrallel index cannot be understood ! you gave {idx}')

        return hub, idx

    def _calculate_region(self, hub, region):
        # Region input
        if isinstance(region, int):
            pass
        elif isinstance(region, str):
            try:
                region = hub.dfields['nr']['list'].index(region)
            except BaseException:
                liste = hub.dfields['nr']['list']
                raise Exception(f'the parrallel system cannot be found !\n you gave {region} in {liste}')
        else:
            raise Exception(f'the parrallel index cannot be understood ! you gave {region}')

        return hub, region

    def _calculate_time(self, R, idx, region, tini, tend):
        # time input
        time = R['time']['value'][:, idx, region, 0, 0]
        if tini:
            idt0 = np.argmin(np.abs(time - tini))
        else:
            idt0 = 0

        if tend:
            idt1 = np.argmin(np.abs(time - tend))
        else:
            idt1 = -1

        return R, idx, region, idt0, idt1

    def _calculate_indexes(self, hub, idx, region, tini, tend):
        R = hub.dfields

        # RUN
        # if not hub.dmisc['run']:
        #     print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        #     hub.run()

        hub, idx = self._calculate_idx(hub, idx)

        hub, region = self._calculate_region(hub, region)

        R, idx, region, idt0, idt1 = self._calculate_time(R, idx, region, tini, tend)

        return hub, idx, region, idt0, idt1

    def generate(
        self,
        separate_variables={},
        lw=1,
        idx=0,
        region=0,
        tini=False,
        tend=False,
        title=''
    ):
        """
        Use the loaded variables to generate the corresponding plot.

        Parameters
        ----------
        separate_variables : Dict
            Set of variables to separate out on the plots
        lw : int
            Line width for the plots
        idx : Union[str, int], default=0
            Index to select between parallel systems if present.
        region : Union[str, int], default=0
            Index to select between multiple regions if present.
        tini : Union[bool, int, float], default=0
            The initial time for the plot.
        tend : Union[bool, int, float], optional
             The end time for the plot. By default the last simulated variable.
        title : str, default=''
            The title of the plot.
        """
        self._hub, self.idx, self.region, self.idt0, self.idt1 = self._calculate_indexes(self._hub, idx, region, tini, tend)


class PlotlyOfflinePlot(Plot):
    """
    Basic plot that uses the `plotly` offline plot feature to render the generated figure
    in a local web browser.
    """

    def show(self):
        if hasattr(self, 'figure') and self.figure is not None:
            pyo.iplot(self.figure)
        else:
            raise Exception('No figure to draw')
