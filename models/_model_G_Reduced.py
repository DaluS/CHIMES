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

_DESCRIPTION = """
    DESCRIPTION : This is the simplest economic post-keynesian model
    TYPICAL BEHAVIOR : metastable oscillations around a solow point
    LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
        Carl Feinstein, editor, Socialism, capitalism
        and economic growth. Cambridge, UK: Cambridge University Press.
        """


# ---------------------------
# user-defined model
# contains parameters and functions of various types

_DPARAM = {

    # ---------
    # %% Fixed-value parameters
    'alpha': None,
    'delta': None,
    'beta': None,
    'nu': None,
    'phinull': None,

    # ---------
    # %% functions
    'lambda': {
        'func': lambda itself=0, g=0, alpha=0, beta=0: itself * (g - alpha - beta),
        'eqtype': 'ode',
        'initial': 0.97,
    },
    'omega': {
        'func': lambda itself=0, phillips=0: itself * phillips,
        'eqtype': 'ode',
        'initial': 0.85,
    },

    # Intermediary
    'phillips': {
        'func': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (1 - lamb)**2,
        'eqtype': 'intermediary',
    },
    'g': {
        'func': lambda pi=0, nu=1, delta=0: pi / nu - delta,
        'eqtype': 'intermediary',
    },
    'pi': {
        'func': lambda omega=0: 1. - omega,
        'eqtype': 'intermediary',
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
# List of presets for specific interesting simulations

_PRESETS = {
    'smallcycle': {
        'fields': {
            'lambda': .97,
            'omega': .85,
        },
        'com': (
            'gives simple '
            'stable sinusoidal oscillations'
        ),
    },
    'bigcycle': {
        'fields': {
            'lambda': .99,
            'omega': .85,
        },
        'com': (
            'give extremely '
            'violent stable oscillations'
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
