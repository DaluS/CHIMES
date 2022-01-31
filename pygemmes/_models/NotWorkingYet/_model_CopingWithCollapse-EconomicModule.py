# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a Goodwin-Keen model coupled with a 3-layer climate model, damages function and abattement of the emissions.

ABSTRACT OF THE ARTICLE : This paper presents a macroeconomic model that combines the economic impact of climate change with the pivotal role of private debt. Using a Stock-Flow Consistent approach based on the Lotka–Volterra logic, we couple its nonlinear monetary dynamics of underemployment and income distribution with abatement costs. A calibration of our model at the scale of the world economy enables us to simulate various planetary scenarios. Our findings are threefold: 1) the +2 °C target is already out of reach, absent negative emissions; 2) the longterm (resp. short-term) results of climate change on economic fundamentals may lead to severe economic consequences without the implementation (resp. in case of too rapid an application) of proactive climate policies. Global warming (resp. too fast transition) forces the private sector to leverage in order to compensate for output and capital losses (resp. to lower carbon emissions), thus endangering financial stability; 3) Implementing an adequate carbon price trajectory, as well as increasing the wage share, fostering employment, and reducing private debt make it easier to avoid unintended degrowth and to reach a +2.5 °C target.

Financial impacts of climate change mitigation
policies and their macroeconomic implications: a
stock-flow consistent approach

TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)
_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # ECONOMIC ODE
        'a': {
            'func': lambda alpha=0, itself=0: alpha * itself,
            'com': 'Exogenous technical progress as an exponential',
        },
        'N': {
            'func': lambda n=0, itself=0, Nmax=1: n * itself * (1-itself/Nmax),
            'com': 'Logistic population curve',
        },
        'K': {
            'func': lambda I=0, itself=0, delta=0, p=1: I/p - itself*delta,
            'com': 'Capital evolution from investment and depreciation',
        },
        'D': {
            'func': lambda I=0, Pi=0, Sh=0: I - Pi + Sh,
            'com': 'Debt as Investment-Profit difference and shareholding',
        },
        'w': {
            'func': lambda phillips=0, itself=0, gammai=0, inflation=0: itself * (phillips + gammai*inflation),
            'com': 'salary evolution through negociation + inflation',
        },
        'p': {
            'func': lambda itself=0, inflation=0: itself * inflation,
            'com': 'price defined by inflation',
        },
    },





    'statevar': {
        # ECONOMIC STATE VARIABLES
        'Y0': {
            'func': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ',
        },
        'Y': {
            'func': lambda Y0=0: Y0,
            'com': 'Useful production after damage and abattement',
        },
        'L': {
            'func': lambda Y0=0, a=1: Y0 / a,
            'com': 'Full instant employement defined around productivity',
        },
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0, p=0, K=0, deltaD=0: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func',
        },
        'GDP': {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'Output with selling price ',
        },
        'inflation': {
            'func': lambda mu=0, eta=0, c=0, p=1: eta*(mu*c/p-1),
            'com': 'markup dynamics',
        },
        'c': {
            'func': lambda omega=0, p=1: omega*p,
            'com': 'Unitary cost '
        },
        'lambda': {
            'func': lambda L=0, N=1: L / N,
            'com': 'statevar by ratio',
        },
        'omega': {
            'func': lambda w=0, L=0, Y=1, p=1: (w * L) / (Y*p),
            'com': 'wage share by ratio as statevar',
        },
        'I': {
            'func': lambda GDP=0, kappa=0: GDP * kappa,
            'com': 'from kappa function',
        },
        'd': {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'ratio as statevar',
        },
        'pi': {
            'func': lambda Pi=0, GDP=1: Pi/GDP,
            'com': 'ratio as statevar',
        },
        'g': {
            'func': lambda I=0, p=1, K=1, delta=0: I/(K*p)-delta,
            'com': 'manual check'},

        # BEHAVIORAL PARAMETRIC FUNCTIONS
        'phillips': {
            'func': lambda philinConst=0, philinSlope=0, lamb=0: philinConst + philinSlope * lamb,
            'com': 'Linear Philips curve',
        },
        # 'kappa': {
        #    'func': lambda k0=0, k1=0, k2=0, pi=0: k0 + k1 * np.exp(k2 * pi),
        #    'com': 'Exponential kappa curve', },
        'kappa': {
            'func': lambda kappalinConst=0, kappalinSlope=0, pi=0, kappalinMin=0, kappalinMax=0: np.clip(kappalinConst + kappalinConst * pi, kappalinMin, kappalinMax),
            'com': 'Relative GDP investment through relative profit',
        },
        'Sh': {
            'func': lambda divlinSlope=0, divlinconst=0, pi=0, GDP=0, divlinMin=0, divlinMax=0: np.clip(GDP*(divlinSlope*pi+divlinconst), divlinMin, divlinMax),
            'com': 'Affine shareholding dividends dependency'
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

lamb = .675
Y = 59.74
d = 1.53
omega = .578
nu = 2.7
p = 1
N = 4.83
nu = 2.7

_PRESETS = {}


_PRESETS = {
    'CopingWithCollapse2016': {
        'fields': {
            'K': Y*nu,
            'D': d*Y*p,
            'p': p,
            'N': N,
            'w': Y*omega*p/(lamb*N),
            'a': Y/(N*lamb),
            'eta': 0.5,
            'mu': 1.3,
            'nu': nu,
            'delta': .04,
            'alpha': .02,
            'r': .03,
            'n': .0305,
            'Tmax': 20
        },
        'com': 'values from copingwithcollapse'
    },
    'DebtAndDamages2018': {
        'fields': {
            'K': Y*nu,
            'D': d*Y*p,
            'p': p,
            'N': N,
            'w': Y*omega*p/(lamb*N),
            'a': Y/(N*lamb),
            'divlinSlope': .553,
            'divlinconst': -.078,
            'divlinMin': 0,
            'divlinMax': 3,
            'Nmax': 7.056,
            'r': .02,
            'n': .0305,
            'nu': 2.7,
            'delta': .04,
            'eta': 0.192,
            'mu': 1.875,
            'kappalinSlope': 0.575,
            'kappalinConst': 0.0318,
            'time': 2015,
        },
        'com': 'Values from debt and damages'
    },
    'FinancialImpact2019': {
        'fields': {
            'K': Y*nu,
            'D': d*Y*p,
            'p': p,
            'N': N,
            'w': Y*omega*p/(lamb*N),
            'a': Y/(N*lamb),
            'divlinSlope': .553,
            'divlinconst': -.078,
            'divlinMin': 0,
            'divlinMax': 3,
            'Nmax': 7.056,
            'r': .02,
            'n': .0305,
            'nu': 2.7,
            'delta': .04,
            'eta': 0.192,
            'mu': 1.875,
            'kappalinSlope': 0.575,
            'kappalinConst': 0.0318,
            'time': 2015,
        },
        'com': 'Values from the article "Financial impacts of climate change mitigation policies and their macroeconomic implications: a stock-flow consistent approach"'
    },
}
