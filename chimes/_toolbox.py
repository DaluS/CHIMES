import os
import cloudpickle
import numpy as np
from typing import Union


from ._config import config  # _SAVE_FOLDER
from ._core_functions._distribution_generator import *
import inspect
from ._core_functions import _utils

__all__ = [
    'load',
    'generate_dic_distribution'
]


def _GenerateIndividualSensitivity(key: str,
                                   mu: Union[float, list],
                                   sigma: float,
                                   disttype: str = 'normal',
                                   dictpreset={},
                                   N: int = 10) -> dict:
    """
    Generate a preset taking random values from a specified distribution.

    Parameters
    ----------
    key : str
        The field name you want to test the sensitivity.
    mu : float or list
        The first parameter of the distribution (typically the mean).
    sigma : float
        The second parameter of the distribution (typically the standard deviation).
    disttype : str, optional
        The type of distribution from which to select values. Options include:
        'log', 'lognormal', 'log-normal' for lognormal distribution.
        'normal', 'gaussian' for Gaussian distribution.
        'uniform' for uniform distribution.
        'uniform-bounds' for uniform distribution with mu and sigma respectively lower and higher bounds.
        Default is 'normal'.
    dictpreset : dict, optional
        A dictionary where you want to add the distribution values. Default is an empty dictionary.
    N : int, optional
        The number of values you want to select from the distribution. Default is 10.

    Returns
    -------
    dict
        The updated dictionary with the generated distribution values.

    Raises
    ------
    Exception
        If the distribution type is not recognized, an exception is raised.

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """

    # - N (int): The number of values you want to select from the distribution.
    size = list(np.shape(mu))
    sign = np.sign(mu)
    mu = np.abs(mu)

    sigma = np.abs(sigma)
    if not size:
        size = [N]
    size[0] = N

    if disttype in ['log', 'lognormal', 'log-normal']:
        if mu != 0:
            # Calculating entry parameters for moments to be correct
            muu = np.log(mu**2 / np.sqrt(mu**2 + sigma**2))
            sigmaa = np.sqrt(np.log(1 + sigma**2 / mu**2))
            dictpreset[key] = np.random.lognormal(muu, sigmaa, size) * sign
        else:
            dictpreset[key] = 0 * np.random.uniform(0, 0, size=size)
    elif disttype in ['normal', 'gaussian']:
        dictpreset[key] = np.random.normal(mu, sigma, size) * sign
    elif disttype in ['uniform-bounds']:
        dictpreset[key] = np.random.uniform(mu, sigma, size) * sign
    elif disttype in ['uniform']:
        dictpreset[key] = np.random.uniform(mu - sigma / 2, mu + sigma / 2, size) * sign
    else:
        f = generate_dic_distribution.__doc__
        raise Exception(f'wrong distribution type input, see docstring for distribution types: \n {f} maybe your type is wrong ?')

    return dictpreset


def generate_dic_distribution(InputDic: dict[str, dict],
                              dictpreset={},
                              N=10) -> dict[str:np.ndarray]:
    """
    Generate N monte-carlo sampled values in random distributions for each key of the InputDic.

    The characteristics for each distributions is in each dictionary.
    The output of the function can be used as input for as `set.dfields(**output)`.

    Parameters
    ----------
    InputDic : dict
        A dictionary where each key corresponds to a field name and each value is another dictionary 
        containing the parameters for the distribution of that field.
    dictpreset : dict, optional
        A dictionary where you want to add the distribution values. Default is an empty dictionary.
    N : int, optional
        The number of sampled values in each distributions. Default is 10.

    Returns
    -------
    dict
        The updated dictionary with the generated distribution values for each field.

    Notes
    -----
    For each field in InputDic, the function calls _GenerateIndividualSensitivity to generate the distribution values. The docstring is: 

    Author
    ------
    Paul Valcke

    Date
    ----
    OLD
    """
    for key, val in InputDic.items():
        if 'type' in val.keys():
            val['disttype'] = val['type']
    for key, val in InputDic.items():
        dictpreset = _GenerateIndividualSensitivity(key,
                                                    val['mu'],
                                                    val['sigma'],
                                                    disttype=val['disttype'],
                                                    dictpreset=dictpreset,
                                                    N=N)
        dictpreset['nx'] = N
    return dictpreset


generate_dic_distribution.__doc__ += _GenerateIndividualSensitivity.__doc__


def _printsubgroupe(sub, it):
    # Check 9/27/22
    print(f"{3*it*' '}---- {it*'Sub'}group : {sub[0]} {60*'-'}")
    print(str(sub[1].__doc__.replace('\n        ', '')))

    subsubgroup = [f for f in inspect.getmembers(
        sub[1]) if ('_' in f[0] and '__' not in f[0])]
    for sub2 in subsubgroup:
        _printsubgroupe(sub2, it + 1)

    subfunc = [f for f in inspect.getmembers(sub[1]) if '_' not in f[0]]
    col = ['name', 'com', 'function']

    ar2 = [[v[0], v[1]['com'], inspect.getsource(v[1]['func']).split(':')[2].replace('\n', '')
            ] for v in subfunc]

    _utils._get_summary(
        lar=[ar2],
        lcol=[col],
        verb=True,
        returnas=False,
    )

    print('\n')


def load_saved(name: str,
               localsave=True,
               verb=True):
    '''
    Load a .chm file to create a hub. You can create those files, by creating a hub
    `Hub=chm.Hub(modelname)
    Hub.save(name)`

    name if the path to the file. It can be relative, it can be with or without .chm
    verb is a boolean, to get a loaded message or not when load
    '''

    _SAVE_FOLDER = config.get_current('_SAVE_FOLDER')
    _PATH_SAVE = os.path.join(
        os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
        _SAVE_FOLDER)

    # NAME MANAGEMENT
    if (name[-4:] != '.chm' and '.' not in name):
        name = name + '.chm'
    if name[-4:] == '.chm':
        pass
    elif '.' in name:
        raise Exception(f"extension not understood :{name.split('.')[1]}, expected .chm or nothing")

    # RELATIVE PATH
    if localsave:
        address = os.path.join(_PATH_SAVE, name)
    else:
        address = name

    # LOADING FILE
    if verb:
        print('loading:', address)
    with open(address, 'rb') as f:
        file = cloudpickle.load(f)
        hub = file['hub']
        description = file['description']

    # CHECKING INTEGRITY
    if verb:
        print('file Loaded!')
        print('Description:', description)

    return hub
