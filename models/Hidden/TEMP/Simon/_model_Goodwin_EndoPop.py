
'''Goodwin model + Court-McIsaac style population endogenization '''

from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
_DESCRIPTION = """
* **Article :**
* **Author  :** Goodwin
* **Coder   :** Simon Lebastard

This is a basic Goodwin model :
    * Two sectors
    * Exogenous technical progress, exogenous population
    * Capital accumulation through investment of profits
    * Consumption through salary
    * Salary-Profit through Philips curve
    * No money, no inflation
    * No loan possibility

The interesting things :
    * Economic cycles (on employment and wage share) are an emergent property
    * trajectories are closed in the phasespace (employment, omega) employment - wageshare

It is written with a price p=1 for homogeneity issues

ENDEGENOUS POPULATION
---------------------
Population N is split into 14 age groups according to the Court-McIsaac model
N1: population of 0-4 yo        Not employable  Not fertile
N2: population of 4-9 yo        Not employable  Not fertile
N3: population of 10-14 yo      Not employable  Not fertile
N4: population of 15-19 yo      Employable      Fertile
N5: population of 20-24 yo      Employable      Fertile
N6: population of 25-29 yo      Employable      Fertile
N7: population of 30-34 yo      Employable      Fertile
N8: population of 35-39 yo      Employable      Fertile
N9: population of 40-44 yo      Employable      Fertile
N10: population of 45-49 yo     Employable      Fertile
N11: population of 50-54 yo     Employable      Not fertile
N12: population of 55-59 yo     Employable      Not fertile
N13: population of 60-64 yo     Employable      Not fertile
N14: population of 65+ yo       Not employable  Not fertile
For the dynamics of the population in each age group, see
Victor Court & Florent McIsaac, A Representation of the World Population Dynamics for Integrated Assessment Models, March 2020

@author: Simon Lebastard
"""

# ######################## PRELIMINARY ELEMENTS #########################

# ################# DEFINING NEW FUNCTIONS ##############################


def dem_transition(y, lvl_min, lvl_max, y_crit, std):
    """
    Implements the Court-McIsaac model of demographics transition.
    BR can be either a birth rate or a death rate,
    potentially specific to an age-group. No power on the denominator for now, to be added later
    """
    return lvl_min + (lvl_max - lvl_min) / (1 + np.exp(std * (y - y_crit)))


def demo_G1(y, N1, Nfertile, BR_low, BR_high, y_crit_BR, BR_std, G1_DR_low, G1_DR_high, G1_y_crit_DR, G1_DR_std):
    "Court demographics transition function: Age group 1/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_1 = dem_transition(y, G1_DR_low, G1_DR_high, G1_y_crit_DR, G1_DR_std)
    BR = dem_transition(y, BR_low, BR_high, y_crit_BR, BR_std)
    return lambda_X * ((np.log(1 - DR_1) - 1) * N1 - np.log(1 - BR) * Nfertile)


def demo_G2(y, N1, N2, G2_DR_low, G2_DR_high, G2_y_crit_DR, G2_DR_std):
    "Court demographics transition function: Age group 2/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_2 = dem_transition(y, G2_DR_low, G2_DR_high, G2_y_crit_DR, G2_DR_std)
    return lambda_X * ((np.log(1 - DR_2) - 1) * N2 + N1)


def demo_G3(y, N2, N3, G3_DR_low, G3_DR_high, G3_y_crit_DR, G3_DR_std):
    "Court demographics transition function: Age group 3/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_3 = dem_transition(y, G3_DR_low, G3_DR_high, G3_y_crit_DR, G3_DR_std)
    return lambda_X * ((np.log(1 - DR_3) - 1) * N3 + N2)


def demo_G4(y, N3, N4, G4_DR_low, G4_DR_high, G4_y_crit_DR, G4_DR_std):
    "Court demographics transition function: Age group 4/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_4 = dem_transition(y, G4_DR_low, G4_DR_high, G4_y_crit_DR, G4_DR_std)
    return lambda_X * ((np.log(1 - DR_4) - 1) * N4 + N3)


def demo_G5(y, N4, N5, G5_DR_low, G5_DR_high, G5_y_crit_DR, G5_DR_std):
    "Court demographics transition function: Age group 5/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_5 = dem_transition(y, G5_DR_low, G5_DR_high, G5_y_crit_DR, G5_DR_std)
    return lambda_X * ((np.log(1 - DR_5) - 1) * N5 + N4)


def demo_G6(y, N5, N6, G6_DR_low, G6_DR_high, G6_y_crit_DR, G6_DR_std):
    "Court demographics transition function: Age group 6/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_6 = dem_transition(y, G6_DR_low, G6_DR_high, G6_y_crit_DR, G6_DR_std)
    return lambda_X * ((np.log(1 - DR_6) - 1) * N6 + N5)


def demo_G7(y, N6, N7, G7_DR_low, G7_DR_high, G7_y_crit_DR, G7_DR_std):
    "Court demographics transition function: Age group 7/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_7 = dem_transition(y, G7_DR_low, G7_DR_high, G7_y_crit_DR, G7_DR_std)
    return lambda_X * ((np.log(1 - DR_7) - 1) * N7 + N6)


def demo_G8(y, N7, N8, G8_DR_low, G8_DR_high, G8_y_crit_DR, G8_DR_std):
    "Court demographics transition function: Age group 8/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_8 = dem_transition(y, G8_DR_low, G8_DR_high, G8_y_crit_DR, G8_DR_std)
    return lambda_X * ((np.log(1 - DR_8) - 1) * N8 + N7)


def demo_G9(y, N8, N9, G9_DR_low, G9_DR_high, G9_y_crit_DR, G9_DR_std):
    "Court demographics transition function: Age group 9/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_9 = dem_transition(y, G9_DR_low, G9_DR_high, G9_y_crit_DR, G9_DR_std)
    return lambda_X * ((np.log(1 - DR_9) - 1) * N9 + N8)


def demo_G10(y, N9, N10, G10_DR_low, G10_DR_high, G10_y_crit_DR, G10_DR_std):
    "Court demographics transition function: Age group 10/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_10 = dem_transition(y, G10_DR_low, G10_DR_high, G10_y_crit_DR, G10_DR_std)
    return lambda_X * ((np.log(1 - DR_10) - 1) * N10 + N9)


def demo_G11(y, N10, N11, G11_DR_low, G11_DR_high, G11_y_crit_DR, G11_DR_std):
    "Court demographics transition function: Age group 11/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_11 = dem_transition(y, G11_DR_low, G11_DR_high, G11_y_crit_DR, G11_DR_std)
    return lambda_X * ((np.log(1 - DR_11) - 1) * N11 + N10)


def demo_G12(y, N11, N12, G12_DR_low, G12_DR_high, G12_y_crit_DR, G12_DR_std):
    "Court demographics transition function: Age group 12/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_12 = dem_transition(y, G12_DR_low, G12_DR_high, G12_y_crit_DR, G12_DR_std)
    return lambda_X * ((np.log(1 - DR_12) - 1) * N12 + N11)


def demo_G13(y, N12, N13, G13_DR_low, G13_DR_high, G13_y_crit_DR, G13_DR_std):
    "Court demographics transition function: Age group 13/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_13 = dem_transition(y, G13_DR_low, G13_DR_high, G13_y_crit_DR, G13_DR_std)
    return lambda_X * ((np.log(1 - DR_13) - 1) * N13 + N12)


def demo_G14(y, N13, N14, G14_DR_low, G14_DR_high, G14_y_crit_DR, G14_DR_std):
    "Court demographics transition function: Age group 14/14"
    dt = 0.01
    dT = 5
    lambda_X = 1. / dT
    DR_14 = dem_transition(y, G14_DR_low, G14_DR_high, G14_y_crit_DR, G14_DR_std)
    return lambda_X * (np.log(1 - DR_14) * N14 + N13)


# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        'a': {'func': lambda a, alpha: a * alpha},
        'N1': {'func': demo_G1, 'units': 'Humans'},
        'N2': {'func': demo_G2, 'units': 'Humans'},
        'N3': {'func': demo_G3, 'units': 'Humans'},
        'N4': {'func': demo_G4, 'units': 'Humans'},
        'N5': {'func': demo_G5, 'units': 'Humans'},
        'N6': {'func': demo_G6, 'units': 'Humans'},
        'N7': {'func': demo_G7, 'units': 'Humans'},
        'N8': {'func': demo_G8, 'units': 'Humans'},
        'N9': {'func': demo_G9, 'units': 'Humans'},
        'N10': {'func': demo_G10, 'units': 'Humans'},
        'N11': {'func': demo_G11, 'units': 'Humans'},
        'N12': {'func': demo_G12, 'units': 'Humans'},
        'N13': {'func': demo_G13, 'units': 'Humans'},
        'N14': {'func': demo_G14, 'units': 'Humans'},
        'K': {'func': lambda K, Ir, delta: Ir - delta * K},
        'w': {'func': lambda w, phillips: w * phillips},
    },

    # Intermediary relevant functions
    'statevar': {
        'N': {
            'func': lambda N1, N2, N3, N4, N5, N6, N7, N8, N9, N10, N11, N12, N13, N14: N1 + N2 + N3 + N4 + N5 + N6 + N7 + N8 + N9 + N10 + N11 + N12 + N13 + N14,
            'definition': 'Total population',
            'units': 'Humans'
        },
        'Nemployable': {
            'func': lambda N4, N5, N6, N7, N8, N9, N10, N11, N12, N13: N4 + N5 + N6 + N7 + N8 + N9 + N10 + N11 + N12 + N13,
            'definition': 'Total employable population',
            'units': 'Humans'
        },
        'Nfertile': {
            'func': lambda N4, N5, N6, N7, N8, N9, N10: N4 + N5 + N6 + N7 + N8 + N9 + N10,
            'definition': 'Total fertile population',
            'units': 'Humans'
        },
        'y': {'func': lambda Y, N: Y / N, 'units': '$.Humans^{-1}.y^{-1}'},
        'beta1': {
            'func': demo_G1,
            'definition': 'Court McIsaac demographics transition function: Age group 1/14',
            'units': 'y^{-1}',
        },
        'beta2': {
            'func': demo_G2,
            'definition': 'Court McIsaac demographics transition function: Age group 2/14',
            'units': 'y^{-1}',
        },
        'beta3': {
            'func': demo_G3,
            'definition': 'Court McIsaac demographics transition function: Age group 3/14',
            'units': 'y^{-1}',
        },
        'beta4': {
            'func': demo_G4,
            'definition': 'Court McIsaac demographics transition function: Age group 4/14',
            'units': 'y^{-1}',
        },
        'beta5': {
            'func': demo_G5,
            'definition': 'Court McIsaac demographics transition function: Age group 5/14',
            'units': 'y^{-1}',
        },
        'beta6': {
            'func': demo_G6,
            'definition': 'Court McIsaac demographics transition function: Age group 6/14',
            'units': 'y^{-1}',
        },
        'beta7': {
            'func': demo_G7,
            'definition': 'Court McIsaac demographics transition function: Age group 7/14',
            'units': 'y^{-1}',
        },
        'beta8': {
            'func': demo_G8,
            'definition': 'Court McIsaac demographics transition function: Age group 8/14',
            'units': 'y^{-1}',
        },
        'beta9': {
            'func': demo_G9,
            'definition': 'Court McIsaac demographics transition function: Age group 9/14',
            'units': 'y^{-1}',
        },
        'beta10': {
            'func': demo_G10,
            'definition': 'Court McIsaac demographics transition function: Age group 10/14',
            'units': 'y^{-1}',
        },
        'beta11': {
            'func': demo_G11,
            'definition': 'Court McIsaac demographics transition function: Age group 11/14',
            'units': 'y^{-1}',
        },
        'beta12': {
            'func': demo_G12,
            'definition': 'Court McIsaac demographics transition function: Age group 12/14',
            'units': 'y^{-1}',
        },
        'beta13': {
            'func': demo_G13,
            'definition': 'Court McIsaac demographics transition function: Age group 13/14',
            'units': 'y^{-1}',
        },
        'beta14': {
            'func': demo_G14,
            'definition': 'Court McIsaac demographics transition function: Age group 14/14',
            'units': 'y^{-1}',
        },
        'pi': {'func': lambda p, Y, Pi: Pi / (p * Y)},
        'omega': {'func': lambda p, Y, w, L: w * L / (p * Y)},
        'employment': {'func': lambda L, Nemployable: L / Nemployable},
        'g': {'func': lambda Ir, K, delta: Ir / K - delta},

        'Y': {'func': lambda K, nu, Nemployable, a: min(K / nu, a * Nemployable)},
        'Pi': {'func': lambda p, Y, w, L: p * Y - w * L},
        'C': {'func': lambda Y, Ir: Y - Ir},
        'Ir': {'func': lambda Pi: Pi},
        'L': {'func': lambda Y, a: Y / a},

        'phillips': {'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment, },
    },
    'parameter': {
        'p': {'value': 1},
        'philinConst': {'value': 0.02},
        'BR_low': {'value': 0.18, 'units': 'Humans.y^{-1}'},
        'BR_high': {'value': 0.39, 'units': 'Humans.y^{-1}'},
        'BR_std': {'value': 0.00087, 'units': 'Humans.$^{-1}'},
        'y_crit_BR': {'value': 4033.6, 'units': '$.Humans^{-1}'},
        'G1_DR_low': {'value': 0.0392, 'units': 'Humans.y^{-1}'},
        'G1_DR_high': {'value': 0.601, 'units': 'Humans.y^{-1}'},
        'G1_DR_std': {'value': 0.000511, 'units': 'Humans.$^{-1}'},
        'G1_y_crit_DR': {'value': 3951.5, 'units': '$.Humans^{-1}'},
        'G2_DR_low': {'value': 0.00458, 'units': 'Humans.y^{-1}'},
        'G2_DR_high': {'value': 0.349, 'units': 'Humans.y^{-1}'},
        'G2_DR_std': {'value': 0.000543, 'units': 'Humans.$^{-1}'},
        'G2_y_crit_DR': {'value': 3441.8, 'units': '$.Humans^{-1}'},
        'G3_DR_low': {'value': 0.00426, 'units': 'Humans.y^{-1}'},
        'G3_DR_high': {'value': 0.335, 'units': 'Humans.y^{-1}'},
        'G3_DR_std': {'value': 0.000587, 'units': 'Humans.$^{-1}'},
        'G3_y_crit_DR': {'value': 3312.8, 'units': '$.Humans^{-1}'},
        'G4_DR_low': {'value': 0.00586, 'units': 'Humans.y^{-1}'},
        'G4_DR_high': {'value': 0.332, 'units': 'Humans.y^{-1}'},
        'G4_DR_std': {'value': 0.00063, 'units': 'Humans.$^{-1}'},
        'G4_y_crit_DR': {'value': 3282.7, 'units': '$.Humans^{-1}'},
        'G5_DR_low': {'value': 0.00857, 'units': 'Humans.y^{-1}'},
        'G5_DR_high': {'value': 0.339, 'units': 'Humans.y^{-1}'},
        'G5_DR_std': {'value': 0.00066, 'units': 'Humans.$^{-1}'},
        'G5_y_crit_DR': {'value': 3364.8, 'units': '$.Humans^{-1}'},
        'G6_DR_low': {'value': 0.010, 'units': 'Humans.y^{-1}'},
        'G6_DR_high': {'value': 0.343, 'units': 'Humans.y^{-1}'},
        'G6_DR_std': {'value': 0.00069, 'units': 'Humans.$^{-1}'},
        'G6_y_crit_DR': {'value': 3323.4, 'units': '$.Humans^{-1}'},
        'G7_DR_low': {'value': 0.0327, 'units': 'Humans.y^{-1}'},
        'G7_DR_high': {'value': 0.011, 'units': 'Humans.y^{-1}'},
        'G7_DR_std': {'value': 0.00072, 'units': 'Humans.$^{-1}'},
        'G7_y_crit_DR': {'value': 3297.5, 'units': '$.Humans^{-1}'},
        'G8_DR_low': {'value': 0.013, 'units': 'Humans.y^{-1}'},
        'G8_DR_high': {'value': 0.354, 'units': 'Humans.y^{-1}'},
        'G8_DR_std': {'value': 0.00064, 'units': 'Humans.$^{-1}'},
        'G8_y_crit_DR': {'value': 3469.5, 'units': '$.Humans^{-1}'},
        'G9_DR_low': {'value': 0.016, 'units': 'Humans.y^{-1}'},
        'G9_DR_high': {'value': 0.342, 'units': 'Humans.y^{-1}'},
        'G9_DR_std': {'value': 0.00060, 'units': 'Humans.$^{-1}'},
        'G9_y_crit_DR': {'value': 3365.7, 'units': '$.Humans^{-1}'},
        'G10_DR_low': {'value': 0.022, 'units': 'Humans.y^{-1}'},
        'G10_DR_high': {'value': 0.357, 'units': 'Humans.y^{-1}'},
        'G10_DR_std': {'value': 0.00054, 'units': 'Humans.$^{-1}'},
        'G10_y_crit_DR': {'value': 3601.1, 'units': '$.Humans^{-1}'},
        'G11_DR_low': {'value': 0.032, 'units': 'Humans.y^{-1}'},
        'G11_DR_high': {'value': 0.381, 'units': 'Humans.y^{-1}'},
        'G11_DR_std': {'value': 0.00052, 'units': 'Humans.$^{-1}'},
        'G11_y_crit_DR': {'value': 4018.9, 'units': '$.Humans^{-1}'},
        'G12_DR_low': {'value': 0.046, 'units': 'Humans.y^{-1}'},
        'G12_DR_high': {'value': 0.393, 'units': 'Humans.y^{-1}'},
        'G12_DR_std': {'value': 0.00048, 'units': 'Humans.$^{-1}'},
        'G12_y_crit_DR': {'value': 4187.2, 'units': '$.Humans^{-1}'},
        'G13_DR_low': {'value': 0.072, 'units': 'Humans.y^{-1}'},
        'G13_DR_high': {'value': 0.394, 'units': 'Humans.y^{-1}'},
        'G13_DR_std': {'value': 0.00048, 'units': 'Humans.$^{-1}'},
        'G13_y_crit_DR': {'value': 4246.3, 'units': '$.Humans^{-1}'},
        'G14_DR_low': {'value': 0.270, 'units': 'Humans.y^{-1}'},
        'G14_DR_high': {'value': 0.492, 'units': 'Humans.y^{-1}'},
        'G14_DR_std': {'value': 0.00054, 'units': 'Humans.$^{-1}'},
        'G14_y_crit_DR': {'value': 4104.9, 'units': '$.Humans^{-1}'},
        'dT': {'value': 5, 'units': 'y'},
    },
    'size': {},
}

_SUPPLEMENTS = {}

# ####################### PRESETS #######################################
_PRESETS = {
    'default-2021': {
        'fields': {
            'dt': 0.01,
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
            'K': 96.53e12 / 3,  # using nu=3 and 2021 GWP reported by WB
            'D': 0,
            'w': .6,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': '',
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
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
                     'z': 'time',
                     'color': 'pi',
                     'idx': 0,
                     'title': ''}],
            'byunits': [],
        },
    },
    'default-1960': {
        'fields': {
            'dt': 0.01,
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
            'w': .6,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': '',
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
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
                     'z': 'time',
                     'color': 'pi',
                     'idx': 0,
                     'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits-2021': {
        'fields': {
            'nx': 5,
            'dt': 0.01,
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
            'K': 96.53e12 * 3,
            'D': 0,
            'w': [.5, .5 * 1.2, .5 * 1.3, .5 * 1.5, .5 * 1.7],
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        'plots': {
            'timetrace': [{'keys': ['employment', 'omega']}],
            'nyaxis': [],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}
