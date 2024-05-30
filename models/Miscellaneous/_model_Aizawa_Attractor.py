'''Aizawa Chaotic Attractor'''

# ######################## PRELIMINARY ELEMENTS #########################
from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
_DESCRIPTION = """
3 Differential attractor. 


## What is this model ?

A 3 Dimensional attractor, with oscillations on a spheres and on its polar axis

"""

_TODO = []
_ARTICLE = "https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor"
_DATE = " 2024/04/23"
_CODER = "Paul Valcke"
_KEYWORDS = ['stochastic', 'Documentation', 'chaos', 'attractor',]
_UNITS = []  # Adding accepted units for fields


_LOGICS = dict(
    differential=dict(
        x={'func': lambda z, b, x, d, y: (z-b)*x-d*y,
            'initial': 0.1},
        y={'func': lambda d, x, z, b, y: d*x + (z-b)*y,
            'initial': 0},
        z={'func': lambda z, x, c, a, e, f, y: c+a*z-(z**3)/3-(x**2+y**2)*(1+e*z) + f*z*x**3,
            'initial': 2.5},
    ),
    statevar=dict(),
    parameter=dict(
        a=.95,
        b=.7,
        c=.6,
        d=3.5,
        e=.25,
        f=.1
    ),
)


# ---------------------------
# List of presets for specific interesting simulations
plotdic = {
    'XYZ': [dict(x='x',
                 y='y',
                 z='z',
                 color='time',
                 # 'cmap= 'jet',
                 idx=0,
                 title='Lorenz 3-dimension Aizawa attractor')],
    'nyaxis': [dict(
        x='time',
        y=[['y'],
           ['x', 'z']],
        # 'cmap= 'jet',
        idx=0,
        title='Multiple axis plot')], }

_PRESETS = {
    'plots': {
        'fields': dict(
        ),
        'com': 'Just the plots',
        'plots': plotdic
    },
}
