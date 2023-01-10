# -*- coding: utf-8 -*-
"""Goodwin-Keen with diverging philips and exponential kappa"""

_DESCRIPTION = """
* **Article :** 
* **Author  :** Steve Keen
* **Coder   :** Paul Valcke

## Description

TODO:
* 
* 
"""

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O
######################################################################

_LOGICS_GK,_PRESETS_GK = importmodel("GK")
_LOGICS2= {
    'statevar': {
        'kappa'     :{'func': lambda pi, k0, k1,k2: k0 + k1 *np.exp(k2*pi)},
        'phillips'  :{'func': lambda employment, phi0,phi1: -phi0+phi1/(1-employment)**2,},
    },
}
_LOGICS=mergemodel(_LOGICS_GK,_LOGICS2)

_SUPPLEMENTS = {}
_PRESETS = {
    'Fred': {
        'fields': {'philinConst': -0.55465958,
                  'philinSlope': 0.60171221, 
                  'k0': -0.04619561,
                  'k1': 1.04679933,
                  'k2': 0,
                  'nu': 4.04271601,
                  'r': 0.01294320,
                  'Delta': .30653839,
                  'delta': 0.03487562,
                  'D': 0.53/4.04271601,
                  'w': 0.68,
                  'K': 1.,
                  'p': 1.,
                  'a': 1.,
                  'N': 0.92/4.04271601,
                  'eta': 0,
                  'mu': 1, },
        'com': '',
        'plots': {},
    },
}