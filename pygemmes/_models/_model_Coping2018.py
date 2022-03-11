# -*- coding: utf-8 -*-
"""
ABSTRACT : This is the model Coping from Bovari 2018: Coping with Collapse: A Stock-Flow Consistent Monetary Macrodynamics of Glabal Warming
TYPICAL BEHAVIOR : BAU and TRANSITION converges toward the good equilibrium, BAU_DAM toward the bad.
LINKTOARTICLE : DOI: 10.1016/j.ecolecon.2018.01.034
@author: Camille GUITTONNEAU, Hugo A. MARTIN, Paul VALCKE
"""
from pygemmes._models import Funcs
from copy import deepcopy
import numpy as np
from pygemmes._models._model_GK import _LOGICS as _LOGICSGK
from pygemmes._models._model_Climate_3Layers import _LOGICS as _LOGICSCLIM

###############################################################################
"""
TODO:
 - regler l'inflation pour qu'elle soit comme Coping 2. ACTUELLEMENT PHILIPS SANS INFLATION
 - verefier unite
"""
###############################################################################
Tini = 2015

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
    # ode
    'ode': {
        # from _def_functions
        'N': Funcs.Population.logistic,
        'w': Funcs.Phillips.salaryfromPhillipsNoInflation,
        # production group
        'K': {
            'func': lambda itself=0., deltad=0., I=0.: I - deltad*itself,
            'com': 'Evolution def. in Eq. (7) in Bovari2018',
            'definition': 'Monetary Capital',
        },
        'D': {
            'func': lambda Sh=0., K=0., Pi=0., deltad=0., p=0., I=0.: p*I - Pi - p*deltad*K + Sh,
            'com': 'Evolution def. in Eq. (8) in Bovari2018',
            'definition': 'Private debt in current $',
        },
        # carbon price group
        'pbackstop': {
            'func': lambda itself=0., deltapbackstop=0.: itself*deltapbackstop,
            'com': 'Exogenous Evolution is implicitely given in Bovari2018',
        },
        'pcarbon_pot': {
            'func': lambda apc=0., bpc=0., itself=0., time=1., Tini=0.: itself*(apc + bpc/(time - (Tini - 1))),
            'com': 'Evolution of carbon price Eq. (38) in Bovari2018',
        },
        'sigmaEm': {
            'func': lambda itself=0., gsigmaEm=0.: itself*gsigmaEm,
            'com': 'Evolution of sigma in Eq. (17) in Bovari2018',
        },
        'gsigmaEm': {
            'func': lambda itself=0., deltagsigmaEm=0.: itself*deltagsigmaEm,
            'com': 'Evolution of gsigma in Eq. (18) in Bovari2018',
        },
        # Emissions group
        'Eland': {
            'func': lambda itself=0., deltaEland=0.: deltaEland*itself,
            'com': 'Evolution of land use emissions in Eq. (19) in Bovari2018',
        },
    },

    # statevar
    'statevar': {
        # from _def_functions
        'phillips': Funcs.Phillips.lin,
        'kappa': Funcs.Kappa.lin,
        'Sh': Funcs.Shareholding.lin,
        'Damage': Funcs.Damage.general,

        # damage group
        'DK': {
            'func': lambda Damage=0., fk=0.: fk*Damage,
            'com': 'Defined in Eq. (28) in Bovari2018'
        },
        'Dy': {
            'func': lambda DK=0., Damage=0.: 1. - (1. - Damage)/(1. - DK),
            'com': 'Defined in Eq. (29) in Bovari2018'
        },
        'deltad': {
            'func': lambda delta=0., DK=0.: delta + DK,
            'definition': 'Capital depreciation with CC',
            'com': 'Defined below Eq. (3) in Bovari2018',
        },
        # emission group
        'Emission': {
            'func': lambda Eind=0., Eland=0.: Eind + Eland,
            'definition': 'Total emissions',
            'com': 'Sum of industrial and Land-Use',
        },
        'Eind': {
            'func': lambda emissionreductionrate=0., sigmaEm=0., Y0=0.: (1. - emissionreductionrate)*sigmaEm*Y0,
            'definition': 'Industrial emissions',
            'com': 'Defined given in Eq. (16) in Bovari2018',
        },
        # production group
        'Y': {
            'func': lambda Abattement=0., Dy=0., Y0=0.: (1. - Abattement)*(1. - Dy)*Y0,
            'com': 'Defined in Eq. (2) in Bovari2018',
            'definition': 'Yearly Production with impacts',
        },
        'Y0': {
            'func': lambda K=0., nu=1.: K / nu,
            'com': 'Definifiotn in Eq. (1) in Bovari2018',
            'definition': 'Yearly Production without impacts',
        },
        'L': {
            'func': lambda Nmax=0., Y0=0., a=1.: np.minimum(Nmax, Y0/a),
            'com': 'Number of workers according to K, Eq. (1) in Bovari2018',
        },
        'I': {
            'func': lambda kappa=0, Y=0: kappa*Y,
            'com': 'Defined in Eq. (6) in Bovari2018',
            'definition': 'Investment in capital',
        },
        'Pi': {
            'func': lambda GDP=0., w=0., L=0., r=0., D=0., p=0., carbontax=0., deltad=0., K=0.: GDP - w*L - r*D - p*carbontax - p*deltad*K,
            'com': 'Defined in Eq. (3) in Bovari2018',
            'definition': 'Monetary profit of private sector',
        },
        'g': {
            'func': lambda I=0., K=1., deltad=0.: (I - deltad*K)/K,
            'com': 'Relative growth of GDP: Kdot / K',
        },

        # carbon price group
        'emissionreductionrate': {
            'func': lambda pbackstop=1., convexitycost=2.6, pcarbon=0: np.minimum(1., (pcarbon/pbackstop)**(1./(convexitycost - 1.))),
            'com': 'Defined in Eq. (31) in Bovari2018',
        },
        'pcarbon': {
            'func': lambda pcarbon_pot=0., pbackstop=0.: np.minimum(pcarbon_pot, pbackstop),
            'definition': 'Real carbon price as the minimum between pcarbon_pot and pbackstop',
            'com': 'The carbon price used in emissionreductionrate',
        },
        'Abattement': {
            'func': lambda sigmaEm=0., pbackstop=0., emissionreductionrate=0., convexitycost=1.: 0.001*sigmaEm*pbackstop*(emissionreductionrate**convexitycost)/convexitycost,
            'definition': 'Rate of production devoted to transition',
            'com': 'Defined in Eq. (30) in Bovari2018',
        },
        'carbontax': {
            'func': lambda Eind=0., pcarbon=0., conv10to15=0.: pcarbon*Eind*conv10to15,
            'definition': 'Carbon tax paid by private sector',
            'com': 'Defined below Eq. (3) in Bovari2018',
        },
        'c': {
            'func': lambda p=0., omega=0.: p * omega,
            'com': 'Production cost to get good inflation function',
        },
    },
}

# add Coping logics
for category, dic in _LOGICS_COPING2018.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# UNITS #######################################################################
_LOGICS['ode']['a']['units'] = '$.Humans^{-1}.y^{-1}'
_LOGICS['ode']['N']['units'] = 'Humans'
_LOGICS['ode']['K']['units'] = '$'
_LOGICS['ode']['w']['units'] = '$.Humans^{-1}.y^{-1}'
_LOGICS['ode']['D']['units'] = '$'
_LOGICS['ode']['p']['units'] = ''
_LOGICS['ode']['CO2AT']['units'] = 'C'
_LOGICS['ode']['CO2UP']['units'] = 'C'
_LOGICS['ode']['CO2LO']['units'] = 'C'
_LOGICS['ode']['T']['units'] = 'Tc'
_LOGICS['ode']['T0']['units'] = 'Tc'
_LOGICS['ode']['pbackstop']['units'] = '$'
_LOGICS['ode']['pcarbon_pot']['units'] = '$.C^{-1}'
_LOGICS['ode']['sigmaEm']['units'] = 'C.$^{-1}'
_LOGICS['ode']['gsigmaEm']['units'] = 'y^{-1}'
_LOGICS['ode']['Eland']['units'] = 'C.y^{-1}'
_LOGICS['statevar']['Y']['units'] = '$'
_LOGICS['statevar']['L']['units'] = 'Humans'
_LOGICS['statevar']['phillips']['units'] = 'y^{-1}'
_LOGICS['statevar']['I']['units'] = '$.y^{-1}'
_LOGICS['statevar']['pi']['units'] = ''
_LOGICS['statevar']['lambda']['units'] = ''
_LOGICS['statevar']['omega']['units'] = ''
_LOGICS['statevar']['GDP']['units'] = '$.y^{-1}'
_LOGICS['statevar']['c']['units'] = ''
_LOGICS['statevar']['Pi']['units'] = '$.y^{-1}'
_LOGICS['statevar']['g']['units'] = 'y^{-1}'
_LOGICS['statevar']['kappa']['units'] = ''
_LOGICS['statevar']['inflation']['units'] = 'y^{-1}'
_LOGICS['statevar']['d']['units'] = 'y'
_LOGICS['statevar']['Emission']['units'] = 'C.y^{-1}'
_LOGICS['statevar']['Sh']['units'] = '$.y^{-1}'
_LOGICS['statevar']['Damage']['units'] = ''
_LOGICS['statevar']['DK']['units'] = ''
_LOGICS['statevar']['Dy']['units'] = ''
_LOGICS['statevar']['deltad']['units'] = 'y^{-1}'
_LOGICS['statevar']['Eind']['units'] = 'C.y^{-1}'
_LOGICS['statevar']['Y0']['units'] = '$.y^{-1}'
_LOGICS['statevar']['emissionreductionrate']['units'] = ''
_LOGICS['statevar']['pcarbon']['units'] = '$.C^{-1}'
_LOGICS['statevar']['Abattement']['units'] = ''
_LOGICS['statevar']['carbontax']['units'] = '$.y^{-1}'

_LOGICS['param']['Tini'] = {'units': 'y'}
_LOGICS['param']['Tmax'] = {'units': 'y'}
_LOGICS['param']['dt'] = {'units': 'y'}
_LOGICS['param']['nx'] = {'units': 'y'}
_LOGICS['param']['alpha'] = {'units': 'y^{-1}'}
_LOGICS['param']['n'] = {'units': 'y^{-1}'}
_LOGICS['param']['Nmax'] = {'units': 'Humans'}
_LOGICS['param']['phi12'] = {'units': 'y^{-1}'}
_LOGICS['param']['CUP'] = {'units': 'C'}
_LOGICS['param']['CAT'] = {'units': 'C'}
_LOGICS['param']['phi23'] = {'units': 'y^{-1}'}
_LOGICS['param']['CLO'] = {'units': 'C'}

_LOGICS['statevar']['F']['units'] = 'W.L^{-2}'
_LOGICS['param']['rhoAtmo'] = {'units': 'W L^{-2} Tc^{-1}'}
_LOGICS['param']['gammaAtmo'] = {'units': 'W L^{-2} Tc^{-1}'}
_LOGICS['param']['Capacity'] = {'units': 'y W L^{-2} Tc^{-1}'}
_LOGICS['param']['Capacity0'] = {'units': 'y W L^{-2} Tc^{-1}'}
_LOGICS['param']['F2CO2'] = {'units': 'W L^{-2}'}

_LOGICS['param']['deltapbackstop'] = {'units': 'y^{-1}'}
_LOGICS['param']['apc'] = {'units': 'y^{-1}'}
_LOGICS['param']['bpc'] = {'units': 'y^{-2}'}
_LOGICS['param']['deltagsigmaEm'] = {'units': 'y^{-1}'}
_LOGICS['param']['deltaEland'] = {'units': 'y^{-1}'}
_LOGICS['param']['philinConst'] = {'units': 'y^{-1}'}
_LOGICS['param']['philinSlope'] = {'units': 'y^{-1}'}
_LOGICS['param']['r'] = {'units': 'y^{-1}'}
_LOGICS['param']['kappalinConst'] = {'units': ''}
_LOGICS['param']['kappalinSlope'] = {'units': ''}
_LOGICS['param']['kappalinMin'] = {'units': ''}
_LOGICS['param']['kappalinMax'] = {'units': ''}
_LOGICS['param']['mu'] = {'units': ''}
_LOGICS['param']['eta'] = {'units': 'y^{-1}'}
_LOGICS['param']['divlinSlope'] = {'units': '$.y^{-1}'}
_LOGICS['param']['divlinconst'] = {'units': '$.y^{-1}'}
_LOGICS['param']['divlinMin'] = {'units': '$.y^{-1}'}
_LOGICS['param']['divlinMax'] = {'units': '$.y^{-1}'}
_LOGICS['param']['pi1'] = {'units': 'Tc^{-1}'}
_LOGICS['param']['pi2'] = {'units': 'Tc^{-2}'}
_LOGICS['param']['pi3'] = {'units': 'Tc^{-zeta3}'}
_LOGICS['param']['zeta3'] = {'units': ''}
_LOGICS['param']['fk'] = {'units': ''}
_LOGICS['param']['delta'] = {'units': 'y^{-1}'}
_LOGICS['param']['nu'] = {'units': 'y'}
_LOGICS['param']['convexitycost'] = {'units': ''}
_LOGICS['param']['conv10to15'] = {'units': ''}
###############################################################################

# Dictionnary of fields for preset
df = {
    # Time iteration
    'dt': 1./12,
    #'Tini':Tini,

    # ode initial conditions
    'pbackstop': 547.22,
    'pcarbon_pot': 3.5,
    'gsigmaEm': -0.0152,
    'Eland': 2.6,
    'CO2AT': 851.,
    'CO2UP': 460.,
    'CO2LO': 1740.,
    'T': 1.07,
    'T0': 0.0068,
    'p': 1.,
    'N': 4.83,
    'time': Tini,

    # parameters
    'n': 0.0305,
    'Nmax': 7.056,
    'alpha': 0.02,
    'delta': 0.04,
    'nu': 2.7,
    'mu': 1.875,
    'eta': 0.192,
    'r': 0.01,

    # carbon policy dynamics
    'convexitycost': 2.6,
    'deltapbackstop': -0.005,
    'conv10to15': 1.160723971/1000.,

    # parametric curves
    'philinSlope': 0.469,
    'philinConst': -0.292,
    'divlinconst': 0.138,
    'divlinSlope': 0.473,
    'divlinMin': 0.,
    'divlinMax': 0.3,
    'kappalinSlope': 0.575,
    'kappalinConst': 0.0318,
    'kappalinMin': 0.,
    'kappalinMax': 0.3,

    # Atmosphere parameters
    'deltaEland': -0.022,
    'deltagsigmaEm': -0.001,
    'gammaAtmo': 1.,  # old value is 0.0176 (to fit with ILOVECLIM)
    'F2CO2': 3.681,
    'CAT': 588.,
    'CUP': 360.,
    'CLO': 1720.,
    'phi12': 0.024,
    'phi23': 0.001,
    'Capacity': 1./0.098,
    'Capacity0': 80,  # old value is 3.52 (to fit with ILOVECLIM)

    # variables for scenarios
    'apc': 0.,
    'bpc': 0.,
    'pi1': 0.,
    'pi2': 0.,
    'pi3': 0.,
    'zeta3': 6.754,
    'fk': 1./3,
}

# dictionnary of fields value that are not explicitly in the model but used for calibration
df0 = {
    'd': 1.53,
    'Eind': 51.79,
    'emissionreductionrate': 0.03,
    'Y': 59.74,
    'lambda': 0.675,
    'omega': 0.578,
    'Dy': 0,
    'climate_sens': 3.1,

    # For scenarios
    'PI1': 0.,
    'PI2': 0.00236,
    'PI3': 0.0000819,
    'APC': 0.15,
    'BPC': 0.5,
}

# second order initial conditions calculation
df0['L'] = df0['lambda'] * df['N']
df0['Abattement'] = 1./(1. + ((1. - df0['emissionreductionrate'])*df0['Y'] *
                              df['convexitycost'])/(0.001*df0['Eind']*df['pbackstop'] *
                                                    df0['emissionreductionrate']**df['convexitycost']*(1. - df0['Dy'])))
df0['Y0'] = df0['Y']/(1. - df0['Dy'])/(1. - df0['Abattement'])
df0['sigmaEm'] = df0['Eind']/(1. - df0['emissionreductionrate'])/df0['Y0']
df0['Y2'] = (1. - df0['Abattement'])*(1. - df0['Dy'])*df0['Y0']

# We integrate our second order initial condition
df['K'] = df['nu'] * df0['Y0']
df['D'] = df0['d'] * df['p'] * df0['Y']
df['w'] = df0['omega'] * df['p'] * df0['Y'] / df0['L']
df['a'] = df0['Y0'] / df0['L']
df['rhoAtmo'] = 3.681/df0['climate_sens']

df['sigmaEm'] = df0['Eind']/(1. - df0['emissionreductionrate'])/df0['Y0']

# plots
plots = {
    'timetrace': [{}],
    'nyaxis': [
        {
            'x': 'time',
            'y': [['lambda', 'omega'],
                  ['d', 'g'],
                  ['kappa', 'pi'],
                  ],
            'idx':0,
            'title':'Classic variables of a Goodwin Keen',
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
        },
        {
            'x': 'time',
            'y': [['lambda', 'omega'],
                  ['d'],
                  ['g'],
                  ['T'],
                  ['Emission']],
            'idx':0,
            'title':'Relevant variables',
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
}

# business as usual
dict_BAU = dict(df)

# business as usual with impacts and no carbon price
dict_BAU_DAM = dict(df)
dict_BAU_DAM['pi1'] = df0['PI1']
dict_BAU_DAM['pi2'] = df0['PI2']
dict_BAU_DAM['pi3'] = df0['PI3']

# business as usual with impacts and no carbon price
dict_TRANSITION = dict(df)
dict_TRANSITION['apc'] = df0['APC']
dict_TRANSITION['bpc'] = df0['BPC']
dict_TRANSITION['pi1'] = df0['PI1']
dict_TRANSITION['pi2'] = df0['PI2']
dict_TRANSITION['pi3'] = df0['PI3']

# presets
_PRESETS = {
    'BAU': {
        'fields': dict_BAU,
        'com': 'Business as Usual (no carbon price and no climate impacts)',
        'plots': dict(plots),
    },
    'BAU_DAM': {
        'fields': dict_BAU_DAM,
        'com': 'Business as Usual with Climate impacts but no carbon price',
        'plots': dict(plots),
    },
    'TRANSITION': {
        'fields': dict_TRANSITION,
        'com': 'Default transition scenario with climate damage and carbon price',
        'plots': dict(plots),
    },
}
