
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin : the perception of employement in
    the Phillips curve has a slight relaxation of a time taulamb : typically it takes
    two years for employement to impact salary negocation

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from chimes.libraries import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from chimes.libraries._model_G import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)


# We add our modifications
# We use lambda0 as the previous lambda measure (it is the instant employement felt)
_LOGICS['statevar']['lamb0'] = Funcs.Definitions.lamb

# We remove lambda from statevar as there is now inertia in it, We place it in 'ode'
_LOGICS['statevar'].pop('employment', None)
_LOGICS['ode']['employment'] = Funcs.Phillips.lambdarelax
_LOGICS['ode']['employment']['initial'] = .91
_LOGICS['param']['taulamb'] = {'value': 0.01,
                               'definition': 'typical time for employement to impact salary nego'}


_LOGICS['ode']['w'] = Funcs.Phillips.salaryfromPhillipsProfitsNoInflation
_LOGICS['ode']['a'] = Funcs.Productivity.verdoorn
_LOGICS['param']['beta'] = {'value': 0.1,
                            'definition': 'impact of growth in productivity increase'}
_LOGICS['param']['zpi'] = {'value': 1,
                           'definition': 'impact of profit in salary negociation'}


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'taulamb': {
        'fields': {
            'dt': 0.01,
            'Tsim': 100,

            'a': 1,
            'N': 1,
            'K': 2.75,
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,

            'employment': 0.9166,
            'taulamb': [0.2, 0.3, 0.4],

            'beta': 0,

            'zpi': 1,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'lamb0'],
                              ['omega'],
                              ],
                        'idx': 0,
                        'title': '',
                        'lw': 1}],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'color': 'time',
                    'idx': 0}],
            'XYZ': [{'x': 'lamb0',
                     'y': 'omega',
                     'z': 'employment',
                     'cinf': 'time',
                     'cmap': 'jet',
                     'index': 0,
                     'title': ''}],
            'byunits': [],
        },
    },
}
