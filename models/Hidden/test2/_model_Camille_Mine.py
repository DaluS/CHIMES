#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION : Elements of the mining sectors in Camille's model for bisectorial
TYPICAL BEHAVIOR :
LINKTOARTICLE: voir Figure 16 du rapport de stage

Created on Thu Jan  20 2022
@author: Camille Guittonneau
"""

import numpy as np
from pygemmes._models import Funcs


_LOGICS = {
    'ode': {
        'R': {
            'func': lambda LVa=0, itself=0, Y_R=0: LVa * itself - Y_R,
            'com': 'reserve of resource', },
        'K_R': {
            'func': lambda I_R=0, itself=0, delta_R=0: I_R - itself * delta_R,
            'com': 'Extraction capital evolution from investment and depreciation', },

        'D_R': {
            'func': lambda I_R=0, Pi_R=0: I_R - Pi_R,
            'com': 'Debt as Investment-Profit difference', },
        'p_R': {
            'func': lambda itself=0, inflation_R=0: itself * inflation_R,
            'initial': .5,
            'com': 'markup inflation', },
    },

    # Intermediary relevant functions
    'statevar': {
        # Productive flux
        'Y_R': {
            'func': lambda LVb=0, R=0, K_R=0: LVb * R * K_R,
            'com': 'extraction output as product of extraction efficiency, extraction capital, and reserve', },
        # Investment flux
        'I_R': {
            'func': lambda kappa_R=0, M=0, p_R=0: kappa_R * M*p_R,
            # 'initial': ,
            'com': 'investment monetary', },
        # Stock flow consistency
        'Pi_R': {
            'func': lambda varphi=0, p_R=0, Y_R=0, r=0, D_R=0: (1-varphi)*p_R*Y_R - r * D_R,
            'com': 'Profit for production-Salary-debt func', },
        'inflation_R': {
            'func': lambda mu=0, eta_R=0, varphi=0, p_R=1: eta_R * (mu * varphi - 1),
            'com': 'extraction markup dynamics', },
        'pi_R': {
            'func': lambda Pi_R=0, p_R=1, Y_R=1: Pi_R/(p_R*Y_R),
            # 'initial': ,
            'com': 'relative profit', },
        'd_R': {
            'func': lambda D_R=0, p_R=1, Y_R=1: D_R / (p_R * Y_R),
            # 'initial': ,
            'com': 'private extraction debt ratio', },
        'kappa_R': {
            'func': lambda k0=0, k1=0, k2=0, pi_R=0: k0 + k1 * np.exp(k2 * pi_R),
            'com': 'Relative GDP investment through relative profit', },

        # Growth
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
        'fields': {},
        'com': '',
        'plots': {'plotbyunits': [{'title': '',
                                   'lw': 1,       # optional
                                   'idx': 0,      # optional
                                   'color': 'k'},  # optional
                                  ],
                  }
    },
}
