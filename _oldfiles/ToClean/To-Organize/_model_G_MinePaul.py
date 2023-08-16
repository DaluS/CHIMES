# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a goodwin model with has a component of its production based on a depleting mining sector
I'd also put scenarios on the intensity curve (a society that goes toward less resource extraction) for publication-friendly content.

TYPICAL BEHAVIOR :
LINKTOARTICLE :

@author: Paul Valcke
"""

import numpy as np

# ----------------------------------------------------------------------------
# We simply do a few modifications on two previous models : we load them as a basis
from pygemmes._models import Funcs
from pygemmes._models._model_G import _LOGICS as _LOGICS0
from pygemmes._models._model_MinePaul import _LOGICS as _MININGSECTOR

from copy import deepcopy

# The model is a start of a Goodwin-Keen model
_LOGICS = deepcopy(_LOGICS0)

# We add the mine
for category, dic in _MININGSECTOR.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


_COUPLING = {
    'ode': {
    },
    'statevar': {
        # THE IMPACT ON PRODUCTION
        'Y': {
            'func': lambda K=0, nuEQ=1, Gamma=0, intensity=0: (K/nuEQ) / (1-intensity*Gamma),
            'com': 'EROI impacting Leontiev'
        },
        'nuEQ': {
            'func': lambda intensity=0, nu=1, nuMine=1: intensity*nuMine+(1-intensity)*nu,
            'com': 'nu from both system together',
            'definition': "nu when pseudo-bisectorial",
        },
        'c': {
            'func': lambda w=0, a=1, Gamma=0, intensity=0:  w/(a*(1+intensity*Gamma)),
            'com': 'price with only labor salary',
        }

    },
    'param': {
    },
}

# We add the coupling
for category, dic in _COUPLING.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {

    },
    'com': ' Default run'},
}
