from chimes.plots.tools.filter import Filter, FilterType
from chimes.plots.showsensitivity import ShowSensitivity

import pytest
from unittest.mock import Mock

import numpy as np
import plotly.graph_objects as go

from types import SimpleNamespace


mock_a_value = {'value': [0, 1]}
mock_delta_value = {'value': [3, 4]}
mock_x_value = {'value': [1, 0]}

mock_time = np.resize(np.array([0, 1]), (2, 1, 1, 1, 1))
mock_time_unwound = [0, 1]


def generate_mock_hub():
    return {
        'a': SimpleNamespace(get_dfields=lambda: mock_a_value),
        'delta': SimpleNamespace(get_dfields=lambda: mock_delta_value),
        'x': SimpleNamespace(get_dfields=lambda: mock_x_value)
    }


class TestShowSensitivity:
    '''ShowSensitivity'''

    filters = [{'fake': 'filter'}]
    config = {'fake': 'config'}

    @pytest.fixture
    def plot(self, monkeypatch):
        plot = ShowSensitivity()
        plot.filters = self.filters
        plot.config = self.config
        return plot

    @pytest.fixture
    def hub(self, monkeypatch):
        hub = generate_mock_hub()

        mock = Mock()
        monkeypatch.setattr(Filter, 'fn', mock)

        return hub

    @pytest.fixture
    def variables(self):
        variables = {
            'a': {'time': {'value': mock_time}, 'employment': {'sensitivity': [{'': {'stdv': mock_a_value}}]}},
            'delta': {'time': {'value': mock_time}, 'employment': {'sensitivity': [{'': {'stdv': mock_delta_value}}]}},
            'x': {'time': {'value': mock_time}, 'employment': {'sensitivity': [{'': {'stdv': mock_x_value}}]}}
        }

        return variables

    @pytest.fixture
    def mocks(self, monkeypatch):
        add_trace = Mock()
        update_layout = Mock()
        Figure = Mock(return_value=SimpleNamespace(
            add_trace=add_trace,
            update_layout=update_layout
        ))
        Scatter = Mock(return_value='scatter_test')
        Layout = Mock(return_value='layout_test')

        monkeypatch.setattr(go, 'Figure', Figure)
        monkeypatch.setattr(go, 'Scatter', Scatter)
        monkeypatch.setattr(go, 'Layout', Layout)

        return Figure, Scatter, Layout, add_trace, update_layout

    def test_load_variables_no_include_filters(self, plot, hub):
        '''load_variables() :: when there are no include filters :: it should copy all variables into the variable map'''
        plot.filters = []

        plot.load_variables(hub)

        assert plot.variables == {
            'a': mock_a_value,
            'delta': mock_delta_value,
            'x': mock_x_value
        }

    def test_load_variables_include_filters(self, plot, hub):
        '''load_variables() :: when there are include filters :: it should run each include filter over each variable in the hub'''
        filter = Filter(include=True, type=FilterType.KEY, field='a')
        plot.filters = [filter]

        plot.load_variables(hub)

        assert filter.fn.call_count == 3
        filter.fn.assert_any_call('a', mock_a_value, {})
        filter.fn.assert_any_call('delta', mock_delta_value, {})
        filter.fn.assert_any_call('x', mock_x_value, {})

    def test_load_variables_exclude_filters(self, plot, hub):
        '''load_variables() :: when there are exclude filters :: it should run each exclude filter over each remaining variable in the hub'''
        filter = Filter(include=False, type=FilterType.KEY, field='a')
        plot.filters = [filter]

        variables = {
            'a': mock_a_value,
            'delta': mock_delta_value,
            'x': mock_x_value
        }

        plot.load_variables(hub)

        assert filter.fn.call_count == 3
        filter.fn.assert_any_call('a', mock_a_value, variables)
        filter.fn.assert_any_call('delta', mock_delta_value, variables)
        filter.fn.assert_any_call('x', mock_x_value, variables)

    def test_load_variables_sector_filters(self, plot, hub):
        '''load_variables() :: when there are sector filters :: it should not run them over the variables in the hub'''
        filter = Filter(include=False, type=FilterType.SECTOR, field='a')

        plot.filters = [filter]

        plot.load_variables(hub)

        filter.fn.assert_not_called()

    def test_create_figure(self, plot, variables, mocks):
        '''generate() :: it should use plotly to create a blank figure'''
        plot.variables = variables
        plot.generate('employment')

        Figure, *_ = mocks

        Figure.assert_called_once()

    def test_generate_scatter_plots(self, plot, variables, mocks):
        '''generate() :: it should add a scatter plot to the figure for each variable in the variables map'''
        Figure, Scatter, Layout, add_trace, update_layout = mocks

        plot.variables = variables
        plot.generate('employment')

        # add_trace should be called 3 times, once for each variable
        assert plot.figure.add_trace.call_count == 3
        plot.figure.add_trace.assert_any_call('scatter_test')

        # Scatter constructor should be called 3 times, once for each variable
        assert Scatter.call_count == 3
        Scatter.call_args_list[0][1]['x'] = Scatter.call_args_list[0][1]['x'].tolist()
        Scatter.call_args_list[1][1]['x'] = Scatter.call_args_list[1][1]['x'].tolist()
        Scatter.call_args_list[2][1]['x'] = Scatter.call_args_list[2][1]['x'].tolist()
        assert Scatter.call_args_list[0][1] == {
            'x': mock_time_unwound,
            'y': mock_a_value,
            'mode': 'lines',
            'name': '$a$',
            'hovertemplate': '%{y}<br>a<extra></extra>'
        }
        assert Scatter.call_args_list[1][1] == {
            'x': mock_time_unwound,
            'y': mock_delta_value,
            'mode': 'lines',
            'name': '$delta$',
            'hovertemplate': '%{y}<br>delta<extra></extra>'
        }
        assert Scatter.call_args_list[2][1] == {
            'x': mock_time_unwound,
            'y': mock_x_value,
            'mode': 'lines',
            'name': '$x$',
            'hovertemplate': '%{y}<br>x<extra></extra>'
        }

    def test_generate_figure_labels(self, plot, variables, mocks):
        '''generate() :: it should set the layout title and axis labels'''
        Figure, Scatter, Layout, add_trace, update_layout = mocks

        plot.variables = variables
        plot.generate('employment')

        # update_layout should be called 3 times, once for each variable
        assert plot.figure.update_layout.call_count == 3
        plot.figure.update_layout.assert_any_call('layout_test')

        # Layout constructor should be called 3 times, once for each variable
        assert Layout.call_count == 3
        Layout.assert_any_call(
            title='Sensitivity on variable $a$ for a lognormal noise of 1%',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Sensitivity on variable $a$'},
            legend={'orientation': 'h'}
        )
        Layout.assert_any_call(
            title='Sensitivity on variable $delta$ for a lognormal noise of 1%',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Sensitivity on variable $delta$'},
            legend={'orientation': 'h'}
        )
        Layout.assert_any_call(
            title='Sensitivity on variable $x$ for a lognormal noise of 1%',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Sensitivity on variable $x$'},
            legend={'orientation': 'h'}
        )

    def test_generate_empty_variables(self, plot):
        '''generate() :: it should raise an exception when the variables map is empty'''
        with pytest.raises(Exception, match='No variables loaded for the plot'):
            plot.generate('employment')

        plot.variables = None
        with pytest.raises(Exception, match='No variables loaded for the plot'):
            plot.generate('employment')

        plot.variables = {}
        with pytest.raises(Exception, match='No variables loaded for the plot'):
            plot.generate('employment')

    def test_generate_no_variable_param(self, plot):
        '''generate() :: it should raise an exception when the variable param is empty'''
        with pytest.raises(Exception, match='Input variable required to show sensitivity figures'):
            plot.generate('')
