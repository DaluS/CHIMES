# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Template for a multisectorial model

"""

#import numpy as np
#from pygemmes._model import Funcs

_LOGICS = {
    'differential': {
        'a': {
            'func': lambda a, b: a*b,
            'size': 'n_prod',
        },
    },
    'statevar': {
        'c': {
            'func': lambda a, b: a*b,
            'size': 'n_prod',
        },
    },
    'parameter': {
        'b': {
            'value': 0,
            'size': ['n_prod', 'n_prod']
        },
    },
    'size': {
        'n_prod': {
            'list': ['mine',
                     'energy',
                     'machines',
                     'products'],
            'definition': 'Productive sectors',
        },
    },
}

_PRESETS = {
    'default': {
        'fields': {},
        'com': "",
        'plots': {},
    },
}


# Check size consistent in operations
# If only one dimension, transform string into list
# If sizes are defined as list, creating a dictionnary

for k1,k2 in listStockFlow.items():
    MC.k1[i]=MC.k1[i-1]+MC.k2[i-1]*dt