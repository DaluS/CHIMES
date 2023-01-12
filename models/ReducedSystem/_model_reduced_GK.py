# -*- coding: utf-8 -*-
'''3-dimensional reduced Goodwin-Keen dynamics'''


_DESCRIPTION ="""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis

LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.

Created on Wed Jul 21 15:11:15 2021

@author: Paul Valcke
"""

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O

_LOGICS = {
    'differential': {
        'employment': {'func': lambda employment, g, alpha, n: employment * (g - alpha - n),},
        'omega': {     'func': lambda omega, phillips, alpha,gammai,inflation: omega * (phillips -alpha- (1-gammai)*inflation),},
        'd': {         'func': lambda d, kappa, pi, g, inflation,Delta:  kappa - pi + pi*Delta  - d*(g+inflation),}
    },
    'statevar': {
        'phillips': {'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,
                     'com': 'Linear Philips'},
        'g':  {'func': lambda kappa, nu, delta: kappa / nu - delta,},
        'pi': {'func': lambda omega, r, d: 1. - omega - r * d},
        'kappa': {'func': lambda pi, k0, k1: k0 + k1 * pi,
                  'com': 'Linear kappa'},
        'inflation': {
            'func': lambda mu, eta, omega: eta*(mu*omega-1),
            'com': 'Markup dynamics',
        },
    },
    'parameter': {
        'Delta': {'value':0,
        'definition': 'shareholding coefficient'}
    },
    'size': {},
}

_SUPPLEMENTS={}
_PRESETS = {'Fred': {
    'fields': {'philinConst': -0.55465958,
                  'philinSlope': 0.60171221, 
                  'k0': -0.04619561,
                  'k1': 1.04679933,
                  'k2': 0,
                  'alpha': 0.01,
                  'n': 0.015,
                  'nu': 4.04271601,
                  'r': 0.01294320,
                  'Delta': .30653839,
                  'delta': 0.03487562,
                  'd': 0.53,
                  'omega': 0.68,
                  'employment':0.92,
                  'eta': 0,
                  'mu': 1, 
                  'Tmax': 2000/4,
                  'dt':0.1   },
    'com': 'Calibration of the US economy by Fred',
    'plots':{'XYZ': [{'x':'employment',
                    'y':'omega',
                    'z':'d',
                    'color':'time'},
                    ]},
},
}
