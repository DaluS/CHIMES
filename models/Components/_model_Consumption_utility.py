"""CHIMES Consumption module: Utility on possessions"""

_DESCRIPTION = """
"Household possession to maximize utilities" 
 
* **Name :** CHIMES consumption module 
* **Article :** E-CHIMES
* **Author  :** Paul Valcke 
* **Coder   :** Paul Valcke

* **Supplements description :** 


"""
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O

utility = lambda H0,U,H:U*(1- np.exp(-H/H0))  
#utility = lambda beta,U,H:U*np.log(1+beta*H)

def Consfunc(C,H,delta,rho):
    return C-delta*H-O.matmul(rho,H)

_LOGICS = { 
    'size'        : {'Nprod': {'list': ['']}},
    'differential': {
        'H': {'func': Consfunc,},
    },
    'statevar'    : {
        'utility': {
            'func': utility,
            'com': 'exponential dampening',
    },
        'relutility': {
            'func' : lambda H,U,p,H0 : (utility(H0,U,H+0.01)-utility(H0,U,H))/(0.01*p),
    },
        'Cweight': {
            'func': lambda relutility,Z : np.exp(Z*relutility)/O.ssum(np.exp(Z*relutility)),
    },
        'Upkeep': {
            'func' : lambda delta, rho, p,H : p*delta*H+p*O.matmul(rho,H),
            'units': "$.y^{-1}"
    },
        'Cupkeep': { 
            'func': lambda rho,delta, H: O.matmul(rho,H)+delta*H,
            'units': "Units.y^{-1}",
    },
        'Cinvest': { 
            'func': lambda Cweight,W,Upkeep,p: Cweight*(W-Upkeep)/p,
            'units': "Units.y^{-1}",
    },
        'C': {
            'func' : lambda Cupkeep,Cinvest: Cupkeep+Cinvest ,
    },
        'W': {
            'func': lambda time,g: np.exp(g*time),
    },
    },

    'parameter'   : {
        'Z': {'value':1},
        'H0': {'value':1},
        'U': {'value':1},
        'rho': {'value':0},
        'p': {'value':1},
        'g': {'value':0}
    },
}

Dimensions = { 
    'scalar': ['Z','W'],
    'matrix': [ 'rho']
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)

#_LOGICS_GOODWIN,_PRESETS0= importmodel('Goodwin')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_GOODWIN, verb=False) 

_SUPPLEMENTS={}
_PRESETS = {
    'preset0': {
        'fields': {},
        'com': '',
        'plots': {'Var': [{'key':'',
                           'mode':False, #sensitivity, cycles
                           'log':False,
                           'idx':0, 
                           'Region':0, 
                           'tini':False, 
                           'tend':False, 
                           'title':''},
                  ],
                  'XY': [{  'x':'',
                            'y':'',
                            'color':'', 
                            'scaled':False,
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':'', 
                            },
                  ],
                  'XYZ': [{ 'x':'',
                            'y':'',
                            'z':'', 
                            'color':'time', 
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':''},
                  ],
                  'cycles_characteristics': [{'xaxis':'omega', 
                                              'yaxis':'employment', 
                                              'ref':'employment', 
                                              'type1':'frequency', 
                                              'normalize':False, 
                                              'Region':0, 
                                              'title':''},
                  ],
                  'plotbyunits': [{'filters_key':(),
                                   'filters_units':(),
                                   'filters_sector':(),
                                   'separate_variables':{}, 
                                   'lw':1, 
                                   'idx':0, 
                                   'Region':0, 
                                   'tini':False, 
                                   'tend':False, 
                                   'title':''}
                  ],
                  'plotnyaxis' : [{'y':[[],[]],
                                   'x':'time', 
                                   'idx':0,
                                   'Region':0,
                                   'log':False,# []
                                   'title':'', 
                                   }
                  ],    
        },
    },
}

