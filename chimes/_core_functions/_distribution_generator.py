import numpy as np
from typing import Union

"""
This file is practical to generate distributions at the right size for the Hub fields. 
Typically, replace one or multiple values in a dictionary by a distribution of values, with the according size `nx`

Author
------
Paul Valcke

Date
----
OLD
"""


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
