# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model with possibility to get loans at the bank, and have a price dynamics.
              As described by keen + inflation

TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs


# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_Goodwin import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)


# We write the fields we want to add/modify
_GK_LOGICS = {
    'differential': {
        # Stock-flow consistency
        'D': {
            'func': lambda I, Pi: I - Pi,
            'com': 'Debt as Investment-Profit difference', },

        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,
    },

    # Intermediary relevant functions
    'statevar': {
        # Stock-flow consistency
        'Pi': {
            'func': lambda w, GDP, L, r, D: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },

        # Intermediary
        'kappa': Funcs.Kappa.exp,
        'inflation': Funcs.Inflation.markup,
        'I': Funcs.Kappa.ifromkappa,
        'd': Funcs.Definitions.d,

        # Growth manually coded
        'g': {
            'func': lambda Ir, K, delta: (Ir - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'parameter': {},
    'size': {},
}

# We add them explicitely
for category, dic in _GK_LOGICS.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .85*1.19,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 3.01,
            'delta': .0051,
            'k0': -0.00651,
            'k1': np.exp(-5.01),
            'k2': 20.01,
            'r': 0.031,
            'p': 1.31,
            'eta': 0.11,
            'gammai': 0.51,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2},
                       {'x': 'time',
                        'y': [['K', 'Y', 'I', 'Pi'],
                              ['inflation', 'g'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'd',
                    'color': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         'color': 'k'},  # optional
                        ],
        },
    },
    'crisis': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'D': 5,
            'K': 2.9,
            'w': .85*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
            'p': 1.3,
            'eta': 0.1,
            'gammai': 0.5,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2}],
            'phasespace': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'd',
                    'color': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         'color': 'k'},  # optional
                        ],
        },
    },
}
