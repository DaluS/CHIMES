import chimes
from chimes.plots.tools.plot import Plot, PlotlyOfflinePlot
from chimes.plots.tools.filter import Filter, FilterType

import plotly.offline as pyo

import pytest
from unittest.mock import Mock

from types import SimpleNamespace


class TestPlot:
    '''Plot'''

    filters = [{'fake': 'filter'}]
    config = {'fake': 'config'}

    dfields = {
        'a': {'value': [0, 1]},
        'delta': {'value': [3, 4]},
        'x': {'value': [1, 0]}
    }

    @pytest.fixture
    def plot(self):
        plot = Plot()
        plot.filters = self.filters
        plot.config = self.config
        return plot

    @pytest.fixture
    def hub(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(Filter, 'fn', mock)

        hub = SimpleNamespace(get_dfields=lambda: self.dfields)
        return hub

    @pytest.fixture
    def exclude_time_filter(self, monkeypatch):
        mock = Mock()

        filter = SimpleNamespace(
            fn=mock,
            _include=False
        )

        monkeypatch.setattr(chimes.plots.tools.plot, 'EXCLUDE_TIME_FILTER', filter)

        return filter

    def test_get_filters(self, plot):
        '''get_filters() :: it should return the filters list'''
        assert plot.get_filters() == self.filters

    def test_get_config(self, plot):
        '''get_config() :: it should return the config object'''
        assert plot.get_config() == self.config

    def test_set_filters(self, plot):
        '''set_filters() :: it should set the filters list'''
        filters = [{'different': 'fakefilter'}]

        plot.set_filters(filters)

        assert plot.filters == filters

    def test_set_config(self, plot):
        '''set_config() :: it should set the config object'''
        config = {'different': 'fakeconfig'}

        plot.set_config(config)

        assert plot.config == config

    def test_add_filter(self, plot):
        '''add_filter() :: it should add the filter to the filter list'''
        filter = {'new': 'fakefilter'}

        plot.add_filter(filter)

        assert plot.filters == [self.filters[0], filter]

    def test_load_variables_no_include_filters(self, plot, hub):
        '''load_variables() :: when there are no include filters :: it should copy all variables into the variable map'''
        plot.filters = []

        plot.load_variables(hub)

        assert plot.variables == self.dfields

    def test_load_variables_include_filters(self, plot, hub, exclude_time_filter):
        '''load_variables() :: when there are include filters :: it should run each include filter over each variable in the hub'''
        filter = Filter(include=True, type=FilterType.KEY, field='a')
        plot.filters = [filter]

        plot.load_variables(hub)

        assert filter.fn.call_count == 3
        filter.fn.assert_any_call('a', self.dfields['a'], {})
        filter.fn.assert_any_call('delta', self.dfields['delta'], {})
        filter.fn.assert_any_call('x', self.dfields['x'], {})

        assert exclude_time_filter.fn.call_count == 3

    def test_load_variables_exclude_filters(self, plot, hub, exclude_time_filter):
        '''load_variables() :: when there are exclude filters :: it should run each exclude filter over each variable in the hub'''
        filter = Filter(include=False, type=FilterType.KEY, field='a')
        plot.filters = [filter]

        plot.load_variables(hub)

        assert filter.fn.call_count == 3
        filter.fn.assert_any_call('a', self.dfields['a'], self.dfields)
        filter.fn.assert_any_call('delta', self.dfields['delta'], self.dfields)
        filter.fn.assert_any_call('x', self.dfields['x'], self.dfields)

        assert exclude_time_filter.fn.call_count == 3

    def test_load_variables_exclude_time(self, plot, hub, exclude_time_filter):
        '''load_variables() :: it should exclude the time variable from the plot'''
        plot.set_filters([])
        plot.load_variables(hub)

        assert exclude_time_filter.fn.call_count == 3
        exclude_time_filter.fn.assert_any_call('a', self.dfields['a'], self.dfields)
        exclude_time_filter.fn.assert_any_call('delta', self.dfields['delta'], self.dfields)
        exclude_time_filter.fn.assert_any_call('x', self.dfields['x'], self.dfields)


@pytest.mark.skip()
class TestCalculateIndicesPlot:
    '''CalculateIndiciesPlot'''

    def test_calc_idx_int(self):
        '''when calculating idx :: it should pass when idx is an integer'''
        pass

    def test_calc_idx_str(self):
        '''when calculating idx :: it should search the hub for idx when it is a string'''
        pass

    def test_calc_idx_str_missing(self):
        '''when calculating idx :: it should raise an exception when idx is a string and it cannot be found on the hub'''
        pass

    def test_calc_region_int(self):
        '''when calculating region :: it should pass when region is an integer'''
        pass

    def test_calc_region_str(self):
        '''when calculating region :: it should search the hub for region when it is a string'''
        pass

    def test_calc_region_str_missing(self):
        '''when calculating region :: it should raise an exception when region is a string and it cannot be found on the hub'''
        pass

    def test_calc_tini_default(self):
        '''when calculating idt0 and idt1 :: it should default idt0 to 0 when tini is not provided'''
        pass

    def test_calc_tend_default(self):
        '''when calculating idt0 and idt1 :: it should default idt1 to -1 when tend is not provided'''
        pass

    def test_calc_idt0(self):
        '''when calculating idt0 and idt1 :: it should calculate the index of idt0 from the time array when tini is provided'''
        pass

    def test_calc_idt1(self):
        '''when calculating idt0 and idt1 :: it should calculate the index of idt1 from the time array when tend is provided'''
        pass


class TestPlotlyOfflinePlot:
    '''PlotlyOfflinePlot'''

    figure = {'fake': 'figure'}

    @pytest.fixture
    def plotlymock(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(pyo, 'iplot', mock)
        return mock

    @pytest.fixture
    def plot(self):
        plot = PlotlyOfflinePlot()
        plot.figure = self.figure
        return plot

    def test_show(self, plotlymock, plot):
        '''show() :: it should use plotly.offline to render the figure in a local web browser'''
        plot.show()

        plotlymock.assert_called_once()
        plotlymock.assert_called_with(self.figure)
        pass

    def test_show_no_figure(self, plotlymock, plot):
        '''show() :: it should raise an exception when there is no figure to display'''
        del plot.figure

        with pytest.raises(Exception, match="No figure to draw"):
            plot.show()
