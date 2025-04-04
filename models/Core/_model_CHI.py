"""Human-Capital Instability: Causal core"""
import numpy as np
from chimes.libraries import Funcs, importmodel, merge_model
from chimes.libraries import Operators as O

_DESCRIPTION = """
* **Article :** https://www.overleaf.com/read/bczdyhfqrdgh
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

Model as presented in "H-C instability".

Two sector (production, consolidated households), with physical (V,K) and nominal (D,Dh) stock-flow (Y,C,I) consistency.

Behavior:
* consumption proportional to sum of income sources
* investment proportional to post-dividends profits
* Wage through employment Philipps curve

**TODO:**
* Presets, presets, presets
* Add endogenisation
"""


######################################################################

employment0 = 0.88277812
omega0 = 0.4969697
pieq = 0.15151515


__KEENLIKE = True
__KAPPACDrive = False
_LOGICS = {
    'differential': {
        'K': {'func': lambda K, I, delta: I - delta * K},
        'V': {'func': lambda Y, Gamma, C, Xi, I: Y - Gamma * Y - C - Xi * I},
        'D': {'func': lambda r, D, w, L, Delta, Pi, C, p: r * D + w * L + Delta * Pi - C * p,
              'initial': 0},
        'Dh': {'func': lambda r, D, w, L, Delta, Pi, C, p: -r * D - w * L - Delta * Pi + C * p},
        'p': {'func': lambda p, inflation: p * inflation},
        'a': {'func': lambda a, alpha: a * alpha,
              'initial': 3},
        'N': {'func': lambda N, n: N * n},
        'w': {'func': lambda w, phillips: w * phillips},
    },

    'statevar': {
        'I': {'func': lambda In, Xi, p: In / (Xi * p)},
        'C': {'func': lambda Cn, p: Cn / p},
        'Pi': {'func': lambda p, Y, Gamma, w, L, delta, Xi, K, r, D: p * Y * (1 - Gamma) - w * L - p * delta * Xi * K - r * D},
        'W': {'func': lambda w, L, r, D, Delta, Pi: w * L + r * D + Delta * Pi},
        'Y': {'func': lambda A, K, a, L, V, Gamma: A * K},  # np.minimum((K,a*L,V*A*Gamma**(-1)))},
        'Yc': {'func': lambda A, K: A * K},
        'Lc': {'func': lambda K, a: K / a},
        'Leff': {'func': lambda L, Lc: L / Lc},
        'L': {'func': lambda Lc: Lc},

        'Cn': {'func': lambda kappaC, W: kappaC * W},
        'In': {'func': lambda p, delta, Xi, K, Delta, kappaI, Pi: p * delta * Xi * K + kappaI * (1 - Delta) * Pi},

        'employment': {'func': lambda L, N: L / N},
        # 'phillips'   :{'func': lambda Phi0,Phi1,phialpha,phii,flambda,alpha,inflation,pi,zpi:Phi0+((pi/pieq)**(zpi))*Phi1*flambda+phii*inflation+phialpha*alpha},
        'phillips': {'func': lambda Phi0, Phi1, flambda: Phi0 + Phi1 * flambda},
        'flambda': {'func': lambda employment: 1 / (1 - employment)**2},

        'nu': {'func': lambda K, Y: K / Y},
        'omega': {'func': lambda w, L, p, Y: w * L / (p * Y)},
        'd': {'func': lambda D, p, Y: D / (p * Y)},
        'pi': {'func': lambda Pi, p, Y: Pi / (p * Y)},
        'productivity': {'func': lambda Y, L: Y / L},
        'g': {'func': lambda I, delta, K: I / K - delta},
        'ROC': {'func': lambda Pi, K, Xi, p: Pi / (p * Xi * K)},
        'Solvability': {'func': lambda D, K, Xi, p: 1 - D / (K * Xi * p)},
        'c': {'func': lambda p, omega, Gamma, nu, delta, Xi: p * (omega + Gamma + nu * delta * Xi)},
        'mu': {'func': lambda p, c: p / c},
        'GDPn': {'func': lambda p, Y, Gamma: p * Y * (1 - Gamma)},
        'GDP': {'func': lambda Y, Gamma: Y * (1 - Gamma)},
        # 'omegaeq': {'func': lambda Gamma,nu,delta,Xi,alpha,n,Delta: 1-Gamma-nu*Xi*delta-nu*Xi*(alpha+n)/(1-Delta),
        #          'symbol':r'$\omega_{eq}$'},
    },

    'parameter': {
        'alpha': {'value': 0.025},
        'n': {'value': 0.02},
        'r': {'value': 0.03},
        'delta': {'value': 0.05},
        'Delta': {'value': 0.1},
        'Phi0': {'value': -0.1010101},
        'Phi1': {'value': 0.0010101},
        'phialpha': {'value': 0.5},
        'phii': {'value': 0.5},
        'inflation': {'value': 0.03},
        'A': {'value': 0.33},
        'Gamma': {'value': 0.2},
        'Xi': {'value': 1},
        'kappaC': {'value': 1},
        'kappaI': {'value': 1},


    },
    'size': {},
}


# ### FORCE THE SYSTEM TO ENDOGENIZE ####################################
if (__KEENLIKE and __KAPPACDrive):
    raise Exception('CHI cannot Be Keenlike and KappacDrive at the same time !')
if __KEENLIKE:
    del _LOGICS['differential']['V']
    del _LOGICS['parameter']['kappaC']
    _LOGICS['statevar']['C'] = {'func': lambda Y, Gamma, I: Y * (1 - Gamma) - I,
                                'com': "KEENLINKE OVERRIDE"}
    _LOGICS['statevar']['Cn'] = {'func': lambda C, p: C * p,
                                 'com': "KEENLINKE OVERRIDE"}

    _LOGICS['statevar']['kappaC'] = {'func': lambda W, Cn: Cn / W,
                                     'com': "KEENLINKE OVERRIDE"}
if __KAPPACDrive:
    del _LOGICS['differential']['V']
    del _LOGICS['parameter']['kappaI']
    _LOGICS['statevar']['I'] = {'func': lambda Y, Gamma, C: Y * (1 - Gamma) - C,
                                'com': "KappC OVERRIDE"}
    _LOGICS['statevar']['In'] = {'func': lambda I, p: I * p,
                                 'com': "KappC OVERRIDE"}
    _LOGICS['statevar']['kappaI'] = {'func': lambda p, delta, Xi, K, Delta, In, Pi: (In - p * delta * Xi * K) / ((1 - Delta) * Pi),
                                     'com': "KappC OVERRIDE"}


#########################################################################


###########################################
def equilibriumpost(hub, ftype='divergent'):
    '''Calculate the equilibrium properties for a diverging phillips curve'''
    R = hub.get_dfields()
    d = {v: R[v]['value'] for v in R.keys()}

    def fm1(x):
        return 1 - np.sqrt(x)

    def fprime(x):
        return 2 / (1 - x)**3

    d['nu'] = d['A']**(-1)

    equilibrium = {'omega': 1 - d['Gamma'] - d['nu'] * d['Xi'] * d['delta'] - d['nu'] * d['Xi'] * (d['alpha'] + d['n']) / (1 - d['Delta']),
                   'lambda': fm1(-d['Phi1'] / (d['Phi0'] + d['alpha'] * (1 - d['phialpha']) + d['inflation'] * (1 - d['phii']))),
                   'growth': d['alpha'] + d['n']}
    equilibrium['pi'] = 1 - d['Gamma'] - d['nu'] * d['Xi'] * d['delta'] - equilibrium['omega']
    equilibrium['pulsation'] = np.sqrt(d['Phi1'] * equilibrium['lambda'] * equilibrium['omega'] * fprime(equilibrium['lambda']) * (1 - d['Delta']) / (d['nu'] * d['Xi'] * d['delta']))
    return equilibrium


_SUPPLEMENTS = {'get_equilibrium': equilibriumpost}


###########################################
_PRESETS = {
    'default': {
        'fields': {
            'K': 2.7,
            'a': 3,
            'p': 1,
            'D': 0,
            'Dh': 0,
            'N': 1,
            'w': .55,
            'alpha': 0.025,
            'n': 0.02,
            'r': 0.03,
            'delta': 0.05,
            'Delta': 0.1,
            'Phi0': -0.1010101,
            'Phi1': 0.0010101,
            'phialpha': 0.5,
            'phii': 0.5,
            'inflation': 0.03,
            'A': 0.33,
            'Gamma': 0.2,
            'Xi': 1,
            'kappaC': 1,
            'kappaI': 1,
            'D': 0,
        },
        'com': 'Goodwin-like behavior',
        'plots': {'XYZ': [{'x': 'employment',
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
}
