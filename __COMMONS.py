# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:43:06 2022

@author: Paul Valcke

ALL THE BASIC FIELDS THAT ONE MIGHT N
"""

import numpy as np

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
