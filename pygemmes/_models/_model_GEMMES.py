# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a Goodwin-Keen model coupled with a 3-layer climate model, damages function and abattement of the emissions.

ABSTRACT OF THE ARTICLE : This paper presents a macroeconomic model that combines the economic impact of climate change with the pivotal role of private debt. Using a Stock-Flow Consistent approach based on the Lotka–Volterra logic, we couple its nonlinear monetary dynamics of underemployment and income distribution with abatement costs. A calibration of our model at the scale of the world economy enables us to simulate various planetary scenarios. Our findings are threefold: 1) the +2 °C target is already out of reach, absent negative emissions; 2) the longterm (resp. short-term) results of climate change on economic fundamentals may lead to severe economic consequences without the implementation (resp. in case of too rapid an application) of proactive climate policies. Global warming (resp. too fast transition) forces the private sector to leverage in order to compensate for output and capital losses (resp. to lower carbon emissions), thus endangering financial stability; 3) Implementing an adequate carbon price trajectory, as well as increasing the wage share, fostering employment, and reducing private debt make it easier to avoid unintended degrowth and to reach a +2.5 °C target.

TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np

# ----------------------------------------------------------------------------
# We simply do a few modifications on two previous models : we load them as a basis
from pygemmes._models import Funcs
from pygemmes._models._model_GK import _LOGICS as _LOGICS0
from pygemmes._models._model_Climate3Layers import _LOGICS as _LOGICSClimate
from copy import deepcopy

# The model is a start of a Goodwin-Keen model
_LOGICS = deepcopy(_LOGICS0)

# We add the climate model sector
for category, dic in _LOGICSClimate.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


_COUPLINGLOGICS = {
    'ode': {
        # COUPLING ODE
        'gsigmaEm': {
            'func': lambda itself=0, deltagsigmaEm=0: itself*deltagsigmaEm,
            'com': 'Evolution of emission rate growth rate',
        },
        'sigmaEm': {
            'func': lambda itself=0, gsigmaEm=0: itself*gsigmaEm,
            'com': 'Emission intensity dynamics',
        },

        # Prices
        'pbackstop': {
            'func': lambda itself=0, deltapbackstop=0: itself*deltapbackstop,
            'com': 'exogenous backstop price on exponential'
        },
        'pcarbon': {
            'func': lambda itself=0, deltapcarbon=0: itself*deltapcarbon,
            'com': 'Exogenous carbon price on exponential'
        },
    },

    'statevar': {
        # BEHAVIORAL PARAMETRIC FUNCTIONS (Because it's not the typical curves)
        'phillips': Funcs.Phillips.lin,
        'kappa': Funcs.Kappa.lin,
        'Sh': Funcs.Shareholding.lin,

        # MODIFIED PRODUCTION FUNCTION :
        'Y0': {
            'func': lambda K=0, nu=1: K / nu,
            'com': 'Leontiev optimized production function ',
        },
        'Y': {
            'func': lambda Y0=0, Dy=0, Abattement=0: Y0*(1-Dy)*(1-Abattement),
            'com': 'Useful production after damage and abattement',
        },
        'L': {
            'func': lambda Y0=0, a=1: Y0 / a,
            'com': 'Full instant employement defined around productivity',
        },
        'Pi': {
            'func': lambda GDP=0, w=0, L=0, r=0, D=0, p=0, K=0, deltaD=0: GDP - w * L - r * D - p*(K*deltaD),
            'com': 'Profit for production-Salary-debt func',
        },
        'c': {
            'func': lambda Abattement=0, Dy=0, w=0, a=1: (w/a)/((1-Abattement)*(1-Dy)),
            'com': 'Unitary cost taking loss of production'
        },

        # EMISSION PART
        'emissionreductionrate': {
            'func': lambda pcarbon=0, pbackstop=1, convexitycost=1: np.minimum((pcarbon/pbackstop)**(1/(convexitycost)), 1),
            'com': 'choice of emission reduction rate weird',
        },
        'Abattement': {
            'func': lambda sigmaEm=0, pbackstop=0, emissionreductionrate=0, convexitycost=1: sigmaEm*pbackstop*(emissionreductionrate**convexitycost)/convexitycost,
            'com': 'emission reduction rate Abattement'
        },
        'Eind': {
            'func': lambda Y0=0, sigmaEm=0, n=0: Y0*sigmaEm*(1-n),
            'com': 'Emission of the industry',
        },
        'Emission': {
            'func': lambda Eind=0: Eind,
            'com': 'Only industrial emission for the moment',
        },

        # COUPLING STATE VARIABLES
        'Damage': {
            'func': lambda T=0, pi1=0, pi2=0, pi3=0, zeta3=1: 1 - 1/(1+pi1*T+pi2*T**2+pi3*T**zeta3),
            'com': 'Agregated damage function',
        },
        'DK': {
            'func': lambda Damage=0, fk=0: fk*Damage,
            'com': "intermediary damage calculation capital",
        },
        'Dy': {
            'func': lambda Damage=0, DK=0: 1 - (1-Damage)/(1-DK),
            'com': 'damage on production',
        },
    },
}

# We add the coupling
for category, dic in _COUPLINGLOGICS.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'Emission0': 38,
        'deltaEmission': 0.01,
        'F2CO2': 3.681,
        'CO2AT': 851,
        'CO2UP': 460,
        'CO2LO': 1740,
        'CUP': 460,
        'CAT': 588,
        'CLO': 1720,
        'phi12': 0.024,
        'phi23': 0.001,
        'Capacity': 1/0.098,
        'Capacity0': 3.52,
        'rhoAtmo': 3.681/3.1,
        'gammaAtmo': 0.0176,
        'T': 1,
        'T0': 0,
        'gsigmaEm': -0.0152,
        'pbackstop': 547,
        'p': 1,
        'lambda': .675,
        'd': 1.53,
        'philinConst': -0.292,
        'philinSlope': 0.469,
        'kappalinSlope': 0.0318,
        'kappalinConst': 0.575,
        'divlinSlope': 0.473,
        'divlinconst': 0.138,
        'pi1': 0,
        'pi2':  0.00236,
        'pi3':  0.00000507,
        'zeta3':  6.754,
        'fk': 1/3
    },
    'com': ' Default run'},
}
