
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
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'Canonical example': {
        'fields': {
            'dt':0.01,
            'lor_sigma':10,
            'lor_rho': 28,
            'lor_beta':  8/3,
        },
        'com': 'Chaotic attractor around two equilibrium, for those parameter values',
        'plots': {
                'XYZ': [{'x': 'x',
                    'y': 'y',
                    'z': 'z',
                    'color': 'time',
                    'cmap': 'jet',
                    'index': 0,
                    'title': 'Lorenz 3-dimension strange attractor'}],
                'XY': [{
                    'y': [['y'],['x','z']],
                    'color': 'time',
                    'cmap': 'jet',
                    'index': 0,
                    'title': 'Multiple axis plot'}],
                'plotnyaxis': [{''}]
                },
    },
}
