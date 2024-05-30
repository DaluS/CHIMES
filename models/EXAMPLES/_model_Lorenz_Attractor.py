'''Lorenz Chaotic Attractor: Butterfly effect!'''

# ######################## PRELIMINARY ELEMENTS #########################
from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
_DESCRIPTION = """
Solving the famous 3-coupled ordinary differential system. Canonical case has the two equilibrium with the strange attraction

## What is this model ?

Developed to study properties of a simplified model of atmospheric convection.
The model is a system of three ordinary differential equations. Parameters are linked to hydrodynamics properties of the atmosphere.

## Why is it interesting ? 

Chaos ! The system when solved numerically around certain values is highly sensitive to initial conditions. 
This is the butterfly effect. The system is also a canonical example of a strange attractor: two equilibrium, both unstable. 
The system will oscillate around one, then switch to the other one, staying in a bounded area of the phase space.

The condition to jump from one to the other are very peculiar, in consequence each bifurcation is an event difficult to predict and that impacts deeplt
the system.

As written on the wikipedia page:
The Lorenz equations can arise in simplified models for:
* lasers
* dynamos
* thermosyphons
* brushless DC motors
* electric circuits
* chemical reactions
* forward osmosis
* The Lorenz equations also arise in simplified models for the behaviour of convection rolls

## what is the purpose of your model

It is a good illustration of a complex system, unexpected behavior and emergent properties.
"""

_TODO = []
_ARTICLE = "https://en.wikipedia.org/wiki/Lorenz_system"
_DATE = " 2023/08/21"
_CODER = "Paul Valcke"
_KEYWORDS = ['stochastic', 'Documentation', 'chaos', 'attractor',]
_UNITS = []  # Adding accepted units for fields


_LOGICS = dict(
    differential=dict(
        x=dict(
            func=lambda lor_sigma, y, x: lor_sigma * (y - x),
            com='reduced-form dynamics',
            definition='rate of convection',
            units='',
            initial=0.2,
        ),
        y=dict(
            func=lambda lor_rho, x, z, y: x * (lor_rho - z) - y,
            definition='horizontal temperature variation',
            com='reduced-form dynamics',
            initial=.13,
            units='',

        ),
        z=dict(
            func=lambda lor_beta, x, y, z: x * y - lor_beta * z,
            definition='vertical temperature variation',
            com='reduced-form dynamics',
            initial=.21,
            units='',
        ),
    ),
    statevar=dict(
        distance1=dict(
            func=lambda x, y, z, lor_beta, lor_rho: np.sqrt((x-np.sqrt(lor_beta*(lor_rho-1)))**2 + (y-np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2),
            com='distance to the equilibrium 1',
        ),
        distance2=dict(
            func=lambda x, y, z, lor_beta, lor_rho: np.sqrt((x+np.sqrt(lor_beta*(lor_rho-1)))**2 + (y+np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2),
            com='distance to the equilibrium 2',
        ),
    ),
    parameter=dict(
        lor_sigma=dict(
            value=10,
            units='',
            definition='Prandtl number',
            symbol=r'$\sigma$',
        ),
        lor_rho=dict(
            value=28,
            units='',
            definition='Rayleigh number',
            symbol=r'$\rho$',
        ),
        lor_beta=dict(
            value=8 / 3,
            units='',
            definition='Geometric factor',
            symbol=r'$\beta$',
        ),
    ),
    size={},
)


def OneTenthPercentUncertainty(hub):
    '''
    Run the canonical example with 1% uncertainty on initial conditions and display it in an nyaxis plot
    '''
    hub.set_preset('Canonical example')
    hub.run_uncertainty(0.1)
    hub._DPLOT.nyaxis(hub, [['x'], ['y'], ['z']], title='Lorenz attractor with 0.1% uncertainty on initial conditions and parameter')


_SUPPLEMENTS = {'OneTenthPercentUncertainty': OneTenthPercentUncertainty}

# ---------------------------
# List of presets for specific interesting simulations
plotdic = {
    'XYZ': [dict(x='x',
                 y='y',
                 z='z',
                 color='time',
                 # 'cmap= 'jet',
                 idx=0,
                 title='Lorenz 3-dimension strange attractor')],
    'nyaxis': [dict(
        x='time',
        y=[['y'],
           ['x', 'z']],
        # 'cmap= 'jet',
        idx=0,
        title='Multiple axis plot')], }

_PRESETS = {
    'Canonical example': {
        'fields': dict(
            dt=0.01,
            lor_sigma=10,
            lor_rho=28,
            lor_beta=8 / 3,
        ),
        'com': 'Chaotic attractor around two equilibrium, for those parameter values',
        'plots': plotdic
    },
    'BeginEQ1': {
        'fields': dict(
            dt=0.01,
            lor_sigma=10,
            lor_rho=28,
            lor_beta=8 / 3,
            x=np.sqrt(27*8 / 3)+0.1,
            y=np.sqrt(27*8 / 3),
            z=27,
        ),
        'com': 'Begins at the first equilibrium',
        'plots': plotdic,
    },
}
