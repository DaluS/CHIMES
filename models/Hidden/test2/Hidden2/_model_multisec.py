
"""
DESCRIPTION :

    Template for a multisectorial model

"""

import numpy as np
#from pygemmes._model import Funcs

_LOGICS = {
    'differential': {
        'a': {
            'func': lambda c: c,
            'multi': ['Nprod', ],
        },
    },
    'statevar': {
        'c': {
            'func': lambda a, b: a*b,
            'multi': ['Nprod', ],
        },
    },
    'parameter': {
        'b': {
            'value': 0,
            'multi': ['Nprod', 'Nprod'],
        },
        'zouplala': {
            'value': 0,
            'multi': ['Nprod', 'Nprod'],
        },
    },
    'size': {
        'Nprod': {
            'list': ['Energy', 'Mine', 'Consumption', 'Capital'],
            'definition': 'Productive sectors',

        },
    },
}

_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
