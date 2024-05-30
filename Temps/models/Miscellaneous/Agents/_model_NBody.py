"""Gravity attraction"""

_DESCRIPTION="""

* **Name :** Gravity trajectories
* **Article :** 
* **Author  :** 
* **Coder   :** Paul Valcke
* **Date    :** 2023/09/22

Exploration of the Three-Body problem and N-Body problem in general. Inspiration from https://en.wikipedia.org/wiki/Three-body_problem
"""

##########################################################################
from chimes._models import Funcs, importmodel,mergemodel,filldimensions#
from chimes._models import Operators as O                              #
import numpy as np                                                       #
##########################################################################


_LOGICS = {
    'size': {
        'Nbody': {
            'value':1,
        },
    },
    'differential': {
        'x': {'func'   : lambda vx: vx,
              'initial': 1,},
        'y': {'func'   : lambda vy: vy,
              'initial': 1,},
        'vx': {'func'   : lambda ax: ax,
               'initial': 0,},
        'vy': {'func'   : lambda ax: ax,
               'initial': 0,},
    },
    'statevar': {

        ### LOCAL CHARACTERISTICS ##########
        # Matrix of distance between particles
        'distances': {
            'func': lambda x, y: np.sqrt((x - O.transpose(x)) ** 2 + (y - O.transpose(y)) ** 2)+1000*np.eye(x),
            'com': 'vector norm',},
        'angle': { 
            'func': lambda x,y: np.atan2(y-O.transpose(y),x-O.transpose(x))
            },

       
         ### ACCELERATION VECTOR
        'ax': {'func': lambda distances,angle,mass: O.ssum2(distances**(-2),mass*O.transpose(mass)*np.cos(angle))},
        'ay': {'func': lambda distances,angle,mass: O.ssum2(distances**(-2),mass*O.transpose(mass)*np.sin(angle))},

    
        # Agregates on all agents
        'meanX': {
            'func': lambda x: O.ssum(x) / O.ssum(x * 0 + 1),
            'com': 'mean position',
        },
        'meanY': {
            'func': lambda y: O.ssum(y) / O.ssum(y * 0 + 1),
            'com': 'mean position',
        },
        # Characteristic on each agent
        'speed': {
            'func': lambda vx,vy : np.sqrt(vx**2+vy**2),
            'com': 'vector norm',
        },
    },
    'parameter': {
        ### SCALARS
        'mass'   :{'value': 1,},
        'Gravity':{'value': 1,},
    },
}

##########################################################################
Dimensions = { 
    'scalar': ['Gravity'],
    'matrix': ['distances'],
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)