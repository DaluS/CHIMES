"""Only the Goodwin core"""

_DESCRIPTION = """

"""


import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O
######################################################################

_LOGICS= {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha ,
              'initial': 3},
        'N': {'func': lambda N,n        : N*n },
        'K': {'func': lambda K,I,delta : I-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
        #'employmenteff': {'func': lambda fl, employment,employmenteff: fl*(employment-employmenteff),
        #                  'initial':.9}
    },

    'statevar': {
        'employment' :{'func': lambda L,N: L/N },
        'Y' :{'func': lambda K,A: K*A },
        'I' :{'func': lambda Y,w,L: Y-w*L },
        'L' :{'func': lambda K,a: K/a },
        #'phillips'  :{'func': lambda employmenteff, philinConst, philinSlope: philinConst + philinSlope * employmenteff,},    
        'phillips'  :{'func': lambda employmenteff, philinConst, philinSlope: philinConst + philinSlope * employmenteff,},    
        'omega': {'func': lambda a,w: w/a},
        #'deltaemploy': {'func': lambda employment, employmenteff: employment-employmenteff,
        #                'symbol': '$\lambda-\lambda_{eff}$'},
    },

    'parameter': {
    #    'fl':{'value':10},
    },
    'size': {},
}


_SUPPLEMENTS = {}
_PRESETS = {
    'default2': {
        'fields': {},
        'com': 'Basic',
        'plots': {'XY': [],
                'plotbyunits': [],
                'plotnyaxis': [],
        },
    },
}