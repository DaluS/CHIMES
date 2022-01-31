# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model based on extensive variables.
Inflation not integrated to the process
TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,

        # Stock-flow consistency
        'D': {
            'func': lambda I=0, Pi=0: I - Pi,
            'com': 'Debt as Investment-Profit difference', },
        'K': {
            'func': lambda I=0, itself=0, delta=0, p=1: I/p - itself * delta,
            'com': 'Capital evolution from investment and depreciation', },

        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,



    },

    # Intermediary relevant functions
    'statevar': {

        # Production function and its employement
        'Y': Funcs.ProductionWorkers.Leontiev_Optimised.Y,
        'L': Funcs.ProductionWorkers.Leontiev_Optimised.L,

        # Parametric behavior functions
        'phillips': Funcs.Phillips.div,
        'kappa': Funcs.Kappa.exp,
        'inflation': Funcs.Inflation.markup,
        'I': Funcs.Kappa.ifromkappa,

        # Intermediary variables with their definitions
        'd': Funcs.Definitions.d,
        'pi': Funcs.Definitions.pi,
        'lambda': Funcs.Definitions.lamb,
        'omega': Funcs.Definitions.omega,
        'GDP': Funcs.Definitions.GDPmonosec,

        'c': {
            'func': lambda w=0, a=1: w/a,
            'com': 'price with only labor salary'},

        # Stock-Flow consistency
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },

        # Auxilliary for practical purpose
        'g': {
            'func': lambda I=0, K=1, delta=0, p=1: (I/p - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'param': {
        'b': {
            'value': 0.5,
            'definition': 'plop',
        },
    },
}


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
            'timetrace': [],
            'plotnyaxis': [{'x': 'time',
                           'y': [['lambda', 'omega'],
                                 ['d'],
                                 ['kappa', 'pi'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            'plot3D': [{'x': 'lambda',
                        'y': 'omega',
                        'z': 'd',
                        'cinf': 'pi',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [{'title': '',
                             'lw': 1,       # optional
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
            'plotnyaxis': [{'x': 'time',
                           'y': [['lambda', 'omega'],
                                 ['d'],
                                 ['kappa', 'pi'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            'plot3D': [{'x': 'lambda',
                        'y': 'omega',
                        'z': 'd',
                        'cinf': 'pi',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [{'title': '',
                             'lw': 1,       # optional
                             'idx': 0,      # optional
                             'color': 'k'},  # optional
                            ],
        },
    },
}
