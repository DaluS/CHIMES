# -*- coding: utf-8 -*-
"""Goodwin-Keen model: debt dynamics with residual consumption"""

_DESCRIPTION = """
* **Article :** 
* **Author  :** Steve Keen
* **Coder   :** Paul Valcke

## Description
It takes carbon emissions as an input, and let them evolves in three layers ( upper ocean, lower ocean, atmosphere)
The atmosphere concentration is driving radiative forcing, changing temperature of atmosphere
Atmosphere is changing its temperature and exchanging energy with ocean

Should be called in an economic model. Typically: 
* Input as "Emission"
* Output as "T"

The Philips and the Kappa parameter functions are here affine

TODO:
* 
* 
"""

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O
######################################################################

_LOGICS= {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha },
        'N': {'func': lambda N,n        : N*n },
        'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
        'p': {'func': lambda p,inflation: p*inflation },
        'D': {'func': lambda w,L,C,r,D,p,Pi,Delta: r*D + w*L - p*C + Pi*Delta },
        'Dh':{'func': lambda w,L,C,r,D,p,Pi,Delta:-r*D - w*L + p*C - Pi*Delta},
    },

    'statevar': {
        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) },
        'd'  :   {'func': lambda p,Y,D  : D  /(p*Y) },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) },
        'employment' :{'func': lambda L,N: L/N },
        'c' :{'func': lambda p,omega: p*omega},
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta },      
        
        'Y' :{'func': lambda K,nu: K/nu },
        'Pi':{'func': lambda p,Y,w,L,r,D: p*Y-w*L-r*D },
        'I' :{'func': lambda kappa,p,Y: kappa*p*Y },
        'C' :{'func': lambda Y,Ir: Y-Ir },
        'Ir':{'func': lambda p,I: I/p },
        'L' :{'func': lambda Y,a: Y/a },

        'GDP':{'func': lambda Y,p:Y*p},

        'inflation' :{'func': lambda c,p, eta,mu : eta*(mu*c/p -1) },
        'kappa'     :{'func': lambda pi, k0, k1: k0 + k1 * pi},
        'phillips'  :{'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},
    },

    'parameter': {
        'Delta': {'value':0,
        'definition': 'shareholding coefficient'}
    },
    'size': {},
}


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