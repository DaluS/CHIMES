# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is the equation for the Famous Lorenz attractor : three differential equations,
that create a chaotic system oscillating in itself.

As it is not planned to have any other models built on it nor it is built on another smaller model,
everything is written in the model and not in `def_fields` nor `def_functions`.

Please note :
    * As ode fields are not in def_fields, they need an initial value
    * Lorenz_x has a definition, a com, a symbol, a unit... None of them are mandatory (usually put in def_fields)
    * Statevar of course do not need an initial value.
    * parameters are defined with a value



LINK TO ARTICLE :
    https://en.wikipedia.org/wiki/Lorenz_system
@author: Paul Valcke
"""

import numpy as np

def Lorenz_Z (Lorenzbeta=0, Lorenz_x=0, Lorenz_y=0, itself=0):
    return Lorenz_x*Lorenz_y-Lorenzbeta*itself


_LOGICS = {
    'ode': {
        'Lorenz_x': {
            'func': lambda Lorenzsigma=0, Lorenz_y=0, itself=0: Lorenzsigma*(Lorenz_y-itself),
            'initial': 0,
            'definition': 'Simplified rate of convection',
            'com': 'Reduced equation from article',
            'unit': '',
            'symbol': r'$\mathcal{x}$'
        },
        'Lorenz_y': {
            'func': lambda Lorenzrho=0, Lorenz_x=0, Lorenz_z=0, itself=0: Lorenz_x*(Lorenzrho-Lorenz_z)-itself,
            'initial': 1,
            'definition': 'horizontal temperature variation',
        },
        'Lorenz_z': {
            'func': Lorenz_Z,
            'initial': 1,
            'com': 'Z',
        },
    },
    'statevar': {
        'Lorenz_distance' : {
            'func': lambda Lorenz_x=0,Lorenz_y=0,Lorenz_z=0 : np.sqrt(Lorenz_x**2 + Lorenz_y**2 + Lorenz_z**2 ),
            'definition': 'distance to the (0,0,0)',
            'com': 'calculated using norm L2'
            },
    },
    'param': {
        'Lorenzrho': {
            'value': 28,
            'definition': 'linked to prandtl number'
        },
        'Lorenzsigma': {
            'value': 10,
            'definition': 'linked to Rayleigh number'
        },
        'Lorenzbeta': {
            'value': 8/3,
            'definition': 'linked to physical dimension of layer'
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

N = 50
_PRESETS = {
    'Canonical': {
        'fields': {
            'Lorenz_x': 1,
            'Lorenz_y': 1,
            'Lorenz_z': 1,
            'Lorenzsigma': 10,
            'Lorenzrho': 28,
            'Lorenzbeta': 8/3,
        },
        'com': 'Typical run giving the butterfly',
        'plots': [],
    },
    'ManyTrajectories': {
        'fields': {
            'Lorenz_x': 1,
            'Lorenz_y': 1,
            'Lorenz_z': np.linspace(1,1.1,N),
            'Lorenzsigma': 10,
            'Lorenzrho': 28,
            'Lorenzbeta': 8/3,
        },
        'com': f'{N} Close initial position evolving independantly',
        'plots': [],
    },
}
