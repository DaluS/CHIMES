# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model based on extensive variables.
Inflation not integrated to the process
TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np


# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'a': {
            'func': lambda alpha=0, itself=0: alpha * itself,
            'com': 'Exogenous technical progress as an exponential',
        },
        'N': {
            'func': lambda beta=0, itself=0: beta * itself,
            'com': 'Exogenous population as an exponential',
        },
        'K': {
            'func': lambda I=0, itself=0, delta=0: I - itself * delta,
            'com': 'Capital evolution from investment and depreciation',
        },
        'D': {
            'func': lambda I=0, Pi=0: I - Pi,
            'com': 'Debt as Investment-Profit difference',
        },
        'W': {
            'func': lambda phillips=0, itself=0: itself * phillips,
            'com': 'salary through negociation',
        },
        'p': {
            'func': lambda itself=0, inflation=0: itself * inflation,
            'com': 'NO INFLATION FOR THE MOMENT',
            'initial': 1,
        },
    },
    # Intermediary relevant functions
    'statevar': {
        'Y': {
            'func': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ',
        },
        'GDP': {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'Output with selling price ',
        },
        'inflation': {
            'func': lambda p=0: 0. * p,
            'com': 'INFLATION NOT CODED',
        },
        'L': {
            'func': lambda K=0, a=1, nu=1: K / (a * nu),
            'com': 'Full instant employement based on capital',
        },
        'Pi': {
            'func': lambda Y=0, W=0, L=0, r=0, D=0: Y - W * L - r * D,
            'com': 'Profit for production-Salary-debt func',
        },
        'lambda': {
            'func': lambda L=0, N=1: L / N,
            'com': 'employement rate',
        },
        'omega': {
            'func': lambda W=0, L=0, Y=1: W * L / Y,
            'com': 'wage share',
        },
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0, pi=0, zphi=1: (pi ** zphi) * (-phi0 + phi1 / (1 - lamb)**2),
            'com': 'Wage increase rate through employement and profit',
        },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, Pi=0, Y=1: k0 + k1 * np.exp(k2 * Pi / Y),
            'com': 'Relative GDP investment through relative profit',
        },
        'solvability': {
            'func': lambda d=0, nu=1: (1 - d/nu),
            'com': 'ability to reimburse debt'
        },
        'I': {
            'func': lambda GDP=0, kappa=0, zkappa=1, solvability=0: GDP * kappa * solvability**zkappa,
            'com': 'Investment value',
        },
        'd': {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'private debt ratio',
        },
        'pi': {
            'func': lambda omega=0, r=0, d=0: 1 - omega - r * d,
            'com': 'relative profit',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {
            'a': 1,
            'N': 1,
            'K': 2.7,
            'D': 0.2,
            'W': .85,
            'p': 1,
            'alpha': 0.02,
            'beta': 0.025,
            'nu': 3,
            'delta': .005,
            # 'phinull': .04,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': [],
    },
    'crisis': {
        'fields': {
            'a': 1,
            'N': 1,
            'K': 2.7,
            'D': 10,
            'W': .85,
            'p': 1,

            'r': 0.0
        },
        'com': (
            'This is a run that should create a debt crisis'
        ),
        'plots': [],
    },
}
