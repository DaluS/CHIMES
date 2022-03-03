#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin-Keen Resource model based on extensive variables.
The Leontiev optimised production function is replaced by a CES.
TYPICAL BEHAVIOR :
LINKTOARTICLE: Green Growth

Created on Fri Feb  18 2022
@author: Camille Guittonneau
"""

import numpy as np
from pygemmes._models import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on two previous models : we load them as a basis
from pygemmes._models._model_GKCES import _LOGICS as _LOGICSCES
from pygemmes._models._model_Camille_Mine import _LOGICS as _LOGICSMine
from copy import deepcopy

# The model is a start of a Goodwin-Keen model with CES
_LOGICS = deepcopy(_LOGICSCES)

# We add the mine sector
for category, dic in _LOGICSMine.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# We write the coupling equations
_LOGICS_COUPLING = {
    # No ODE in mining sector are not modified
    'ode': {
        # Stock-flow consistency
        'K_0': Funcs.Kappa.kfromIr,
    },
    # We only modified stock-flux related quantities and production function
    'statevar': {


        # Definition of capital is slightly changed
        'K': {
            'func': lambda K_0=0, Y_R=0, theta=0: (K_0**theta)*(Y_R**(1-theta)),
            'com': 'capital boost from mining', },

        # A flux of money is paying for ressources
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, varphi=0, p_R=0, M=0, r=0, D=0: GDP - w * L - r * D - (1-varphi)*p_R*M,
            'com': 'Profit for production-Salary-debt func', },
        'c': {
            'func': lambda omega=0, varphi=0, m=0: omega + (1 - varphi) * m,
            'com': 'production cost', },
    },
    'param': {
        'theta': {
            'value': 1,
            'definition': 'Cobb-Douglas coefficient'},
        'varphi': {
            'value': .0,
            'definition': 'extraction cost'},
        'm': {
            'value': .0,
            'definition': 'pro cost coeff'},
    },
}


# We do add them
for category, dic in _LOGICS_COUPLING.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

_PRESETS = {
    'Nomining': {
        'fields': {'K_0': 0.0001,
                   'K_R': 0.0001,
                   'D_R': 0.001,
                   'p_R': 0.1, },
        'com': '',
        'plots': {'plotbyunits': [{'title': '',
                                   'lw': 1,
                                   'idx': 0,
                                   'color': 'k'},
                                  ],
                  },
    },
}
