# -*- coding: utf-8 -*-

# Here we decide what the user will see
from ._core import Hub
from ._models import get_available_models  # get_dfields_overview
from ._utilities._solvers import get_available_solvers
from ._utilities._saveload import get_available_output, load
from ._models import _DFIELDS
from ._utilities import _utils
from . import _plots as plots
import inspect

import matplotlib.pyplot as plt
import numpy as np

from ._config import _FIELDS_EXPLOREMODEL
from ._config import _FIELDS_SHOWLIST

# #############################################################################

__all__ = [
    'get_available_fields',
    'get_available_plots',
    'get_available_output',
    'generate_preset_from_model_preset',
    'generate_dic_distribution'
]



def get_available_plots():
    # Check 09/27/22
    '''
    Print all the plots routines with their docstring and dependencies
    '''
    all_functions = inspect.getmembers(plots, inspect.isfunction)

    for i in all_functions:
        print(f"##### {i[0]} {'#'*(30-len(i[0]))}####################")
        print( inspect.signature(i[1]))
        print(i[1].__doc__)


def get_available_fields(returnas=False,exploreModels=_FIELDS_EXPLOREMODEL,showModels=_FIELDS_SHOWLIST):
    # Check 09/27/22
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
    models = get_available_models(returnas=list,verb=False)

    if exploreModels+showModels:
        fieldsnotinDfields = []
        if exploreModels:
            for model in models:
                #print(model)
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

    # ------------------
    # get column headers
    col2 = [
        'Field', 'definition', 'group', 'value', 'units', 'In model'

    ]

    # ------------------
    # get values
    ar2 = [
        [k0,
         v0['definition'],
         v0['group'],
         v0['value'],
         v0['units'],
         str(v0['inmodel']) if showModels else (len(v0['inmodel']) if len(v0['inmodel']) else '')
         ]
        for k0, v0 in dparam_sub.items() if v0['group'] != 'Numerical'
    ]

    return _utils._get_summary(
        lar=[ar2],
        lcol=[col2],
        verb=True,
        returnas=returnas,
    )


def generate_preset_from_model_preset(targetmodel,
                                      outputmodel,
                                      targetpreset=False,
                                      targetdpreset=False,
                                      returnas='hub'):
    '''
    Open targetmodel, with or without preset/dpreset, and then gives all necessary
    values to outputmodel so that, if they solve the same equations on different approaches,
    they give the same result

    Please note that if they have different mechanism inside with different
    parameters, you have to manually set them so that they have the same behavior.


    Parameters
    ----------
    targetmodel : model name of the model we will copy the value
        DESCRIPTION.
    targetpreset : the preset name for targetmodel. Optional
        DESCRIPTION. The default is False.
    targetdpreset : the dictionnary preset for targetpreset
        DESCRIPTION. The default is False.
    outputmodel : the name of the model we will use after
        DESCRIPTION.
    returnas : (dict,'hub','dpreset') gives different type of output depending of the situation :
        * dict is a dict of field : value
        * hub is outputmodel loaded with the preset
        * dpreset is a dictionnary with this preset inside
        The default is 'hub'.

    Returns
    -------
    None.

    '''
    # LOADING TARGET
    # IF PRESET AND PRESET FILE GIVEN
    if targetpreset and targetdpreset:
        hub = Hub(targetmodel, preset=targetpreset,
                  dpresets=targetdpreset, verb=False)

    # ELIF PRESET NAME GIVEN
    elif targetpreset:
        hub = Hub(targetmodel, preset=targetpreset, verb=False)

    # ELSE USE OF BASIC VALUES
    else:
        hub = Hub(targetmodel, verb=False)

    hub_output = Hub(outputmodel, verb=False)

    # COPY OF THE PARAMETERS INTO A NEW DICTIONNARY
    FieldToLoad = hub_output.get_dparam(returnas=dict, eqtype=[None, 'ode'])
    # group=('Numerical',),)
    R = hub.get_dparam(returnas=dict)
    tdic = {}
    for k, v in FieldToLoad.items():
        val = R[k]['value']
        if 'initial' in v.keys():
            tdic[k] = val[0][0]
        else:
            tdic[k] = val
    _DPRESETS = {'Copy'+targetmodel: {'fields': tdic, }, }

    if returnas == dict:
        return tdic
    if returnas == 'hub':
        return Hub(outputmodel, preset='Copy'+targetmodel,
                   dpresets=_DPRESETS, verb=False)
    if returnas == 'preset':
        return _DPRESETS


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
    return dictpreset

