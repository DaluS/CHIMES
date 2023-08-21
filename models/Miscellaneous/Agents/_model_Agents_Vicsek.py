"""Movement synchronization"""

_DESCRIPTION="""

* **Name :** Vicsek Agent-Based dynamics
* **Article :** https://en.wikipedia.org/wiki/Vicsek_model
* **Author  :** 
* **Coder   :** Paul Valcke
"""

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Funcs
from pygemmes._models import Operators as O


###############################################################################
def lognorm(x,y,r0):
    return np.exp(- ((np.log(x)-r0)**2) /(2*y**2))/(2*x*y*np.sqrt(2*np.pi))

def localmeantheta(closeenough,anglediff):
    return np.sum(anglediff*closeenough,axis=-1)[...,np.newaxis]/np.sum(closeenough,axis=-1)[...,np.newaxis]

Nagents=50
x0 = np.random.normal(size=Nagents)
y0 = np.random.normal(size=Nagents)
z0 = np.random.normal(size=Nagents)
X= np.zeros((1,1,Nagents,1));X[0,0,:,0]=x0
Y= np.zeros((1,1,Nagents,1));Y[0,0,:,0]=y0
Z= np.zeros((1,1,Nagents,1));Z[0,0,:,0]=z0



_LOGICS = {
    'size': {
        'Nagents': {
            'value':Nagents,
        },
    },
    'differential': {
        'x': {'func': lambda vx: vx,
            'initial': X,
            'size': ['Nagents'],},
        'y': {'func': lambda vy: vy,
            'initial': Y,
            'size': ['Nagents'],},
        'theta': {'func': lambda weightmeangle,noise,nx,nr,Nagents: -weightmeangle+noise * np.random.normal(0,size=(nx, nr, Nagents, 1)),
            'initial': Z,
            'size': ['Nagents'],},
    },
    'statevar': {
        ### ACCELERATION VECTOR
        'vx': {'func': lambda v,theta: v*np.cos(theta),
               'size': ['Nagents'], },
        'vy': {'func': lambda v,theta: v*np.sin(theta),
               'size': ['Nagents'], },

        ### LOCAL CHARACTERISTICS ##########
        # Matrix of distance between particles
        'distances': {
            'func': lambda x, y: np.sqrt((x - O.transpose(x)) ** 2 + (y - O.transpose(y)) ** 2),
            'com': 'vector norm',
            'size': ['Nagents', 'Nagents'],
        },
        'anglediff': {
            'func': lambda theta : theta-O.transpose(theta),
            'size': ['Nagents', 'Nagents'],

        },
        'closeenough': {
            'func': lambda distances, distscreen : np.heaviside(distscreen-distances,0),
            'size': ['Nagents', 'Nagents'],
        },
        'weightmeangle': {
            'func': localmeantheta,
            'com': 'with an heaviside',
            'size': ['Nagents'],
        },
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
            'size': ['Nagents'],
        },
    },
    'parameter': {
        ### SCALARS
        'noise'   :{'value': 1, },
        'distscreen':{ 'value': 1,},
        'v': {'value': 0.1},
    },
}

####################################################
def plotTrajectories(hub):
    '''Plot of all trajectories'''
    import matplotlib.pyplot as plt
    R=hub.get_dparam()
    coord = { k : R[k]['value'][:,0,0,:,0] for k in ['x','y'] }

    for i in range(R['Nagents']['value']):
        plt.plot(coord['x'][:,i],coord['y'][:,i])

    plt.plot(coord['x'][0,:],coord['y'][0,:],'*',c='k')
    plt.axis('scaled')
    plt.show()
_SUPPLEMENTS={'PlotTrajectories':plotTrajectories}

####################################################
_PRESETS = {
    'synchronisation': {
        'fields': {
            'Nagents':Nagents,
            'x':  X,
            'y': Y,
            'noise':  1,
            'theta':  Z,
            'distscreen':  3,
            'v':  0.1,
        },
        'com': 'Agents are going to synchronize in one direction',
        'plots':{'XYZ':[{'x':'meanX',
                         'y':'meanY',
                         'z':'time'}]},
    },
    'TooNoisy': {
        'fields': {
            'Nagents':Nagents,
            'x':  X,
            'y': Y,
            'noise': 10,
            'theta':  Z,
            'distscreen':  3,
            'v':  0.1,
        },
        'com': 'Agents cannot synchronize',
        'plots': {'XYZ':[{'x':'meanX',
                         'y':'meanY',
                         'z':'time'}]},
    },
    'LowSync': {
        'fields': {
            'Nagents':Nagents,
            'x':  X,
            'y': Y,
            'noise': 6,
            'theta':  Z,
            'distscreen':  3,
            'v':  0.1,
            'Tmax':300
        },
        'com': 'Agents cannot synchronize',
        'plots': {'XYZ':[{'x':'meanX',
                         'y':'meanY',
                         'z':'time'}]},
    },
}

