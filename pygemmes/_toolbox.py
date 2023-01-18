

from ._core import Hub
from ._models import get_available_models  
from ._models import _DFIELDS
from ._utilities import _utils
from . import _plots as plots
import inspect
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from ._config import _FIELDS_EXPLOREMODEL

# FULLY CHECKED DECEMBER 2022 
# #############################################################################

__all__ = [
    'get_available_fields',
    'get_available_plots',
    'generate_dic_distribution'
]

def get_available_plots():
    # Check 01 2023
    '''
    Print all the plots routines with their docstring and dependencies
    '''
    all_functions = inspect.getmembers(plots, inspect.isfunction)

    dic={i[0]: {'documentation': i[1].__doc__,
                'signature': inspect.signature(i[1])}  for i in all_functions}
    plotdf=pd.DataFrame(dic)
    return plotdf.transpose().style.set_properties(**{'text-align': 'left'})


def get_available_fields(exploreModels=_FIELDS_EXPLOREMODEL):
    # Check 2022
    '''
    Will load the library of fields, then all available models,
    and will print the ensemble of fields with their properties and the models they are in.

    * returnas can be used on "list,dict"
    * Exploremodels will read all models to check the variables defined inside
    * showModels will show you the list of models that use this field

    if a field has no group, then it is only defined in model files
    '''

    # INITIALIZE
    dparam_sub = _DFIELDS
    for key, val in dparam_sub.items():
        dparam_sub[key]['inmodel'] = []
    models = get_available_models(Return=list,verb=False)



    if exploreModels:
        fieldsnotinDfields = []
        if exploreModels:
            for model in models:
                hub = Hub(model, verb=False)
                params = hub.get_dparam(returnas=dict)
                for key in params.keys():
                    if key in dparam_sub:
                        if 'inmodel' not in dparam_sub[key].keys():
                            dparam_sub[key]['inmodel'] = []
                        dparam_sub[key]['inmodel'].append(model)
                    else:
                        fieldsnotinDfields.append([key.ljust(20), model])

    print(f'{len(dparam_sub)} fields in the library \n')

    dic = {k0:{
            'definition':v0['definition'], 
            'group':v0['group'],
            'value':v0['value'], 
            'units':v0['units'], 
            'In model': str(v0['inmodel'])}
              for k0, v0 in dparam_sub.items() if v0['group'] != 'Numerical'}
    modeldf=pd.DataFrame(dic)
    return modeldf.transpose()#.style.set_properties(**{'text-align': 'left'})


def _GenerateIndividualSensitivity(key, mu, sigma, disttype='normal', dictpreset={}, N=10):
    '''
    Generate a preset taking random values in one distribution.

    INPUT :
        * key : the field name you want to test the sensitivity
        * mu : the first parameter of your distribution (mean typically)
        * sigma : the second parameter of your distribution (std typically)
        * dispreset : dictionnary you want to add the distribution in
        * disttype : the type of distribution you pick the value on :
            1. 'log','lognormal','log-normal' for lognormal distribution
            2. 'normal','gaussian' for gaussian distribution
        * N : the number of value you want to pick

        IF THE DISTRIBUTION IS LOG, then mu is the median value

    '''
    if disttype in ['log', 'lognormal', 'log-normal']:
        dictpreset[key] = np.random.lognormal(np.log(mu), sigma, N)
    elif disttype in ['normal', 'gaussian']:
        dictpreset[key] = np.random.normal(mu, sigma, N)
    elif disttype in ['uniform']:
        dictpreset[key] = np.random.uniform(mu, sigma, N)
    else:
        raise Exception('wrong distribution type input')
    return dictpreset


def generate_dic_distribution(InputDic, dictpreset={}, N=10):
    '''
    Wrapup around GenerateIndividualSensitivity function, to generate multiple distributions entangled.

    InputDic should look like :
        {
        'alpha': {'mu': .02,
                  'sigma': .2,
                  'type': 'normal'},
        'k2': {'mu': 20,
               'sigma': .2,
               'type': 'log'},
        'mu': {'mu': 1.3,
               'sigma': .2,
               'type': 'uniform'},
        }

    'type' can be :
        1. 'log','lognormal','log-normal' for lognormal distribution
        2. 'normal','gaussian' for gaussian distribution
        3. 'uniform' for uniform distribution in interval [mu,sigma]

    Be careful, grid will generate N**len(InputDic.key()) run if activated !

    GenerateIndividualSensitivity :
        Generate a preset taking random values in one distribution.

    INPUT :
        * mu : the first parameter of your distribution (mean typically)
        * sigma : the second parameter of your distribution (std typically)
        * dispreset : dictionnary you want to add the distribution in
        * disttype : the type of distribution you pick the value on :
            1. 'log','lognormal','log-normal' for lognormal distribution
            2. 'normal','gaussian' for gaussian distribution
        * N : the number of value you want to pick

        IF THE DISTRIBUTION IS LOG, then mu is the median value
    '''
    dictpreset = {}
    for key, val in InputDic.items():
        dictpreset = _GenerateIndividualSensitivity(key,
                                                    val['mu'],
                                                    val['sigma'],
                                                    disttype=val['type'],
                                                    dictpreset=dictpreset,
                                                    N=N)
        dictpreset['nx']=N
    return dictpreset

