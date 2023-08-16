# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    Leontiev production function replaced by a CES function
    replaced by a CES (its generalisation).

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""
import numpy as np

_LOGICS = {
    'statevar': {
        # Characteristics of a CES
        'cesLcarac': {
            'func': lambda A, K, a, b, CESexp: A*(K/a) * (1-b)**(1/CESexp),
            'com': 'Typical Labour in CES',
            'size': ['Nprod'],
        },
        'cesYcarac': {
            'func': lambda K, A, b, CESexp: K*A*b**(-1/CESexp),
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
    'size': {'Nprod': {'list':['1']},},
}

_PRESETS = {
    'CES': {
        'fields': {},
        'com': (
            ''),
        'plots': {
        },
    },
}
