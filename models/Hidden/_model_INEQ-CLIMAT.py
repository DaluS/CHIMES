"""Climate-Inequality dynamics"""

_DESCRIPTION = """

* **Article :**
* **Author  :** Paul Valcke, Loic Giacconne
* **Coder   :** Paul Valcke
* **Date    :** 2023/10/25

This model encompass:
* Two household sectors (workers and capitalists)
* One production sector, that has two family of capital: energy and products.
* the energy sector has two technology with different infrastructure, a green and a brown one
* A self-organized dynamics with dividends, wages, prices,




"""

_LOGICS = {
    'size': {},
    'differential': {

        # CAPITAL
        'Ky': {'func': lambda Iy, deltay, Ky: Iy - deltay * Ky,
               'initial': 3},
        'Kg': {'func': lambda Ig, deltag, Kg: Ig - deltag * Kg,
               'initial': 1},
        'Kb': {'func': lambda Ib, deltab, Kb: Ib - deltab * Kb,
               'initial': 1},

        # EFFICIENCY
        'ay': {'func': lambda ay, alpha: ay * alpha},
        'ab': {'func': lambda ab, alpha: ab * alpha},
        'ag': {'func': lambda ag, alpha: ag * alpha},

        # CLIMATE MODULE
        'Temperature': {'func': lambda Emissions, Ct: Emissions * Ct,
                        'initial': 0},

        # PRICES
        'w': {'func': lambda: 0},
        'p': {'func': lambda: 0},

        # Population
        'N': {'func': lambda N, n: N * n},
    },
    'statevar': {
        # Physical output
        'Y': {'func': lambda Ky, nuy: Ky / nuy,
              'definition': 'Useful output',
              'units': 'Units.y^{-1}'},
        'Emissions': {'func': lambda Kb, sigma: Kb * sigma},
        'Energy': {'func': lambda Kb, Kg, nub, nug: Kb / nub + Kg / nug,
                   'def': 'POST EROI energy'},

        # Investment theory
        'I': {'func': lambda s, Y: s * Y,
              'definition': 'Investment in capital'},
        'Iy': {'func': lambda I, epsilony: epsilony * I,
               'definition': 'Investment in output'},
        'Ib': {'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * (1 - epsilong),
               'definition': 'Investment in brown energy'},
        'Ig': {'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * epsilong,
               'definition': 'Investment in green energy'},

        # TO ENDOGENIZE CORRECTLY
        'epsilonb': {'func': lambda: 0.5},
        'epsilony': {'func': lambda: 0.5},

        # LABOR
        'Ly': {'func': lambda Ky, ay: Ky / ay},
        'Lb': {'func': lambda Kb, ab: Kb / ab},
        'Lg': {'func': lambda Kg, ag: Kg / ag},


        # PROFITS
        'Pi': {'func': lambda p, Y, w, Ly, deltay, K, r, D, Energy: p * Y - w * Ly - p * deltay * K - r * D - p * Energy},
        'ROCg': {'func': lambda omegag, nug, deltag: (1 - omegag - deltag * nug) / nug},
        'ROCb': {'func': lambda omegab, nub, deltab: (1 - omegab - deltab * nub) / nub},
        'ROCy': {'func': lambda Pi, p, K: Pi / (p * K)},

        # Wage shares:
        'omegag': {'func': lambda w, Lg, p, Yg: 0}


    },
    'parameter': {
        's': {'value': 0.15,
              'definition': 'saving rate',
              'units': ''},
        'sb': {'value': 0.01},
        'sg': {'value': 0.03},

        'nuy': {'value': 3,
                'definition': 'productive capital to output ratio',
                'units': 'y'},
        'nub': {'value': 3},
        'nug': {'value': 3},
        'deltay': {'value': 0.03,
                   'definition': 'depreciation of capital',
                   'units': r'y^{-1}'},
        'deltab': {'value': 0.03,
                   'definition': 'depreciation of capital',
                   'units': r'y^{-1}'},
        'deltag': {'value': 0.03,
                   'definition': 'depreciation of capital',
                   'units': r'y^{-1}'},

        'Ct': {'value': 0.01,
               'definition': 'Carbon-Temperature proportionality'}
    }
}


# ################## SUPPLEMENTS IF NEEDED ###################################
_SUPPLEMENTS = {}

# ################## DEFIMING PRESETS WITH THEIR SUPPLEMENTS #################
_PRESETS = {}
