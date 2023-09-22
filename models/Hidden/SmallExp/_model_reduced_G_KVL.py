"""
It is the reduced version of a Goodwin model, with another writing : when the model is established,
one can rather than calculate (N,a,K,w), calculate the dynamics only on employment and wage share.
In consequence it is a 2- differential equation model, but with the same dynamics as _model_goodwin.

The rest of the documentation is in _model_Goodwin

This version is slightly different, just on its change on the productivity rate :
* alpha is a function of g (physical growth rate, through Kaldor-Verdorn effect)
* alpha is a function of the employment : a lot of employees will make the

LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from chimes._models import Funcs


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'employment': {
            'func' : lambda employment, alphaKLV,n,g: employment*( g- n - alphaKLV ),
            'com' : "reduced 2-var system",
        },
        'omega': {
            'func' : lambda omega, phillips,alphaKLV: omega*(phillips-alphaKLV),
            'com' : 'reduced 2-var system',
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'phillips': Funcs.Phillips.div,

        'alphaKLV': {
            'func': lambda alpha, alpha0, alpha1, g, employment: alpha + alpha0*g + alpha1* employment,
            'com': 'Kaldor Verdoorn + Learning by doing',
            'definition': 'Endogenous ,technical progress rate',
            'units':'y^{-1}'},
        'g': {
            'func': lambda omega, delta ,nu : (1-omega)/nu - delta,
            'com': 'explicit reduced formula',
        },
    },
    'parameter': {
        'alpha0': {'value': 0.0,
                   'definition': 'dependency to growth in technical progress',
                   'units':''},
        'alpha1': {'value': 0.0,
                   'definition': 'dependency to employment in technical progress',
                   'units':'y^{-1}'},
    },
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

plots= {
    '3D': [{'x':'omega',
           'y':'employment',
           'z':'alphaKLV',
           'color':'time',
            'index':0}]
}
Nplots = {
    '3D': [{'x':'omega',
           'y':'employment',
           'z':'alphaKLV',
           'color':'time',
            'index':i} for i in range(5)],
    'byunits':[{'idx':i,
                'separate_variables':{'y^{-1}':'phillips'},
                } for i in range(5)]
}

_PRESETS = {
    'GoodwinLike':{
        'fields': {
            'alpha0':0,
            'alpha1':0,
    },
        'com': 'Behaves as a typical goodwin',
        'plots': plots,
    },
    'GoodwinKV': {
        'fields': {
            'alpha0': 0.2,
            'alpha1': 0,
        },
        'com': 'Add Kaldor-Verdorn progress',
        'plots':  plots,
    },
    'GoodwinL': {
        'fields': {
            'alpha0': 0,
            'alpha1': 0.05,
        },
        'com':'Add learning by doing method',
        'plots':  plots,
    },
    'Both': {
        'fields': {
            'nx': 5,
            'alpha0': np.linspace(0,0.5,5),
            'alpha1': 0.06,
        },
        'com': 'Add learning by doing method',
        'plots': Nplots,
    },
}

