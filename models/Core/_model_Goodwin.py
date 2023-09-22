'''Goodwin model: Stock-flow consistency core '''

_DESCRIPTION = """
* **Date    :** 
* **Article :** 
* **Author  :** Goodwin
* **Coder   :** Paul Valcke

This is a basic Goodwin model :
    * Two sectors
    * Exogenous technical progress, exogenous population
    * Capital accumulation through investment of profits
    * Consumption through salary
    * Salary-Profit through Philips curve
    * No money, no inflation
    * No loan possibility
    * Affine Phillips curve

The interesting things :
    * growth is an emergent property
    * Economic cycles (on employment and wage share) are an emergent property
    * trajectories are closed in the phasespace (employment, omega) employment - wageshare

Profit is not optimizing labor: labor is determined from capital (omega can be bigger than 1)
this conserve closed-loop phase-space trajectory

It is written with a price p=1 for homogeneity issues

"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from chimes._models import Funcs, importmodel,mergemodel

# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha },
        'N': {'func': lambda N,n        : N*n },
        'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
    },

    # Intermediary relevant functions
    'statevar': {
        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) },
        'employment' :{'func': lambda L,N: L/N },
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta },      
        
        'Y' :{'func': lambda K,nu: K/nu },
        'Pi':{'func': lambda p,Y,w,L: p*Y-w*L},
        'C' :{'func': lambda Y,Ir: Y-Ir },
        'Ir':{'func': lambda Pi: Pi },
        'L' :{'func': lambda Y,a: Y/a },

        'phillips'  :{'func': lambda employment, phi0,phi1: -phi0+phi1/(1-employment)**2,},

        #'phillips'  :{'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},
    },
    'parameter': {
        'p': {'value':1},
    },
    'size': {},
}

_SUPPLEMENTS={}

# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.1,
            'a': 1,
            'N': 1,
            'K': 2,
            'D': 0,
            'w': .75,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': 'Classic "Goodwin" Closed trajectory, here with negative profits.',
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'XY': [{'x': 'omega',
                            'y': 'employment',
                            'color': 'time',
                            'idx': 0}],
            'XYZ': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'time',
                    'color': 'pi',
                    'idx': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'nx':50,
            'dt': 0.1,
            'a': 1,
            'N': 1,
            'K': 2.7,
            'D': 0,
            'w': .5*np.arange(1,2,0.02),
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        'plots': {
            'cycles_characteristics':[{'xaxis':'omega',
                           'yaxis':'employment',
                           'ref':'employment',
                           'type1':'frequency'}]
        },
    },
}
