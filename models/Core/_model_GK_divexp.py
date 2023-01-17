
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
    'test': {
        'fields': {},
        'com': '',
        'plots': {'XYZ': [{ 'x': 'employment',
                            'y': 'omega',
                            'z': 'd',
                            'color': 'time',
                            'idx': 0,
                            'title': ''}],
                 'plotbyunits': [],
                 'plotnyaxis': [{'x': 'time',
                           'y': [['employment', 'omega'],
                                 ['d'],['pi','kappa'],['inflation']
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],},
    },
}