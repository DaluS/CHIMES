# -*- coding: utf-8 -*-
"""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
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
        'CO2AT': {
            'func': lambda Emission=0, phi12=0, CO2UP=0, CUP=1, CAT=1, itself = 0: Emission - phi12*itself + phi12*CAT/CUP*CO2UP,
            'com': 'CO2 in atmosphere (Gt C)',
        },
        'CO2UP': {
            'func': lambda phi12=0, phi23=0, CAT=1, CUP=1, CLO=1, CO2AT=0, itself=0, CO2LO=0: phi12*CO2AT - itself*(phi12*CAT/CUP-phi23) + phi23*CUP/CLO*CO2LO,
            'com': 'CO2 in upper layer of ocean (Gt C)',
        },
        'CO2LO': {
            'func': lambda phi23=0, CO2UP=0, CUP=1, CLO=1, itself = 0: phi23*CO2UP - phi23*CUP/CLO*itself,
            'com': 'CO2 in lower layer of ocean (Gt C)',
        },
        'T': {
            'func': lambda F=0, rhoAtmo=0, itself=0, gammaAtmo=0, T0=0, C=0: (F - rhoAtmo*itself - gammaAtmo*(itself-T0))/C,
            'com': 'Temperature anomaly in atmosphere',
        },
        'T0': {
            'func': lambda gammaAtmo=0, T=0, itself=0, C0=1: (gammaAtmo*(T-itself))/C0,
            'com': 'Temperature anomaly in ocean',
        },
    },
    'statevar': {
        'F': {
            'func': lambda F2CO2=0, CO2AT=0, CAT=1: F2CO2 / np.log(2) * np.log(CO2AT/CAT),
            'com': 'Temperature forcing from CO2',
        },
        'Emission': {
            'func': lambda Emission0=0, deltaEmission=0, time=0: Emission0*np.exp(-time*deltaEmission),
            'com': 'CO2 Emission rate ',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'Emmission0': 38,
        'deltaEmission': 0.01,
        'F2CO2': 3.681,
        'CO2AT': 851,
        'CO2UP': 460,
        'CO2LO': 1740,
        'CUP': 460,
        'CAT': 588,
        'CLO': 1720,
        'phi12': 0.024,
        'phi23': 0.001,
        'C': 1/0.098,
        'C0': 3.52,
        'rhoAtmo': 0,
        'gammaAtmo': 0.0176,
    },
    'com': ' Default run'},
}
