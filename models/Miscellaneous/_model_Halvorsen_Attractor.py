'''Halvorsen Chaotic Attractor'''

# ######################## PRELIMINARY ELEMENTS #########################
from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
_DESCRIPTION = """
3 Differential attractor. Nice symmetry.


"""

_TODO = []
_ARTICLE = ""
_DATE = " 2024/04/23"
_CODER = "Paul Valcke"
_KEYWORDS = ['stochastic', 'Documentation', 'chaos', 'attractor',]
_UNITS = []  # Adding accepted units for fields


_LOGICS = dict(
    differential=dict(
        x={'func': lambda a, x, y, z: -a*x-4*y-4*z-y*y,
            'initial': 0.1},
        y={'func': lambda a, x, y, z: -a*y-4*z-4*x-z*z,
            'initial': 0},
        z={'func': lambda a, x, y, z: -a*z-4*x-4*y-x*x,
            'initial': 2.5},
    ),
    statevar=dict(),
    parameter=dict(
        a=1.4,
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
