# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin, with a slightly different wage
    negociation : now the wage increase rate depends of the profit

    $ \dfrac{\partial w}{\partial t}= w \Phi(\lambda) \pi^{z_{\pi}}$

LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_G import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)

_LOGICS['ode']['w'] = Funcs.Phillips.salaryfromPhillipsProfitsNoInflation
_LOGICS['param']['zpi'] = {'value': 0.5,
                           'definition': 'impact of profit in salary negociation'}


# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'zpi': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': .5*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
            'zpi': [0.5, 1, 2, 5]
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                           'y': [['lambda', 'omega'],
                                 ['K'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                        'y': 'omega',
                        'z': 'time',
                        'cinf': 'pi',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'byunits': [],
        },
    },
}
