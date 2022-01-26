#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Resource only model based on extensive variables.
TYPICAL BEHAVIOR : 
LINKTOARTICLE: voir Figure 16 du rapport de stage

Created on Tue Jan  4 15:12:33 2022
@author: Camille Guittonneau
"""

import numpy as np


# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types

_LOGICS = {
    'ode': {
        'R': {
            'func': lambda a=0, itself=0, M=0: a * itself - M,
            'com': 'reserve of resource', },
        'K_R': {
            'func': lambda I_R=0, itself=0, delta_R=0: I_R - itself * delta_R,
            'com': 'Extraction capital evolution from investment and depreciation', },
        },
    # Intermediary relevant functions
    'statevar': {
        'M': {
            'func': lambda b=0, R=0, K_R=0: b * R * K_R,
            'com': 'extraction output as product of extraction efficiency, extraction capital, and reserve', },
        'I_R': {
            'func': lambda kappa_R=0, M=0: kappa_R * M,
            'com': 'value of investment in extraction capital' , },
        },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.01,
            'R': 100000,
            'M': 100,
            'a': 0.1,
            'b': 0.1,
            'K_R': 2.9,
            'delta_R': .005,
            'kappa_R': .05,
        },
        'com': '',
        'plots': [],
    },
}











