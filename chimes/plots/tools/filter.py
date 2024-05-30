from enum import Enum

import numpy as np


# Globally define the filter functions so that they can be hooked in to each of the classes below
def key_filter_fn(self, key, value, variables):
    if key == self._field and self._include is True:
        variables[key] = value
        if 'value' in variables[key]:
            variables[key]['value'] = np.copy(value['value'])
    elif key == self._field and self._include is False:
        if key in variables:
            del variables[key]


def unit_filter_fn(self, key, value, variables):
    if value['units'] == self._field and self._include is True:
        variables[key] = value
        if 'value' in variables[key]:
            variables[key]['value'] = np.copy(value['value'])
    elif value['units'] == self._field and self._include is False:
        if key in variables:
            del variables[key]


def sector_filter_fn(self, key, value, variables):
    # TODO: Implement sector filters
    pass


class FilterType(Enum):
    """
    Possible filter types.

    Types
    -----
    1. KEY
        Filter for a specific variable name.
    2. UNIT
        Filter all variables that are in the given unit.
    3. SECTOR
        Filter all variables that are in the given sector (requires multi-sectoral model).
    """
    KEY = 1
    UNIT = 2
    SECTOR = 3


class Filter:
    """
    Represents a rule for specifying which variables should be present in a given plot. Filters can either
    include or exclude target variable(s) and can specify different target variables via the FilterType.

    Attributes
    ----------
    _include : bool
        Whether to include (True) or exclude (False) the target variable(s).
    _type : FilterType
        Type of target to filter on (see FilterType).
    _field : str
        Filter target.
    """
    def __init__(self, include: bool = True, type: FilterType = FilterType.KEY, field: str = ''):
        self._include = include if include is True else False
        self._type = type
        self._field = field

    def fn(self, key, value, variables):
        """
        Run the filter logic for a specific key-value pair from the hub.

        Parameters
        ----------
        key : str
            Key for a variable from the hub.
        value : object
            Contains the results of the run for this variable on the hub.
        variables : Dict
            Variable map to copy into / exclude matching variables from.
        """
        if self._type == FilterType.KEY:
            return key_filter_fn(self, key, value, variables)
        elif self._type == FilterType.UNIT:
            return unit_filter_fn(self, key, value, variables)
        elif self._type == FilterType.SECTOR:
            return sector_filter_fn(self, key, value, variables)
        else:
            pass


class KeyFilter(Filter):
    """
    Filter for a specific key (variable name).
    """
    def __init__(self, *args, **kwargs):
        super(KeyFilter, self).__init__(*args, **kwargs)
        self._type = FilterType.KEY


class IncludeKeyFilter(KeyFilter):
    """
    Include a specific variable by name.
    """
    def __init__(self, *args, **kwargs):
        super(IncludeKeyFilter, self).__init__(*args, **kwargs)
        self._include = True


class ExcludeKeyFilter(KeyFilter):
    """
    Exclude a specific variable by name.
    """
    def __init__(self, *args, **kwargs):
        super(ExcludeKeyFilter, self).__init__(*args, **kwargs)
        self._include = False


class UnitFilter(Filter):
    """
    Filter on all variables that are in a specific unit. Eg, filter all variables which
    are in unit $ dollars.
    """
    def __init__(self, *args, **kwargs):
        super(UnitFilter, self).__init__(*args, **kwargs)
        self._type = FilterType.UNIT


class IncludeUnitFilter(UnitFilter):
    """
    Include all variables for a given unit.
    """
    def __init__(self, *args, **kwargs):
        super(IncludeUnitFilter, self).__init__(*args, **kwargs)
        self._include = True


class ExcludeUnitFilter(UnitFilter):
    """
    Exclude all variables for a given unit.
    """
    def __init__(self, *args, **kwargs):
        super(ExcludeUnitFilter, self).__init__(*args, **kwargs)
        self._include = False


class SectorFilter(Filter):
    """
    Filter for all variables in a given sector of a multi-sectoral model.
    """
    def __init__(self, *args, **kwargs):
        super(SectorFilter, self).__init__(*args, **kwargs)
        self._type = FilterType.SECTOR


class IncludeSectorFilter(SectorFilter):
    """
    Include all variables for a given sector.
    """
    def __init__(self, *args, **kwargs):
        super(IncludeSectorFilter, self).__init__(*args, **kwargs)
        self._include = True


class ExcludeSectorFilter(SectorFilter):
    """
    Exclude all variables for a given sector.
    """
    def __init__(self, *args, **kwargs):
        super(ExcludeSectorFilter, self).__init__(*args, **kwargs)
        self._include = False
