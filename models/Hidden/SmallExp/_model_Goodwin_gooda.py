
'''Goodwin model with increasing profit rate '''

_DESCRIPTION = """
* **Article :** 
* **Author  :**
* **Coder   :** Paul Valcke

a = K/L, 
increasing return $\epsilon$
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from chimes._models import Funcs, importmodel,mergemodel

# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha ,
              'definition': 'machines per worker' ,
              'com': 'exogenous',
              'units': 'units.Humans^{-1}'},
        'N': {'func': lambda N,n        : N*n },
        'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
        #'nu':{'func': lambda nu, epsilon,g : -nu*(epsilon-1)*g},
    },

    # Intermediary relevant functions
    'statevar': {
        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) },
        'employment' :{'func': lambda L,N: L/N },
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta },      
        
        'Y' :{'func': lambda K,nu: K/nu },
        'Pi':{'func': lambda p,Y,w,L,delta,K: p*Y-w*L- p - p*delta*K},
        'C' :{'func': lambda Y,Ir: Y-Ir },
        'Ir':{'func': lambda Pi,delta,K,Delta: Pi*(1-Delta)+ delta*K },
        'L' :{'func': lambda K,a: K/a },
        'productivity' : {'func':       lambda Y,L: Y/L ,
                          'definition': 'productivity per worker',
                          'com':        'deduced from Y and L'},

        'phillips'  :{'func': lambda phi0,phi1, employment: -phi0 +  phi1 / (1 - employment)**2,},
        
        #'phillips'  :{'func': lambda zpi,pi, phi0,phi1, employment: -phi0 + (pi/0.15)**zpi  * phi1 / (1 - employment)**2,
        #              'com' : 'pi in diverging phillips'},

        #'alpha' : {'func': lambda time: 0.02*(1+time*0.01)}
        #'n' : {'func': lambda time: 0.025*(1+time*0.01)}
        #'delta' : {'func': lambda time: 0.005*(1+time*0.01)}
        'Gamma' : {'func': lambda time: 0.05+0*0.1*(1+time*0.01)}
        #'Delta' :  {'func': lambda time: 0.1*(1+time*0.01)}
        #'nu' : {'func': lambda time: 3*(1-time*0.01)}
        #'alpha' ,'n','delta' ,'phinull','Gamma','Delta','nu              
    },
    'parameter': {
        'p': {'value':1},
        'epsilon': {'value':1},
        'zpi': {'value':1}
    },
    'size': {},
}

_SUPPLEMENTS={}

# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2,
            'D': 0,
            'w': .6,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': '',
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'XY': [{'x': 'employment',
                            'y': 'omega',
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
            'nx':5,
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
            'timetrace': [{'keys': ['employment', 'omega']}],
            'nyaxis': [],
            'XY': [{'x': 'employment',
                           'y': 'omega',
                            'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}
