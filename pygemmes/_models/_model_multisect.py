# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Template for a multisectorial model

"""

import numpy as np
#from pygemmes._model import Funcs


# ######################## OPERATORS ####################################
#from ..__config import _OPTIMIZE_EINSUM
_OPTIMIZE_EINSUM=True
def Matop(M,V):
    return np.einsum('ijkl,ijk->ijk',M,V,optimize=_OPTIMIZE_EINSUM)
    # return np,einsum('ijkl,ijk->ijl',M,V)

def ScalarProd(V1,V2):
    return np.einsum('ijk,ijk->ij',V1,V2,optimize=_OPTIMIZE_EINSUM)

def Sum(V1):
    return np.einsum('ijk->ij',V1,optimize=_OPTIMIZE_EINSUM)
# #######################################################################

_LOGICS = {
    'differential': {
        'a': {
            'func': lambda c: c,
            'size': ['Nprod', ],
        },
    },
    'statevar': {
        'c': {
            'func': lambda a, b: Matop(b,a),
            'size': ['Nprod', ],
        },
    },
    'parameter': {
        'b': {
            'value': 0,
            'size': ['Nprod', 'Nprod']
        },
    },
    'size': {
        'Nprod': {
            'value': 4,
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
