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


_DPARAM = {

    # ---------
    # Fixed-value parameters
    'r': {'value': None},
    'k0': {'value': None},
    'k1': {'value': None},
    'k2': {'value': None},
    'alpha': {'value': None},
    'delta': {'value': None},
    'beta': {'value': None},
    'nu': {'value': None},
    'phi0': {'value': None},
    'phi1': {'value': None},

    # ---------
    # functions

    # former variables
    'a': {
        'value': lambda alpha=0, a=0: alpha * a,
        'com': 'Exogenous technical progress as an exponential',
        'type': 'differential',
    },
    'N': {
        'value': lambda beta=0, N=0 : beta*N,
        'com': 'Exogenous population as an exponential',
        'type': 'differential',
    },
    'K': {
        'value': lambda I=0, K=0, delta=0: I - K*delta,
        'com' : 'Capital evolution from investment and depreciation',
        'type': 'differential',
    },
    'W': {
        'value': lambda W=0, philips=0 : W * philips,
        'com': 'Wage evolution through philips curve',
        'type': 'differential',
    },
    'D': {
        'value': lambda I=0, Pi=0: I - Pi,
        'com' : 'Debt as Investment-Profit difference',
        'type': 'differential',
    },

    # Intermediary
    'Y': {
        'value': lambda K=0, nu=0: K / nu,
        'type': 'intermediary',
    },
    'L': {
        'value': lambda K=0, a=0, nu=0: K / (a * nu),
        'type': 'intermediary',
    },
    'Pi': {
        'value': lambda Y=0, W=0, L=0, r=0, D=0: Y - W*L - r*D,
        'type': 'intermediary',
    },
    'lamb': {
        'value': lambda L=0, N=0: L / N,
        'type': 'intermediary',
    },
    'omega': {
        'value': lambda W=0, L=0, Y=0: W * L / Y,
        'type': 'intermediary',
    },
    'philips': {
        'value': lambda phi0=0,  phi1=0, lambd=0: -phi0 + phi1 / (1-lambd)**2,
        'type': 'intermediary',
    },
    'kappa': {
        'value': lambda k0=0, k1=0, k2=0, Pi=0, Y=0: k0 + k1 * np.exp(k2*Pi/Y),
        'type': 'intermediary',
    },
    'I': {
        'value': lambda Y=0, kappa=0: Y * kappa,
        'type': 'intermediary',
    },
    'g': {
        'value': lambda omega=0, nu=0, delta=0: (1-omega) / nu - delta,
        'type': 'auxilliary',
    },
    'd': {
        'value': lambda D=0, Y=0: D / Y,
        'type': 'auxilliary',
    },
    'pi': {
        'value': lambda omega=0, r=0, d=0: 1 - omega - r*d,
        'type': 'auxilliary',
    },
    'i': {
        'value': lambda Y=0: Y*0,
        'type': 'auxilliary',
    },
}
