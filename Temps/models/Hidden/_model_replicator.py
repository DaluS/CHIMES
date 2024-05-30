"""Social dynamics"""

_DESCRIPTION ="""
https://en.wikipedia.org/wiki/Replicator_equation

deterministic monotone non-linear and non-innovative game dynamic used in evolutionary game theory
it allows the fitness function to incorporate the distribution of the population types rather than setting the fitness of a particular type constant. 
This important property allows the replicator equation to capture the essence of selection
"""

################# IMPORTS ##################################################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from chimes._models import Funcs, importmodel,mergemodel,filldimensions
from chimes._models import Operators as O

# ######################## LOGICS #######################################

_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'x': {
            'func' : lambda x,fit: x*(fit-O.ssum(x*fit)),
            'definition': " proportion of type in the population",
            'com' : "",
            'initial': 1,
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'fit' :{
            'func':  lambda nx,nr,noise : noise*np.random.normal(loc=0,size=(nx, nr, 1, 1)),
        },
    },
    'parameter': {
        'noise':{'value':1},
    },
    'size': {'Nprod': {'value': 10}},
}