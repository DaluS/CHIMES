# -*- coding: utf-8 -*-
"""
ABSTRACT : This is the model Coping from Bovari 2018.

TYPICAL BEHAVIOR :
LINKTOARTICLE : Coping with Collapse: A Stock-Flow Consistent
Monetary Macrodynamics of Glabal Warming.

@author: Camille GUITTONNEAU, Hugo A. MARTIN
"""

"""
TODO:
 - regler l'inflation pour qu'elle soit comme Coping 2.
 - parametrer tout le bordel
 - verefier unite
"""

# imports --------------------------------------------------------------
# packages

# models

# globals --------------------------------------------------------------
# constants and statevar
from pygemmes._models import Funcs
from copy import deepcopy
import numpy as np
from pygemmes._models._model_GK import _LOGICS as _LOGICSGK
from pygemmes._models._model_GK import _PRESETS as _PRESETSGK
from pygemmes._models._model_Climate_3Layers import _LOGICS as _LOGICSCLIM
from pygemmes._models._model_Climate_3Layers import  _PRESETS as _PRESETSCLIM
NU = 2.7
CONVEXITYCOST = 2.6
emissionreductionrate_INI = 0.03
Y_INI = 59.74
lambda_INI = 0.675
omega_INI = 0.578
Dy_INI = 0

# initial conditions
CO2AT_INI = 851.
CO2UP_INI = 460.
CO2LO_INI = 1740.
d_INI = 1.53
Eind_INI = 51.79
Eland_INI = 2.6
gsigmaEm_INI = -0.0152
p_INI = 1.
pbackstop_INI = 547.22
pcarbon_INI = 3.5
N_INI = 4.83
T_INI = 1.07
T0_INI = 0.0068

# second order initial conditions
L_INI = lambda_INI * N_INI
Abattement_INI = 1 / (1 + ((1 - emissionreductionrate_INI) * Y_INI * CONVEXITYCOST) /
                      (0.001 * Eind_INI * pbackstop_INI * emissionreductionrate_INI ** CONVEXITYCOST * (1 - Dy_INI)))
Y0_INI = Y_INI / (1 - Dy_INI) / (1 - Abattement_INI)
sigmaEm_INI = Eind_INI / (1 - emissionreductionrate_INI) / Y0_INI
Y_INI2 = (1.-Abattement_INI) * (1.-Dy_INI) * Y0_INI

# local functions ------------------------------------------------------

# model ----------------------------------------------------------------
_LOGICS = deepcopy(_LOGICSGK)
# the main logics is from Goodwin-Keen
for category, dic in _LOGICSGK.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# add the logics of climate module to the model logics
for category, dic in _LOGICSCLIM.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# remove unused variables and params
del _LOGICS['ode']['pseudot']
del _LOGICS['statevar']['Ir']

# add plenty of stuff
_LOGICS_COPING2018 = {

    'ode': {

        'N': Funcs.Population.logistic,
        'w': Funcs.Phillips.salaryfromPhillipsNoInflation,

        # production group
        'K': {
            'func': lambda itself=0., deltad=0., I=0.: I - deltad*itself,
            'initial': NU * Y0_INI,
            'com': 'Evolution of capital in Coping 2018',
        },

        'D': {
            'func': lambda Sh=0., K=0., Pi=0., deltad=0., p=0., I=0.: p*I - Pi - p*deltad*K + Sh,
            'initial': d_INI * p_INI * Y_INI,
            'com': 'Evolution of private debt',
        },

        # carbon price group
        'pbackstop': {
            'func': lambda itself=0., deltapbackstop=0.: itself*deltapbackstop,
            'initial': pbackstop_INI,
            'com': 'Evolution of the backstop technology price',
        },

        'pcarbon_pot': {
            'func': lambda apc=0., bpc=0., itself=0., time=1.: itself*(apc + bpc/(time+1)),
            'initial': pcarbon_INI,
            'com': 'Potential carbon price',
        },

        'sigmaEm': {
            'func': lambda itself=0., gsigmaEm=0.: itself*gsigmaEm,
            'initial': sigmaEm_INI,
            'com': 'Evolution of the sigma emission intensity of industries',
        },

        'gsigmaEm': {
            'func': lambda itself=0., deltagsigmaEm=0.: itself*deltagsigmaEm,
            'initial': gsigmaEm_INI,
            'com': 'Evolution of the gsigma emission intensity of industries',
        },

        # Emissions group
        'Eland': {
            'func': lambda itself=0., deltaEland=0.: deltaEland*itself,
            'initial': Eland_INI,
            'com': 'Evolution of land use emissions',
        },

    },

    'statevar': {
        'phillips': Funcs.Phillips.lin,
        'kappa': Funcs.Kappa.lin,
        'Sh': Funcs.Shareholding.lin,

        # damage group
        'Damage': Funcs.Damage.general,

        'DK': {
            'func': lambda Damage=0., fk=0.: fk*Damage,
            'com': 'classic DY variable'
        },

        'Dy': {
            'func': lambda DK=0., Damage=0.: 1. - (1.-Damage)/(1.-DK),
            'com': 'classic DY variable'
        },

        'deltad': {
            'func': lambda delta=0., DK=0.: delta + DK,
            'com': 'Depreciation of Capital plus climate damage on capital',
        },

        # emission group
        'Emission': {
            'func': lambda Eind=0., Eland=0.: Eind + Eland,
            'com': 'Endogenous total emissions',
        },

        'Eind': {
            'func': lambda emissionreductionrate=0., sigmaEm=0., Y0=0.: (1. - emissionreductionrate)*sigmaEm*Y0,
            'com': 'Endogenous industrial emissions',
        },

        # production group
        'Y': {
            'func': lambda Abattement=0., Dy=0., Y0=0.: (1.-Abattement)*(1.-Dy)*Y0,
            'com': 'Yearly Production with climate damage and abatment',
        },

        'Y0': {
            'func': lambda K=0., nu=1.: K / nu,
            'com': 'Yearly Production without climate damage and abatment',
        },

        'L': {
            'func': lambda Nmax=0., Y0=0., a=1.: np.minimum(Nmax, Y0 / a),
            'com': '',
        },

        'I': {
            'func': lambda kappa=0, Y=0: kappa * Y,
            'com': 'investment function',
        },

        'Pi': {
            'func': lambda GDP=0., w=0., L=0., r=0., D=0., p=0., carbontax=0., deltad=0., K=0.: GDP - w*L - r*D - p*carbontax - p*deltad*K,
            'com': 'Profit',
        },

        'g': {
            'func': lambda I=0., K=1., deltad=0.: (I - deltad*K)/K,
            'com': 'Relative growth of GDP',
        },

        # carbon price group
        'emissionreductionrate': {
            'func': lambda pbackstop=1., convexitycost=2.6, pcarbon=0: np.minimum(1., (pcarbon/pbackstop)**(1./(convexitycost - 1.))),
            'com': 'Yearly Production without climate damage and abatment',
        },

        'pcarbon': {
            'func': lambda pcarbon_pot=0., pbackstop=0.: np.minimum(pcarbon_pot, pbackstop),
            'com': 'Real carbon price',
        },

        'Abattement': {
            'func': lambda sigmaEm=0., pbackstop=0., emissionreductionrate=0., convexitycost=1: 0.001*sigmaEm*pbackstop*(emissionreductionrate**convexitycost)/convexitycost,
            'com': 'Definition of abatment ratio',
        },

        'carbontax': {
            'func': lambda Eind=0., pcarbon=0., conv10to15=0.: pcarbon*Eind*conv10to15,
            'com': 'Carbon tax paid by private sector',
        },

        'c': {
            'func': lambda p=0., omega=0.: p * omega,
            'com': '',
        }
    },
}


# add Coping logics
for category, dic in _LOGICS_COPING2018.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# initial conditions
_LOGICS['ode']['N']['initial'] = N_INI
_LOGICS['ode']['w']['initial'] = omega_INI * p_INI * Y_INI / L_INI
_LOGICS['ode']['CO2AT']['initial'] = CO2AT_INI
_LOGICS['ode']['CO2UP']['initial'] = CO2UP_INI
_LOGICS['ode']['CO2LO']['initial'] = CO2LO_INI
_LOGICS['ode']['T']['initial'] = T_INI
_LOGICS['ode']['T0']['initial'] = T0_INI
_LOGICS['ode']['p']['initial'] = p_INI
_LOGICS['ode']['a']['initial'] = Y0_INI / L_INI


# presets
_PRESETS = {'coping': {
    'fields': {
        # parameters
        'n': 0.0305,
        'Nmax': 7.056,
        'philinConst': -0.292,
        'philinSlope': 0.469,
        'alpha': 0.02,
        'delta': 0.04,
        'nu': NU,
        'mu': 1.875,
        'divlinconst': 0.138,
        'divlinSlope': 0.473,
        'divlinMin': 0,
        'divlinMax': 0.3,
        'kappalinSlope': 0.575,
        'kappalinConst': 0.0318,
        'kappalinMin': 0,
        'kappalinMax': 0.3,
        # see for kappanlinMin and kappalinMax
        'eta': 0.192,
        'convexitycost': CONVEXITYCOST,
        'deltapbackstop': -0.005,
        'conv10to15': 1.160723971/1000,
        'pi1': 0,
        'pi2':  0.00236,
        'pi3':  0.0000819,
        'zeta3':  6.754,
        'fk': 1./3,
        'deltaEland': -0.022,
        'deltagsigmaEm': -0.001,
        'gammaAtmo': 0.0176,
        'rhoAtmo': 3.681/3.1,  # hence climate sensitivity not in the model (3.1)
        'F2CO2': 3.681,
        'CAT': 588,
        'CUP': 360,
        'CLO': 1720,
        'phi12': 0.024,
        'phi23': 0.001,
        'Capacity': 1./0.098,
        'Capacity0': 3.52,
        'r': 0.01,
        'apc': 0.05,
        'bpc': 0.5,

    },
    'com': ' Default run',
    'plots': {
        'timetrace': [{}],
        'nyaxis': [{
            'x': 'time',
            'y': [['lambda', 'omega'],
                  ['d', 'g'],
                  ['kappa', 'pi'],
                  ],
            'idx':0,
            'title':'',
            'lw':1},
            {
            'x': 'time',
            'y': [['CO2AT', 'CO2UP', 'CO2LO'],
                  ['T', 'T0'],
                  ['F'],
                  ['Emission', 'Eind', 'Eland']],
            'idx':0,
            'title':'All climatic variables',
            'lw':1
        },
            {
            'x': 'time',
            'y': [['L', 'N'],
                  ['Y', 'Y0', 'Pi', 'I'],
                  ['c', 'p'],
                  ['pcarbon', 'pbackstop']],
            'idx':0,
            'title':'Twin variables',
            'lw':1
        }
        ],
        'phasespace': [],
        '3D': [{'x': 'lambda',
                'y': 'omega',
                'z': 'd',
                'cinf': 'pi',
                'cmap': 'jet',
                'index': 0,
                'title': ''
                }
               ],
        'byunits': [],
    },
},
}
