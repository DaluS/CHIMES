# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model with possibility to get loans at the bank, and have a price dynamics.
TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

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
_GK_LOGICS = {
    'ode': {
        # Stock-flow consistency
        'D': {
            'func': lambda I=0, Pi=0: I - Pi,
            'com': 'Debt as Investment-Profit difference', },

        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,



    },

    # Intermediary relevant functions
    'statevar': {
        # Stock-flow consistency
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },

        # Intermediary
        'kappa': Funcs.Kappa.exp,
        'inflation': Funcs.Inflation.markup,
        'I': Funcs.Kappa.ifromkappa,
        'd': Funcs.Definitions.d,

        # Growth manually coded
        'g': {
            'func': lambda Ir=0, K=1, delta=0: (Ir - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'param': {
    },
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
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
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
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                           'y': [['lambda', 'omega'],
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
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                        'y': 'omega',
                        'z': 'd',
                        'cinf': 'pi',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'byunits': [{'title': '',
                             'lw': 2,       # optional
                             'idx': 0,      # optional
                             'color': 'k'},  # optional
                            ],
            'cycles_characteristics': [{'xaxis': 'omega',
                                        'yaxis': 'lambda',
                                        'ref': 'lambda'}
                                       ]
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
                        'y': [['lambda', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                    'y': 'omega',
                    'z': 'd',
                    'cinf': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         'color': 'k'},  # optional
                        ],
            'cycles_characteristics': [{'xaxis': 'omega',
                                        'yaxis': 'lambda',
                                        'ref': 'lambda'}
                                       ]
        },
    },
}
