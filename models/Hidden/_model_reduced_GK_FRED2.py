'''GK with affine kappa and philips, with US data'''


from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np
from chimes.libraries import Operators as O
_DESCRIPTION = """
* **Article :**
* **Author  :** Hugo Bailly, Frederic Mortier
* **Coder   :** Paul Valcke
"""

_LOGICS = {
    'size': {},
    ###################################################################
    'differential': {
        'omega': {'func': lambda omega, employment, gamma, rho, alpha: omega * (gamma + rho * employment - alpha)},
        'employment': {'func': lambda employment, nu, delta, alpha, beta, k0, k1, omega, r, debt: employment * ((k0 + k1 * (1 - omega - r * debt)) / nu - delta - alpha - beta)},
        'debt': {'func': lambda debt, r, Delta, k0, k1, nu, delta, omega: debt * (r * (1 - Delta) - (k0 + k1 * (1 - omega - r * debt)) / nu + delta) + (k0 + k1 * (1 - omega - r * debt)) - (1 - omega) * (1 - Delta)},

    },
    'parameter': {
        'rho': {'value': 0}, },
}


# ########################## SUPPLEMENTS ################################################
'''Specific parts of code that are accessible'''
_SUPPLEMENTS = {}


# ########################### PRESETS #####################################################


_PRESETS = {
    'FredValues': {
        'fields':
        {
            'alpha': 0.01019082,
            'beta': 0.01568283,
            'gamma': -0.5768167,
            'rho': 0.624795,
            'k0': -0.0419826,
            'k1': 0.9851812,
            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,
            'Delta': 0.2780477,
            'omega': 0.6900101,
            'employment': 0.9383604,
            'debt': 0.5282786,
        },
        'com': ('Data given by F.Mortier on US calibration'),
        'plots': {},
    },
    'Goodwin': {
        'fields':
        {
            # 'alpha': ,
            # 'beta': ,
            'gamma': -0.5768167,
            'rho': 0.624795,
            'k0': 0,
            'k1': 1,
            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,
            'Delta': 0,
            'omega': 0.6900101,
            'employment': 0.9383604,
            'debt': 0,
        },
        'com': ('Data given by F.Mortier on US calibration'),
        'plots': {},
    },
}
