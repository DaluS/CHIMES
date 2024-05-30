from chimes.plots.tools.plot import PlotlyOfflinePlot
from chimes.plots.tools.filter import FilterType

import plotly.graph_objects as go

from pylatexenc.latex2text import LatexNodes2Text


class ShowSensitivity(PlotlyOfflinePlot):
    """
    Display the sensitivity of each parameter in the output of a hub model run.
    """

    def __init__(self, *args, **kwargs):
        super(ShowSensitivity, self).__init__(*args, **kwargs)

        self._name = 'Show Sensitivity'
        self._description = 'Display how sensitive is the parameter value on a run.'

        self.filters = []  # Default to showing all variables

    def load_variables(self, hub):
        self.variables = {}

        # Ignore any SectorFilters in the list
        filters = [filter for filter in self.filters if filter._type != FilterType.SECTOR]

        has_include = False
        for filter in filters:
            if filter._include is True:
                has_include = True
                for key, value in hub.items():
                    filter.fn(key, value.get_dfields(), self.variables)

        # If there were no include filters, copy each variable into the variable set
        if has_include is False:
            for key, value in hub.items():
                self.variables[key] = value.get_dfields()
                # self.variables[key]['value'] = np.copy(value['value'])

        # Finally, run any exclude filters if they are present
        for filter in filters:
            if filter._include is False:
                for key, value in hub.items():
                    filter.fn(key, value.get_dfields(), self.variables)

    def generate(self, variable):
        if variable is None or variable == '':
            raise Exception('Input variable required to show sensitivity figures')

        if self.variables is None or self.variables == {}:
            raise Exception('No variables loaded for the plot')

        self.figure = go.Figure()
        # D = {}
        # D[variable] = {}

        for k, R in self.variables.items():
            time = R['time']['value'][:, 0, 0, 0, 0]  # (100, 10, 1, 1, 1)
            # print(time, R[variable]['sensitivity'][0]['']['stdv'])
            symbol = R.get(k, {'symbol': f'${k}$'})['symbol'] if 'symbol' in R.get(k, {'symbol': f'${k}$'}) else f'${k}$'
            symbol = symbol if symbol not in ['', '$$'] else f'${k}$'

            hover_template = '%{y}<br>' + LatexNodes2Text().latex_to_text(symbol) + '<extra></extra>'

            self.figure.add_trace(
                go.Scatter(
                    x=time,
                    y=R[variable]['sensitivity'][0]['']['stdv'],
                    mode='lines',
                    name=symbol,
                    hovertemplate=hover_template
                )
            )

            self.figure.update_layout(go.Layout(
                title=f"Sensitivity on variable {symbol} for a lognormal noise of 1%",
                xaxis=dict(title='Time'),
                yaxis=dict(title=f"Sensitivity on variable {symbol}"),
                legend=dict(orientation='h'),
            ))
