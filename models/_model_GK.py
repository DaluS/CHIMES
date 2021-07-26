# -*- coding: utf-8 -*-
"""
Here we define the parameters and set of equation for a model of type 'GK'

All parameters can have value:
    - None: set to the default value found in _def_fields.py
    - scalar: int or float
    - list or np.ndarray used for benchmarks
    - function (callable): in that can it will be treated as a variable
                            the function will be called at each time step

"""


import numpy as np


# ---------------------------
# user-defined function order (optional)

_FUNC_ORDER = None

_DESCRIPTION = ""
_PRESETS = {}
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
