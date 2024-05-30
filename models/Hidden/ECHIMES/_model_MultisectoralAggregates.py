'''State variables, monosectoral, calculated on a productive multisectoral'''

from chimes.libraries import Funcs, importmodel, merge_model
import numpy as np
from chimes.libraries import Operators as O
_DESCRIPTION = ''' '''


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'statevar': {
        'pAGG': {'func': lambda p, basket: O.sprod(p, basket),
                 'definition': 'price deflator',
                 'units': '',
                 'symbol': r'$p_{\bigcirc}$'
                 },
        'GDPnomY': {'func': lambda p, Gamma, Y: O.sprod(p, Y - O.matmul(O.transpose(Gamma), Y)),
                    'com': 'calculated on Y',
                    'definition': 'nominal expected GDP',
                    'symbol': r'$Y^{NY}_{\bigcirc}$',
                    'units': '$.y^{-1}'
                    },
        'GDPnom2': {'func': lambda C, p, I, c, dotV: O.sprod(C, p) + O.ssum(I) + O.sprod(c, dotV),
                    'com': 'calculated on C+I+cdotV',
                    'definition': 'Inventory accountability nominal GDP',
                    'symbol': r'$Y^{NV}_{\bigcirc}$',
                    'units': '$.y^{-1}'
                    },
        'GDP': {'func': lambda GDPnomY, pAGG: GDPnomY / pAGG,
                'com': 'GDP on production deflated',
                'definition': 'deflated expected GDP',
                'symbol': r'$Y_{\bigcirc}$',
                'units': 'y^{-1}'
                },
        'CAGG': {'func': lambda p, C: O.sprod(p, C),
                 'com': 'Nominal consumption',
                 'symbol': r'$C_{\bigcirc}$',
                 'units': '$.y^{-1}',
                 },
        'IAGG': {'func': lambda I: O.ssum(I),
                 'com': 'nominal investment',
                 'symbol': r'$I_{\bigcirc}$',
                 'units': '$.y^{-1}',
                 },
        'VAGG': {'func': lambda V, c: O.sprod(V, c),
                 'com': 'nominal inventory',
                 'symbol': r'$V_{\bigcirc}$',
                 'units': '$.y^{-1}',
                 },
        'KAGGpass': {'func': lambda Xi, p, K: O.sprod(O.matmul(Xi, p), K),
                     'com': 'capital value on its creation',
                     'definition': 'nominal passive capital value',
                     'symbol': r'$K^{\Xi}_{\bigcirc}$',
                     'units': '$',
                     },
        'LAGG': {'func': lambda L: O.ssum(L),
                 'definition': 'total workers',
                 'symbol': r'$L_{\bigcirc}$',
                 'units': 'Humans'
                 },
        'aAGG': {'func': lambda GDP, LAGG: GDP / LAGG,
                 'definition': 'aggregated productivity',
                 'symbol': r'$a_{\bigcirc}$',
                 'units': 'Humans^{-1}.y^{-1}'
                 },
        'DAGG': {'func': lambda D: O.ssum(D),
                 'definition': 'sum of private debt',
                 'symbol': r'$D_{\bigcirc}$',
                 'units': '$'
                 },
        'omegaAGG': {'func': lambda w, L, z, GDPnomY: O.sprod(w * z, L) / GDPnomY,
                     'definition': 'aggregated wage share',
                     'symbol': r'$\omega_{\bigcirc}$',
                     'units': ''
                     },
        'uAGG': {'func': lambda u, K, b, nu: O.sprod(u, K * b / nu) / O.sprod(K, b / nu),
                 'definition': 'agregated use rate of capital',
                 'symbol': r'$u_{\bigcirc}$',
                 'units': ''
                 },
        'nuAGG': {'func': lambda KAGGpass, GDPnomY: KAGGpass / GDPnomY,
                  'com': 'On active capital',
                  'definition': 'agregated return on capital',
                  'symbol': r'$\nu_{\bigcirc}$',
                  'units': 'y'
                  },
        'deltaAGG': {'func': lambda delta, Xi, p, K, KAGGpass: O.sprod(delta, O.matmul(Xi, p) * K) / KAGGpass,
                     'definition': 'agregated capital degradation rate',
                     'symbol': r'$\delta_{\bigcirc}$',
                     'units': 'y^{-1}'
                     },
        'dAGG': {'func': lambda D, GDPnomY: O.ssum(D) / GDPnomY,
                 'com': 'on YGDP',
                 'definition': 'relative agregated debt',
                 'symbol': r'$d_{\bigcirc}$',
                 'units': 'y'
                 },
        'rdAGG': {'func': lambda r, D, GDPnomY: r * O.ssum(D) / GDPnomY,
                  'com': 'on YGDP',
                  'definition': 'relative private debt weight',
                  'symbol': r'$d_{\bigcirc}$',
                  'units': ''
                  },
        'gammaAGG': {'func': lambda p, Gamma, Y: O.sprod(p, O.matmul(O.transpose(Gamma), Y)) / O.sprod(p, Y),
                     'definition': 'agregated part of intermediary consumption',
                     'symbol': r'$\gamma_{\bigcirc}$',
                     'units': ''
                     },
        'XiAGG': {'func': lambda p, nu, delta, b, Xi, Y: O.sprod(p, O.matmul(O.transpose(Xi), Y) * nu * delta / b) / O.sprod(p, Y * nu * delta / b),
                  'definition': 'agregated relative size of capital',
                  'symbol': r'$\Xi_{\bigcirc}$',
                  'units': ''
                  },
        'xiAGG': {'func': lambda deltaAGG, nuAGG, XiAGG: deltaAGG * nuAGG * XiAGG,
                  'definition': 'aggregated relative weight of capital destruction',
                  'symbol': r'$\xi_{\bigcirc}$',
                  'units': ''
                  },
        'piAGG': {'func': lambda omegaAGG, gammaAGG, xiAGG, r, dAGG: 1 - omegaAGG - gammaAGG - xiAGG - r * dAGG,
                  'definition': 'aggregated relative profit',
                  'com': 'on expected',
                  'symbol': r'$\pi_{\bigcirc}$',
                  'units': ''
                  },
        'ROCAGG': {'func': lambda piAGG, nuAGG, XiAGG: piAGG / (nuAGG * XiAGG),
                   'definition': 'aggregated relative profit',
                   'com': 'on expected',
                   'symbol': r'$\pi_{\bigcirc}$',
                   'units': ''
                   },
        'cAGG': {'func': lambda omegaAGG, gammaAGG, xiAGG, pAGG: (omegaAGG + gammaAGG + xiAGG) * pAGG,
                 'definition': 'aggregated relative cost',
                 'symbol': r'$c_{\bigcirc}$',
                 'units': '$'
                 },
    },
}

_PRESETS = {}
