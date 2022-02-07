# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a mine-depleting model

TYPICAL BEHAVIOR :
LINKTOARTICLE :

@author: Paul Valcke
"""

import numpy as np


from pygemmes._models import Funcs


__r0 = 1000
_LOGICS = {
    'ode': {
        # COUPLING ODE
        'R': {
            'func': lambda Y=0, intensity=0: -Y*intensity,
            'com': 'Only removed by production',
            'initial': __r0*0.9,
        },
    },
    'statevar': {
        'Quality': {
            'func': lambda R0=1, R=0.5, qRslope=1: np.log(R0/(R0-R))*(1/qRslope),
            'definition': 'quality of best resource',
            'com': 'exponential distribution'
        },
        'nuMine': {
            'func': lambda nu0=0, Quality=1, a=1: nu0/(Quality*a),
            'com': 'impact of quality on production',
            'definition': 'return of capital of mining sector',
        },
        'Gamma': {
            'func': lambda Gamma0=0, a=1, Quality=1, Gammabase=1: Gammabase + Gamma0/(Quality*a),
            'definition': 'Generalised EROI (recipie)',
            'com': 'based on quality',
        },

    },
    'param': {
        'intensity': {
            'value': 0.8,
            'definition': 'part of output which is material',
            'units': ''
        },
        'qRslope': {
            'value': 1,
            'definition': 'slope in resource quality concentration',
            'units': ''
        },
        'Gamma0': {
            'value': 0.01,
            'definition': 'Quality-dependent EROI contribution',
            'units': ''
        },
        'Gammabase':  {
            'value': 0.01,
            'definition': 'Quality-independent EROI contribution',
            'units': ''
        },
        'R0': {
            'value': __r0,
            'definition': 'initial quantity of ressources'},
        'nu0': {
            'value': 7,
            'definition': 'nu at snapshot'}
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
    },
    'com': ' Default run'},
}
