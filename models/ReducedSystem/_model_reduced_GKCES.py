# -*- coding: utf-8 -*-
"""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability

We added substituability between K and L, with an optimization of profit

LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.

Created on Wed Jul 21 15:11:15 2021

@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'differential': {
        'employment': {
            'func': lambda employment, g, alpha, n, CESexp, omega, dotomega: employment * (g - alpha - n- dotomega/(omega*(1-omega)*CESexp)),
            'com': 'reduced 3variables dynamical expression'
        },
        'omega': {
            'func': lambda dotomega: dotomega,
            'com': 'see dotomega',
        },
        'd': {
            'func': lambda d, kappa, pi, g, r, omega, dotomega, CESexp: kappa - (1-omega)+d*(r-g+dotomega/(CESexp*(1-omega))),
            'com': 'no solvability in loans'
        }
    },
    'statevar': {
        'phillips': {
            'func': lambda phi0, phi1, employment: (-phi0 + phi1 / (1 - employment)**2),
            'com': 'salary negociation on employement and profit',
        },
        'g': {
            'func': lambda kappa, nu, delta: kappa / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'func': lambda omega, r, d: 1. - omega - r * d,
            'com': 'Goodwin relative profit',
        },
        'kappa': {
            'func': lambda k0, k1, k2, pi: k0 + k1 * np.exp(k2 * pi),
            'com': 'Relative GDP investment through relative profit',
        },
        #'inflation': {
        #    'func': lambda mu, CESexp, omega: CESexp*(mu*omega-1),
        #    'com': 'Markup dynamics',
        #},
        'nu': {
            'func': lambda A,omega, b, CESexp : (A*((1-omega)/b)**(-1/CESexp))**(-1),
            'com': 'endogenous optimized'
        },
        'dotomega': {
            'func': lambda omega,CESexp,phillips,alpha : omega * (CESexp/(1+CESexp))* (phillips -alpha),
            'units':'y^{-1}',
        }
    },
    'parameter': {},
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'dt':0.01,

        'employment': 0.88,
        'omega': 0.95,
        'd': 8,

        'CESexp':100,
        'alpha': 0.02,
        'n': 0.025,
        'A': 1/3,
        'CESexp':100,
        'delta': .005,
        'phinull': .1,
        'k0': -0.0065,
        'k1': np.exp(-5),
        'k2': 20,
        'r': 0.03, },
    'com': ' Default run : large fluctuation with high substituability',
    'plots': {'nyaxis': [{'x': 'time',
                          'y': [['employment'],
                                ['omega'],
                                ['kappa','pi'],
                                ['d']],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'd',
                    'color': 'time',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
              },
    },
}
