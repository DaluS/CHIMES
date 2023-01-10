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
        'employment': {
            'func' : lambda employment, newalpha,beta,delta,omega,nu: employment*( (1-omega)/nu - newalpha - beta - delta),
            'com' : "reduced 2-var system",
        },
        'omega': {
            'func' : lambda omega, phillips,newalpha: omega*(phillips-newalpha),
            'com' : 'reduced 2-var system',
        },
        'noisecumulate': {
            'func': lambda noise,nx,nr: noise*np.random.normal(size=(nx, nr, 1, 1)),
            'initial': 0,
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'phillips': Funcs.Phillips.div,
        'newalpha': {
            'func': lambda alpha, noise, nx, nr: alpha * (1 + noise*np.random.normal(size=(nx, nr, 1, 1))),

        'com': 'alpha coefficient with a percentage of noise',
        'definition': 'technical progress rate with noise',
        'units':'y^{-1}',
        'symbol': r'$\alpha_{\sigma}$'
        },
    },
    'parameter': {
        'noise': {'value':0.5,
                  'definition': 'noise amplitude on alpha'}
    },
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
