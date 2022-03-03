#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin-Keen Resource model based on extensive variables.
TYPICAL BEHAVIOR :
LINKTOARTICLE: voir Figure 16 du rapport de stage

Created on Thu Jan  20 2022
@author: Camille Guittonneau
"""

import numpy as np

# ----------------------------------------------------------------------------
# We simply do a few modifications on two previous models : we load them as a basis
from pygemmes._models._model_GK import _LOGICS as _LOGICS0
from pygemmes._models._model_Camille_Mine import _LOGICS as _LOGICSMine
from copy import deepcopy

# The model is a start of a Goodwin-Keen model
_LOGICS = deepcopy(_LOGICS0)

# We add the mine sector
for category, dic in _LOGICSMine.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# We write the coupling equations
_LOGICS_COUPLING = {
    # No ODE in mining sector are not modified
    'ode': {
    },
    # We only modified stock-flux related quantities and production function
    'statevar': {
        # Definition of capital is slightly changed
        'Kstar': {
            'func': lambda K=0, Y_R=0, theta=0: (K**theta)*(Y_R**(1-theta)),
            'com': 'capital boost from mining', },
        'Y': {
            'func': lambda Kstar=0, nu=1: Kstar/nu,
            'com': 'Leontief optimized production output', },
        'L': {
            'func': lambda Kstar=0, nu=1, a=1: Kstar / (nu * a),
            'com': 'Full instant employement based on capital', },

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
        'fields': {},
        'com': '',
        'plots': {'plotbyunits': [{'title': '',
                                   'lw': 1,
                                   'idx': 0,
                                   'color': 'k'},
                                  ],
                  },
    },
}
