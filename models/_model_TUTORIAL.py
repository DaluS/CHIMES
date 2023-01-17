
'''Tutorial on how to write a model. Read the file !'''


_DESCRIPTION ="""
The first line is the short description of the model 

THIS DOCSTRING IS THE LONG DESCRIPTION OF THE MODEL.
PUT EVERYTHING YOU WANT THE USER TO KNOW BEFORE HE LOADS THE MODEL.

* **Name :**
* **Article :** 
* **Author  :** 
* **Coder   :** 

* **Supplements description :** 

TODO:
* EVERYTHING you want to change
* ...
"""

# ######################## PRELIMINARY ELEMENTS #########################
'''pygemmes model are python files. you can do operations with them an within them.
If you need other libraries of functions from python, you can get them here'''
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O

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
'p': {  'func': lambda p,inflation : p*inflation,
        'initial':1,
        'units': '$.Units^{-1}',
        'definition' : 'nominal value per physical unit produced',
        'com': 'inflation driven',
        'symbol': '$\mathcal{P}$',
        'size' : ['__ONE__','__ONE__']},
but 'p': {'func': lambda p,inflation : p*inflation,} works too !       
'''

_LOGICS = { 'size'        : {},
            'differential': {
            'p': {  'func': lambda p,inflation : p*inflation,
                    'initial':10,
                    'units': '$.Units^{-1}',
                    'definition' : 'nominal value per physical unit produced',
                    'com': 'inflation driven',
                    'symbol': '$\mathcal{P}$',
                    'size' : ['__ONE__','__ONE__']},
            },
            'statevar'    : {},
            'parameter'   : {},}

# Advanced possibilites : You can import other model files and merge them
#_LOGICS_GOODWIN,_PRESETS0= importmodel('Goodwin')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_GOODWIN, verb=True) 

_SUPPLEMENTS={}
_PRESETS = {
    'presetname1': {           # Name of the preset
        'fields': {'Tmax':50,  # Dictionnary of all changed values
                   'dt':0.1},  
        'com': 'description of the preset',
        'plots': {},           # All the plots you want to print  
    },
}