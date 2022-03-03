# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    PREPARE A CONSUMPTION LOGICS FOR MONOGEM

LINKTOARTICLE:

@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs
# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'H': {
            'func': lambda G=0, deltah=0, itself=0, rho=0: G - deltah*itself - rho*itself,
            'com': 'Household capital accumulation'},
        'Dh': {
            'func': lambda itself=0, w=0, L=0, r=0, p=0, C=0: -w*L + r*itself + C*p,
            'com': 'Stock-flow on household, no share/bank profits'},
    },

    # Intermediary relevant functions
    'statevar': {
        'C': {
            'func': lambda Hid=0, H=0, fC=1, rho=0: (Hid-H)*fC + rho*H,
            'com': 'consumption to rectify possession+its consumption'},
        'Hid': {
            'func': lambda N=0, h=0, x=0, w=0, p=1, Omega0=0: N*h*(1+np.exp(-x*(w/p) - Omega0))**-1,
            'com': 'Ideal Possession from logistic on salary'},
        'Omega': {
            'func': lambda w=0, p=1, lamb=0, L=1, r=0, D=0: lamb*(w/p + r*D/(p*L)),
            'com': 'Purchasing power'},
    },
    'param': {
    },
}



# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{}],
            'phasespace': [{}],
            '3D': [{}],
            'byunits': [],
        },
    },
}
