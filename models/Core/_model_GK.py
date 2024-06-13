
"""Goodwin-Keen model: savings-investment dynamics with """

from chimes.libraries import Funcs, importmodel, merge_model
from chimes.libraries import Operators as O
import numpy as np
_DESCRIPTION = """
## What is this model ?

This is a Goodwin model with a few modifications. 
The bigger the profits rate $\pi$, the bigger the investment, which appears as debt-financed. 
Since the system is respecting Say's law $Y=C+I$, more investment at a constant production means less consumption.
In consequence, the system behaves as if households where loaning money to the firms, prefering not to consume at the instant.

In term of equations: 
* In a Goodwin model $I=\pi Y$
* In a Goodwin-Keen model $I = \kappa(\pi) Y$, kappa being a parametric function 

Since the debt equation is $\dot{D}= rD + wL - p*C$, it becomes $\dot{D} = pY * (\kappa(\pi)-\pi)$

## Why is it interesting ? 

Private debt is often overlooked and allow another angle of approach. 
A non-linear kappa curve will also break the closed cycles aspect of a Goodwin. 
In certains conditions there can be a debt crisis

## Expected behavior

The equilibrium is now stable in most cases, and another equilibrium (inifinite debt ratio) also appears. 
The "bad" solovian equilibrium is also stable, meaning that an economy can be driven toward it. 

## What is important to remember

It is a nice illustration of two-attractor dynamics in economy, however the investment mechanism without inflation correction is at best naive.
Debt-fundings is also not the only locally stabilizing mechanism to consider 
"""

_TODO = ['Better models !']
_ARTICLE = " "
_DATE = "2021"
_CODER = "Paul Valcke"
_KEYWORDS = ['Goodwin', 'Toy-model', 'Debt', 'Crises',]


######################################################################

_LOGICS = dict(
    differential=dict(
        a=dict(func=lambda a, alpha: a * alpha),
        N=dict(func=lambda N, n: N * n),
        K=dict(func=lambda K, Ir, delta: Ir - delta * K),
        w=dict(func=lambda w, phillips: w * phillips),
        p=dict(func=lambda p, inflation: p * inflation),
        D=dict(func=lambda w, L, C, r, D, p: r * D + w * L - p * C),
        Dh=dict(func=lambda w, L, C, r, D, p, : -r * D - w * L + p * C),
    ),

    statevar=dict(
        pi=dict(func=lambda p, Y, Pi: Pi / (p * Y)),
        d=dict(func=lambda p, Y, D: D / (p * Y)),
        omega=dict(func=lambda p, Y, w, L: w * L / (p * Y)),
        employment=dict(func=lambda L, N: L / N),
        c=dict(func=lambda p, omega: p * omega),
        g=dict(func=lambda Ir, K, delta: Ir / K - delta),
        Y=dict(func=lambda K, nu: K / nu),
        Pi=dict(func=lambda p, Y, w, L, r, D: p * Y - w * L - r * D),
        I=dict(func=lambda kappa, p, Y: kappa * p * Y),
        C=dict(func=lambda Y, Ir: Y - Ir),
        Ir=dict(func=lambda p, I: I / p),
        L=dict(func=lambda Y, a: Y / a),

        GDP=dict(func=lambda Y, p: Y * p),

        inflation=dict(func=lambda c, p, eta, mu: eta * (mu * c / p - 1)),

        # Divergent Phillips, exponential kappa
        kappa=dict(func=lambda pi, k0, k1, k2: k0 + k1 * np.exp(k2 * pi),
                   com='Exponential kappa function'),
        phillips=dict(func=lambda employment, phi0, phi1: -phi0 + phi1 / (1 - employment)**2,
                      com='Divergent Phillips curve'),

        # Affine for both
        # 'kappa'     :{'func': lambda pi, k0, k1: k0 + k1 * pi},
        # 'phillips'  :{'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},
    ),

    parameter=dict(
        Delta=0,
    )
)


def ThreeDynamics(hub):
    """Draw three qualitatively different Dynamical phase-space associated with a Goodwin-Keen"""
    
    print('HAHQAHQAH')
    for preset in ['default', 'debtcrisis', 'debtstabilisation']:
        hub.set_preset(preset, verb=False)
        hub.run(verb=False)
        hub.plot_preset('debtstabilisation')


_SUPPLEMENTS = {'ThreeDynamics': ThreeDynamics}
_PRESETS = {
    'default': {
        'fields': {
            'alpha': 0.01019082,
            'n': 0.01568283,

            'k0': -0.0065,
            'k1': 0.006737946999085467,
            'k2': 20,
            'phinull': 0.1,

            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,

            'eta': 0.1,
            'dt': 0.01,

            'a': 1,
            'N': 1,
            'K': 3.607,
            'D': 0,
            'w': .7,

            'Tsim': 50,
        },
        'com': 'Convergence to equilibrium',
        'plots': {'XY': [{'x': 'employment',
                          'y': 'omega',
                          'color': 'd',
                          'idx': 0,
                          'title': ''}],
                  'XYZ': [{'x': 'employment',
                          'y': 'omega',
                           'z': 'd',
                           'color': 'time',
                           'idx': 0,
                           'title': ''}],
                  'byunits': [{'title': 'plot by units'}],
                  'nyaxis': [{'x': 'time',
                              'y': [['employment', 'omega'],
                                    ['d'], ['pi', 'kappa'], ['inflation']
                                    ],
                              'idx': 0,
                              'title': '',
                              'lw': 1}],
                  'Onevariable': [{'key': 'employment',
                                   'mode': 'cycles',
                                   'log': False,
                                   'idx': 0,
                                   'Region': 0,
                                   'tini': False,
                                   'tend': False,
                                   'title': ''}]
                  },
    },
    'debtcrisis': {'fields': {
        'alpha': 0.01019082,
        'n': 0.01568283,

        'k0': -0.0065,
        'k1': 0.006737946999085467,
        'k2': 20,
        'phinull': 0.1,

        'nu': 3.844391,
        'r': 0.02083975,
        'delta': 0.04054871,

        'eta': 0.,
        'dt': 0.01,

        'a': 1,
        'N': 1,
        'K': 3.07,
        'D': 0,
        'w': .7,

        'Tsim': 50,
    },
        'com': 'Path toward infinite relative debt',
        'plots': {
        'XYZ': [{'x': 'employment',
                 'y': 'omega',
                 'z': 'd',
                 'color': 'time',
                          'idx': 0,
                          'title': ''}],
        'nyaxis': [{'x': 'time',
                    'y': [['employment', 'omega'],
                          ['d'], ['pi', 'kappa'], ['inflation']
                          ],
                    'idx': 0,
                    'title': '',
                    'lw': 1}],
    }
    },
    'debtstabilisation': {
        'fields': {
            'alpha': 0.01019082,
            'n': 0.01568283,

            'k0': -0.0065,
            'k1': 0.003737946999085467,
            'k2': 20,
            'phinull': 0.1,

            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,

            'eta': 0.01,
            'mu': 1.5,
            'dt': 0.01,

            'a': 1,
            'N': 1,
            'K': 3.307,
            'D': 0,
            'w': .7,

            'dt': 0.05,
            'Tsim': 300,
        },
        'com': 'Stabilization through excess of debt',
        'plots': {'XYZ': [{'x': 'employment',
                           'y': 'omega',
                           'z': 'd',
                           'color': 'time',
                           'idx': 0,
                           'title': 'Goodwin-Keen phase-space dynamics'}],
                  },
    },
}
