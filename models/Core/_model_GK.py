
"""Goodwin-Keen model: debt dynamics with residual consumption"""

_DESCRIPTION = """
* **Date    :** 2023/08/21
* **Article :** 
* **Author  :** Steve Keen
* **Coder   :** Paul Valcke

## Description
A Goodwin model with possibility of reducing consumption to increase investment.
It verifies Say's law and generate private debt. 
Converging equilibrium and possibility of Debt-Crisis

The Philips and the Kappa parameter functions are here respectively diverging and exponential


"""

import numpy as np
from chimes._models import Funcs, importmodel,mergemodel
from chimes._models import Operators as O
######################################################################

_LOGICS= {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha },
        'N': {'func': lambda N,n        : N*n },
        'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
        'p': {'func': lambda p,inflation: p*inflation },
        'D': {'func': lambda w,L,C,r,D,p,Pi,Delta: r*D + w*L - p*C + Pi*Delta },
        'Dh':{'func': lambda w,L,C,r,D,p,Pi,Delta:-r*D - w*L + p*C - Pi*Delta },
    },

    'statevar': {
        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) },
        'd'  :   {'func': lambda p,Y,D  : D  /(p*Y) },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) },
        'employment' :{'func': lambda L,N: L/N },
        'c' :{'func': lambda p,omega: p*omega},
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta },      
        
        'Y' :{'func': lambda K,nu: K/nu },
        'Pi':{'func': lambda p,Y,w,L,r,D: p*Y-w*L-r*D },
        'I' :{'func': lambda kappa,p,Y: kappa*p*Y },
        'C' :{'func': lambda Y,Ir: Y-Ir },
        'Ir':{'func': lambda p,I: I/p },
        'L' :{'func': lambda Y,a: Y/a },

        'GDP':{'func': lambda Y,p:Y*p},

        'inflation' :{'func': lambda c,p, eta,mu : eta*(mu*c/p -1) },
        
        # Divergent Phillips, exponential kappa
        'kappa'     :{'func': lambda pi, k0, k1,k2: k0 + k1 *np.exp(k2*pi)},
        'phillips'  :{'func': lambda employment, phi0,phi1: -phi0+phi1/(1-employment)**2,},

        # Affine for both
        #'kappa'     :{'func': lambda pi, k0, k1: k0 + k1 * pi},
        #'phillips'  :{'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},    
    },

    'parameter': {
        'Delta': {'value':0,
        'definition': 'shareholding coefficient'}
    },
    'size': {},
}

def ThreeDynamics(hub):
    """Draw three qualitatively different Dynamical phase-space associated with a Goodwin-Keen"""
    for preset in ['default','debtcrisis','debtstabilisation']:
        hub.set_preset(preset,verb=False)
        hub.run(verb=False)
        hub.plot_preset('debtstabilisation')

_SUPPLEMENTS = {'ThreeDynamics':ThreeDynamics}
_PRESETS = {
    'default': {
        'fields': {
            'alpha': 0.01019082,
            'n':  0.01568283,

            'k0' :      -0.0065   ,                  
            'k1' :       0.006737946999085467   ,    
            'k2' :       20              ,         
            'phinull' :  0.1   ,   

            'nu':      3.844391,
            'r':     0.02083975,
            'delta': 0.04054871,

            'eta':0.1,
            'dt': 0.01,

            'a': 1,
            'N': 1,
            'K': 3.607,
            'D': 0,
            'w': .7,

            'Tmax':50,
        },
        'com': 'Convergence to equilibrium',
        'plots': {'XY': [{'x': 'employment',
                        'y': 'omega',
                        'color': 'd',
                        'idx': 0,
                        'title': ''}],
                 'XYZ': [{'x': 'employment',
                        'y': 'omega',
                        'z': 'd',
                        'color': 'time',
                        'idx': 0,
                        'title': ''}],
                'byunits': [{'title':'plot by units'}],
                'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                                ['d'],['pi','kappa'],['inflation']
                                ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
                'Onevariable':[{'key':'employment', 
                            'mode':'cycles', 
                            'log':False,
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':''}]
        },
    },
    'debtcrisis':{'fields': {
            'alpha': 0.01019082,
            'n':  0.01568283,

            'k0' :      -0.0065   ,                  
            'k1' :       0.006737946999085467   ,    
            'k2' :       20              ,         
            'phinull' :  0.1   ,   

            'nu':      3.844391,
            'r':     0.02083975,
            'delta': 0.04054871,

            'eta':0.,
            'dt': 0.01,

            'a': 1,
            'N': 1,
            'K': 3.07,
            'D': 0,
            'w': .7,

            'Tmax':50,
        },
        'com': 'Path toward infinite relative debt',
        'plots': {
                 'XYZ': [{'x': 'employment',
                        'y': 'omega',
                        'z': 'd',
                        'color': 'time',
                        'idx': 0,
                        'title': ''}],
                'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                                ['d'],['pi','kappa'],['inflation']
                                ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
}
    },
    'debtstabilisation': {
        'fields': {
            'alpha': 0.01019082,
            'n':  0.01568283,

            'k0' :      -0.0065   ,                  
            'k1' :       0.003737946999085467   ,    
            'k2' :       20              ,         
            'phinull' :  0.1   ,   

            'nu':      3.844391,
            'r':     0.02083975,
            'delta': 0.04054871,

            'eta':0.01,
            'mu':1.5,
            'dt': 0.01,

            'a': 1,
            'N': 1,
            'K': 3.307,
            'D': 0,
            'w': .7,

            'dt':0.05,
            'Tmax':300,
        },
        'com': 'Stabilization through excess of debt',
        'plots': {'XYZ': [{'x': 'employment',
                        'y': 'omega',
                        'z': 'd',
                        'color': 'time',
                        'idx': 0,
                        'title': 'Goodwin-Keen phase-space dynamics'}],
        },
    },
}
