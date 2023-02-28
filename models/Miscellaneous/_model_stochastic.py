"""Stochastic dynamics """

_DESCRIPTION ="""
solve $\dot{y} = y \sigma$, with sigma a guassian noise
"""

################# IMPORTS ##################################################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O

# ######################## LOGICS #######################################

_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'y': {
            'func' : lambda y,noisamp: y*noisamp,
            'com' : "noise on growth rate",
            'initial': 1,
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'noisamp' :{
            'func':  lambda nx,nr,noise : noise*np.random.normal(loc=0,size=(nx, nr, 1, 1)),
        },
    },
    'parameter': {
        'noise': {'value':0.5,
                  'definition': 'noise amplitude on growth rate'}

    },
    'size': {},
}
###################################
def plot(hub):
    import matplotlib.pyplot as plt 

    R=hub.dparam
    y= R['y']['value'][:,:,0,0,0]
    t= R['time']['value'][:,0,0,0,0]

    plt.figure()
    for j in range(np.shape(y)[1]):
        plt.plot(t,y[:,j])
    plt.show()

_SUPPLEMENTS = {
    'plot':plot
}



_PRESETS = {
    'Onevar': {
        'fields': {
            'y':1,
            'nx':1,
            'noise':1,
            },
        'com':'One variable',
        'plots': {'Var': [{'key':'y',
                           'mode':'sensitivity'}] },
    },
    '10': {
        'fields': {
            'y': 1,
            'nx': 10,
            'noise': 1,
            'dt':0.01,
        },
        'com': 'One hundred parrallel run',
        'plots': {'Var': [{'key': 'y',
                           'mode': 'sensitivity'}]}

        }
}
