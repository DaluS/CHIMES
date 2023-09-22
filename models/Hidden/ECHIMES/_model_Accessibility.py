'''Adding accessibility into the system'''

_DESCRIPTION = ''' '''

from chimes._models import Funcs, importmodel,mergemodel
from chimes._models import Operators as O
import numpy as np


###########################################################################



_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'statevar': {
        ### ACCESSIBILITY
        'AcY': {
            'func': lambda V,Gamma,kY,softmin,K : np.maximum(0,O.ssum2((1-np.exp(-kY*O.transpose(V/K)/(Gamma+.00001)))**(-softmin))**(-1/softmin)),
            'com': 'Softmin with Gamma',
            'definition': 'Accessibility to intermediate production',
            'symbol': r'$\mathcal{A}^Y$',
            'size': ['Nprod']
        },
        'AcI': {
            'func': lambda V,Xi,kI,softmin,K :    np.maximum(0,O.ssum2((1-np.exp(-kI*O.transpose(V/K) / (Xi+.00001) ))**(-softmin))**(-1/softmin)),
            'com': 'Softmin with Xi',
            'definition': 'Accessibility to Investment',
            'symbol': r'$\mathcal{A}^I$',
            'size': ['Nprod']
        },
        'AcC': {
            'func': lambda V,kC,K :np.maximum(0,1-np.exp(-kC*V/K)),
            'com': 'Softmin',
            'definition': 'Accessibility to consumption',
            'symbol': r'$\mathcal{A}^C$',
            'size': ['Nprod']
        },
        ### USE AND ACCESSIBILITY
        'u': {'func': lambda u0,AcY,softmin : (u0**(-softmin)+AcY**(-softmin))**(-1/softmin),
              'com': 'both diminution and accessibility',
              'definition': 'Effective use of capital',
              'size': ['Nprod']
        },

        ### CONSUMPTION
        'C': {
            'func': lambda W, Cpond, p,AcC: AcC*Cpond * W / p,
            'com': 'Accessible consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },

        ### INVESTMENT
        'I': {
            'func': lambda Idelta, Ilever,AcI: AcI *  (Idelta + Ilever),
            'com': 'Accessible explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
    },
    'parameter':{
        #'Idelta': {'value':0},
        'Ilever': {'value':0},
        'kC': {'value':10,
               'definition': 'accessibility to consumption',
              'size':['Nprod']},
        'kI': {'value': 10,
               'definition': 'accessibility to consumption',
              'size':['Nprod']},
        'kY': {'value': 10,
               'definition': 'accessibility to consumption',
              'size':['Nprod']},
        'softmin': {'value':100.},
        #'Gamma': {'value':0.01,
        #          'size':['Nprod','Nprod']},
        'Xi': {'value':0.01,
                  'size':['Nprod','Nprod']},
        #'u0': {'value':1},
        #'V': {'value':10,
        #      'size':['Nprod']}
    },
}


_SUPPLEMENTS= {}

_PRESETS={
    '3sectors': {
        'fields': {'Nprod':['Y','I','C'],
                   'V':[.5,1,0.1],
                   'kC':1.,
                   'kY':[1,10.,1],
                   'kI':1.,
                   'Gamma':[[0.1,0,0],
                            [0.5,0,0],
                            [0.3,0,0]],
                   'Xi':[[0,1,0],
                         [0,1,0],
                         [0,1,0]]},
        'com': ('Check of the structure working as intended'),
        'plots': {},
    },}