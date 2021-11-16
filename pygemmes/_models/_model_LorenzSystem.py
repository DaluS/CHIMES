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
        'x': {
            'func': lambda sigma=0, y=0, itself=0: sigma*(y-itself),
            'com': 'X coordinate',
            'initial': 0,
        },
        'y': {
            'func': lambda rho=0, x=0, z=0, itself=0: x*(rho-z)-itself,
            'com': 'Y coordinate',
            'initial': 1,
        },
        'z': {
            'func': lambda beta=0, x=0, y=0, itself=0: x*y-beta*itself,
            'com': 'Z coordinate',
            'initial': 1,
        },
    },
    'statevar': {
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'Canonical example': {
        'fields': {
            'x': np.linspace(1, 1.1, 10),
            'y': 1,
            'z': 1,
            'sigma': 10,
            'rho': 28,
            'beta': 8/3,
        },
        'com': '',
        'plots': [],
    },
}
