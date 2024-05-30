import pytest
import copy

from chimes.plots.tools.filter import Filter, FilterType
from chimes.plots.tools.filter import KeyFilter, IncludeKeyFilter, ExcludeKeyFilter
from chimes.plots.tools.filter import UnitFilter, IncludeUnitFilter, ExcludeUnitFilter
from chimes.plots.tools.filter import SectorFilter, IncludeSectorFilter, ExcludeSectorFilter


class TestFilter:
    @pytest.fixture(scope="session")
    def filter(self):
        _filter = Filter(include=False, type=FilterType.SECTOR, field='field')
        return _filter

    '''Filter :: constructor()'''

    def test_set_include(self, filter):
        '''it should set _include'''
        assert filter._include is False

    def test_set_type(self, filter):
        '''it should set _type'''
        assert filter._type == FilterType.SECTOR

    def test_set_field(self, filter):
        '''it should set _field'''
        assert filter._field == 'field'


class TestKeyFilter:
    '''KeyFilter'''

    _field = 'test'

    _value = {
        'value': [3, 4, 5]
    }

    _variables = {
        'omega': {
            'value': [1, 2, 3]
        }
    }

    @pytest.fixture(autouse=True)
    def variables(self):
        key = self._field

        value = self._value

        variables = copy.deepcopy(self._variables)

        return key, value, variables

    @pytest.fixture(autouse=True)
    def filter(self):
        return KeyFilter(field=self._field)

    def test_set_type_to_key(self, filter):
        '''constructor() :: it should set _type to FilterType.KEY'''
        assert filter._type == FilterType.KEY

    def test_run_include_filter_key_matches(self, filter, variables):
        '''fn() :: when include is True :: it should add the variable to the variable map when the key matches'''
        key, value, variables = variables

        filter.fn(key, value, variables)
        assert variables == {'omega': self._variables['omega'], self._field: self._value}

    def test_run_include_filter_key_not_matches(self, filter, variables):
        '''fn() :: when include is True :: it should not modify the variable map when the key does not match'''
        key, value, variables = variables

        filter._field = 'missing key'

        filter.fn(key, value, variables)
        assert variables == self._variables

    def test_run_exclude_filter_key_matches(self, filter, variables):
        '''fn() :: when include is False :: it should remove the variable from the variable map when the key matches'''
        key, value, variables = variables

        key = 'omega'
        filter._field = 'omega'
        filter._include = False

        filter.fn(key, value, variables)
        assert variables == {}

    def test_run_exclude_filter_key_not_matches(self, filter, variables):
        '''fn() :: when include is False :: it should not modify the variable map when the key does not match'''
        key, value, variables = variables

        filter._include = False

        filter.fn(key, value, variables)
        assert variables == self._variables


class TestIncludeKeyFilter:
    '''IncludeKeyFilter'''

    def test_set_include_to_true(self):
        '''constructor() :: it should set _include to True'''
        filter = IncludeKeyFilter()
        assert filter._include is True


class TestExcludeKeyFilter:
    '''ExcludeKeyFilter'''

    def test_set_include_to_false(self):
        '''constructor() :: it should set _include to False'''
        filter = ExcludeKeyFilter()
        assert filter._include is False


class TestUnitFilter:
    '''UnitFilter'''

    _field = 'test'

    _value = {
        'value': [3, 4, 5],
        'units': '$'
    }

    _variables = {
        'omega': {
            'value': [1, 2, 3],
            'units': '$'
        }
    }

    @pytest.fixture(autouse=True)
    def variables(self):
        key = self._field

        value = self._value

        variables = copy.deepcopy(self._variables)

        return key, value, variables

    @pytest.fixture(autouse=True)
    def filter(self):
        return UnitFilter(field='$')

    def test_set_type_to_unit(self, filter):
        '''constructor() :: it should set _type to FilterType.Unit'''
        assert filter._type == FilterType.UNIT

    def test_add_variable_to_map_when_unit_matches(self, filter, variables):
        '''fn() :: when include is True :: it should add the variable to the variable map when the unit matches'''
        key, value, variables = variables

        filter.fn(key, value, variables)
        assert variables == {'omega': self._variables['omega'], self._field: value}

    def test_not_add_variable_to_map_when_unit_does_not_match(self, filter, variables):
        '''fn() :: when include is True :: it should not modify the variable map when the unit does not match'''
        key, value, variables = variables

        filter._field = ''

        filter.fn(key, value, variables)
        assert variables == self._variables

    def test_remove_variable_from_map_when_unit_matches(self, filter, variables):
        '''fn() :: when include is False :: it should remove the variable from the variable map when the unit matches'''
        key, value, variables = variables

        filter._include = False
        key = 'omega'

        filter.fn(key, value, variables)
        assert variables == {}

    def test_not_remove_variable_from_map_when_unit_matches(self, filter, variables):
        '''fn() :: when include is False :: it should not modify the variable map when the unit does not match'''
        key, value, variables = variables

        filter._include = False

        filter.fn(key, value, variables)
        assert variables == self._variables


class TestIncludeUnitFilter:
    '''IncludeUnitFilter'''

    def test_set_include_to_true(self):
        '''constructor() :: it should set _include to True'''
        filter = IncludeUnitFilter()
        assert filter._include is True


class TestExcludeUnitFilter:
    '''ExcludeUnitFilter'''

    def test_set_include_to_false(self):
        '''constructor() :: it should set _include to False'''
        filter = ExcludeUnitFilter()
        assert filter._include is False


@pytest.mark.skip()
class TestSectorFilter:
    '''SectorFilter'''

    def test_set_type_to_sector(self):
        '''constructor() :: it should set _type to FilterType.SECTOR'''
        filter = SectorFilter()
        assert filter._type == FilterType.SECTOR

    def test_add_variable_to_map_when_sector_matches(self):
        '''fn() :: when include is True :: it should add the sector to the variable map when the variable is in the sector'''
        pass

    def test_not_add_variable_to_map_when_sector_does_not_match(self):
        '''fn() :: when include is True :: it should not modify the variable map when the variable is not in the sector'''
        pass

    def test_remove_variable_from_map_when_sector_matches(self):
        '''fn() :: when include is False ::  it should remove the sector from the variable map when the variable is in the sector'''
        pass

    def test_not_remove_variable_from_map_when_sector_matches(self):
        '''fn() :: when include is False :: it should not modify the variable map when the variable is not in the sector'''
        pass


class TestIncludeSectorFilter:
    '''IncludeSectorFilter'''

    def test_set_include_to_true(self):
        '''constructor() :: it should set _include to True'''
        filter = IncludeSectorFilter()
        assert filter._include is True


class TestExcludeSectorFilter:
    def test_set_include_to_false(self):
        '''constructor() :: it should set _include to False'''
        filter = ExcludeSectorFilter()
        assert filter._include is False
