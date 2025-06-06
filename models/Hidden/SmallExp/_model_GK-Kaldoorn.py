
"""
DESCRIPTION :

    This is a small modificaiton of GoodwinKeen, with now a endogenous growth rate :

    $\dfrac{\partial a}{\partial t}= a (\alpha + \beta g)$


LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""
import numpy as np
from chimes.libraries import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from chimes.libraries._model_GK import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)

# We add our modifications
_LOGICS['ode']['w'] = Funcs.Phillips.salaryfromPhillipsNoInflation
_LOGICS['ode']['a'] = Funcs.Productivity.verdoorn
_LOGICS['param']['beta'] = {'value': 0.5,
                            'definition': 'impact of growth in productivity increase'}

# ----------------------------------------------------------------------------
# List of presets for specific interesting simulations
betavec = np.arange(0, 1, 0.1)
_PRESETS = {
    'beta-productivity': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': .5 * 1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
            'alpha': 0.02,
            'beta': betavec,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
                              ],
                        'idx': 0,
                        'title': '',
                        'lw': 1}],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'color': 'time',
                    'idx': 0}],
            'XYZ': [{'x': 'employment',
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
