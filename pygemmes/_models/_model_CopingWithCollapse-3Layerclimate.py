# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a Goodwin-Keen model coupled with a 3-layer climate model, damages function and abattement of the emissions.

ABSTRACT OF THE ARTICLE : This paper presents a macroeconomic model that combines the economic impact of climate change with the pivotal role of private debt. Using a Stock-Flow Consistent approach based on the Lotka–Volterra logic, we couple its nonlinear monetary dynamics of underemployment and income distribution with abatement costs. A calibration of our model at the scale of the world economy enables us to simulate various planetary scenarios. Our findings are threefold: 1) the +2 °C target is already out of reach, absent negative emissions; 2) the longterm (resp. short-term) results of climate change on economic fundamentals may lead to severe economic consequences without the implementation (resp. in case of too rapid an application) of proactive climate policies. Global warming (resp. too fast transition) forces the private sector to leverage in order to compensate for output and capital losses (resp. to lower carbon emissions), thus endangering financial stability; 3) Implementing an adequate carbon price trajectory, as well as increasing the wage share, fostering employment, and reducing private debt make it easier to avoid unintended degrowth and to reach a +2.5 °C target.


ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np
from pygemmes._models import Funcs

# ---------------------------
# user-defined function order (optional)
_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # ATMOSPHERE ODE
        'CO2AT': Funcs.Atmosphere.Three_Layers.CO2AT,
        'CO2UP': Funcs.Atmosphere.Three_Layers.CO2UP,
        'CO2LO': Funcs.Atmosphere.Three_Layers.CO2LO,
        'T': Funcs.Atmosphere.ThreeLayers.T,
        'T0': Funcs.Atmosphere.ThreeLayers.T0,

        'pseudot': {
            'func': lambda T=0: 1,
            'com': 'false time because practical',
            'initial': 0,
        },

        # ECONOMIC ODE



    },
    'statevar': {
        'F': Funcs.Atmosphere.F,

        'Emission': {
            'func': lambda Emission0=0, deltaEmission=0, pseudot=0: Emission0*np.exp(-pseudot*deltaEmission),
            'com': 'CO2 Emission rate ',
        },
    },
}


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
    },
    'com': ' Default run'},
}
