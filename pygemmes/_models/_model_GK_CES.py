# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin : the Leontiev optimised function has been
    replaced by a CES (its generalisation). We

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_GK import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)


# We write the fields we want to add/modify
_CES_LOGICS = {
    'statevar': {
        # Characteristics of a CES
        'cesLcarac': Funcs.ProductionWorkers.cesLcarac,
        'cesYcarac': Funcs.ProductionWorkers.cesYcarac,
        'omegacarac': Funcs.ProductionWorkers.omegacarac,

        # From it are deduced optimised quantities
        'nu': Funcs.ProductionWorkers.CES_Optimised.nu,
        'l': Funcs.ProductionWorkers.CES_Optimised.l,

        # From it are deduced Labor and Output
        'Y': Funcs.ProductionWorkers.CES_Optimised.Y,
        'L': Funcs.ProductionWorkers.CES_Optimised.L,
    },
}

# We add them explicitely
for category, dic in _CES_LOGICS.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'CES': {
        'fields': {
            'dt': 0.01,
            'Tmax': 100,

            'a': 1,
            'N': 1,
            'K': 2.75,
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'delta': .005,
            'phinull': 0.1,

            'CESexp': 1000,
            'A': 1/3,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                           'y': [['lambda', 'lamb0'],
                                 ['omega'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            '3D': [{'x': 'lamb0',
                        'y': 'omega',
                        'z': 'lambda',
                        'cinf': 'time',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'byunits': [],
        },
    },
}
