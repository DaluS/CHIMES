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
    'differential': {
        'x': {
            'func': lambda lor_sigma, y, x: lor_sigma*(y-x),
            'com': 'X',
            'initial': 0.2,
        },
        'y': {
            'func': lambda lor_rho, x, z, y: x*(lor_rho-z)-y,
            'com': 'Y',
            'initial': .13,
        },
        'z': {
            'func': lambda lor_beta, x, y, z: x*y-lor_beta*z,
            'com': 'Z',
            'initial': .21,
        },
    },
    'statevar': {
    },
    'parameter': {
        'lor_sigma':{
            'value':10,
        },
        'lor_rho': {
            'value': 28,
        },
        'lor_beta': {
            'value': 8/3,
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'Canonical example': {
        'fields': {
        },
        'com': '',
        'plots': [],
    },
}
