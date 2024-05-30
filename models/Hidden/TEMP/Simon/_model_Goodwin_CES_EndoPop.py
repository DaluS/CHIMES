
'''Goodwin with a CES production function and Court-McIsaac population endogenization'''
# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np
from chimes.libraries import Funcs, importmodel, merge_model
_DESCRIPTION = """
DESCRIPTION :

    This is a small modificaiton of Goodwin : the Leontiev optimised function has been
    replaced by a CES (its generalisation).

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke, Simon Lebastard
"""


# ######################## LOGICS #######################################
_LOGICS, _PRESETS0, _SUPPLEMENTS_G = importmodel('Goodwin_EndoPop')

_CES_LOGICS = {
    'statevar': {
        # Characteristics of a CES
        'cesLcarac': {
            'func': lambda u, A, K, a, b, CESexp: A * (u * K / a) * (1 - b)**(1 / CESexp),
            'com': 'Typical Labour in CES',
            'size': ['Nprod'],
        },
        'cesYcarac': {
            'func': lambda u, K, A, b, CESexp: u * K * A * b**(-1 / CESexp),
            'com': 'Typical Y in CES',
            'size': ['Nprod'],
        },
        'omegacarac': {
            'func': lambda w, cesLcarac, p, cesYcarac: w * cesLcarac / (p * cesYcarac),
            'com': 'Typical omega from K,p,w',
            'symbol': r'$\omega^c$',
            'size': ['Nprod'],
        },

        # From it are deduced optimised quantities
        'nu': {
            'func': lambda omega, b, A, CESexp: ((1 - omega) / b)**(-1. / CESexp) / A,
            'com': 'nu deduced from CES optimisation of profit',
            'size': ['Nprod'],
        },
        'l': {
            'func': lambda omegacarac, CESexp, Nemployable, cesLcarac: np.minimum(np.maximum((omegacarac**(-CESexp / (1 + CESexp)) - 1)**(1 / CESexp), 0), Nemployable / cesLcarac),
            'com': 'impact of elasticity on real employment',
            'size': ['Nprod'],
        },

        # From it are deduced Labor and Output
        'Y': {
            'func': lambda u, K, omegacarac, l, b, CESexp, A: u * K * ((1 - omegacarac * l) / b)**(1. / CESexp) * A,
            'com': 'Y CES with optimisation of profit',
            'size': ['Nprod'],
        },
        'L': {
            'func': lambda l, cesLcarac: cesLcarac * l,
            'com': 'L CES, deduced from l',
            'size': ['Nprod'],
        },
    },
    'parameter': {
        'u': {'value': 1},

    },
    'size': {'Nprod': {'list': ['1']}, },
}

_LOGICS = merge_model(_LOGICS, _CES_LOGICS, verb=False)


# ####################### PRESETS #######################################
_PRESETS = {
    'CES_1960': {
        'fields': {
            'dt': 0.01,
            'Tsim': 100,

            'a': 1.39e12 / ((0.044 + 0.042 + 0.038 + 0.035 + 0.030 + 0.025 + 0.024 + 0.021 + 0.017 + 0.013) * 2.5e9),  # calibrated for employable population to not be initially limiting
            'N1': 0.074 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N2': 0.064 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N3': 0.053 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N4': 0.044 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N5': 0.042 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N6': 0.038 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N7': 0.035 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N8': 0.030 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N9': 0.025 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N10': 0.024 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N11': 0.021 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N12': 0.017 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N13': 0.013 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N14': 0.023 * 2.5e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'K': 1.39e12 * 3,  # using nu=3 and 2021 GWP reported by WB
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'delta': .005,
            'phinull': 0.1,

            'CESexp': 1000,
            'A': 1 / 3,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'employment'],
                              ['omega'],
                              ],
                        'idx': 0,
                        'title': '',
                        'lw': 1}],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'color': 'time',
                    'idx': 0}],
            'XYZ': [{'x': 'employment',
                     'y': 'omega',
                     'z': 'pi',
                     'color': 'time',
                     'idx': 0,
                     'title': ''}],
            'byunits': [],
        },
    },
    'CES_2021': {
        'fields': {
            'dt': 0.01,
            'Tsim': 100,

            'a': 96.53e12 / ((0.041 + 0.039 + 0.038 + 0.038 + 0.036 + 0.033 + 0.030 + 0.029 + 0.025 + 0.020) * 7.888e9),  # calibrated for employable population to not be initially limiting
            'N1': 0.042 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N2': 0.044 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N3': 0.043 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N4': 0.041 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N5': 0.039 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N6': 0.038 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N7': 0.038 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N8': 0.036 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N9': 0.033 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N10': 0.030 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N11': 0.029 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N12': 0.025 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N13': 0.020 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'N14': 0.044 * 7.888e9,  # male share from https://www.populationpyramid.net/world/2023/ and 2021 world population
            'K': 96.53e12 * 3,  # using nu=3 and 2021 GWP reported by WB
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'delta': .005,
            'phinull': 0.1,

            'CESexp': 1000,
            'A': 1 / 3,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'employment'],
                              ['omega'],
                              ],
                        'idx': 0,
                        'title': '',
                        'lw': 1}],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'color': 'time',
                    'idx': 0}],
            'XYZ': [{'x': 'employment',
                     'y': 'omega',
                     'z': 'pi',
                     'color': 'time',
                     'idx': 0,
                     'title': ''}],
            'byunits': [],
        },
    },
}
