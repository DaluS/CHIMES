'''Rossler Chaotic Attractor'''

# ######################## PRELIMINARY ELEMENTS #########################
from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
_DESCRIPTION = """
3 Differential attractor. One equilibrium point

$$\dfrac{\partial x}{\partial t} = -y - z$$
$$\dfrac{\partial y}{\partial t} = x+ay$$
$$\dfrac{\partial z}{\partial t} = b + z(x-c) $$


## What is this model ?

A 3 Dimensional attractor, that can exhibit chaotic behavior. 
It is mostly a 2D unstable oscillator on the XY plane, that extend to 3D at large scale, then go back to the equilibrium point

## Why is it interesting ?

## what is the purpose of your model

It is a good illustration of a complex system, unexpected behavior and emergent properties.
"""

_TODO = []
_ARTICLE = "https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor"
_DATE = " 2024/04/23"
_CODER = "Paul Valcke"
_KEYWORDS = ['stochastic', 'Documentation', 'chaos', 'attractor',]
_UNITS = []  # Adding accepted units for fields


_LOGICS = dict(
    differential=dict(
        x={'func': lambda y, z: -y-z,
            'initial': 1},
        y={'func': lambda y, x, ros_a: x+ros_a*y,
            'initial': 1},
        z={'func': lambda x, z, ros_c, ros_b: ros_b+z*(x-ros_c),
            'initial': 1},
    ),
    statevar=dict(),
    parameter=dict(
        ros_a=0.1,
        ros_b=0.1,
        ros_c=14
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
                 title='3-dimension Rossler attractor')],
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
