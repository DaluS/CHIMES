# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modification of a Goodwin in which we put a buffer for capital :
        investment first go into the buffer then into capital

LINKTOARTICLE: Nothing has been published

@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_G import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)


# We write the fields we want to add/modify
_CES_LOGICS = {
    'ode': {
        'B': Funcs.Kappa.bfromIr,
        'K': Funcs.Kappa.kfromB,
    },
    'param': {
        'tauK': {'value': 1,
                 'definition': 'typical time for capital to be effective'}}
}

# We add them explicitely
for category, dic in _CES_LOGICS.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'B': {
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

            'B': 0.1,
            'tauK': 0.1
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'plotnyaxis': [{'x': 'time',
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
            'plot3D': [{'x': 'lamb0',
                        'y': 'omega',
                        'z': 'lambda',
                        'cinf': 'time',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [],
        },
    },
}
