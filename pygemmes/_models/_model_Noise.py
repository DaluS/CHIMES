# -*- coding: utf-8 -*-
"""
ABSTRACT :
    It is just as extremely simple model with stochastic noise to show that we can do that as all
    posh people do. The equation solved here is y'=y*noise, with noise being a gaussian noise.

    YES YOU ARE DOING FANCY FINANCE, NOW ASK FOR A LOT OF MONEY FOR SENSELESS SIMULATIOOOOOONS


Created on Sun 32/12 23:59:59 2021

@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


#_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'y': {
            'func': lambda itself=0, Noisesigma=0: itself * Noisesigma * np.random.normal(),
            'com': 'exponential noise !',
            'initial': 1,
        },
    },
    'statevar': {
    },
    'param': {
        'Noisesigma': {
            'value': 1,
            'definition': 'gaussian noise amplitude',
        },
    }
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {},
    'com': ''},
}
