# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Template for a multisectorial model. It is meaningless, just for numerical test

"""

import numpy as np
from pygemmes._models import Funcs


# ######################## OPERATORS ####################################

# #######################################################################

_LOGICS = {
    'differential': {
        'Z': {
            'func': lambda OPER: OPER,
            'size': ['Nprod', ],
            'initial': 1,
        },

        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,

        # Stock-flow consistency
        'K': Funcs.Kappa.kfromIr,

        # Price Dynamics
        'w': {
            'func': lambda phillips, w, pi: w * phillips,
            'com': 'Phillips impact (no negociation)'
        }
    },
    'statevar': {

        # Production function and its employement
        'Y': Funcs.ProductionWorkers.Leontiev_Optimised.Y,
        'L': Funcs.ProductionWorkers.Leontiev_Optimised.L,

        # Parametric behavior functions
        'phillips': Funcs.Phillips.div,
        'I': Funcs.Kappa.ifromnobank,
        'Ir': Funcs.Kappa.irfromI,
        # Intermediary variables with their definitions
        'pi': Funcs.Definitions.pi,
        'employment': Funcs.Definitions.employment,
        'omega': Funcs.Definitions.omega,
        'GDP': Funcs.Definitions.GDPmonosec,

        'c': Funcs.Inflation.costonlylabor,

        # Stock-Flow consistency
        'Pi': {
            'func': lambda GDP, w, L, r, D: GDP - w * L,
            'com': 'Profit for production-Salary', },

        # Auxilliary for practical purpose
        'g': {
            'func': lambda I, K, delta: (I - K * delta) / K,
            'com': 'relative growth rate'},

        'OPER': {
            'func': lambda Z, MATRIX: np.matmul(MATRIX,Z),
            'size': ['Nprod', ],
        },
    },
    'parameter': {
        'MATRIX': {
            'value': 0,
            'size': ['Nprod', 'Nprod']
        },
    },
    'size': {
        'Nprod': {
            #'value': 4,
            'list': ['energy','mine','capital','consumption'],
        },
    },
}

_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
