"""
It is the reduced version of a Goodwin model, with another writing : when the model is established,
one can rather than calculate (N,a,K,w), calculate the dynamics only on employment and wage share.
In consequence it is a 2- differential equation model, but with the same dynamics as _model_goodwin.

The rest of the documentation is in _model_Goodwin

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
    'differential': {
        # Exogenous entries in the model
        'y': {
            'func' : lambda y,noisamp: y*noisamp,
            'com' : "noise on growth rate",
            'initial': 1,
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'noisamp' :{
            'func':  lambda nx,nr,noise : noise*np.random.normal(loc=0,size=(nx, nr, 1, 1)),
        },
    },
    'parameter': {
        'noise': {'value':0.5,
                  'definition': 'noise amplitude on growth rate'}

    },
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'Onevar': {
        'fields': {
            'y':1,
            'nx':1,
            'noise':1,
            },
        'com':'One variable',
        'plots': {'Var': [{'key':'y',
                           'mode':'sensitivity'}] },
    },
    '10': {
        'fields': {
            'y': 1,
            'nx': 10,
            'noise': 1,
            'dt':0.01,
        },
        'com': 'One hundred parrallel run',
        'plots': {'Var': [{'key': 'y',
                           'mode': 'sensitivity'}]}

        }
}
