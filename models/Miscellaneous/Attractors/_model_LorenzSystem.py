'''Lorenz Chaotic Attractor: Butterfly effect!'''


_DESCRIPTION = """
* **Date    :** 2023/08/21
* **Article :** https://en.wikipedia.org/wiki/Lorenz_system
* **Author  :** Edward Lorenz
* **Coder   :** Paul Valcke

Solving the famous 3-coupled ordinary differential system. Canonical case has the two equilibrium with the strange attraction

"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from chimes._models import Funcs, importmodel,mergemodel

_LOGICS = {
    'differential': {
        'x': {
            'func': lambda lor_sigma, y, x: lor_sigma*(y-x),
            'com': 'X',
            'definition':'One of the dimension',
            'symbol':r'$\mathcal{r}$',
            'initial': 0.2,
        },
        'y': {
            'func': lambda lor_rho, x, z, y: x*(lor_rho-z)-y,
            'com': 'Y',
            'initial': .13,
        },
        'z': {
            'func': lambda lor_beta, x, y, z: x*y-lor_beta*z,
            'com': 'Z',
            'initial': .21,
        },
    },
    'statevar': {
    },
    'parameter': {
        'lor_sigma':{
            'value':10,
        },
        'lor_rho': {
            'value': 28,
        },
        'lor_beta': {
            'value': 8/3,
        },
    },
    'size': {},
}

_SUPPLEMENTS={}

# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'Canonical example': {
        'fields': {
            'dt':0.01,
            'lor_sigma':10,
            'lor_rho': 28,
            'lor_beta':  8/3,
        },
        'com': 'Chaotic attractor around two equilibrium, for those parameter values',
        'plots': {
                'XYZ': [{'x': 'x',
                    'y': 'y',
                    'z': 'z',
                    'color': 'time',
                    #'cmap': 'jet',
                    'idx': 0,
                    'title': 'Lorenz 3-dimension strange attractor'}],
                'nyaxis': [{
                    'x':'time',
                    'y': [['y'],
                          ['x','z']],
                    #'cmap': 'jet',
                    'idx': 0,
                    'title': 'Multiple axis plot'}],
                },
    },
}
