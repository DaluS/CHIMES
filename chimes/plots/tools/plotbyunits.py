from .plot import PlotlyOfflinePlot, CalculateIndicesPlot

import plotly.graph_objects as go
import plotly.subplots as subplots

from pylatexenc.latex2text import LatexNodes2Text

import math


SUBPLOT_COLUMNS = 2


class PlotByUnits(PlotlyOfflinePlot, CalculateIndicesPlot):
    """
    Group and display all variables by their units. Variables that have the same unit will be gathered and displayed together
    on the same subplot. These subplots are then arranged in a grid.

    Config
    ----------
    latex_plot_titles : Boolean, default=True
        Set to False to disable latex rendering in plot titles
    latex_legend_group_titles : Boolean, default=True
        Set to False to disable latex rendering in the legend group titles
    latex_legend_names : Boolean, default=True
        Set to False to disable latex rendering in the legend variable names
    """

    def __init__(self, *args, **kwargs):
        super(PlotByUnits, self).__init__(*args, **kwargs)

        self._name = 'Plot By Units'
        self._description = 'Plot all params for a model, with subplots grouping each param that have the same units.'

        self.filters = []  # Default to showing all variables

    def _generate_subplot(
        self,
        row,
        col,
        unit,
        params,
        lw=1,
        idx=0,
        region=0,
        idt0=False,
        idt1=False,
        title=''
    ):
        unit = unit if unit != '' else 'Dimensionless'
        unit_escaped = unit.replace('$', 'Dollars')
        unit_latex = f'${unit_escaped}$'

        # Setup plot title and legendgrouptitle_text so we can apply config options to disable them below
        plot_title = unit_latex
        legendgrouptitle_text = unit_latex

        # Disable latex plot titles if disabled in the config
        if self.config.get('latex_plot_titles', True) is False:
            # if 'latex_plot_titles' in self.config and self.config['latex_plot_titles'] is False:
            plot_title = unit

        # Disable latex legend group titles if disabled in the config
        if self.config.get('latex_legend_group_titles', True) is False:
            # if 'latex_legend_group_titles' in self.config and self.config['latex_legend_group_titles'] is False:
            legendgrouptitle_text = unit

        i = ((row - 1) * SUBPLOT_COLUMNS) + (col - 1)
        self.figure.layout.annotations[i]['text'] = plot_title

        R = self._hub.get_dfields(returnas=dict)
        vx = R['time']['value'][idt0:idt1, idx, region, 0, 0]

        for param in params:
            key = list(param.keys())[0]
            symbol = R.get(key, {'symbol': f'${key}$'})['symbol'] if 'symbol' in R.get(key, {'symbol': f'${key}$'}) else f'${key}$'
            symbol = symbol if symbol not in ['', '$$'] else f'${key}$'

            # Setup legend name for the variable so we can apply config options to disable latex if needed below
            name = symbol

            # Add python variable names next to the latex symbols if enabled in the config
            # if 'latex_python_variables' in self.config and self.config['latex_python_variables'] is True:
            if self.config.get('latex_python_variables', True) is True:
                # Remove the bounding $s from the latex to examine the interior expression
                inner_symbol = symbol[1:-1]

                # If the python variable name is different from the core of the latex expression, write the variable name
                # on the right inside ()
                if key != inner_symbol:
                    name = f'${inner_symbol} \\:({key})$'

            # Disable latex legend names if disabled in the config
            if self.config.get('latex_legend_names', True) is False:
                # if 'latex_legend_names' in self.config and self.config['latex_legend_names'] is False:
                name = key

            hover_template = '%{y}<br>' + LatexNodes2Text().latex_to_text(symbol) + '<extra></extra>'

            vy = param[key]['value'][idt0:idt1, idx, region, 0, 0]
            self.figure.add_trace(
                go.Scatter(
                    x=vx,
                    y=vy,
                    name=name,
                    hovertemplate=hover_template,
                    legendgroup=i,
                    legendgrouptitle_text=legendgrouptitle_text,
                    # legendgrouptitle_text=f'$'+R[name]['units']+'$' if R[name]['units'] != '' else 'dimensionless',
                ),
                row=row,
                col=col
            )

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
        if self.variables is None or self.variables == {}:
            raise Exception('Variables map is empty')

        super(PlotByUnits, self).generate(separate_variables, lw, idx, region, tini, tend, title)

        # Group variables by unit
        units_map = {}

        for k, v in self.variables.items():
            units = v.get('units', '')

            if len(v['value'].shape) == 5:
                if units not in units_map:
                    units_map[units] = []
                if units in units_map:
                    units_map[units].append({k: v})

        units = units_map.keys()

        # Calculate subplot layout
        SUBPLOT_ROWS = math.ceil(len(units) / 2)

        # Create subplot container
        self.figure = subplots.make_subplots(
            rows=SUBPLOT_ROWS,
            cols=SUBPLOT_COLUMNS,
            subplot_titles=(['title 1' for _ in range(0, len(units))])
        )

        # Build each subplot
        row, col = 1, 1
        for unit, params in units_map.items():
            self._generate_subplot(
                row,
                col,
                unit,
                params,
                lw=lw,
                idx=self.idx,
                region=self.region,
                idt0=self.idt0,
                idt1=self.idt1
            )

            if col + 1 > SUBPLOT_COLUMNS:
                col = 1
                row += 1
            else:
                col += 1

        self.figure.update_layout(legend=dict(groupclick="toggleitem"))
