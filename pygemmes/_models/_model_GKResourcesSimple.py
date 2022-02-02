#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin-Keen Resource model based on extensive variables.
TYPICAL BEHAVIOR :
LINKTOARTICLE: voir Figure 16 du rapport de stage

Created on Thu Jan  20 2022
@author: Camille Guittonneau
"""

import numpy as np
from pygemmes._models import Funcs


# ---------------------------
# user-defined model
# contains parameters and functions of various types

_LOGICS = {
    'ode': {
        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,

        'K': {
            'func': lambda I=0, itself=0, delta=0: I - itself * delta,
            'com': 'production capital evolution from investment and depreciation', },


        'R': {
            'func': lambda LVa=0, itself=0, M=0: LVa * itself - M,
            'com': 'reserve of resource', },
        'K_R': {
            'func': lambda I_R=0, itself=0, delta_R=0: I_R - itself * delta_R,
            'com': 'Extraction capital evolution from investment and depreciation', },

        'D_R': {
            'func': lambda I_R=0, Pi_R=0: I_R - Pi_R,
            'com': 'Debt as Investment-Profit difference', },
        'D': {
            'func': lambda p=0, I=0, Pi=0: p*I - Pi,
            'com': 'Debt as Investment-Profit difference', },
        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,

        'p_R': {
            'func': lambda itself=0, inflation_R=0: itself * inflation_R,
            'initial': .5,
            'com': 'markup inflation', },
    },

    # Intermediary relevant functions
    'statevar': {

        # Productive flux
        'M': {
            'func': lambda LVb=0, R=0, K_R=0: LVb * R * K_R,
            'com': 'extraction output as product of extraction efficiency, extraction capital, and reserve', },
        'Y': {
            'func': lambda Kstar=0, nu=1: Kstar/nu,
            'com': 'Leontief optimized production output', },
        'GDP': Funcs.Definitions.GDPmonosec,

        # PRODUCTION RELATED QUANTITIES
        'Kstar': {
            'func': lambda K=0, M=0, theta=0: (K**theta)*(M**(1-theta)),
            'com': 'capital boost from mining', },
        'L': {
            'func': lambda Kstar=0, nu=1, a=1: Kstar / (nu * a),
            # 'initial': .9,
            'com': 'Full instant employement based on capital', },

        # Investment flux
        'I_R': {
            'func': lambda kappa_R=0, M=0, p_R=0: kappa_R * M*p_R,
            # 'initial': ,
            'com': 'investment monetary', },
        'I': {
            'func': lambda kappa=0, GDP=0: kappa * GDP,
            # 'initial': ,
            'com': 'investment in monetary', },

        # Stock flow consistency
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, varphi=0, p_R=0, M=0, r=0, D=0: GDP - w * L - r * D - (1-varphi)*p_R*M,
            'com': 'Profit for production-Salary-debt func', },
        'Pi_R': {
            'func': lambda varphi=0, p_R=0, M=0, r=0, D_R=0: (1-varphi)*p_R*M - r * D_R,
            'com': 'Profit for production-Salary-debt func', },
        'c': {
            'func': lambda omega=0, varphi=0, m=0: omega + (1 - varphi) * m,
            'com': 'production cost', },

        # Definitions
        'lambda': Funcs.Definitions.lamb,
        'omega': Funcs.Definitions.omega,
        'd': Funcs.Definitions.d,
        'pi': Funcs.Definitions.pi,
        'inflation': Funcs.Inflation.markup,

        'inflation_R': {
            'func': lambda mu=0, eta_R=0, varphi=0, p_R=1: eta_R * (mu * varphi - 1),
            'com': 'extraction markup dynamics', },
        'pi_R': {
            'func': lambda Pi_R=0, p_R=1, M=1: Pi_R/(p_R*M),
            # 'initial': ,
            'com': 'relative profit', },
        'd_R': {
            'func': lambda D_R=0, p_R=1, M=1: D_R / (p_R * M),
            # 'initial': ,
            'com': 'private extraction debt ratio', },

        # Parametric curve
        'phillips': Funcs.Phillips.div,
        'kappa': Funcs.Kappa.exp,

        'kappa_R': {
            'func': lambda k0=0, k1=0, k2=0, pi_R=0: k0 + k1 * np.exp(k2 * pi_R),
            'com': 'Relative GDP investment through relative profit', },

        # Growth
        'g': {
            'func': lambda I=0, K=1, delta=0, p=1: (I/p - K * delta)/K,
            # 'initial': ,
            'com': 'Explicit'},
        'g_r': {
            'func': lambda I_R=0, K_R=1, delta_R=0, p_R=1: (I_R/p_R - K_R * delta_R)/K_R,
            'definition': 'Growth rate of mining sector',
            'com': 'CAREFUL UNIT I_R'},



    },


    # Parameters
    'param':
        {
        'LVa': {
            'value': .99,
            'definition': 'reserve growth'},
        'LVb': {
            'value': .1,
            'definition': 'predation rate'},
        'theta': {
            'value': 1,
            'definition': 'Cobb-Douglas coefficient'},
        'delta_R': {
            'value': .005,
            'definition': 'extraction capital depreciation rate'},

        'varphi': {
            'value': .0,
            'definition': 'extraction cost'},
        'm': {
            'value': .0,
            'definition': 'pro cost coeff'},

        'eta_R': {
            'value': 1,
            'definition': 'time rate on resource price adjustment'},


    },


}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {'K_R': 0.0001,
                   'D_R': 0.001,
                   'p_R': 0.1, },
        'com': '',
        'plots': {
            'timetrace': [{}],
            'plotnyaxis': [{'x': 'time',
                           'y': [['lambda', 'omega'],
                                 ['d'],
                                 ['kappa', 'pi'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            'plot3D': [{'x': 'lambda',
                        'y': 'omega',
                        'z': 'd',
                        'cinf': 'pi',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [{'title': '',
                             'lw': 1,       # optional
                             'idx': 0,      # optional
                             'color': 'k'},  # optional
                            ],
        },
    },
}


# 'inflation_R': {
#             'func': lambda mu=0, eta_R=0, varphi=0: eta_R * (mu * varphi - 1),
#             #'initial': ,
#             'com': 'extraction markup dynamics', },


# 'inflation_R': {
#     'func': lambda mu=0: 0,
#     #, eta_R=0, varphi=0: eta_R * (mu * varphi - 1),
#     #'initial': ,
#     'com': 'extraction markup dynamics', },


# 'inflation_R':     {
#             'value': .1,
#             'definition': 'CACA'},
