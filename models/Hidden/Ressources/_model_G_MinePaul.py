
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
from chimes.libraries import Funcs
from chimes.libraries._model_Goodwin import _LOGICS as _LOGICS0
from chimes.libraries._model_MinePaul import _LOGICS as _MININGSECTOR

from copy import deepcopy

# The model is a start of a Goodwin-Keen model
_LOGICS = deepcopy(_LOGICS0)

# We add the mine
for category, dic in _MININGSECTOR.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


_COUPLING = {
    'differential': {
    },
    'statevar': {
        # THE IMPACT ON PRODUCTION
        'Y': {
            'func': lambda K, nuEQ, Gamma, intensity: (K / nuEQ) / (1 - intensity * Gamma),
            'com': 'EROI impacting Leontiev'
        },
        'nuEQ': {
            'func': lambda intensity, nu, nuMine: intensity * nuMine + (1 - intensity) * nu,
            'com': 'nu from both system together',
            'definition': "nu when pseudo-bisectorial",
            'units': 'y'
        },
        'c': {
            'func': lambda w, a, Gamma, intensity: w / (a * (1 + intensity * Gamma)),
            'com': 'price with only labor salary',
        }

    },
    'parameter': {},
    'size': {},
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
