"""CHIMES Consumption module: Utility on possessions"""

_DESCRIPTION = """
"Household possession to maximize utilities" 
 
* **Name :** CHIMES consumption module 
* **Article :** E-CHIMES
* **Author  :** Paul Valcke 
* **Coder   :** Paul Valcke

* **Supplements description :** 


"""
#########################################################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O

#########################################################

#########################################################
_LOGICS = { 
    'size': {'Nprod': {'list': ['']}},
    'differential': {
        'u0': {'func': lambda u0,zu,V,V0,sigma : (sigma*(V0/V-1)*(1-u0)**zu),
               'com': 'Dynamics on V0/V' }, 
    },
    'statevar'    : {
        'V0': {
            'func': lambda epsilonV,K,A,b,CESexp:1,# epsilonV*A*K*b**(-1/CESexp),
            'com': 'characteristic inventory on production',
    },
        'v': {
            'func': lambda V,V0: V/V0,
            'com': 'relative inventory'
        },
        'inflationdotV' :{'func': lambda chi,V0,V: chi *(V0/V-1),
                    'com': 'V0/V'},
    },
    
    'parameter'   : {
        'epsilonV': {'value':0.1},
        'zu'      : {'value':1  },
        'chi'     : {'value':1  }  

    },
}

#########################################################
Dimensions = { 
    'scalar': [],
    'matrix': []
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)

#########################################################
_SUPPLEMENTS={}

#########################################################
_PRESETS = {}