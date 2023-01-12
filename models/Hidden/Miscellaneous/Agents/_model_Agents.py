
"""
DESCRIPTION : This is a model of "agents" to show how we can incorporte it into pygemmes

Those agents are very simple (not economic) :
    * they have a position (x,y), a speed (vx,vy)
    * they are attracted by a point (x0,y0) through a spring mechanism
    * there is noise on their acceleration

We also show how we can calculate agregated properties, and inter-agent properties

"""

import numpy as np
from pygemmes._models import Funcs


# ######################## OPERATORS ####################################
def sprod(X,Y):
    return np.matmul(np.moveaxis(X,-1,-2),Y)
def ssum(X):
    return np.matmul(np.moveaxis(X,-1,-2),X*0+1)
def transpose(X):
    return np.moveaxis(X, -1, -2)
def matmul(M,V):
    return np.matmul(M,V)
# #######################################################################




_LOGICS = {
    'size': {
        'Nagents': {
            'value':10,
        },
    },
    'differential': {
        'x': {'func': lambda vx: vx,
            'initial': 0,
            'size': ['Nagents'],},
        'y': {'func': lambda vy: vy,
            'initial': 0,
            'size': ['Nagents'],},
        'vx': {'func': lambda ax: ax,
            'initial': 0,
            'size': ['Nagents'],},
        'vy': {'func': lambda ay: ay,
            'initial': 0,
            'size': ['Nagents'],},

    },
    'statevar': {
        ### ACCELERATION VECTOR
        'ax': {'func': lambda x, x0, Nagents, nx, nr, k, noise: k * (x0 - x) + noise * np.random.normal(
            size=(nx, nr, Nagents, 1)),
               'size': ['Nagents'], },
        'ay': {'func': lambda y, y0, Nagents, nx, nr, k, noise: k * (y0 - y) + noise * np.random.normal(
            size=(nx, nr, Nagents, 1)),
               'size': ['Nagents'], },

        ### LOCAL CHARACTERISTICS ##########
        # Matrix of distance between particles
        'distances': {
            'func': lambda x, y: np.sqrt((x - transpose(x)) ** 2 + (y - transpose(y)) ** 2),
            'com': 'vector norm',
            'size': ['Nagents', 'Nagents'],
        },
        # Agregates on all agents
        'meanX': {
            'func': lambda x: ssum(x) / ssum(x * 0 + 1),
            'com': 'mean position',
        },
        'meanY': {
            'func': lambda y: ssum(y) / ssum(y * 0 + 1),
            'com': 'mean position',

        # Characteristic on each agent
        'speed': {
            'func': lambda vx,vy : np.sqrt(vx**2+vy**2),
            'com': 'vector norm',
            'size': ['Nagents'],
        },
        'angle': {
            'func': lambda vx, vy: np.atan2(vy,vx),
            'com': 'vector angle',
            'size': ['Nagents'],
        },

    },
},


    'parameter': {
        ### SCALARS
        'k'  :{'value':1,
               'definition':'attraction constant',
               'size': ['Nagents'],},
        'x0'      :{'value': 0,},
        'y0'      :{'value': 0,},
        'noise'   :{'value': 1, },
    },
}


_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
