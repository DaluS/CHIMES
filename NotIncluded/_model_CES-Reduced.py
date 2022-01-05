# -*- coding: utf-8 -*-
"""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis, more convergent with more substituability
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


def omegap(eta=0, phillips=0, alpha=0, omega=0):
    return omega*((eta/(1+eta))*(phillips-alpha)),


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'lambda': {
            'func': lambda itself=0, g=0, alpha=0, beta=0, kappa=0, nu=1, omegap=0, omega=0.5, delta=0, eta=1: itself * (kappa/nu - alpha - beta-delta - omegap/omega * (eta*(1-omega))**(-1)),
            'com': ''
        },
        'omega': {
            'func': lambda omegap=0: omegap,
            'com': 'CES expression of omegap',
            # 'initial': 0.8,
        },
        'd': {
            'func': lambda itself =0, kappa=0, pi=0, g=0, i=0: kappa - pi - itself*(g+i),
            'com': ''
        }
    },
    'statevar': {
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: (-phi0 + phi1 / (1 - lamb)**2),
            'com': 'salary negociation on employement and profit',
        },
        'nu': {
            'func': lambda A=1, omega=0, b=1, eta=1: (1/A)*((1-omega)/b)**(-1/eta),
            'com': "endogenous return on capital"
        },
        'g': {
            'func': lambda kappa=0, nu=1, delta=0: kappa / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'func': lambda omega=0, r=0, d=0: 1. - omega - r * d,
            'com': 'Goodwin relative profit',
        },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, pi=0, solvability=0: (k0 + k1 * np.exp(k2 * pi))*solvability,
            'com': 'Relative GDP investment through relative profit',
        },
        'omegap': {
            'func': lambda eta=0, phillips=0, alpha=0, omega=0: omega*((eta/(1+eta))*(phillips-alpha)),
            'com': 'loan dampening if non solvable',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'lambda': 0.95,
        'omega': 0.85,
        'd': 2,
        'alpha': 0.02,
        'beta': 0.025,
        'nu': 3,
        'delta': .005,
        'phinull': .04,
        'k0': -0.0065,
        'k1': np.exp(-5),
        'k2': 20,
        'r': 0.03, },
    'com': ' Default run'},
}
