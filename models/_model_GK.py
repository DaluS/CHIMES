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

_DPARAM = {

    # ---------
    # exogenous parameters
    # can also have a time variation (just replace by a function of time)
    # useful for studying the model's reaction to an exogenous shock
    'r': None,
    'k0': None,
    'k1': None,
    'k2': None,
    'alpha': None,
    'delta': None,
    'beta': None,
    'nu': None,
    'phinull': None,

    # ---------
    # functions

    # differential equations (ode)
    'a': {
        'func': lambda alpha=0, itself=0: alpha * itself,
        'initial': 1,
        'com': 'Exogenous technical progress as an exponential',
        'eqtype': 'ode',
    },
    'N': {
        'func': lambda beta=0, itself=0: beta * itself,
        'initial': 1.,
        'com': 'Exogenous population as an exponential',
        'eqtype': 'ode',
    },
    'K': {
        'func': lambda I=0, itself=0, delta=0: I - itself * delta,
        'initial': 2.7,
        'com': 'Capital evolution from investment and depreciation',
        'eqtype': 'ode',
    },
    'W': {
        'func': lambda itself=0, phillips=0: itself * phillips,
        'initial': 0.85,
        'com': 'Wage evolution through phillips curve',
        'eqtype': 'ode',
    },
    'D': {
        'func': lambda I=0, Pi=0: I - Pi,
        'initial': 0.1,
        'com': 'Debt as Investment-Profit difference',
        'eqtype': 'ode',
    },

    # Intermediary functions (endogenous, computation intermediates)
    'Y': {
        'func': lambda K=0, nu=1: K / nu,
        'eqtype': 'intermediary',
    },
    'L': {
        'func': lambda K=0, a=1, nu=1: K / (a * nu),
        'eqtype': 'intermediary',
    },
    'Pi': {
        'func': lambda Y=0, W=0, L=0, r=0, D=0: Y - W * L - r * D,
        'eqtype': 'intermediary',
    },
    'lambda': {
        'func': lambda L=0, N=1: L / N,
        'eqtype': 'intermediary',
    },
    'omega': {
        'func': lambda W=0, L=0, Y=1: W * L / Y,
        'eqtype': 'intermediary',
    },
    'phillips': {
        'func': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (1 - lamb)**2,
        'eqtype': 'intermediary',
    },
    'kappa': {
        'func': lambda k0=0, k1=0, k2=0, Pi=0, Y=1: k0 + k1 * np.exp(k2*Pi/Y),
        'eqtype': 'intermediary',
    },
    'I': {
        'func': lambda Y=0, kappa=0: Y * kappa,
        'eqtype': 'intermediary',
    },

    # auxiliary, not used for computation but for interpretation
    # => typically computed at the end after the computation
    'g': {
        'func': lambda omega=0, nu=1, delta=0: (1 - omega) / nu - delta,
        'eqtype': 'auxiliary',
    },
    'd': {
        'func': lambda D=0, Y=1: D / Y,
        'eqtype': 'auxiliary',
    },
    'pi': {
        'func': lambda omega=0, r=0, d=0: 1 - omega - r * d,
        'eqtype': 'auxiliary',
    },
    'i': {
        'func': lambda Y=0: Y * 0,
        'eqtype': 'auxiliary',
    },
    'phi0': {
        'func': lambda phinull=0: phinull / (1 - phinull**2),
        'eqtype': 'auxiliary',
    },
    'phi1': {
        'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
        'eqtype': 'auxiliary',
    },
}


# ---------------------------
# New formalism


_LOGICS = {
    'ode': {
        'a': {
            'logic': lambda alpha=0, itself=0: alpha * itself,
            'com': 'Exogenous technical progress as an exponential',
        },
        'N': {
            'logic': lambda beta=0, itself=0: beta * itself,
            'com': 'Exogenous population as an exponential',
        },
        'K': {
            'logic': lambda I=0, itself=0, delta=0: I - itself * delta,
            'com': 'Capital evolution from investment and depreciation',
        },
        'D': {
            'logic': lambda I=0, Pi=0: I - Pi,
            'com': 'Debt as Investment-Profit difference',
        },
        'W': {
            'logic': lambda phillips=0, itself=0: itself*phillips,
            'com': 'salary through negociation',
        },
        'p': {
            'logic': lambda itself=0, inflation=0: itself*inflation,
            'com': 'NO INFLATION FOR THE MOMENT',
            'initial': 1,
        },
    },
    # Intermediary relevant functions
    'statevar': {
        'Y': {
            'logic': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ',
        },
        'GDP': {
            'logic': lambda Y=0, p=0: Y*p,
            'com': 'Output with selling price ',
        },
        'inflation': {
            'logic': lambda p=0: 0,
            'com': 'INFLATION NOT CODED',
        },
        'L': {
            'logic': lambda K=0, a=1, nu=1: K / (a * nu),
            'com': 'Full instant employement based on capital',
        },
        'Pi': {
            'logic': lambda Y=0, W=0, L=0, r=0, D=0: Y - W * L - r * D,
            'com': 'Profit for production-Salary-debt logic',
        },
        'lambda': {
            'logic': lambda L=0, N=1: L / N,
            'com': 'employement rate',
        },
        'omega': {
            'logic': lambda W=0, L=0, Y=1: W * L / Y,
            'com': 'wage share',
        },
        'phillips': {
            'logic': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (1 - lamb)**2,
            'com': 'Wage increase rate through employement',
        },
        'kappa': {
            'logic': lambda k0=0, k1=0, k2=0, Pi=0, Y=1: k0 + k1 * np.exp(k2*Pi/Y),
            'com': 'Relative GDP investment through relative profit',
        },
        'I': {
            'logic': lambda GDP=0, kappa=0: GDP * kappa,
            'com': 'Investment value',
        },
        'd': {
            'logic': lambda D=0, GDP=1: D / GDP,
            'com': 'private debt ratio',
        },
        'pi': {
            'logic': lambda omega=0, r=0, d=0: 1 - omega - r * d,
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
