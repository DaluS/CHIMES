# -*- coding: utf-8 -*-
"""
"""
# ---------------------------
# user-defined function order (optional)

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

_LOGICS = {

    'ode': {
        'lambda': {
            'logic': lambda itself=0, g=0, alpha=0, beta=0: itself * (
                g - alpha - beta),
            'com': 'reduced 2variables dynamical expression'
        },
        'omega': {
            'logic': lambda itself=0, phillips=0: itself * phillips,
            'com': 'reduced 2variables dynamical expression',
            # 'initial': 0.8,
        },
    },

    'statevar': {
        'phillips': {
            'logic': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (
                1 - lamb)**2,
            'com': 'divergin Philips',
        },
        'g': {
            'logic': lambda pi=0, nu=1, delta=0: pi / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'logic': lambda omega=0: 1. - omega,
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
}
