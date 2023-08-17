"""
Created on Mon Mar 21 13:43:06 2022
@author: Paul Valcke
ALL THE BASIC FIELDS THAT ONE MIGHT NEED
"""

import numpy as np
import os

# ################# LOGS AND PRINTS IN THE SYSTEM #############################
_VERB = True        #! Print by default when actions are done
__PRINTLOGO = False #! Print the logo
__PRINTINTRO = False#! Print tutorial text

# pgm.get_...
_FIELDS_EXPLOREMODEL =False #! get_available_fields will check existing models
_MODELS_SHOWDETAILS = True  #! Show docstring of each model 

# ################# TYPES OF PRINT 
_MARKDOWN = True # Outputs are all Markdown


# ################## MODELS FILES LOCATION AND NAME ###########################
# FLAG FOR MODEL LOCATION : False if in the library, true in documents

_FROM_USER = False                 # Location of nodel files (NOT CHECKED)
_MODEL_NAME_CONVENTION = '_model_' # The convention for pygemmes to know where models are
_MODEL_FOLDER = 'models'           # Files in the local library
_MODEL_FOLDER_HIDDEN = 'Hidden'


# ################# MODELS FILE CONTENT #######################################
# ELEMENTS IN A MODEL
_LMODEL_ATTR = ['_LOGICS', # Contains all the fields
                'presets'] # Contains specific values and plot to try


# FIELDS THAT MUST BE OBTAINED WHEM LOADING A MODEL
_DMODEL_KEYS = {
    'logics': dict,
    'presets': dict,
    'file': str,
    'description': str,
    'name': str,
}

_LTYPES = [int,
           float,
           np.int_,
           np.float_]

_LTYPES_ARRAY = [list,
                 tuple,
                 np.ndarray]

_LEQTYPES = ['differential',  # Every differentially defined variables (PDE, ODE...)
             'statevar',      # State variables (deduced from everything else)
             'parameter',     # Fixed-value
             'size'           # Size of tensors, special type parrameter
             ]

# ######################### DPARAM CONTENT ####################################
# POSSIBLE KEYS IN DPARAM
_LEXTRAKEYS = [
    'func',      # The function animating it
    'kargs',     # List of all the dependencies
    'args',      # dictionnary of all dependencies
    'initial',   # initial value if differential
    'source_exp',# Explaining the expression
    'isneeded',  # Auxilliary or not
    'analysis',  # Contains all analysys (time derivative, cycles...)
    'size'       # Name of the dimension in the multisectoriality
]


# ############################ DEF_FIELDS #####################################
_DEFAULTSIZE = '__ONE__'
__DEFAULTFIELDS = {
    'value': {
        'default': None,
        'type': (int, float, np.int_, np.float_, np.ndarray, list),
        'allowed': None,
    },
    'definition': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'com': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'units': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            # Any physical quantity of something (capital, ressources...)
            'Units',
            'y',       # Time
            '$',       # Money
            'C',       # Carbon Concentration
            'Tc',      # Temperature (Celsius)
            'Humans',  # Population
            'W',       # Energy
            'L',       # Length
            '',        # Dimensionless
        ],
    },
    'symbol': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'group': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'multisect': {
        'default': '',
        'type': str,
        'allowed': None,
    }  ,
    'size':{
        'default': [_DEFAULTSIZE,_DEFAULTSIZE] ,
        'type': list,
        'allowed': None
    }
}

################################## LOCAL CHANGES #####################
# ADDRESSES
_PATH_HERE = os.path.dirname(__file__)
_PATH_USER_HOME = os.path.expanduser('~')
_PATH_PRIVATE_MODELS = os.path.join(
    _PATH_USER_HOME, '.pygemmes', _MODEL_FOLDER)
_PATH_MODELS = os.path.join(os.path.dirname(_PATH_HERE), _MODEL_FOLDER)
