"""Energy (Green-Brown) + Output (Grey) Capital model with market allocation"""

import numpy as np

_DESCRIPTION = """
## What is this model ?

This model is the capital core properties for ICED (Inequality-Climate-Economy-Decarbonation).
It cover the output and investment dynamics in three types of capitals and its consequences

## Why is it interesting ?

It allows to see how -social consequences and climate feedback aside- technology coefficient and climate policies will impact decoupling. 



## what is the purpose of your model

The less efficient energy production is, the more investment is allocated to it.
The technology with the higher capital-to-output ratio will have the bigger investment.
The investment is causal of the capital amount, and the emissions are consequence of the amount of capital.
In consequence, the model capture the inertia of decarbonation.

Beyond the natural evolution of the market, we add the following mechanisms:
* Voluntary destruction of brown capital at a rate $\delta^C$
* Carbon tax taken from brown sector to green sector

## Expected behavior

* The system start with high investment into brown as its rentability is higher
* A bigger carbon tax makes a rapid boost early stage for green that then slow down as the relative effects dampens
* Without voluntary destruction of brown capital, the emissions will at best slow down as fast as the natural depreciation rate of brown assets

"""
_TODO = ['Completing the model', 'that should be done']
_ARTICLE = "https://www.overleaf.com/read/fxppgztffzph#6fa1cb"
_DATE = "2023/12/07 model file creation"
_CODER = "Paul Valcke"
_KEYWORDS = ['module', 'capital', 'investment', 'decarbonation']
_UNITS = []  # Optional: Adding accepted units for fields
# ###########################################################

_LOGICS = {
    'differential': {
        # The three types of capital
        'Ky': {
            'func': lambda Ky, Iy, deltay: Iy - deltay * Ky,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'initial': 1.6},
        'Kg': {
            'func': lambda Kg, deltag, Ig: Ig - deltag * Kg,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'initial': 0.1},
        'Kb': {
            'func': lambda Kb, deltab, Ib: Ib - deltab * Kb,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'initial': .75},

        # the automatisation of each technology
        'ay': {
            'func': lambda ay, alphay: ay * alphay,
            'units': 'Humans.Units^{-1}',
            'com': 'Basic exogenous technological change',
            'initial': 3},
        'ag': {
            'func': lambda ag, alphag: ag * alphag,
            'com': 'Basic exogenous technological change',
            'units': 'Humans.Units^{-1}',
            'symbol': r'$a_g$',
            'initial': 3},
        'ab': {
            'func': lambda ab, alphab: ab * alphab,
            'com': 'Basic exogenous technological change',
            'units': 'Humans.Units^{-1}',
            'symbol': r'$a_b$',
            'initial': 3},

        # investment allocation
        'epsilony': {'func': lambda sigmay, epsilony, uE: sigmay * epsilony * (1 - epsilony) * (1 - uE),
                     'initial': .65,
                     'definition': 'share of investment into energy capital',
                     'com': "lazy way to ensure that enough energy is available. Unstable mechanism in a CHI",
                     'symbol': r'$\epsilon_y$',
                     'units': ''},

    },
    'statevar': {
        # Investment - Consumption repartition
        'Y': {'func': lambda Ay, Ky: Ay*Ky},  # , uE, CESexp: Ay * Ky*(1+(1/uE)**(-CESexp))**(-1/CESexp)},
        'C': {'func': lambda Y, omega: Y*omega,
              'units': 'Units.y^{-1}'},
        'I': {'func': lambda Y, C: Y - C,
              'units': 'Units.y^{-1}'},

        # Productive-Green-Brown repartition
        'Iy': {
            'func': lambda I, epsilony: I * epsilony,
            'units': r'$.y^{-1}', },
        'Ig': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * epsilong,
            'units': r'$.y^{-1}', },
        'Ib': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * (1 - epsilong),
            'units': r'$.y^{-1}', },

        # Energy level
        'uE': {'func': lambda Ky, E, Eeff: Ky / (Eeff*E),
               'units': '',
               'definition': 'use of energy capital',
               'symbol': r'$u_E$'},
        'E': {'func': lambda Ab, Ag, Kb, Kg: Ab * Kb + Ag * Kg,
              'definition': 'Energy flux',
              'units': r'Units.y^{-1}'},
        'Color': {'func': lambda Ag, Kg, E: Ag*Kg/E,
                  'units': '',
                  'definition': '1 energy is fully green, 0 fully brown'},
        'Emission': {'func': lambda pollb, Ab, Kb: Ab*Kb,
                     'definition': 'Carbon emissions',
                     'units': 'Carbon.y^{-1}'},

        # Market repartition for Green-Brown
        'rocb': {'func': lambda Ab, omega, ay, ab, deltab, pc, p, pollb: Ab - omega * ay / ab - deltab - pc/p*pollb*Ab,
                 'definition': 'Return of capital for brown technology',
                 'com':        'no carbon tax',
                 'symbol':     r'$\mathcal{R}^{oc}_B$',
                 'units':      'y^{-1}'},
        'rocg': {'func': lambda Ag, omega, ay, ag, deltag, Ab, pollb, p, pc, Kb, Kg: Ag - omega * ay / ag - deltag+(Kb/Kg) * pc/p*pollb*Ab,
                 'definition': 'Return of capital for green technology',
                 'com':        'no carbon tax',
                 'symbol':     r'$\mathcal{R}^{oc}_G$',
                 'units':      'y^{-1}'},
        'epsilong': {
            'func': lambda rocg, rocb, zi, zg: .5 * (1 + np.tanh(zi * (rocg - rocb - 1 + zg))),
            'units': '',
            'symbol': r'$\epsilon_g$',
            'definition': 'share of energy investment in green',
            'com': 'market allocation through ROC'},




        # Auxilliary
        'g': {'func': lambda Iy, deltay, K: Iy/K - deltay,
              'definition': "growth rate usefull output",
              'com': 'its definition'},

        # AGGREGATES :
        # 'omega': {'func': lambda w, L, p, Y: w * L / (p * Y)},
        # 'd': {'func': lambda D, p, Y: D / (p * Y)},
        # 'pi': {'func': lambda Pi, Y: Pi / Y},
        # 'Pi': {'func': lambda p, Y, w, L, delta, K, r, D: p * Y - w * L - p * delta*K - r * D},
        'L': {'func': lambda Ky, ay, Kb, ab, Kg, ag: Ky / ay + Kb / ab + Kg / ag},
        'a': {'func': lambda K, L: K / L},
        'nu': {'func': lambda K, Y: K / Y},
        'delta': {'func': lambda K, Ky, Kb, Kg, deltab, deltag, deltay: (Kb*deltab+Kg*deltag+Ky*deltay)/K},
        'prod': {'func': lambda Y, L: Y / L,
                 'units': 'Units.Humans^{-1}.y^{-1}'},
        'K': {'func': lambda Ky, Kb, Kg: Ky + Kb + Kg},
        'deltab': {'func': lambda deltab0, deltaC: deltab0 + deltaC,
                   'symbol': r'$\delta_b$', },


    },
    'parameter': {
        'pc': {'value': 0,
               'definition': 'carbon price',
               'units': r'$.C^{-1}',
               'symbol': r'$p_{carbon}$'},
        'pollb': {'value': 1,
                  'definition': 'Carbon intensity of producing 1 unit of energy through Kb',
                  'units': r'C.Units^{-1}',
                  'symbol': r''
                  },
        'Eeff': {'value': 1,
                 'units': '',
                 'definition': 'Energy consumption efficiency',
                 'symbol': r'$E_{eff}$'},

        # Automation rate
        'alphab': 0.025,
        'alphag': 0.035,
        'alphay': 0.025,

        # By default depreciation rate
        'deltay': 0.05,
        'deltab0': 0.05,
        'deltag': 0.05,
        'deltaC': {'value': 0,
                   'definition': 'Voluntary destruction of brown capital',
                   # 'com':        'Ad-hoc shape',
                   'units':      'y^{-1}',
                   'symbol':     r'$\delta^{carb}_b$'},


        # Capital efficiency rate
        'Ab': 2,
        'Ay': 1 / 2,
        'Ag': 1,
        # Market reactions
        'sigmay': 20,
        'zi': 1,
        'zg': .5,

    }
}


_PRESETS = {
    'default': {
        'com': 'Changes nothing, just plot holders',
        'fields': {},
        'plots': {
            'nyaxis': [
                dict(y=[['ab', 'ag'], ['Ag'], ['Emission']],
                     title='Extensive technological properties'),
                dict(y=[['epsilony', 'epsilong'], ['Eeff'], ['Color']],
                     title='Repartition'),
                dict(y=[['nu'], ['a'], ['delta', 'g'], ['prod']],
                     title='Monosectoral equivalent'),
            ],

        },
    },
}
