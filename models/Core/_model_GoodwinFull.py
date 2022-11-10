# -*- coding: utf-8 -*-
"""
This is a basic Goodwin model :
    * Two sectors
    * Exogenous technical progress, exogenous population
    * Capital accumulation through investment of profits
    * Consumption through salary
    * Salary-Profit through Philips curve
    * No money, no inflation
    * No loan possibility


The interesting things :
    * growth is an emergent property
    * Economic cycles (on employment and wage share) are an emergent property
    * trajectories are closed in the phasespace (lambda, omega) employment - wageshare

This construction has debt and inventory possible dynamics, but the Goodwin hypothesis are cancelling their dynamics

Link : https://en.wikipedia.org/wiki/Goodwin_model_(economics) (notations differs)

@author: Paul Valcke
"""
# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel


# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'a':{'func': lambda a, alpha: a*alpha,
            'com': 'ODE exogenous, exponential',},
        'N':{'func': lambda N, n: N*n,
            'com': 'ODE exogenous, exponential',},

        # Price Dynamics
        'w': {'func': lambda phillips, w : w * phillips,
            'com': 'Phillips impact (no negociation)'},
        'p': {'func': lambda p, inflation: p * inflation,
            'com': 'through inflation',},

        # Stock-flow consistency
        'K': Funcs.Kappa.kfromIr,

        #### DIFFERENTIAL THAT COULD EVOLVES BUT WILL HERE REMAINS CONSTANT
        'D': {'func': lambda D,r,C,p,w,L : r*D+w*L-p*C,
            'com': 'Full form No shareholding',
              'initial':0},
        'Dh': {'func': lambda Dh, r, C, p, w, L: r*Dh-w*L+p*C,
            'com': 'No shareholding',
               'initial':0},
        'V': {'func': lambda dotV: dotV,
            'com': 'expression in dotV',
              'initial':1},
        'u': {'func': lambda u, dotV, V, sigma: sigma * (1 - u) * (-dotV) / V,
            'com': 'response to inventory variation',
              'initial':.9999},

        #### AUXILLIARY
        'H': {'func': lambda C,deltah,H: C-deltah*H,
              'com': 'Consumption is accumulation',
              'initial':0},},

    # Intermediary relevant functions
    'statevar': {
        # Labor estimation
        'L': Funcs.ProductionWorkers.Leontiev_Optimised.Lfa,

        # PHYSICAL FLOWS
        'Y': {'func': lambda K,nu,u : u*K/nu,
              'com': 'prod with use rate'},
        'C': {'func': lambda w, L, p: w * L / p,
              'units': 'Units.y^{-1}'},
        'Ir': Funcs.Kappa.irfromI,
        'dotV': {'func':lambda Y,C,Ir: Y-C-Ir,
                 'com': 'non intermediary cons',
                 'units':'Units.y^{-1}'},

        # MONETARY FLOWS
        'GDP': Funcs.Definitions.GDPmonosec,
        'I': Funcs.Kappa.ifromnobank,
        'W': {'func': lambda w, L,: w * L,
            'definition': 'Total income of household',
            'com': 'no shareholding, no bank possession',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'},
        'Pi': {'func': lambda GDP, W, r, D: GDP - W - r * D,
            'com': 'Profit for production-Salary', },

        # PRICES DYNAMICS
        'phillips': Funcs.Phillips.div,
        'inflation': {
            'func': lambda p,c: 0,
            'com': 'No inflation',
        },
        'c': Funcs.Inflation.costonlylabor,

        # Intermediary variables with their definitions
        'pi': Funcs.Definitions.pi,
        'employment': Funcs.Definitions.employment,
        'omega': Funcs.Definitions.omega,

        # Auxilliary for practical purpose
        'g': {
            'func': lambda I, K, delta: (I - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'parameter': {},
    'size': {},
}


# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .5*1.19,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 31,
            'delta': .0051,
            'phinull': 0.11,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['lambda', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                    'y': 'omega',
                    'z': 'time',
                    'cinf': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': [.5, .5*1.2, .5*1.3, .5*1.5, .5*1.7],
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        'plots': {
            'timetrace': [{'keys': ['lambda', 'omega']}],
            'nyaxis': [],
            'phasespace': [{'x': 'lambda',
                           'y': 'omega',
                            'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}
