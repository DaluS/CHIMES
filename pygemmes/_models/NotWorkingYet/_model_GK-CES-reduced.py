# -*- coding: utf-8 -*-
"""
D. Bastidas et al., Math. and Financial Economics, 2018

"Daniel Bastidas, Adrien Fabre, Florent Mc Isaac"
"Minskyan classical growth cycles: "
"stability analysis of a stock-flow consistent macrodynamic model, "
"Mathematics and Financial Economics,"
"2018, issue 13, pages 359-391"

'https://doi.org/10.1007/s11579-018-0231-6'


DESCRIPTION :
    * 2 sector model ( Household and Firms ) with loans.
    * The structure is the same as in a Goodwin-Keen typical models
    * Productiob function has been substituted from an optimised Leontiev to a CES (Constant Elasticity of substitution)
    * In consequence the optimisation problem makes the quantity of workers a function of wage share

This is the reduced version : the dynamical variables are lambda,omega,d
s dynamics is for speculation

We add explicitely the calculation of L

TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np
from pygemmes._models import Funcs  # To get access to all pre-coded practical functions

# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # reduced system after paper derivation
        'omega': {
            'func': lambda itself=1, eta=1, phillips=1, alpha=0.1: itself * (eta / (1 + eta)) * (phillips - alpha),
            'com': 'Explicit reduced dynamics'
        },
        'lambda': {
            'func': lambda g=0, alpha=0, n=0: g - alpha - n,
            'com': "explicit reduced dynamics",
        },
        'd': {
            'func': lambda itself=0, kappa=0, pi=0, g=0, s=0: -itself*g + kappa - pi + s,
            'com': "explicit reduced dynamics",
        },
        's': {
            'func': lambda itself=0, Speculation=0, g=0, weirdterm=0: itself*(Speculation - g + weirdterm),
            'com': "explicit reduced dynamics",
        },

        # Not needed for computation
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,
        'K': {
            'func': lambda g=0, itself=0: itself * g,
            'com': 'auxilliary from growth',
        },


    },

    # Intermediary relevant functions
    'statevar': {
        # Needed for computation
        'phillips': Funcs.Phillips.exp,
        'kappa': Funcs.Kappa.exp,
        'Speculation': Funcs.Speculation.exp,

        'pi': {
            'func': lambda omega=1, r=1, d=1: 1 - omega - r*d,
            'com': 'stockflow reduced',
        },

        'weirdterm': {
            'func': lambda eta=1, phillips=1, alpha=0.1, omega=0.5: (1 / (1 + eta)) * (phillips - alpha) * omega/(1-omega),
            'com': 'compensing term in all EQ',
        },
        # Not needed for computation
        'L': {
            'func': lambda N=0, lamb=0: lamb*N,
            'com': 'Auxilliary forn lambda'
        },
        'g': {
            'func': lambda kappa=0, nu=1, delta=0, weirdterm=0: kappa/nu - delta - weirdterm,
            'com': 'explicit expression',
        },


    },
    'param': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'article': {
        'fields': {
            # Time parameter
            'dt': 0.01,
            'Tmax': 200,

            # initial ode values
            'lambda': 0.96,
            'omega': 0.65,
            'd': 2.94,
            's': 0,

            # Production function
            #'A': 1./3.,
            #'b': 0.135,
            'eta': 100,

            # Time rates
            'alpha': 0.02,
            'n': 0.01,   # 'n' in _def_fields
            'delta': 0.01,
            'r': 0.04,

            # Phillips curve
            'phiexp0': -0.01,
            'phiexp1': 2.35e-23,
            'phiexp2': 50,

            # Kappa curve
            'k0': 0.05,
            'k1': 0.05,
            'k2': 1.75,

            # Speculation curve
            'SpecExpo1': 0,
            'SpecExpo2': 0,
            'SpecExpo3': 0,
            'SpecExpo4': 0,
        },
        'com': 'speculation removed',
        'plots': [],
    },
}
