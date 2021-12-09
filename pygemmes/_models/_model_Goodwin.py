# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model based on extensive variables.
TYPICAL BEHAVIOR : Oscillations around Solow point
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


# ---------------------------
# user-defined function order (optional)
_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types
_LOGICS = {
    'ode': {
        'a': {
            'func': lambda alpha=0, itself=0: alpha * itself,
            'com': 'Exogenous technical progress as an exponential', },
        'N': {
            'func': lambda n=0, itself=0: n * itself,
            'com': 'Exogenous population as an exponential', },
        'K': {
            'func': lambda I=0, itself=0, delta=0: I - itself * delta,
            'com': 'Capital evolution from investment and depreciation', },
        'w': {
            'func': lambda phillips=0, itself=0: itself * phillips,
            'com': 'salary through negociation', },
    },
    # Intermediary relevant functions
    'statevar': {
        'Y': {
            'func': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ', },
        'L': {
            'func': lambda K=0, a=1, nu=1: K / (a * nu),
            'com': 'Full instant employement based on capital', },
        'Pi': {
            'func': lambda Y=0, w=0, L=0: Y - w * L,
            'com': 'Profit for production-Salary', },
        'lambda': {
            'func': lambda L=0, N=1: L / N,
            'com': 'employement rate', },
        'omega': {
            'func': lambda w=0, L=0, Y=1: w * L / Y,
            'com': 'wage share', },
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (1 - lamb)**2,
            'com': 'Wage increase rate through employement and profit', },
        'I': {
            'func': lambda Y=0, pi=0: Y*pi,
            'com': 'Investment value', },
        'pi': {
            'func': lambda Pi=0, Y=1: Pi/Y,
            'com': 'relative profit', },
        'g': {
            'func': lambda omega=0, nu=1: (1-omega)/nu,
            'com': 'relative growth rate'}
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {
            'a': 1,
            'N': 1,
            'K': 2.7,
            'w': .85,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
        },
        'com': (
            'Oscillations'),
        'plots': [],
    },
}
