"""Goodwin system with noise on technical progress"""

_DESCRIPTION ="""

There is a normal noise on the value of alpha. That's it!

* **Article :** 
* **Author  :** 
* **Coder   :** Paul Valcke
* **Date    :** 2023/08/18
"""


import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O

# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'employment': {
            'func' : lambda employment, newalpha,beta,delta,omega,nu: employment*( (1-omega)/nu - newalpha - beta - delta),
            'com' : "reduced 2-var system",
        },
        'omega': {
            'func' : lambda omega, phillips,newalpha: omega*(phillips-newalpha),
            'com' : 'reduced 2-var system',
        },
        'noisecumulate': {
            'func': lambda noise,nx,nr: noise*np.random.normal(size=(nx, nr, 1, 1)),
            'initial': 0,
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'phillips': Funcs.Phillips.div,
        'newalpha': {
            'func': lambda alpha, noise, nx, nr: alpha * (1 + noise*np.random.normal(size=(nx, nr, 1, 1))),

        'com': 'alpha coefficient with a percentage of noise',
        'definition': 'technical progress rate with noise',
        'units':'y^{-1}',
        'symbol': r'$\alpha_{\sigma}$'
        },
    },
    'parameter': {
        'noise': {'value':0.5,
                  'definition': 'noise amplitude on alpha'}
    },
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
