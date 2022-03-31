# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Template for a multisectorial model

"""

import numpy as np
from pygemmes._model import Funcs

_LOGICS = {
    'differential': {
        'a': {
            'func': lambda a, b: a*b,
            'size': ['Nprod', ],
        },
    },
    'statevar': {
        'c': {
            'func': lambda a, b: a*b,
            'size': ['Nprod', ],
        },
    },
    'parameter': {
        'b': {
            'value': 0,
            'size': ['Nprod', 'Nprod']
        },
    },
},

_PRESETS = {
    'default': {
        'fields': {},
        'com': (),
        'plots': {},
    },
},
# Check size consistent in operations
# If only one dimension, transform string into list
