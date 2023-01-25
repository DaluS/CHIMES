"""Extension to CHIMES: the core with alternative processes"""

_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY
* **Article :** https://www.overleaf.com/project/62fbdce83176c9784e52236c    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

**Changes compared to CHIMES0 :**
* Changing the dynamics on u,i,accessibility  
"""

import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O


_LOGICS = { 'size'        : {},
            'differential': {},
            'statevar'    : {},
            'parameter'   : {},}
'''
'p': {  'func': lambda p,inflation : p*inflation,
        'initial':1,
        'units': '$.Units^{-1}',
        'definition' : 'nominal value per physical unit produced',
        'com': 'inflation driven',
        'symbol': '$\mathcal{P}$',
        'size' : ['__ONE__','__ONE__']},
'p': { 'func' lambda p,inflation : p*inflation}, # for short
'''

_LOGICS_CHIMES0,_PRESETS= importmodel('CHIMES0')
_LOGICS = mergemodel(_LOGICS, _LOGICS_CHIMES0, verb=False) 

_SUPPLEMENTS={}
'''
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
'''

