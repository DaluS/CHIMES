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


_DPARAM = {

    # ---------
    # Fixed-value parameters
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

    # former variables
    'a': {
        'value': lambda alpha=0, self=0: alpha * self,
        'com': 'Exogenous technical progress as an exponential',
        'eqtype': 'ode',
    },
    'N': {
        'value': lambda beta=0, self=0: beta*self,
        'com': 'Exogenous population as an exponential',
        'eqtype': 'ode',
    },
    'K': {
        'value': lambda I=0, self=0, delta=0: I - self*delta,
        'com' : 'Capital evolution from investment and depreciation',
        'eqtype': 'ode',
    },
    'W': {
        'value': lambda self=0, philips=0: self * philips,
        'com': 'Wage evolution through philips curve',
        'eqtype': 'ode',
    },
    'D': {
        'value': lambda I=0, Pi=0: I - Pi,
        'com' : 'Debt as Investment-Profit difference',
        'eqtype': 'ode',
    },

    # Intermediary computed but not stored
    'Y': {
        'value': lambda K=0, nu=1: K / nu,
        'eqtype': 'intermediary',
    },
    'L': {
        'value': lambda K=0, a=1, nu=1: K / (a * nu),
        'eqtype': 'intermediary',
    },
    'Pi': {
        'value': lambda Y=0, W=0, L=0, r=0, D=0: Y - W*L - r*D,
        'eqtype': 'intermediary',
    },
    'lambda': {
        'value': lambda L=0, N=1: L / N,
        'eqtype': 'intermediary',
    },
    'omega': {
        'value': lambda W=0, L=0, Y=1: W * L / Y,
        'eqtype': 'intermediary',
    },
    'philips': {
        'value': lambda phi0=0,  phi1=0, lamb=0: -phi0 + phi1 / (1-lamb)**2,
        'eqtype': 'intermediary',
    },
    'kappa': {
        'value': lambda k0=0, k1=0, k2=0, Pi=0, Y=1: k0 + k1 * np.exp(k2*Pi/Y),
        'eqtype': 'intermediary',
    },
    'I': {
        'value': lambda Y=0, kappa=0: Y * kappa,
        'eqtype': 'intermediary',
    },

    # auxiliary, not computed, but can be retrieved at the end
    'g': {
        'value': lambda omega=0, nu=1, delta=0: (1-omega) / nu - delta,
        'eqtype': 'auxiliary',
    },
    'd': {
        'value': lambda D=0, Y=1: D / Y,
        'eqtype': 'auxiliary',
    },
    'pi': {
        'value': lambda omega=0, r=0, d=0: 1 - omega - r*d,
        'eqtype': 'auxiliary',
    },
    'i': {
        'value': lambda Y=0: Y*0,
        'eqtype': 'auxiliary',
    },
    'phi0': {
        'value': lambda phinull=0: phinull / (1- phinull**2),
        'eqtype': 'auxiliary',
    },
    'phi1': {
        'value': lambda phinull=0: phinull**3 / (1- phinull**2),
        'eqtype': 'auxiliary',
    },
}
