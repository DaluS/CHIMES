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


# ---------------------------
# user-defined function order (optional)

_FUNC_ORDER = None



# ---------------------------
# user-defined model
# contains parameters and functions of various types

_DPARAM = {

    # ---------
    # Fixed-value parameters
    'alpha': {'value': None},
    'delta': {'value': None},
    'beta': {'value': None},
    'nu': {'value': None},
    'phi0': {'value': None},
    'phi1': {'value': None},

    # ---------
    # functions

    # former variables

    # Intermediary
    'lambda': {
        'value': lambda lamb=0, g=0, alpha=0, beta=0: lambd*(g-alpha-beta),
        'type': 'intermediary',
    },
    'omega': {
        'value': lambda omega=0, philips=0: omega*phillips,
        'type': 'intermediary',
    },
    'philips': {
        'value': lambda phi0=0,  phi1=0, lambd=0: -phi0 + phi1 / (1-lamb)**2,
        'type': 'intermediary',
    },
    'g': {
        'value': lambda omega=0, nu=0, delta=0: pi / nu - delta,
        'type': 'auxilliary',
    },
    'pi': {
        'value': lambda omega=0, r=0, d=0: 1. - omega,
        'type': 'auxilliary',
    },
}
