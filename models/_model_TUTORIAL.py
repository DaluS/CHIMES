# -*- coding: utf-8 -*-
"""
THIS DOCSTRING IS THE DESCRIPTION OF THE MODEL.
PUT EVERYTHING YOU WANT THE USER TO KNOW BEFORE HE LOADS THE MODEL.
Typically :
* Model name
* what is does
* What are the hypotheses
* Main properties
* Link to the article
* Who coded it
* What needs to be done in the file
"""

# ######################## PRELIMINARY ELEMENTS #########################
'''pygemmes model are python files. you can do operations with them an within them.
If you need other libraries of functions from python, you can get them here'''
# import numpy as np (if you need exponential, pi, log, of matrix products...)
# from pygemmes._models import Funcs (if you need already coded functions

# ######################## LOGICS #######################################
'''
_LOGICS is a dict with the possible keys : 
    'size' (for multisectoral purposes)
    'differential' (for variable defined by a differential expression)
    'statevar' (for variables defined by an equation)
    'parameter' (for constants)
    
    if you do not have one of those, the system will assume it is empty
    
_LOGICS = { 'size'        : {},
            'differential': {},
            'statevar'    : {},
            'parameter'   : {},}
            
            
An example of field to put in 'differential' :            
'p': {
    'func': lambda p,inflation : p*inflation,
    'initial':1,
    'units': '$.Units^{-1}',
    'definition' : 'nominal value per physical unit produced',
    'com': 'inflation driven',
    'symbol': '$\mathcal{P}$',
    'size' : ['__ONE__','__ONE__']
},
but 'p': {'func': lambda p,inflation : p*inflation,} works too !
            
'''

_LOGICS = { 'size'        : {},
            'differential': {},
            'statevar'    : {},
            'parameter'   : {},}

# ####################### PRESETS #######################################
'''
_PRESETS Must be a dict 
_PRESETS = {
    'presetname1': {
        'fields': {},
        'com': '',
        'plots': {},
    },
}
    [...]
'''

_PRESETS = {
    'presetname1': {
        'fields': {},
        'com': '',
        'plots': {},
    },
}