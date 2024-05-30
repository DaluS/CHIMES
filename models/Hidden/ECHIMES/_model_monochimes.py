'''Monosectoral core equivalent in ECHIMES'''

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np
from chimes.libraries import Operators as O
_DESCRIPTION = """
# Monosectoral generalistic core
* **Article :** https://www.overleaf.com/read/tzcxmpvvqvmh
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

## Description

"""


_LOGICS = {
    'size': {},
    'differential': {
        # MONETARY STOCK-FLOW CONSISTENCY
        'D': {'func': lambda W, C: W - C},
        'Dh': {'func': lambda W, C: -W + C},

        # PHYSICAL STOCK-FLOW CONSISTENCY
        'V': {'func': lambda dotV: dotV},
        'K': {'func': lambda Ir, delta, K: Ir - delta * K},

        # PRICES
        'p': {'func': lambda p, inflation: p * inflation},
        'w0': {'func': lambda Phillips, w0, gammai, inflation: w0 * (Phillips + gammai * inflation)},

        # EXOGENOUS SCALING
        'a0': {'func': lambda a0, alpha: a0 * alpha},
        'N': {'func': lambda N, n: N * n},
    },
    'statevar': {
        # definitions
        'w': {'func': lambda w0, z: w0 * z},
        'a': {'func': lambda a0, b: a0 * b},
        'pi': {'func': lambda Pi, p, Y: Pi / (p * Y)},
        'omega': {'func': lambda w, L, p, Y: w * L / (p * Y)},
        'd': {'func': lambda D, p, Y: D / (p * Y)},
        'ROC': {'func': lambda Pi, K, p, Xi: Pi / (p * K * Xi)},

        # Related
        'productivity': {'func': lambda Y, L: Y / L},
        'employment': {'func': lambda L, N: L / N},
        'L': {'func': lambda l, K, a: l * K / a},

        'c': {'func': lambda omega, Gamma, nu, delta, Xi, p: p * omega + p * Gamma + p * nu * delta * Xi},
        'mu': {'func': lambda p, c: p / c},
        'nu': {'func': lambda K, Y: K / Y},
        'g': {'func': lambda Ir, K, delta: Ir / K - delta},

        # Physical fluxes
        'deltaK': {'func': lambda delta, K: delta * K,
                   'symbol': r'$\delta K$'},
        'Y': {'func': lambda K, A: K * A},
        'Cr': {'func': lambda C, p: C / p},
        'Ir': {'func': lambda I, p, Xi: I / (p * Xi)},
        'dotV': {'func': lambda Y, Gamma, Cr, Xi, Ir: Y * (1 - Gamma) - Cr - Xi * Ir},
        'Pi': {'func': lambda p, Y, Gamma, w, L, deltaK, Xi, r, D: p * Y * (1 - Gamma) - w * L - p * deltaK * Xi - r * D},

        # Monetary fluxes
        'W': {'func': lambda w, L, r, D, Delta, Pi: w * L + r * D + Delta * Pi},
        'I': {'func': lambda p, delta, K, Ipond, Delta, Pi: Ipond * (1 - Delta) * Pi + p * delta * K},
        'C': {'func': lambda Cpond, W: Cpond * W},

        'Phillips': {'func': lambda phi0, phi1, employment: -phi0 + phi1 / (1 - employment)**2},
        # 'Phillips'  : {'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},
        #                      'com': 'LINEAR',},
    },
    'parameter': {
        # 'inflation':{'value':0},
        'gammai': {'value': 0,
                   'symbol': r'$\gamma i$'},
        'Ipond': {'value': 1},
        'Cpond': {'value': 1},
        'Gamma': {'symbol': r'$\Gamma$'},
        # 'Delta': {'symbol':r'$\Delta$'}
    }
}

###############################################################################
# ############################ EXTENSIONS ######################################
_LOGICS_COSTPUSH = {  # inflation with cost-push dynamics
    'statevar': {'inflation': {'func': lambda etap, mu0, mu: etap * np.log(mu0 / mu)},
                 },
    'parameter': {'etap': {'value': 0},
                  'mu0': {'value': 1},
                  },
}


def l(omegacarac, CESexp):
    return np.select([omegacarac < 1, omegacarac >= 1],
                     [(np.maximum(omegacarac**(-CESexp / (1 + CESexp)) - 1, 10**(-3)))**(1 / CESexp),
                     .7])


_LOGICS_CES = {  # Capital-Labor substituability
    'statevar': {'Y': {'func': lambda A, K, l, CESexp: A * K * (1 + l**(-CESexp))**(-1 / CESexp)},
                 'omegacarac': lambda w, a, p, A, Gamma: w / (A * a * p * (1 - Gamma)),
                 'l': {'func': l},
                 'L': {'func': lambda K, a, l: l * K / a}},
    'parameter': {'CESexp': {'value': 10**3}, }}

_LOGICS_PHILLIPS = {  # Profit in Phillips and lag in lambda
    'differential': {'employmenteff': {'func': lambda employment, employmenteff, flambda: (employment - employmenteff) * flambda}},
    'statevar': {'Phillips': {'func': lambda zpi, pi, phi0, phi1, employmenteff: -phi0 + (pi / 0.15)**zpi * phi1 / (1 - employmenteff)**2}},
    'parameter': {'zpi': {'value': 0.1},
                  'flambda': {'value': 10}, }, }

_LOGICS_PROGRESS = {  # Kaldor-Verdorn, Learning by doing, capital efficiency
    'differential': {'a': {'func': lambda a, alpha, betag, g, employment, betalambda: a * (alpha + betag * g + betalambda * employment)}},
    'parameter': {'betag': {'value': 0},
                  'betalambda': {'value': 0}}}

_LOGICS_INCREASING_RETURN = {  # Exponent on production function (Leontiev)
    'statevar': {'Y': {'func': lambda K, A, epsilony: (K * A)**(epsilony)}, },
    'parameter': {'epsilony': {'value': 1}}}

_LOGICS_BKBUFF = {  # Capital going through a buffer
    'differential': {'B': {'func': lambda Ir, B, fB: Ir - B * fB,
                           'initial': 0},
                     'K': {'func': lambda K, B, fB, delta: B * fB - delta * K}},
    'statevar': {'fB': {'func': lambda V, K, fb0: fb0 * V / K},
                 'dotV': {'func': lambda Y, Gamma, Cr, Xi, B, fB: Y * (1 - Gamma) - Cr - Xi * B * fB}, },
    'parameter': {'fB0': {'value': 100}, }}

_LOGICS_DELTAENDO = {
    'differential': {'Delta': {'func': lambda g, geff, fdelta: (g - geff) * fdelta}},
    # 'statevar': {'geff': {'func': lambda alpha,n, omega: 1.5*(alpha+n)*omega}},
    'parameter': {'geff': {'value': .045},
                  'fdelta': {'value': 1}}
}


def Increaseparam(paramname, value0, f):
    return {'statevar': {paramname: {'func': lambda ftime, time: value0 * np.exp(f * time)}, },
            'parameter': {'ftime': {'value': f}}}


_LOGICS_CHANGEPARAM = Increaseparam('Delta', .1, 0.01)

# _LOGICS = merge_model(_LOGICS, _LOGICS_COSTPUSH     )
# _LOGICS = merge_model(_LOGICS, _LOGICS_CES          )
# _LOGICS = merge_model(_LOGICS, _LOGICS_PHILLIPS     )
# _LOGICS = merge_model(_LOGICS, _LOGICS_PROGRESS     )
# _LOGICS = merge_model(_LOGICS, _LOGICS_INCREASING_RETURN)
# _LOGICS = merge_model(_LOGICS, _LOGICS_RECRUITMENT   )
# _LOGICS = merge_model(_LOGICS, _LOGICS_BKBUFF        )
_LOGICS = merge_model(_LOGICS, _LOGICS_DELTAENDO)
# _LOGICS = merge_model(_LOGICS, _LOGICS_CHANGEPARAM)
###############################################################################

Dimensions = {
    'matrix': [],
    'vector': []
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nprod'],
       'matrix': ['Nprod', 'Nprod']}
# _LOGICS=fill_dimensions(_LOGICS,Dimensions,DIM)

###############################################################################
_PRESETS = {
    'Goodwin': {
        'fields': {
            'D': 0,
            'Dh': 0,
            'p': 1,
            'a': 3,
            'N': 1,
            'V': 1,
            'w': .65,

            'Delta': 0,
            'Gamma': 0,
            'nu': 3,

            'Cpond': 1,
            'Ipond': 1,

            'alpha': 0.02,
            'n': 0.025,
            'delta': 0.05,
            'r': 0.03,

            'philinConst': -0.292,
            'philinSlope': 0.469,
        },
        'com': 'Simple monosectoral',
        'plots': {}
    },
}
