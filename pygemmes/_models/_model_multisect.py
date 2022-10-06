# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Template for a multisectorial model

"""

import numpy as np
#from pygemmes._models import Funcs


# ######################## OPERATORS ####################################

# #######################################################################

_LOGICS = {
    'differential': {
        'Z': {
            'func': lambda OPER,Z: OPER-0.5*Z,
            'size': ['Nprod', ],
            'initial': 1,
        },

    },
    'statevar': {
        'OPER': {
            'func': lambda Z, MATRIX: np.matmul(MATRIX,Z),
            'size': ['Nprod', ],
        },
    },
    'parameter': {
        'MATRIX': {
            'value': 0,
            'size': ['Nprod', 'Nprod']
        },
    },
    'size': {
        'Nprod': {
            #'value': 4,
            'list': ['energy','Capital','Cons'],
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
