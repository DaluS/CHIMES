from chimes.plots.tools.filter import Filter, FilterType
from chimes.plots.tools.plotbyunits import PlotByUnits
from chimes.plots.tools.plot import CalculateIndicesPlot

import pytest
from unittest.mock import Mock

import numpy as np

import plotly.subplots as subplots
import plotly.graph_objects as go

from types import SimpleNamespace


mock_params = {
    'separate_variables': {},
    'lw': 1,
    'idx': 0,
    'region': 0,
    'tini': True,
    'tend': False,
    'title': ''
}

mock_a_value = {
    'value': np.resize(np.array([0, 1]), (2, 1, 1, 1, 1)),
    'units': ''
}
mock_delta_value = {
    'value': np.resize(np.array([3, 4]), (2, 1, 1, 1, 1)),
    'units': '$'
}
mock_x_value = {
    'value': np.resize(np.array([1, 0]), (2, 1, 1, 1, 1)),
    'units': '$'
}
mock_phi_value = {
    'value': np.resize(np.array([2, 3]), (2, 1, 1, 1, 1)),
    'units': 'Humans'
}

mock_time = np.resize(np.array([0, 1]), (2, 1, 1, 1, 1))
mock_time_unwound = [0, 1]

mock_dfields = {
    'time': {
        'value': mock_time
    },
    'a': {
        'symbol': r'$a$',
        'value': mock_a_value
    },
    'delta': {
        'symbol': r'$\delta$',
        'value': mock_delta_value
    },
    'x': {
        'symbol': r'$x$',
        'value': mock_x_value
    },
    'phi': {
        'symbol': r'$phi$',
        'value': mock_phi_value
    }
}


class TestPlotByUnits:
    '''PlotByUnits'''

    variables = {
        'a': mock_a_value,
        'delta': mock_delta_value,
        'x': mock_x_value,
        'phi': mock_phi_value
    }

    hub = SimpleNamespace(
        get_dfields=lambda returnas: mock_dfields
    )

    @pytest.fixture
    def plot(self, monkeypatch):
        plot = PlotByUnits()

        plot.variables = self.variables

        # Fields calculated by CalculateIndicesPlot super class
        plot._hub = self.hub
        plot.idx = 0
        plot.region = 0
        plot.idt0 = 0
        plot.idt1 = 2

        return plot

    @pytest.fixture
    def mock_calc_idx(self, monkeypatch):
        mock_calc_idx = Mock()
        monkeypatch.setattr(CalculateIndicesPlot, 'generate', mock_calc_idx)

        return mock_calc_idx

    @pytest.fixture
    def mock_plot_functions(self, monkeypatch):
        mock_make_subplots = Mock()
        monkeypatch.setattr(subplots, 'make_subplots', mock_make_subplots)

        mock_add_trace = Mock()

        mock_go_scatter = Mock(side_effect=lambda x, y, name, hovertemplate, legendgroup, legendgrouptitle_text: name)
        # mock_go_scatter.return_value = 'scatter'
        monkeypatch.setattr(go, 'Scatter', mock_go_scatter)

        mock_update_layout = Mock()

        mock_make_subplots.return_value = SimpleNamespace(
            layout=SimpleNamespace(
                annotations=[{'text': ''}, {'text': ''}, {'text': ''}]
            ),
            add_trace=mock_add_trace,
            update_layout=mock_update_layout
        )

        return mock_make_subplots, mock_add_trace, mock_go_scatter, mock_update_layout

    def test_calculate_indices(self, plot, mock_calc_idx):
        '''generate() :: it should invoke its parent class generate() to calculate the plot indices'''
        plot.generate(**mock_params)

        mock_calc_idx.assert_called_once()
        mock_calc_idx.assert_called_with(*(list(mock_params.values())))

    def test_generate_grid(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: it should genereate a subplot layout for the figure'''
        mock_make_subplots, *_ = mock_plot_functions

        plot.generate(**mock_params)

        mock_make_subplots.assert_called_once()
        mock_make_subplots.assert_called_with(
            rows=2,
            cols=2,
            subplot_titles=['title 1', 'title 1', 'title 1']
        )

    def test_generate_add_trace(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: it should add a trace for each variable in the variable map'''
        _, mock_add_trace, _, _ = mock_plot_functions

        plot.generate(**mock_params)

        assert mock_add_trace.call_count == 4

    def test_missing_variable_symbol(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: it should default to using the variable name when its symbol is missing or empty'''
        _, mock_add_trace, _, _ = mock_plot_functions

        # No symbol
        del mock_dfields['a']['symbol']

        plot.generate(**mock_params)
        mock_add_trace.assert_any_call('$a$', row=1, col=1)

        # Empty symbol
        mock_dfields['a']['symbol'] = ''

        plot.generate(**mock_params)
        mock_add_trace.assert_any_call('$a$', row=1, col=1)

        # Empty latex symbol
        mock_dfields['a']['symbol'] = '$$'

        plot.generate(**mock_params)
        mock_add_trace.assert_any_call('$a$', row=1, col=1)

        # Reset mock_dfields back to its previous value
        mock_dfields['a']['symbol'] = '$a$'

    def test_generate_set_subplot_titles(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: it should set the subplot titles to match the units'''
        plot.generate(**mock_params)

        assert plot.figure.layout.annotations == [{'text': '$Dimensionless$'}, {'text': '$Dollars$'}, {'text': '$Humans$'}]

    def test_generate_group_units(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: it should group variables with the same unit into a single subplot'''
        _, mock_add_trace, mock_go_scatter, _ = mock_plot_functions

        plot.generate(**mock_params)

        assert mock_add_trace.call_count == 4
        mock_add_trace.assert_any_call('$a$', row=1, col=1)
        mock_add_trace.assert_any_call(r'$\delta \:(delta)$', row=1, col=2)
        mock_add_trace.assert_any_call('$x$', row=1, col=2)
        mock_add_trace.assert_any_call('$phi$', row=2, col=1)

        assert mock_go_scatter.call_count == 4
        calls = mock_go_scatter.call_args_list
        for i in range(0, len(calls)):
            calls[i][1]['x'], calls[i][1]['y'] = calls[i][1]['x'].tolist(), calls[i][1]['y'].tolist()
        mock_go_scatter.assert_any_call(x=[0, 1], y=[0, 1], name='$a$', hovertemplate='%{y}<br>a<extra></extra>', legendgroup=0, legendgrouptitle_text='$Dimensionless$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[3, 4], name=r'$\delta \:(delta)$', hovertemplate='%{y}<br>δ<extra></extra>', legendgroup=1, legendgrouptitle_text='$Dollars$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[1, 0], name='$x$', hovertemplate='%{y}<br>x<extra></extra>', legendgroup=1, legendgrouptitle_text='$Dollars$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[2, 3], name='$phi$', hovertemplate='%{y}<br>phi<extra></extra>', legendgroup=2, legendgrouptitle_text='$Humans$')

    def test_generate_empty_variables(self, plot):
        '''generate() :: it should raise an exception when the variables map is empty'''
        plot.variables = None
        with pytest.raises(Exception, match='Variables map is empty'):
            plot.generate(**mock_params)

        plot.variables = {}
        with pytest.raises(Exception, match='Variables map is empty'):
            plot.generate(**mock_params)

    def test_latex_plot_titles(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: Config :: it should not render latex in the subplot titles when the config option is disabled'''
        plot.config['latex_plot_titles'] = False

        plot.generate(**mock_params)

        assert plot.figure.layout.annotations == [{'text': 'Dimensionless'}, {'text': '$'}, {'text': 'Humans'}]

    def test_latex_python_variables(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: Config :: it should not render python variables names along with the latex symbols when the config option is disabled'''
        _, _, mock_go_scatter, _ = mock_plot_functions

        plot.config['latex_python_variables'] = False

        plot.generate(**mock_params)

        assert mock_go_scatter.call_count == 4
        calls = mock_go_scatter.call_args_list
        for i in range(0, len(calls)):
            calls[i][1]['x'], calls[i][1]['y'] = calls[i][1]['x'].tolist(), calls[i][1]['y'].tolist()
        mock_go_scatter.assert_any_call(x=[0, 1], y=[0, 1], name='$a$', hovertemplate='%{y}<br>a<extra></extra>', legendgroup=0, legendgrouptitle_text='$Dimensionless$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[3, 4], name=r'$\delta$', hovertemplate='%{y}<br>δ<extra></extra>', legendgroup=1, legendgrouptitle_text='$Dollars$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[1, 0], name='$x$', hovertemplate='%{y}<br>x<extra></extra>', legendgroup=1, legendgrouptitle_text='$Dollars$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[2, 3], name='$phi$', hovertemplate='%{y}<br>phi<extra></extra>', legendgroup=2, legendgrouptitle_text='$Humans$')

    def test_latex_legend_group_titles(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: Config :: it should not render latex in the legend group titles when the config option is disabled'''
        _, _, mock_go_scatter, _ = mock_plot_functions

        plot.config['latex_legend_group_titles'] = False

        plot.generate(**mock_params)

        assert mock_go_scatter.call_count == 4
        calls = mock_go_scatter.call_args_list
        for i in range(0, len(calls)):
            calls[i][1]['x'], calls[i][1]['y'] = calls[i][1]['x'].tolist(), calls[i][1]['y'].tolist()
        mock_go_scatter.assert_any_call(x=[0, 1], y=[0, 1], name='$a$', hovertemplate='%{y}<br>a<extra></extra>', legendgroup=0, legendgrouptitle_text='Dimensionless')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[3, 4], name=r'$\delta \:(delta)$', hovertemplate='%{y}<br>δ<extra></extra>', legendgroup=1, legendgrouptitle_text='$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[1, 0], name='$x$', hovertemplate='%{y}<br>x<extra></extra>', legendgroup=1, legendgrouptitle_text='$')
        mock_go_scatter.assert_any_call(x=[0, 1], y=[2, 3], name='$phi$', hovertemplate='%{y}<br>phi<extra></extra>', legendgroup=2, legendgrouptitle_text='Humans')

    def test_latex_legend_names(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: Config :: it should not render latex in the legend names when the config option is disabled'''
        _, mock_add_trace, _, _ = mock_plot_functions

        plot.config['latex_legend_names'] = False

        plot.generate(**mock_params)

        assert mock_add_trace.call_count == 4
        mock_add_trace.assert_any_call('a', row=1, col=1)
        mock_add_trace.assert_any_call('delta', row=1, col=2)
        mock_add_trace.assert_any_call('x', row=1, col=2)
        mock_add_trace.assert_any_call('phi', row=2, col=1)

    def test_latex_python_variables_disabled_legend_names(self, plot, mock_calc_idx, mock_plot_functions):
        '''generate() :: Config :: it should not render latex in the legend names when the config option is disabled even if python variables are enabled'''
        _, mock_add_trace, _, _ = mock_plot_functions

        plot.config['latex_legend_names'] = False
        plot.config['latex_python_variables'] = True

        plot.generate(**mock_params)

        assert mock_add_trace.call_count == 4
        mock_add_trace.assert_any_call('a', row=1, col=1)
        mock_add_trace.assert_any_call('delta', row=1, col=2)
        mock_add_trace.assert_any_call('x', row=1, col=2)
        mock_add_trace.assert_any_call('phi', row=2, col=1)
