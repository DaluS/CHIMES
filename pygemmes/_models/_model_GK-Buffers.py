# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin-Keen model based on extensive variables.

We added the following processes inside :
    * Endogenous productivity growth from growth itself : (beta=0 for classic situation)
    * Buffer on capital accumulation : Investment in capital goes first in Bk then in K, with a rate of change fk
    * NOTTAKEN INTO ACCOUNT HERE Buffer on wage negociation : Percieved employement is the consequence of a societal buffer, with a rate of change flambda
    * Profit on wage negociation : Philips curve is dampened by firm's profit, with a convexity coefficient Zpi
    * Solvability in investment : Banks refuse to lend money if firm has a small solvalibity, with a convexity coefficient Zs


TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

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
        'a': {
            'func': lambda alpha=0, itself=0, beta=0, g=0: alpha * itself + beta * g,
            'com': 'Endogenous technical progress through growth', },
        'N': {
            'func': lambda n=0, itself=0: n * itself,
            'com': 'Exogenous population as an exponential', },
        'B': {
            'func': lambda I=0, itself=0, fk=0, p=1: I/p - itself * fk,
            'com': 'Capital Buffer with constant timerate', },
        'K': {
            'func': lambda I=0, itself=0, delta=0, B=0, fk=0: B*fk - itself * delta,
            'com': 'Capital evolution from buffer and depreciation', },
        'D': {
            'func': lambda I=0, Pi=0: I - Pi,
            'com': 'Debt as Investment-Profit difference', },
        'w': {
            'func': lambda phillips=0, itself=0, gammai=0, inflation=0, pi=0, zpi=0: itself * (phillips*pi**zpi + gammai*inflation),
            'com': 'salary through negociation+profit', },
        'p': {
            'func': lambda itself=0, inflation=0: itself * inflation,
            'com': 'markup inflation', },
    },
    # Intermediary relevant functions
    'statevar': {
        'Y': {
            'func': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ', },
        'GDP': {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'Output with selling price ', },
        'inflation': {
            'func': lambda mu=0, eta=0, omega=0: eta*(mu*omega-1),
            'com': 'markup dynamics', },
        'L': {
            'func': lambda K=0, a=1, nu=1: K / (a * nu),
            'com': 'Full instant employement based on capital', },
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },
        'lambda': {
            'func': lambda L=0, N=1: L / N,
            'com': 'instant employement rate', },
        'omega': {
            'func': lambda w=0, L=0, Y=1, p=1: (w * L) / (Y*p),
            'com': 'wage share', },
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: (-phi0 + phi1 / (1 - lamb)**2),
            'com': 'salary negociation on employement and profit',
        },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, pi=0: k0 + k1 * np.exp(k2 * pi),
            'com': 'Relative GDP investment through relative profit', },
        'I': {
            'func': lambda GDP=0, kappa=0, d=0, nu=1, zsolv=0: GDP * kappa * (1 - d/nu)**zsolv,
            'com': 'Investment value', },
        'd': {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'private debt ratio', },
        'pi': {
            'func': lambda Pi=0, GDP=1: Pi/GDP,
            'com': 'relative profit', },
        'g': {
            'func': lambda I=0, K=0, delta=0, B=0, fk=0: B*fk - K * delta,
            'com': 'relative growth rate'},
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'Basic': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': .85*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
            'p': 1.3,
            'eta': 0.1,
            'gammai': 0.5,
            'B': 0,
            'fk': 100,
            'flamb': 100,
            'beta': 0,
            'zpi': 0,
            'zsolv': 0,

        },
        'com': (
            'This preset gives a pure GK behavior'),
        'plots': [],
    },
    'Default': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'D': 2,
            'K': 2.9,
            'w': .85*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
            'r': 0.03,
            'p': 1.3,
            'eta': 0.1,
            'gammai': 0.5,
            'B': 0,
            'fk': 0.4,
            'flamb': 0.5,
            'beta': 0.1,
            'zpi': 2,
            'zsolv': 2,
        },
        'com': (
            'Basic run using all specificities of this model'),
        'plots': [],
    },
}
