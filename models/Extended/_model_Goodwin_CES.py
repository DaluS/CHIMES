# -*- coding: utf-8 -*-
'''Goodwin with a CES production function'''

_DESCRIPTION="""
DESCRIPTION :

    This is a small modificaiton of Goodwin : the Leontiev optimised function has been
    replaced by a CES (its generalisation).

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel

# ######################## LOGICS #######################################
_LOGICS,_PRESETS0= importmodel('Goodwin')

_CES_LOGICS = {
    'statevar': {
        # Characteristics of a CES
        'cesLcarac': {
            'func': lambda u,A, K, a, b, CESexp: A*(u*K/a) * (1-b)**(1/CESexp),
            'com': 'Typical Labour in CES',
            'size': ['Nprod'],
        },
        'cesYcarac': {
            'func': lambda u,K, A, b, CESexp: u*K*A*b**(-1/CESexp),
            'com': 'Typical Y in CES',
            'size': ['Nprod'],
        },
        'omegacarac':  {
            'func': lambda w, cesLcarac, p, cesYcarac: w*cesLcarac/(p*cesYcarac),
            'com': 'Typical omega from K,p,w',
            'symbol': '$\omega^c$',
            'size': ['Nprod'],
        },

        # From it are deduced optimised quantities
        'nu': {
            'func': lambda omega, b, A, CESexp: ((1 - omega) / b)**(-1./CESexp) / A,
            'com': 'nu deduced from CES optimisation of profit',
            'size': ['Nprod'],
        },
        'l': {
            'func': lambda omegacarac, CESexp: np.maximum((omegacarac**(-CESexp/(1+CESexp)) - 1)**(1/CESexp),0),
            'com': 'impact of elasticity on real employment',
            'size': ['Nprod'],
        },

        # From it are deduced Labor and Output
        'Y': {
            'func': lambda u,K, omegacarac, l, b, CESexp, A: u*K*((1 - omegacarac*l) / b)**(1./CESexp) * A,
            'com': 'Y CES with optimisation of profit',
            'size': ['Nprod'],
        },
        'L': {
            'func': lambda l, cesLcarac: cesLcarac*l,
            'com': 'L CES, deduced from l',
            'size': ['Nprod'],
        },
    },
    'parameter': {
        'u': {'value':1},

    },
    'size': {'Nprod': {'list':['1']},},
}

_LOGICS= mergemodel(_LOGICS, _CES_LOGICS, verb=False)


# ####################### PRESETS #######################################
_PRESETS = {
    'CES': {
        'fields': {
            'dt': 0.01,
            'Tmax': 100,

            'a': 1,
            'N': 1,
            'K': 2.75,
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'delta': .005,
            'phinull': 0.1,

            'CESexp': 1000,
            'A': 1/3,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'plotnyaxis': [{'x': 'time',
                           'y': [['lambda', 'lamb0'],
                                 ['omega'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            'plot3D': [{'x': 'lamb0',
                        'y': 'omega',
                        'z': 'lambda',
                        'cinf': 'time',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [],
        },
    },
}
