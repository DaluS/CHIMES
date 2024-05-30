"""Stochastic movement in a two-relative equilibrium potential"""
import numpy as np

_DESCRIPTION = """
# Tipping point in an independant landscape: 1D with no position feedback


## What is this model ?
A particle of position `x` in a potential `V(x)`.
Its acceleration is due to potential and a brownian motion.

The potential has to equilibrium position `x_1` and `x_2` with different potential values.
There is barrier between them which is the maximum of the potential between `x_1` an `x_2`.

## What is the expected behavior ?
The particle remain trapped around an equilibrium position.
If noise is too small, the particle remains in its local basin.
A fluctuation big enough will make it move from one side to the other.
At small temporal scale the system oscillate with noise around one attractor.
At large temporal scale the system oscillate from one equilibrium to the other.

## Why is it interesting ?

[Blablabla]
"""

_TODO = ['implement presets',
         'implement equilibrium position',
         'add interest and theory',
         'implement visualisations']
_ARTICLE = ""
_DATE = " 2023/12/14"
_CODER = "Paul Valcke"
_KEYWORDS = ['stochastic', 'Documentation', '',]
_UNITS = []  # Adding accepted units for fields


def V(x, v1, v2, v3):
    return v1*x + v2*x**2 + v3*x**4


def dV(x, v1, v2, v3):
    return v1 + 2*v2*x + 4*v3*x**3


_LOGICS = {
    'differential': {
        'v': {'func': lambda a: a,
              'initial': 0},
        'x': {'func': lambda v: v,
              'initial': -6},
    },
    'statevar': {
        'a': lambda T, nx, x, v1, v2, v3, v, damp: -dV(x, v1, v2, v3) + T * np.random.normal(loc=0, size=(nx, 1, 1, 1)) - damp*v,
    },
    'parameter': {
        'T': 40,
        'v1': .5,
        'v2': -10,
        'v3': 0.1,
        'damp': 0.05
    }
}