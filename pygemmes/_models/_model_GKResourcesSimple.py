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


# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types

_LOGICS = {
    'ode': {
        'R': {
            'func': lambda LVa=0, itself=0, M=0: LVa * itself - M,
            'com': 'reserve of resource', },
        'K_R': {
            'func': lambda I_R=0, itself=0, delta_R=0: I_R - itself * delta_R,
            'com': 'Extraction capital evolution from investment and depreciation', },
        'K': {
            'func': lambda I=0, itself=0, delta=0: I - itself * delta,
            'com': 'production capital evolution from investment and depreciation', },
        'ell': {
            'func': lambda alpha=0, itself=0: alpha * itself,
            'com': 'productivity; Exogenous technical progress as an exponential', },
        'N': {
            'func': lambda n=0, itself=0: n * itself,
            'com': 'Exogenous population as an exponential', },
        'D_R': {
            'func': lambda p_R=0, I_R=0, Pi_R=0: p_R*I_R - Pi_R,
            'com': 'Debt as Investment-Profit difference', },
        'D': {
            'func': lambda p=0, I=0, Pi=0: p*I - Pi,
            'com': 'Debt as Investment-Profit difference', },
        'w': {
            'func': lambda phillips=0, itself=0, gammai=0, inflation=0: itself * (phillips + gammai*inflation),
            'com': 'salary through negociation', },
        'p': {
            'func': lambda itself=0, inflation=0: itself * inflation,
            'com': 'markup inflation', },
        'p_R': {
            'func': lambda itself=0, inflation_R=0: itself * inflation_R,
            'com': 'markup inflation', },
        },
        
    # Intermediary relevant functions
    'statevar': {
        'M': {
            'func': lambda LVb=0, R=0, K_R=0: LVb * R * K_R,
            'com': 'extraction output as product of extraction efficiency, extraction capital, and reserve', },
        'I_R': {
            'func': lambda kappa_R=0, M=0: kappa_R * M,
            'com': 'value of investment in extraction capital' , },
        'I': {
            'func': lambda kappa=0, Y=0: kappa * Y,
            'com': 'value of investment in production capital' , },
        'Y': {
            'func': lambda Kstar=0, L=0: min(Kstar/nu, ell*L),
            'com': 'Leontief optimized production output' , },
        'GDP': {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'Output with selling price ', },
        'Kstar': {
            'func': lambda K=0, M=0: (K**theta)*(M**(1-theta)),
            'com': 'matter capital' , },
        
        'L': {
            'func': lambda K=0, a=1, nu=1: K / (a * nu),
            'com': 'Full instant employement based on capital', },
        
        'Pi' : {
            'func': lambda GDP=0, w=0, L=0, varphi=0, p_R=0, M=0: GDP - w * L - (1-varphi)*p_R*M,
            'com': 'Profit for production-Salary-debt func', },

        'Pi_R' : {
            'func': lambda varphi=0, p_R=0, M=0: (1-varphi)*p_R*M,
            'com': 'Profit for production-Salary-debt func', },
        'pi': {
            'func': lambda Pi=0, GDP=1: Pi/GDP,
            'com': 'relative profit', },
        'pi_R': {
            'func': lambda Pi_R=0, p_R=1, M=1: Pi_R/(p_R*M),
            'com': 'relative profit', },
        'inflation': {
            'func': lambda mu=0, eta=0, omega=0: eta*(mu*omega-1),
            'com': 'markup dynamics', },
        'inflation_R'
        'lamb': {
            'func': lambda L=0, N=1: L / N,
            'com': 'employement rate', },
        'omega': {
            'func': lambda w=0, L=0, GDP=1: (w * L) / GDP,
            'com': 'wage share', },
        'd': {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'private debt ratio', },
        'd_R': {
            'func': lambda D_R=0, p_R=1, M=1: D_R / (p_R * M),
            'com': 'private extraction debt ratio', },
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: -phi0 + phi1 / (1 - lamb)**2,
            'com': 'Wage increase rate through employement and profit', },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, pi=0: k0 + k1 * np.exp(k2 * pi),
            'com': 'Relative GDP investment through relative profit', },
        'kappa_R': {
            'func': lambda k0=0, k1=0, k2=0, pi_R=0: k0 + k1 * np.exp(k2 * pi_R),
            'com': 'Relative GDP investment through relative profit', },
        'g': {
            'func': lambda I=0, K=1, delta=0, p=1: (I - K * delta)/K,
            'com': 'relative growth rate'},
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
            'LVa': 0.1,
            'LVb': 0.1,
            'K_R': 2.9,
            'delta': .005,
            'delta_R': .005,
            'kappa': .05,
            'kappa_R': .05,
            'Kstar': 17,
            'K': 2.9,
            'L':0.9,
            'nu': 3,
            'ell': 1,
            'theta':0.5,
            'alpha': 0.02,
            'N': 1,
            'n': 0.025,
            'gammai': 0.5,
            'k0': -0.0065,
            'k1': np.exp(-5),
            'k2': 20,
        },
        'com': '',
        'plots': [],
    },
}











