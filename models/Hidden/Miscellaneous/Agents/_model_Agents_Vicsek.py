
"""
This is a collective movement agent-based model : https://en.wikipedia.org/wiki/Vicsek_model

Try :
```
hub=pgm.Hub('Agents_Vicsek','default')
hub.run()
R=hub.get_dparam()
coord = { k : R[k]['value'][:,0,0,:,0] for k in ['x','y'] }
for i in range(100):
    plt.plot(coord['x'][:,i],coord['y'][:,i])
plt.axis('scaled')
plt.show()
```
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
            'func': lambda x, y: np.sqrt((x - transpose(x)) ** 2 + (y - transpose(y)) ** 2),
            'com': 'vector norm',
            'size': ['Nagents', 'Nagents'],
        },
        'anglediff': {
            'func': lambda theta : theta-transpose(theta),
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
            'func': lambda x: ssum(x) / ssum(x * 0 + 1),
            'com': 'mean position',
        },
        'meanY': {
            'func': lambda y: ssum(y) / ssum(y * 0 + 1),
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


_PRESETS = {
    'default': {
        'fields': {
            'Nagents':Nagents,
            'x':  X,
            'y': Y,
            'noise':  10,
            'theta':  Z,
            'distscreen':  3,
            'v':  0.1,
        },
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
