# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin. Assume that labour productivity (parameter a in our basic model) is not exogenous 
    but depends upon the growth rate of investment (in R & D). This leads to adding the following equation:
    dot(a) / a = alpha + beta * g



TYPICAL BEHAVIOR: Locally Unstable, the good equilibrium is an unstable focuse


@author: Weiye Zhu
"""


# ######################## PRELIMINARY ELEMENTS #########################
from IPython.display import display, HTML

display(HTML(data="""
<style>
    div#notebook-container    { width: 99%; }
    div#menubar-container     { width: 65%; }
    div#maintoolbar-container { width: 99%; }
</style>
"""))

import sys 

path = "/Users/zhu/Desktop/GEJP/GEMMES" 
sys.path.insert(0, path)
import pygemmes as pgm

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel






# ######################## LOGICS #######################################
_LOGICS,_PRESETS0= importmodel('Goodwin')

_GE_LOGICS = {
    'differential': {
        # Endogenous Labor Productivity
        'a': {
            'func': lambda a, alpha, beta, g: a*(alpha + beta * g),
            'com': 'Labor Productivity depends on investment', },

    }
}

_LOGICS = mergemodel(_LOGICS, _GE_LOGICS, verb=True) 




# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .5*1.19,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 3,
            'delta': .0051,
            'phinull': 0.11,
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
                    'color': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'nx':5,
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
        'plots': {
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