
"""
DESCRIPTION :

    PREPARE AN INVENTORY LOGICS, YET SAY LAW IS STILL VALID
    This is a non-impacting extension of a Goodwin-Keen model, all of those connexion are either
    having a value of zero (dotV)... or auxilliary ( H , Dh)

    RELAXING SAY'S LAW WILL REQUIRE REDEFINITION OF PI


LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs
# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_GK import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)

# ---------------------------
# user-defined model
# contains parameters and functions of various types


_INVENTORY = {
    'ode': {
        'V': {
            'func': lambda dotV: dotV,
            'com': 'logic in statevar dotV',
        },
        'H': {
            'func': lambda H, deltah, C: C - H*deltah,
            'com': 'Goods-Consume-Deterioration'
        },
        'Dh': {
            'func': lambda w, L, C, p: C*p - w*L,
            'com': 'salary and consumption',
        },
        'M': {
            'func': lambda M: 0,
            'com': 'empty placeholder'}
    },

    # Intermediary relevant functions
    'statevar': {
        'dotV': {
            'func': lambda Y, Ir, C: Y - Ir - C,
            'definition': 'variation of inventory',
            'com': 'Output Conso Invest'},
        'C': {
            'func': lambda Ir, Y: Y-Ir,
            'com': 'Says law'},
        'm': Funcs.Definitions.m,
        'v': Funcs.Definitions.v,
        'inflation': Funcs.Inflation.markupInventory,
        # 'inflation': Funcs.Inflation.markupInventY,
    },
    'param': {
    },
}

# We add them explicitely
for category, dic in _INVENTORY.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{}],
            'phasespace': [{}],
            '3D': [{}],
            'byunits': [],
        },
    },
}
