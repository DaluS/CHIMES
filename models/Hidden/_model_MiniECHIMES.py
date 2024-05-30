"""Minimal Core for ECHIMES"""

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np
from chimes.libraries import Operators as O
_DESCRIPTION = """
* **Article :** https://www.overleaf.com/read/thbdnhbtrbfx
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
* **Date    :** 14/09/23

## Description
Minimal version of the model
"""


_LOGICS = {
    'size': {'Nprod': {'list': ['MONO']}},
    'differential': {
        'N': {'func': lambda N, n: N * n},
        'a': {'func': lambda a, alpha: a * alpha},
        'w': {'func': lambda w, Phillips, i, Phii: w * (Phillips + i * Phii)},
        'p': {'func': lambda i, p: i * p},
        'D': {'func': lambda r, D, w, L, p, C, Delta, Pi, Tn: r * D + w * L + Delta * Pi - p * C - Tn},
        'Dh': {'func': lambda r, D, w, L, p, C, Delta, Pi: -O.sprod(r * D + w * L + Delta * Pi - p * C)},
        'V': {'func': lambda Y, Gamma, Xi, I, C: Y - Gamma * Y - Xi * I - C},
        'K': {'func': lambda I, delta, K: I - delta * K},
    },
    'statevar': {
        'dKn': {'func': lambda K, delta, Xi, p: K * delta * O.matmul(Xi, p),
                'symbol': r'$(\delta K)^n'},
        'Y': {'func': lambda K, nu, u: u * K / nu},
        'L': {'func': lambda K, a, u: u * K / a},
        'Pi': {'func': lambda p, Y, Gamma, dKn: p * Y - Y * O.matmul(Gamma, p) - dKn},
        'In': {'func': lambda Pi, dKn, Delta, kappaI: dKn + Pi * kappaI * (1 - Delta)},
        'I': {'func': lambda In, Xi, p: In / O.matmul(Xi, p)},
        'C': {'func': lambda w, L, r, D, Pi, Delta, kappaC, p: kappaC * O.ssum(w * L + r * D + Pi * Delta) / p},
        'Tn': {'func': lambda Gamma, Y, Xi, I: Gamma * Y + Xi * I,
               'symbol': r'$\mathcal{T}^n$'},
        'Phillips': {'func': lambda Phi0, Phi1, L, N, : Phi0 + Phi1 / (1 - O.ssum(L) / N)**2}
    },
    'parameter': {
        'i': {'value': 1},
        'kappaI': {'value': 1,
                   'symbol': r'$\kappa^I$'},
        'kappaC': {'value': 1,
                   'symbol': r'$\kappa^C$'},
        'Phi0': {'value': -0.1010101,
                 'symbol': r'$\Phi^0$'},
        'Phi1': {'value': 0.0010101,
                 'symbol': r'$\Phi^1$'},
        'Phii': {'value': 0.0010101,
                 'symbol': r'$\Phi^i$'},
        'Gamma': {'symbol': r'$\Gamma$'},
        'Delta': {'symbol': r'$\Delta$'},
        'Xi': {'symbol': r'$\Xi$'}
    }
}

_SUPPLEMENTS = {}
_PRESETS = {}
