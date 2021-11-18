# -*- coding: utf-8 -*-
"""
DESCRIPTION : Just the description of a second order ODE y''+2*gamma*y + Omega^2 y = 1
The criteria for the qualitative behavior Delta = gamma-Omega2
    * Delta = 0 Critcal
    * Delta > 0 Overdamped
    * Delta < 0 Underdamped
TYPICAL BEHAVIOR : Dampening oscillations
@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'thetap': {
            'func': lambda Final=1, itself=0, Omega=0, gamma=0, theta=0: -Omega**2*(theta-Final) - 2*gamma*itself,
            'com': 'Exogenous technical progress as an exponential',
            'initial': 0,
        },
        'theta': {
            'func': lambda thetap=0: thetap,
            'com': 'Exogenous population as an exponential',
            'initial': 1,
        },
    },
    'statevar': {
        'Energy': {
            'func': lambda theta=0, thetap=0, Omega=0, Final=0: Omega*(theta-Final)**2+thetap**2,
            'com': 'Energy',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'Perfect Oscillations': {
        'fields': {
            'thetap': [0, 0, 0],
            'theta': [1, 2, 0],
            'Final': [1, 0, 0],
            'Omega': 10,
            'gamma': 0,
        },
        'com': '',
        'plots': [],
    },
    'FirstOrder': {
        'fields': {
            'thetap': [0, 0, 0],
            'theta': [1, 2, 0],
            'Final': [1, 0, 0],
            'Omega': 0,
            'gamma': 1,
        },
        'com': '',
        'plots': [],
    },
    "Overdamp": {
        'fields': {
            'thetap': [0, 0, 0],
            'theta': [1, 2, 0],
            'Final': [1, 0, 0],
            'Omega': 0.1,
            'gamma': 1,
        },
        'com': '',
        'plots': [],
    },

    'Critical': {
        'fields': {
            'thetap': [0, 0, 0],
            'theta': [1, 2, 0],
            'Final': [1, 0, 0],
            'Omega': 1,
            'gamma': 1,
        },
        'com': '',
        'plots': [],
    },
    'Underdamped': {
        'fields': {
            'thetap': [0, 0, 0],
            'theta': [1, 2, 0],
            'Final': [1, 0, 0],
            'Omega': 1,
            'gamma': 0.1,
        },
        'com': '',
        'plots': [],
    },
}
