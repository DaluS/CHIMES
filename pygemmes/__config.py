# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:43:06 2022

@author: Paul Valcke

ALL THE BASIC FIELDS THAT ONE MIGHT NEED
"""

import numpy as np
import os

# ################## MODELS FILES LOCATION AND NAME ###########################
# FLAG FOR MODEL LOCATION : False if in the library, true in documents
_FROM_USER = False

# NAME OF MODEL FILES
_MODEL_NAME_CONVENTION = '_model_'

# ADDRESSES
_PATH_HERE = os.path.dirname(__file__)
_PATH_USER_HOME = os.path.expanduser('~')
_PATH_PRIVATE_MODELS = os.path.join(
    _PATH_USER_HOME, '.pygemmes', '_models')
_PATH_MODELS = os.path.join(_PATH_HERE, '_models')


# ####################### SOLVER BY DEFAULT ###################################
_SOLVER = 'eRK4-homemade'


# ################# MODELS FILE CONTENT #######################################

# ELEMENTS IN A MODEL
_LMODEL_ATTR = ['_LOGICS',
                'presets']

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

_LEQTYPES = ['differential',  # all differentials
             'statevar',
             'parameter',
             'size'
             ]

_MULTISECT_DEFAULT = '__one'

# ######################### DPARAM CONTENT ####################################
# POSSIBLE KEYS IN DPARAM
_LEXTRAKEYS = [
    'func',     # The function animating it
    'kargs',    # List of all the dependencies
    'args',     # dictionnary of all dependencies
    'initial',  # initial value if differential
    'source_exp',  # Explaining the expression
    'isneeded',  # Auxilliary or not
    'analysis',  # Contains all analysys (time derivative, cycles...)
    'size',  # Name of the dimension in the multisectoriality
    'list',  # labels of sectors
    'dict',  # relation label - index
]

# ############################ DEF_FIELDS #####################################
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
        'default': 'No comment',
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
    'size': {
        'default': 1,
        'type': int,
        'allowed': None,
    }
}
