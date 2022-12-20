# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin-Keen. Assume that labour productivity (parameter a in our basic model) is not exogenous 
    but depends upon the growth rate of investment (in R & D). This leads to adding the following equation:
    dot(a) / a = alpha + beta * g



TYPICAL BEHAVIOR: Locally Unstable, the good equilibrium is an unstable focuse


@author: Weiye Zhu
"""


# ######################## PRELIMINARY ELEMENTS #########################

import sys 

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel


# ######################## LOGICS #######################################
_LOGICS,_PRESETS0= importmodel('GK')
_GKEndo_LOGICS = {
    'differential': {
        # Endogenous Labor Productivity
        'a': {
            'func': lambda a, alpha, beta, g: a*(alpha + beta * g),
            'com': 'Labor Productivity depends on investment', },

    }
}

_LOGICS = mergemodel(_LOGICS, _GKEndo_LOGICS, verb=False) 
_PRESETS=_PRESETS0
'''
# ####################### PRESETS #######################################
plotdict= {
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
                        'log':[False,False],
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
                         },  # optional
                        ],
        }



_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .85*1.19,
            'alpha': 0.0251,
            'beta': 0.,
            'n': 0.0251,
            'nu': 3.01,
            'delta': .051,
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
        'plots': plotdict,
    },
    'defaultGK': {
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
            'beta':0.,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': plotdict,
    },
    'farfromEQ': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'D': 5,
            'K': 2.1,
            'w': .85*1.2,
            'alpha': 0.025,
            'beta': 0.5,
            'n': 0.02,
            'nu': 3,
            'delta': .081,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
            'p': 1.3,
            'eta': 0.1,
            'gammai': 0.5,
        },
        'com': (
            'Far from equilibrium run'),
        'plots': plotdict,
    },
    'crisis': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'D': 5,
            'K': 2.1,
            'w': .78 ,
            'alpha': 0.025,
            'beta': 0.5,
            'n': 0.02,
            'nu': 3,
            'delta': .08,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
            'p': 1.3,
            'eta': 0.1,
            'gammai': 0.5,
        },
        'com': ('Slowly diverging to crisis'),
        'plots': plotdict,
    },
}
'''