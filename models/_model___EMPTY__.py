# -*- coding: utf-8 -*-
"""Template to write your model"""

_DESCRIPTION = """
Template to write your model 

* **Name :**
* **Article :** 
* **Author  :** 
* **Coder   :** 

* **Supplements description :** 

**TODO:**
* 
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

#_LOGICS_GOODWIN,_PRESETS0= importmodel('Goodwin')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_GOODWIN, verb=True) 

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


