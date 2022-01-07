# -*- coding: utf-8 -*-
"""
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

# ---------------------------
# user-defined function order (optional)


#_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'lambda': {
            'func': lambda itself=0: itself * np.random.normal(0, scale=0.1),
            'com': 'reduced 3variables dynamical expression'
        },
    },
    'statevar': {
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {},
    'com': ''},
}
