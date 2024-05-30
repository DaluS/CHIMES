"""CHIMES Consumption module: Utility on possessions"""

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O
_DESCRIPTION = """
"Household possession to maximize utilities"

* **Name :** CHIMES consumption module
* **Article :** E-CHIMES
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

* **Supplements description :**


"""


def utility(H0, U0, H):
    return U0 * (1 - np.exp(-(H / H0)))
# utility = lambda beta,U,H:U*np.log(1+beta*H)


def Consfunc(C, H, delta, rho):
    return


_LOGICS = {
    'size': {'Nprod': {'list': ['']}},
    'differential': {
        'H': {'func': lambda C, H, delta, rho: C - delta * H - O.matmul(rho, H), },
        'Dh': {'func': lambda W, p, C: W - O.ssum(p * C),
               'initial': 0},
    },
    'statevar': {
        'utility': {
            'func': lambda H0, U0, H: U0 * (1 - np.exp(-H / H0)),
            'com': 'exponential dampening',
        },
        'relutility': {
            'func': lambda H, U0, p, H0: (utility(H0, U0, H + 0.01) - utility(H0, U0, H)) / (0.01 * p),
        },
        'Cweight': {
            'func': lambda relutility, Z: np.exp(Z * relutility) / O.ssum(np.exp(Z * relutility)),
        },
        'Upkeep': {
            'func': lambda delta, rho, p, H: O.ssum(p * (delta * H + O.matmul(rho, H))),
            'units': "$.y^{-1}"
        },
        'Cupkeep': {
            'func': lambda rho, delta, H: O.matmul(rho, H) + delta * H,
            'units': "Units.y^{-1}",
        },
        'Cinvest': {
            'func': lambda Cweight, W, Upkeep, p: Cweight * (W - Upkeep) / p,
            'units': "Units.y^{-1}",
        },
        'Winvest': {
            'func': lambda Cweight, W, Upkeep, p: Cweight * (W - Upkeep) / p,
            'units': "$.y^{-1}",
            'symbol': r'$\mathcal{W}^{invest}$'
        },
        'C': {
            'func': lambda Cupkeep, Cinvest: Cupkeep + Cinvest,
        },
        #    'W': {
        #        'func': lambda time,g: np.exp(g*time),
        # },
    },

    'parameter': {
        'Z': {'value': 10000},
        'H0': {'value': 100},
        'U0': {'value': 1},
        'rho': {'value': 0},
        'p': {'value': 1},
        'g': {'value': 0}
    },
}

#########################################################
Dimensions = {
    'scalar': ['Z', 'W', 'Nprod', 'g', 'Dh'],
    'matrix': ['rho']
    # 'vector': will be deduced by fill_dimensions
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nprod'],
       'matrix': ['Nprod', 'Nprod']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)
#########################################################
_SUPPLEMENTS = {}
#########################################################
preset2goods = {
    'Nprod': ['Goods', 'Fuel'],
    'Dh': 0,
    'g': 0.02,
    'rho': [[0, 0],
            [1, 0]],
    'U0': [1, 0],
    'H0': [100, 1],
    'H': [0, 0],
    'p': [1, 0.1],
    'delta': [0.01, 0],
}

preset3goods = {
    'Nprod': ['Infra', 'Upkeep', 'Service'],
    'rho': [[0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]],
    'U0': [1, 0, 5],
    'H0': [1, 1, 100],
    'H': [0, 0, 0],
    'p': [10, 1, 1],
    'delta': [0.01, 0, 0],
}

presetN_log = {
    'Nprod': ['one', 'two', 'three', 'last'],
    'rho': 0,
    'U0': [1, 1, 1, 5],
    'Z': 2000,
    'H0': [5, 5, 5, 100],
    'H': 0,
    'p': [1, 2, 5, 1],
    'delta': [0.05, 0.05, 0.05, 1]
}


_PRESETS = {
    'preset2goods': {
        'fields': preset2goods,
        'com': 'two types of goods : infra and upkeep',
        'plots': {'byunits': [{'filters_key': ('Cupkeep', 'Cinvest'),
                               'separate_variables': {'undefined': ['relutility']}}]
                  }
    },
    'preset3goods': {
        'fields': preset3goods,
        'com': '3 types of goods : Infra (Think house,cars), Upkeep good (energy to activate infras), Services',
        'plots': {'byunits': [{'filters_key': ('Cupkeep', 'Cinvest'),
                               'separate_variables': {'undefined': ['relutility']}}]
                  }
    },
    'presetN': {
        'fields': presetN_log,
        'com': 'Goal logistics',
        'plots': {'byunits': [{'filters_key': ('Cupkeep', 'Cinvest'),
                               'separate_variables': {'undefined': ['relutility']}}]
                  }
    }

}
'''
        'Var': [{'key':'',
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
                  'byunits': [{'filters_key':(),
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
                  'nyaxis' : [{'y':[[],[]],
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
'''
