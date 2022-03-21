# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:43:06 2022

@author: Paul Valcke

ALL THE BASIC FIELDS THAT ONE MIGHT NEED
"""

import numpy as np
import os


# WHERE TO LOOK AT IN YOUR MODEL
_FROM_USER = False

# ADDRESSES
_PATH_HERE = os.path.dirname(__file__)
_PATH_USER_HOME = os.path.expanduser('~')
_PATH_PRIVATE_MODELS = os.path.join(_PATH_USER_HOME, '.pygemmes', '_models')
_PATH_MODELS = os.path.join(_PATH_HERE, '_models')

_MODEL_NAME_CONVENTION = '_model_'

# FROM CHECKS
_LMODEL_ATTR = ['_LOGICS',
                'presets']
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

_LEQTYPES = ['ode',
             'pde',
             'statevar',
             'param',
             'undeclared']


_LEXTRAKEYS = [
    'func',
    'kargs',
    'args',
    'initial',
    'grid',
    'multi_ind',
    'source_kargs',
    'source_exp',
    'source_name',
    'isneeded',
    'cycles',
    'cycles_bykey'
]


# FROM _def_fields
__DOTHECHECK = True
__FILLDEFAULTVALUES = True
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
    'dimension': {
        'default': 'undefined',
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
    'type': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'intensive',
            'extensive',
            'dimensionless',
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
}
