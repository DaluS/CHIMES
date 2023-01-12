# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a Goodwin model written with `Functions` library.
    It is a two-sector model ( Household and Firm ), with salary negociation.
    There is no "money" explicitely (money and real units are equivalent), and there is no debt mechanism possible.
    There is no consumption behavior : it is a Say's law behind

    The interesting things :
        * growth is an emergent propertie
        * Economic cycles (on employement and wage share) are an emergent propertie
        * The cycles are metastable : trajectories are closed

    It is the basis of many different models !


LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,
        # Stock-flow consistency
        #'K': Funcs.Kappa.kfromIr,

    },

    # Intermediary relevant functions
    'statevar': {
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': .5*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'time',
                    'cinf': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': [.5, .5*1.2, .5*1.3, .5*1.5, .5*1.7],
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        's': {
            'timetrace': [{'keys': ['employment', 'omega']}],
            'nyaxis': [],
            'phasespace': [{'x': 'employment',
                           'y': 'omega',
                            'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}
