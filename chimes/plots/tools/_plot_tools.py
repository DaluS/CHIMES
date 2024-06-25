"""
Visualization Toolbox Module

This module provides utility functions for visualization tasks. It includes functions for plotting
lines with different colorings, finding corresponding indices in a simulation model, expanding
multisectoral keys, and fetching values from a model dictionary.

Contents:
    - _multiline: Plot lines with different colorings, to be used within another plot.
    - _indexes: Find the corresponding indices for given input parameters in a simulation model.
    - _key: Expand a key input in case it's multisectoral.
    - fetch_value: Fetch values from the 'dfields' dictionary in a model and return the values of a key.

Author:
    Paul Valcke

Last Modified:
    Date: 2024-01-19
"""

import numpy as np
from typing import Union, List, Tuple
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Linestyles for matplotlib
_LS = [
    (0, ()),
    (0, (1, 1)),
    (0, (5, 1)),  # densely dashed
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (5, 5)),
    (0, (3, 5, 1, 5)),
    (0, (3, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
    (0, (1, 5)),  # dotted
    (0, (5, 10)),
    (0, (5, 5))
]

# Linestyles for plotly
_plotly_dashstyle = ['solid',
                     'dot',
                     'dash',
                     'longdash',
                     'dashdot']

# Colors for plotly
_plotly_colors = [
    'rgba(31, 119, 180, 0.5)',    # Blue
    'rgba(255, 127, 14, 0.5)',    # Orange
    'rgba(44, 160, 44, 0.5)',     # Green
    'rgba(214, 39, 40, 0.5)',     # Red
    'rgba(148, 103, 189, 0.5)',   # Purple
    'rgba(140, 86, 75, 0.5)',     # Brown
    'rgba(227, 119, 194, 0.5)',   # Pinkish Purple
    'rgba(127, 127, 127, 0.5)',   # Gray
    'rgba(188, 189, 34, 0.5)',    # Olive Green
    'rgba(23, 190, 207, 0.5)',    # Turquoise
    'rgba(255, 0, 255, 0.5)',     # Magenta
    'rgba(0, 255, 255, 0.5)',     # Cyan
    'rgba(255, 255, 0, 0.5)',     # Yellow
    'rgba(127, 255, 127, 0.5)',   # Light Green
    'rgba(0, 0, 0, 0.5)',         # Black
    'rgba(127, 255, 255, 0.5)',   # Light Blue
    'rgba(255, 127, 255, 0.5)',   # Light Purple
    'rgba(255, 200, 0, 0.5)',     # Orange
    'rgba(200, 200, 0, 0.5)',     # Yellow-Green
    'rgba(255, 182, 193, 0.5)',   # Pink
]


def _multiline(xs: List[Union[List[float], np.ndarray]],
               ys: List[Union[List[float], np.ndarray]],
               c: List[float],
               ax: plt.Axes = None,
               **kwargs) -> LineCollection:
    """
    Plot lines with different colorings, to be used within another plot.

    Parameters
    ----------
    xs : List[Union[List[float], np.ndarray]]
        Iterable container of x coordinates.
    ys : List[Union[List[float], np.ndarray]]
        Iterable container of y coordinates.
    c : List[float]
        Iterable container of numbers mapped to colormap.
    ax : plt.Axes, optional
        Axes to plot on.
    kwargs : optional
        Passed to LineCollection.

    Notes
    -----
    len(xs) == len(ys) == len(c) is the number of line segments.
    len(xs[i]) == len(ys[i]) is the number of points for each line (indexed by i).

    Returns
    -------
    lc : LineCollection instance.

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """
    # Find axes
    ax = plt.gca() if ax is None else ax

    # Create LineCollection
    segments = [np.column_stack([x, y]) for x, y in zip(xs, ys)]
    lc = LineCollection(segments, **kwargs)

    # Set coloring of line segments
    lc.set_array(np.asarray(c))

    # Add lines to axes and rescale
    ax.add_collection(lc)
    ax.autoscale()
    return lc


def _indexes(hub,
             idx: Union[int, str] = 0,
             Region: Union[int, str] = 0,
             tini: Union[bool, int, float] = False,
             tend: Union[bool, int, float] = False,
             returnas='Tuple'):
    """
    Find the corresponding indices for the given input parameters.

    Parameters
    ----------
    hub : chm.Hub
        The simulation hub.
    idx : Union[int, str]
        The parallel system index or name.
    Region : Union[int, str]
        The regional system index or name.
    tini : Union[bool, int, float]
        Initial time for the search. It can be an int (iteration number),
        a float (time value), or a Bool (maximum simulated domain).
    tend : Union[bool, int, float]
        End time for the search. It can be an int (iteration number),
        a float (time value), or a Bool (maximum simulated domain).
    returnas : str, optional
        Choose whether you return it as a tuple or as a dictionary.
        Dictionary is recommended when you put it directly as input into another function.

    Returns
    -------
    Union[tuple, Dict[str, int]]
        A tuple or dictionary containing the simulation hub, parallel system index, 
        regional system index, initial time index, and end time index.

    Notes
    -----
    - The `idx` and `Region` parameters can be either integers or strings.
    - If strings are provided, they should match the names of the parallel
      and regional systems, respectively.
    - The `tini` and `tend` parameters can be integers (iteration numbers),
      floats (time values), or Booleans (for maximum simulated domain).
    - This function do not accept vectorisation of inputs: use it in a for loop

    Examples
    --------
    >>> _indexes(hub)  # Returns the default indices [0, 0, 0, -1]
    >>> _indexes(hub, 'parallel3', 'USA')  # Returns indices for 'parallel3' and 'USA'
    >>> _indexes(hub, 'parallel3', 'USA', returnas='dict')  # Returns indices as a dictionary

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """
    R = hub.dfields

    if not hub.dflags['run'][0]:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()

    # idx input
    if type(idx) is int or isinstance(idx, np.integer):
        pass
    elif type(idx) is str:
        try:
            idx = R['nx']['list'].index(idx)
        except ValueError:
            liste = R['nx']['list']
            raise Exception(f'The parallel system cannot be found!\nYou gave {idx} in {liste}')
    else:
        raise Exception(f'The parallel index cannot be understood! You gave {idx} of type {type(idx)}')

    # Region input
    if type(Region) is int or isinstance(Region, np.integer):
        pass
    elif type(Region) is str:
        try:
            Region = R['nr']['list'].index(Region)
        except ValueError:
            liste = R['nr']['list']
            raise Exception(f'The region system cannot be found!\nYou gave {Region} in {liste}')
    else:
        raise Exception(f'The region index cannot be understood! You gave {Region} of type {type(Region)}')

    time = R['time']['value'][:, idx, Region, 0, 0]
    if type(tini) is float:
        idt0 = np.argmin(np.abs(time - tini))
    elif type(tini) is bool:
        idt0 = 0
    elif type(tini) is int:
        idt0 = tini
    else:
        raise Exception(f'Tini could not be understood ! You gave {tini}')

    if type(tend) is float:
        idt1 = np.argmin(np.abs(time - tend))
    elif type(tend) is bool:
        idt1 = hub.dflags['run'][0]
    elif type(tend) is int:
        idt1 = tend
    else:
        raise Exception(f'Tend could not be understood ! You gave {tend}')

    if returnas == 'Tuple':
        return hub, idx, Region, idt0, idt1
    elif returnas == 'Dict':
        return dict(hub=hub, idx=idx, Region=Region, idt0=idt0, idt1=idt1)
    else:
        raise ValueError(f"Invalid value for 'returnas' ({returnas}). Choose 'Tuple' or 'Dict'.")


def _key(R: dict, key: [str, list]):
    """
    Expand a key input in case it's multisectoral.

    Parameters
    ----------
    R : dict
        The dictionary containing information about the model structure.
    key : Union[str, List[str]]
        The key to expand. If a list, the first element is the key, and the second is the sector name.

    Returns
    -------
    Tuple[str, int, str]
        A tuple containing the original key, the sector index, and the sector name.

    Notes
    -----
    - If `key` is a list, the first element will be the key, and the second one will be the name of the sector.
    - If `key` is a string, it will be treated as a single-sector key.

    Examples
    --------
    >>> _key(R, 'keyname')  # return ('keyname', 0, '')
    >>> _key(R, ['keyname', 'sectorname'])  # return ('keyname', sector_index, 'sectorname')

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """
    if isinstance(key, list):
        key_sector = R[R[key[0]]['size'][0]]['list'].index(key[1])
        key, key_name = key[0], key[1]
    else:
        key_sector, key_name = 0, ''

    return key, key_sector, key_name


def value(R: dict,
          key: str,
          tini: int = 0,
          tend: int = -1,
          idx: Union[int, np.array, Tuple, bool] = 0,
          region: Union[int, np.array, Tuple, bool] = 0,
          ms1: Union[int, np.array, Tuple, list, bool] = 0,
          ms2: Union[int, np.array, Tuple, list, bool] = 0
          ) -> np.ndarray:
    """
    Fetch values from the 'dfields' dictionary 'R' and return the values of 'key'.
    If 'key' is a parameter, return an array of its value with the same size as the time vector. 
    if idx,region,ms1,ms2 is True, return the full dimension

    Parameters
    ----------
    R : dict
        The dictionary containing information about the model.
    key : str
        The key to fetch values from.
    tini : int, optional
        Initial time index, by default 0.
    tend : int, optional
        End time index, by default -1.
    idx : Union[int, np.array, Tuple, list], optional
        Index or indices along the first dimension, by default 0.
    region : Union[int, np.array, Tuple, list], optional
        Index or indices along the second dimension, by default 0.
    ms1 : Union[int, np.array, Tuple, list], optional
        Index or indices along the third dimension, by default 0.
    ms2 : Union[int, np.array, Tuple, list], optional
        Index or indices along the fourth dimension, by default 0.

    Returns
    -------
    np.ndarray
        The fetched values.

    Notes
    -----
    - The function fetches values from the 'dfields' dictionary based on the provided indices and key.
    - If 'key' is a tensored key, it returns a sliced array based on the specified indices.

    Examples
    --------
    >>> fetch_value(R, 'keyname')  # return array for the key 'keyname' with default indices
    >>> fetch_value(R, 'region_key', idx=[0, 1], region=[2, 3])  # return sliced array for multiregion

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """

    dic = R[key]

    # Boolean management and parameters management
    if (type(idx) is bool and idx is True):
        idx = np.arange(len(dic['value'][0, :, 0, 0, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][:, 0, 0, 0]))
    if (type(region) is bool and region is True):
        region = np.arange(len(dic['value'][0, 0, :, 0, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, :, 0, 0]))
    if (type(ms1) is bool and ms1 is True):
        ms1 = np.arange(len(dic['value'][0, 0, 0, :, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, 0, :, 0]))
    if (type(ms2) is bool and ms2 is True):
        ms2 = np.arange(len(dic['value'][0, 0, 0, 0, :])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, 0, 0, :]))

    if dic.get('eqtype', None) is None:
        t = R['time']['value'][tini:tend, 0, 0, 0, 0]
        V = np.expand_dims(dic['value'], axis=0)
        V2 = np.tile(V, (len(t),) + (1,) * len(np.shape(dic['value'])))
        return V2[tini:tend, idx, region, ms1, ms2]
    else:
        return dic['value'][tini:tend, idx, region, ms1, ms2]
###############################################################################################################################


# Linestyles for matplotlib
_LS = [
    (0, ()),
    (0, (1, 1)),
    (0, (5, 1)),  # densely dashed
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (5, 5)),
    (0, (3, 5, 1, 5)),
    (0, (3, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
    (0, (1, 5)),  # dotted
    (0, (5, 10)),
    (0, (5, 5))
]

# Linestyles for plotly
_plotly_dashstyle = ['solid',
                     'dot',
                     'dash',
                     'longdash',
                     'dashdot']

# Colors for plotly
_plotly_colors = [
    'rgba(31, 119, 180, 0.5)',    # Blue
    'rgba(214, 39, 40, 0.5)',     # Red
    'rgba(255, 127, 14, 0.5)',    # Orange
    'rgba(44, 160, 44, 0.5)',     # Green
    'rgba(148, 103, 189, 0.5)',   # Purple
    'rgba(140, 86, 75, 0.5)',     # Brown
    'rgba(227, 119, 194, 0.5)',   # Pinkish Purple
    'rgba(127, 127, 127, 0.5)',   # Gray
    'rgba(188, 189, 34, 0.5)',    # Olive Green
    'rgba(23, 190, 207, 0.5)',    # Turquoise
    'rgba(255, 0, 255, 0.5)',     # Magenta
    'rgba(0, 255, 255, 0.5)',     # Cyan
    'rgba(255, 255, 0, 0.5)',     # Yellow
    'rgba(127, 255, 127, 0.5)',   # Light Green
    'rgba(0, 0, 0, 0.5)',         # Black
    'rgba(127, 255, 255, 0.5)',   # Light Blue
    'rgba(255, 127, 255, 0.5)',   # Light Purple
    'rgba(255, 200, 0, 0.5)',     # Orange
    'rgba(200, 200, 0, 0.5)',     # Yellow-Green
    'rgba(255, 182, 193, 0.5)',   # Pink
]


def value(R: dict,
          key: str,
          tini: int = 0,
          tend: int = -1,
          idx: Union[int, np.array, Tuple, bool] = 0,
          region: Union[int, np.array, Tuple, bool] = 0,
          ms1: Union[int, np.array, Tuple, list, bool] = 0,
          ms2: Union[int, np.array, Tuple, list, bool] = 0
          ) -> np.ndarray:
    """
    Fetch values from the 'dfields' dictionary 'R' and return the values of 'key'.
    If 'key' is a parameter, return an array of its value with the same size as the time vector. 
    if idx,region,ms1,ms2 is True, return the full dimension

    Parameters
    ----------
    R : dict
        The dictionary containing information about the model.
    key : str
        The key to fetch values from.
    tini : int, optional
        Initial time index, by default 0.
    tend : int, optional
        End time index, by default -1.
    idx : Union[int, np.array, Tuple, list], optional
        Index or indices along the first dimension, by default 0.
    region : Union[int, np.array, Tuple, list], optional
        Index or indices along the second dimension, by default 0.
    ms1 : Union[int, np.array, Tuple, list], optional
        Index or indices along the third dimension, by default 0.
    ms2 : Union[int, np.array, Tuple, list], optional
        Index or indices along the fourth dimension, by default 0.

    Returns
    -------
    np.ndarray
        The fetched values.

    Notes
    -----
    - The function fetches values from the 'dfields' dictionary based on the provided indices and key.
    - If 'key' is a tensored key, it returns a sliced array based on the specified indices.

    Examples
    --------
    >>> fetch_value(R, 'keyname')  # return array for the key 'keyname' with default indices
    >>> fetch_value(R, 'region_key', idx=[0, 1], region=[2, 3])  # return sliced array for multiregion

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """

    dic = R[key]

    # Boolean management and parameters management
    if (type(idx) is bool and idx is True):
        idx = np.arange(len(dic['value'][0, :, 0, 0, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][:, 0, 0, 0]))
    if (type(region) is bool and region is True):
        region = np.arange(len(dic['value'][0, 0, :, 0, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, :, 0, 0]))
    if (type(ms1) is bool and ms1 is True):
        ms1 = np.arange(len(dic['value'][0, 0, 0, :, 0])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, 0, :, 0]))
    if (type(ms2) is bool and ms2 is True):
        ms2 = np.arange(len(dic['value'][0, 0, 0, 0, :])) if dic.get('eqtype', None) is not None \
            else np.arange(len(dic['value'][0, 0, 0, :]))

    if dic.get('eqtype', None) is None:
        t = R['time']['value'][tini:tend, 0, 0, 0, 0]
        V = np.expand_dims(dic['value'], axis=0)
        V2 = np.tile(V, (len(t),) + (1,) * len(np.shape(dic['value'])))
        return V2[tini:tend, idx, region, ms1, ms2]
    else:
        return dic['value'][tini:tend, idx, region, ms1, ms2]
