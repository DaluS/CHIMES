# -*- coding: utf-8 -*-
"""
D. Bastidas et al., Math. and Financial Economics, 2018

"Daniel Bastidas, Adrien Fabre, Florent Mc Isaac"
"Minskyan classical growth cycles: "
"stability analysis of a stock-flow consistent macrodynamic model, "
"Mathematics and Financial Economics,"
"2018, issue 13, pages 359-391"

'https://doi.org/10.1007/s11579-018-0231-6'


DESCRIPTION :
    * 2 sector model ( Household and Firms ) with loans.
    * The structure is the same as in a Goodwin-Keen typical models
    * Productiob function has been substituted from an optimised Leontiev to a CES (Constant Elasticity of substitution)
    * In consequence the optimisation problem makes the quantity of workers a function of wage share

This is the reduced version : the dynamical variables are lambda,omega,d
s dynamics is for speculation

We add explicitely the calculation of L

TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np
from pygemmes._models import Funcs  # To get access to all pre-coded practical functions

# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,

        # Stock-flow consistency
        'D': {
            'func': lambda I=0, Pi=0, Speculation=0: I - Pi-Speculation,
            'com': 'Debt as Investment-Profit difference', },
        'K': {
            'func': lambda I=0, itself=0, delta=0, p=1: I/p - itself * delta,
            'com': 'Capital evolution from investment and depreciation', },

        # Funcs.Kappa.kfromI,

        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,

    },

    # Intermediary relevant functions
    'statevar': {

        # Production function and its employement
        'cesLcarac': Funcs.ProductionWorkers.cesLcarac,
        'cesYcarac': Funcs.ProductionWorkers.cesYcarac,
        'nu': Funcs.ProductionWorkers.CES_Optimised.nu,
        'omegacarac': Funcs.ProductionWorkers.omegacarac,
        'l': Funcs.ProductionWorkers.CES_Optimised.l,

        'Y': Funcs.ProductionWorkers.CES_Optimised.Y,
        'L': Funcs.ProductionWorkers.CES_Optimised.L,

        # Parametric behavior functions
        'phillips': Funcs.Phillips.exp,
        'kappa': Funcs.Kappa.exp,
        'Speculation': Funcs.Speculation.exp,
        'inflation': Funcs.Inflation.markup,
        'I': Funcs.Kappa.ifromkappa,

        # Intermediary variables with their definitions
        'd': Funcs.Definitions.d,
        'pi': Funcs.Definitions.pi,
        'lambda': Funcs.Definitions.lamb,
        'omega': Funcs.Definitions.omega,
        'GDP': Funcs.Definitions.GDPmonosec,
        's': Funcs.Definitions.s,

        'c': {
            'func': lambda w=0, a=1: w/a,
            'com': 'price with only labor salary'},

        # Stock-Flow consistency
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },

        # UNPRACTICAL
        'g': {
            'func': lambda I=0, delta=0, p=1, K=1: (I/p - K * delta)/K,
            'com': 'Homemade expression', },

    },
    'param': {
        'CESexp': {
            'value': 1000,
            'definition': 'Coefficient in CES function'
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'article': {
        'fields': {
            # Time parameter
            'dt': 0.01,
            'Tmax': 200,

            # initial ode values
            'K': 2.7,
            'w': .85,
            'D': 0.1,
            'a': 1,
            'N': 1,

            # Production function
            'A': 1./3.,
            'b': 0.135,
            'CESexp': 100,

            # Time rates
            'alpha': 0.02,
            'n': 0.01,
            'delta': 0.01,
            'r': 0.04,
            'eta': 0.1,

            # Phillips curve
            'phiexp0': -0.01,
            'phiexp1': 2.35e-23,
            'phiexp2': 50,

            # Kappa curve
            'k0': 0.05,
            'k1': 0.05,
            'k2': 1.75,

            # Speculation curve
            'SpecExpo1': 0,
            'SpecExpo2': 0,
            'SpecExpo3': 0,
            'SpecExpo4': 0,

        },
        'com': 'speculation removed',
        'plots': [],
    },
}
