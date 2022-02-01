# -*- coding: utf-8 -*-
"""
DESCRIPTION :
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
        'Lorenz_x': {
            'func': lambda Lorenzsigma=0, Lorenz_y=0, itself=0: Lorenzsigma*(Lorenz_y-itself),
            'com': 'X',
            'initial': 0,
        },
        'Lorenz_y': {
            'func': lambda Lorenzrho=0, Lorenz_x=0, Lorenz_z=0, itself=0: Lorenz_x*(Lorenzrho-Lorenz_z)-itself,
            'com': 'Y',
            'initial': 1,
        },
        'Lorenz_z': {
            'func': lambda Lorenzbeta=0, Lorenz_x=0, Lorenz_y=0, itself=0: Lorenz_x*Lorenz_y-Lorenzbeta*itself,
            'com': 'Z',
            'initial': 1,
        },
    },
    'statevar': {
    },
    'param': {
        'Lorenzrho': {
            'value': 28,
            'definition': 'param1 in lorentz'
        },
        'Lorenzsigma': {
            'value': 10,
            'definition': 'param2 in lorentz'
        },
        'Lorenzbeta': {
            'value': 8/3,
            'definition': 'param3 in lorentz'
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'Canonical': {
        'fields': {
            'Lorenz_x': np.linspace(1, 1.1, 1),
            'Lorenz_y': 1,
            'Lorenz_z': 1,
            'Lorenzsigma': 10,
            'Lorenzrho': 28,
            'Lorenzbeta': 8/3,
        },
        'com': '',
        'plots': [],
    },
}
