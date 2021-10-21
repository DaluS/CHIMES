# -*- coding: utf-8 -*-
"""
ABSTRACT: This is the simplest economic post-keynesian model.
TYPICAL BEHAVIOR : metastable oscillations around a solow point
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


def omega(itself=0, phillips=0):
    """ bla bla"""
    a = itself * phillips
    return a


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'lambda': {
            'func': lambda itself=0, g=0, alpha=0, beta=0: itself * (g - alpha - beta),
            'com': 'reduced 2variables dynamical expression'
        },
        'omega': {
            'func': omega,  # lambda itself=0, phillips=0: itself * phillips,
            'com': 'reduced 2variables dynamical expression',
            # 'initial': 0.8,
        },
    },
    'statevar': {
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: (-phi0 + phi1 / (1 - lamb)**2),
            'com': 'salary negociation on employement and profit',
        },
        'g': {
            'func': lambda pi=0, nu=1, delta=0: pi / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'func': lambda omega=0: 1. - omega,
            'com': 'Goodwin relative profit',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'smallcycle': {
        'fields': {
            'lambda': .97,
            'omega': .85,
        },
        'com': (
            'simple stable sinusoidal oscillations'
        ),
    },
    'bigcycle': {
        'fields': {
            'lambda': .99,
            'omega': .85,
        },
        'com': (
            'extremely violent stable oscillations'
        ),
    },
    'badnegociation': {
        'fields': {
            'phinull': .3,
        },
        'com': (
            'displace the Solow Point and '
            'allow big cycles with few harmonics'
        ),
    },
}
