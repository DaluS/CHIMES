"""TEST USED IN PYTEST"""

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O
_DESCRIPTION = """

TEST OF:
Importmodel
Mergemodel


"""
# ################ IMPORTS ##################################################

# ################# ALL THE NEW FIELDS LOGICS ###############################
_LOGICS = {'size': {},
           'differential': {},
           'statevar': {},
           'parameter': {}, }
'''
'p': {  'func': lambda p,inflation : p*inflation,
        'initial':1,
        'units': '$.Units^{-1}',
        'definition' : 'nominal value per physical unit produced',
        'com': 'inflation driven',
        'symbol': r'$\mathcal{P}$',
        'size' : ['__ONE__','__ONE__']},
'p': { 'func' lambda p,inflation : p*inflation}, # for short
'''

# ################# MODELS YOU WANT TO MERGE THE NEW LOGICS INTO ############

# _LOGICS_GOODWIN,_PRESETS0= importmodel('Goodwin')
# _LOGICS = merge_model(_LOGICS, _LOGICS_GOODWIN, verb=False)

# ################# ADDING DIMENSIONS TO VARIABLES IF NOT DONE BEFORE #######
'''
Comment the line in 'Dimensions' you want to be filled by default.
The system does not handle automatically multiple types of matrix/vector dimensions. do it manually
Modify DIM
'''
Dimensions = {
    # 'scalar': [],
    'matrix': [],
    'vector': [],       #
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nprod'],
       'matrix': ['Nprod', 'Nprod']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)

# ################## SUPPLEMENTS IF NEEDED ###################################
_SUPPLEMENTS = {}

# ################## DEFIMING PRESETS WITH THEIR SUPPLEMENTS #################
_PRESETS = {
    'preset0': {
        'fields': {
            'fields1': 0,
            'fields2': 0,
        },
        'com': 'This is doing something ',
        'plots': {'Var': [{'key': '',
                           'mode': False,  # sensitivity, cycles
                           'log': False,
                           'idx': 0,
                           'Region': 0,
                           'tini': False,
                           'tend': False,
                           'title': ''},
                          ],
                  'XY': [{'x': '',
                          'y': '',
                          'color': '',
                          'scaled': False,
                          'idx': 0,
                          'Region': 0,
                          'tini': False,
                          'tend': False,
                          'title': '',
                          },
                         ],
                  'XYZ': [{'x': '',
                           'y': '',
                           'z': '',
                           'color': 'time',
                           'idx': 0,
                           'Region': 0,
                           'tini': False,
                           'tend': False,
                           'title': ''},
                          ],
                  'cycles_characteristics': [{'xaxis': 'omega',
                                              'yaxis': 'employment',
                                              'ref': 'employment',
                                              'type1': 'frequency',
                                              'normalize': False,
                                              'Region': 0,
                                              'title': ''},
                                             ],
                  'byunits': [{'filters_key': (),
                               'filters_units': (),
                               'filters_sector': (),
                               'separate_variables': {},
                               'lw': 1,
                               'idx': 0,
                               'Region': 0,
                               'tini': False,
                               'tend': False,
                               'title': ''}
                              ],
                  'nyaxis': [{'y': [[], []],
                              'x': 'time',
                              'idx': 0,
                              'Region': 0,
                              'log': False,  # []
                              'title': '',
                              }
                             ],
                  },
    },
}
