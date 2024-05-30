# -*- coding: utf-8 -*-
"""
ABSTRACT : This is the model with two social classes from Giraud and Graselli 2021 entitled "Household debt:
the missing link between inequality and secular stagnation" where we put impacts of global warming.
TYPICAL BEHAVIOR : To be determined
LINKTOARTICLE : DOI: Not yet
@author: Loïc GIACCONE, Hugo A. MARTIN
"""
from copy import deepcopy
import numpy as np
from chimes.libraries import Funcs
from chimes.libraries._model_Climate_3Layers import _LOGICS as _LOGICSCLIM

###############################################################################
"""
TODO:
 - Tout reste à faire
 - Mettre a jour tous les commentaires
"""

_LOGICS = deepcopy(_LOGICSCLIM)
# the logics from Climate are set in our current _LOGICS
for category, dic in _LOGICSCLIM.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

_LOGICS['param'] = {}
del _LOGICS['ode']['pseudot']

# add plenty of stuff
_LOGICS_Ineq = {
    # ode
    'ode': {
        # from functions_library
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.logistic,
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': Funcs.Inflation.pricefrominflation,

        # production group
        'K': {
            'func': lambda itself=0., deltad=0., I=0.: I - deltad * itself,
            'initial': 123,
            'com': 'Evolution def. in Eq. (7) in Bovari2018',
            'definition': 'Monetary Capital',
        },
        'Dw': {
            'func': lambda p=0., Cw=0., w=0., L=0., r=0., Ctaxw=0., itself=0.: p * Cw - w * L + r * itself + p * Ctaxw,
            'initial': 30.,
            'com': 'To be written',
            'definition': 'Workers debt in current $',
            'units': '$',
        },
        'Di': {
            'func': lambda p=0., Ci=0., rk=0., K=0., r=0., Ctaxi=0., Ctaxf=0., DK=0., itself=0.: p * Ci - rk * p * K + r * itself + p * (Ctaxi + Ctaxf + DK * K),
            'initial': 30.,
            'com': 'To be written',
            'definition': 'Investors debt in current $',
            'units': '$',
        },

        # carbon price group
        'pbackstop': {
            'func': lambda itself=0., deltapbackstop=0.: itself * deltapbackstop,
            'com': 'Exogenous Evolution is implicitely given in Bovari2018',
        },
        'pcarbon_pot': {
            'func': lambda apc=0., bpc=0., itself=0., time=1., Tini=0.: itself * (apc + bpc / (time - (Tini - 1))),
            'com': 'Evolution of carbon price Eq. (38) in Bovari2018',
        },

        # Emissions group
        'sigmaEm': {
            'func': lambda itself=0., gsigmaEm=0.: itself * gsigmaEm,
            'com': 'Evolution of sigma in Eq. (17) in Bovari2018',
        },
        'gsigmaEm': {
            'func': lambda itself=0., deltagsigmaEm=0.: itself * deltagsigmaEm,
            'com': 'Evolution of gsigma in Eq. (18) in Bovari2018',
        },
        'Eland': {
            'func': lambda itself=0., deltaEland=0.: deltaEland * itself,
            'com': 'Evolution of land use emissions in Eq. (19) in Bovari2018',
        },
    },

    # statevar
    'statevar': {
        # from functions_library
        'omega': Funcs.Definitions.omega,
        'phillips': Funcs.Phillips.lin,
        'Damage': Funcs.Damage.general,

        # population group
        'Ni': {
            'func': lambda N=0., prop_i=0.: prop_i * N,
            'definition': 'Number of investors',
            'com': 'to do',
            'units': 'Humans',
        },
        'Nw': {
            'func': lambda N=0., prop_i=0.: (1. - prop_i) * N,
            'definition': 'Number of workers',
            'com': 'to do',
            'units': 'Humans',
        },
        'lambda': {
            'func': lambda L=0., Nw=1.: L / Nw,
        },

        # damage group
        'DK': {
            'func': lambda Damage=0., fk=0.: fk * Damage,
            'com': 'Defined in Eq. (28) in Bovari2018'
        },
        'Dy': {
            'func': lambda DK=0., Damage=0.: 1. - (1. - Damage) / (1. - DK),
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
            'func': lambda EindI=0., Eindi=0., Eindw=0.: EindI + Eindi + Eindw,
            'definition': 'Industrial emissions',
            'com': 'Defined given in Eq. (16) in Bovari2018',
        },
        'Eindi': {
            'func': lambda emissionreductionrate=0., sigmaEm=0., Ci=0.: (1. - emissionreductionrate) * sigmaEm * Ci,
            'definition': 'Emissions due to investors consumption',
            'com': 'to do',
            'units': 'C.y^{-1}',
        },
        'Eindw': {
            'func': lambda emissionreductionrate=0., sigmaEm=0., Cw=0.: (1. - emissionreductionrate) * sigmaEm * Cw,
            'definition': 'Emissions due to workers consumption',
            'com': 'to do',
            'units': 'C.y^{-1}',
        },
        'eindi': {
            'func': lambda Eindi=0., Ni=1.: Eindi / Ni,
            'definition': 'Yearly Emissions per investor',
            'com': 'to do',
            'units': 'C.Humans^{-1}.y^{-1}',
        },
        'eindw': {
            'func': lambda Eindw=0., Nw=1.: Eindw / Nw,
            'definition': 'Yearly Emissions per worker',
            'com': 'to do',
            'units': 'C.Humans^{-1}.y^{-1}',
        },
        'EindI': {
            'func': lambda emissionreductionrate=0., sigmaEm=0., I=0.: (1. - emissionreductionrate) * sigmaEm * I,
            'definition': 'Yeraly Emissions due to investments',
            'com': 'to do',
            'units': 'C.y^{-1}',
        },

        # production group
        'Y': {
            'func': lambda Abattement=0., Dy=0., Y0=0.: (1. - Abattement) * (1. - Dy) * Y0,
            'com': 'Defined in Eq. (2) in Bovari2018',
            'definition': 'Yearly Production with impacts',
        },
        'Y0': {
            'func': lambda K=0., nu=1.: K / nu,
            'com': 'Definifiotn in Eq. (1) in Bovari2018',
            'definition': 'Yearly Production without impacts',
        },
        'L': {
            'func': lambda Nw=0., Y0=0., a=1.: np.clip(Y0 / a, 0., Nw),
            'com': 'Number of workers according to K, Eq. (1) in Bovari2018',
        },
        'I': {
            'func': lambda Ci=0, Cw=0, Y=0: -(Cw + Ci) + Y,
            'definition': 'Investment in money',
            'units': '$.y^{-1}',
            'com': 'Investments adapt to consumption',
        },

        # prices
        'inflation': {
            'func': lambda eta=0., mu=0., omega=0.: eta * (mu * omega - 1.),
            'definition': 'Inflation from wage share',
        },

        # debts
        'dw': {
            'func': lambda Dw=0., p=1., Y=1.: Dw / p / Y,
            'definition': 'Workers debt ratio',
            'com': 'To do',
            'units': '',
        },
        'di': {
            'func': lambda Di=0., p=1., Y=1.: Di / p / Y,
            'definition': 'Investors debt ratio',
            'com': 'To do',
            'units': '',
        },
        'df': {
            'func': lambda Df=0., p=1., Y=1.: Df / p / Y,
            'definition': 'Firms debt ratio',
            'com': 'To do',
            'units': '',
        },
        'Df': {
            'func': lambda Di=0., Dw=0.: -(Di + Dw),
            'definition': 'Firms debt in current $',
            'com': 'To do',
            'units': '$',
        },
        # 'Dfdot': {
        #    'func': lambda p=0., Cw=0., Ci=0., w=0., rk=0., L=0., K=0., r=0., Dw=0., Di=0.: -(p*Cw - w*L + r*Dw + p*Ci - rk*p*K + r*Di),
        #    'definition': 'Derivative of private debt ratio',
        #    'com': 'To do',
        #    'units': '$.y^{-1}',
        # },

        # consumption
        'Cw': {
            'func': lambda Y=0., cw=0.: cw * Y,
            'definition': 'Total consumption of workers',
            'com': 'To do',
            'units': '$',
        },
        'Ci': {
            'func': lambda Y=0., ci=0.: ci * Y,
            'definition': 'Total consumption of investors',
            'com': 'To do',
            'units': '$',
        },
        'cw': {
            'func': lambda omega=0., r=0., dw=0., cminus=0., Ac=0., Kc=1., Cc=0., Qc=1., Bc=0., nuc=1.: np.maximum(cminus, Ac + (Kc - Ac) / (Cc + Qc * np.exp(np.minimum(-Bc * (omega - r * dw), 30.)))**(1. / nuc)),
            'com': 'consumption function of workers',
            'units': '',
        },
        'ci': {
            'func': lambda rk=0., nu=0., r=0., di=0., cminus=0., Ac=0., Kc=1., Cc=0., Qc=1., Bc=0., nuc=1.: np.maximum(cminus, Ac + (Kc - Ac) / (Cc + Qc * np.exp(np.minimum(-Bc * (rk * nu - r * di), 30.)))**(1. / nuc)),
            'com': 'consumption function of investors',
            'units': '',
        },

        # carbon price group
        'emissionreductionrate': {
            'func': lambda pbackstop=1., convexitycost=2.6, pcarbon=0: np.minimum(1., (pcarbon / pbackstop)**(1. / (convexitycost - 1.))),
            'com': 'Defined in Eq. (31) in Bovari2018',
        },
        'pcarbon': {
            'func': lambda pcarbon_pot=0., pbackstop=0.: np.minimum(pcarbon_pot, pbackstop),
            'definition': 'Real carbon price as the minimum between pcarbon_pot and pbackstop',
            'com': 'The carbon price used in emissionreductionrate',
        },
        'Abattement': {
            'func': lambda sigmaEm=0., pbackstop=0., emissionreductionrate=0., convexitycost=1.: 0.001 * sigmaEm * pbackstop * (emissionreductionrate**convexitycost) / convexitycost,
            'definition': 'Rate of production devoted to transition',
            'com': 'Defined in Eq. (30) in Bovari2018',
        },
        'Ctaxw': {
            'func': lambda Eindw=0., pcarbon=0., Epsilon=0., conv10to15=0.: Epsilon * pcarbon * Eindw * conv10to15,
            'definition': 'Carbon tax paid by workers for their consumption',
            'com': 'Defined below Eq. (3) in Bovari2018',
        },
        'Ctaxi': {
            'func': lambda Eindi=0., pcarbon=0., Epsilon=0., Eindw=0., conv10to15=0.: conv10to15 * pcarbon * (Eindi + (1 - Epsilon) * Eindw),
            'definition': 'Carbon tax paid by investors for their consumption',
            'com': 'Defined below Eq. (3) in Bovari2018',
        },
        'Ctaxf': {
            'func': lambda EindI=0., pcarbon=0., conv10to15=0.: pcarbon * EindI * conv10to15,
            'definition': 'Carbon tax paid by investors for firms investments',
            'com': 'Defined below Eq. (3) in Bovari2018',
        },


        # other
        'rk': {
            'func': lambda Theta=0., nu=1., omega=0., r=0, dw=0., di=0., delta=0.: Theta * (1. - omega + r * (dw + di) - delta * nu) / nu,
            'definition': 'To do',
            'com': 'To do',
            'units': '',
        },
    },

    'param': {
        'Theta': {
            'value': 0.5,
            'definition': 'Parameter in rk',
            'units': '',
            'symbol': r'$\Theta$',
        },
        'Epsilon': {
            'value': 0.9,
            'definition': 'Carbon Tax Redistribution',
            'units': '',
            'symbol': r'$\varepsilon$',
        },
        'prop_i': {
            'value': 0.02,
            'definition': 'Proportion of investors in population',
            'units': '',
            'symbol': r'prop$_i$',
        },
    },
}

for category, dic in _LOGICS_Ineq.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v

# TO DO

# units
_LOGICS['ode']['K']['units'] = '$'
_LOGICS['statevar']['Y0']['units'] = '$.y^{-1}'
# _LOGICS['param']['nu'] = {'units': 'y'}
_LOGICS['statevar']['L']['units'] = 'Humans'
_LOGICS['ode']['a']['units'] = '$.Humans^{-1}.y^{-1}'
# _LOGICS['param']['alpha'] = {'units': 'y^{-1}'}
_LOGICS['statevar']['I']['units'] = '$.y^{-1}'
# _LOGICS['statevar']['deltad']['units'] = 'y^{-1}'
_LOGICS['ode']['w']['units'] = '$.Humans^{-1}.y^{-1}'
_LOGICS['statevar']['phillips']['units'] = 'y^{-1}'
# _LOGICS['param']['philinConst'] = {'units': 'y^{-1}'}
# _LOGICS['param']['philinSlope'] = {'units': 'y^{-1}'}

# On n'a pas gamma
_LOGICS['statevar']['lambda']['units'] = ''
_LOGICS['statevar']['inflation']['units'] = 'y^{-1}'
_LOGICS['ode']['N']['units'] = 'Humans'

# _LOGICS['param']['n'] = {'units': 'y^{-1}'}
# _LOGICS['param']['Nmax'] = {'units': 'Humans'}

_LOGICS['ode']['p']['units'] = ''

_LOGICS['statevar']['inflation']['units'] = 'y^{-1}'

# _LOGICS['param']['mu'] = {'units': ''}
# _LOGICS['param']['eta'] = {'units': 'y^{-1}'}

_LOGICS['statevar']['omega']['units'] = ''

# _LOGICS['param']['r'] = {'units': 'y^{-1}'}
# _LOGICS['param']['cminus'] = {'units': ''}
# _LOGICS['param']['Ac'] = {'units': ''}
# _LOGICS['param']['Bc'] = {'units': ''}
# _LOGICS['param']['Cc'] = {'units': ''}
# _LOGICS['param']['Kc'] = {'units': ''}
# _LOGICS['param']['nuc'] = {'units': ''}
# _LOGICS['param']['Qc'] = {'units': ''}
# _LOGICS['param']['Cw'] = {'units': '$'}
# _LOGICS['param']['Ci'] = {'units': '$'}
# _LOGICS['param']['cw'] = {'units': ''}
# _LOGICS['param']['ci'] = {'units': ''}
# _LOGICS['param']['dw'] = {'units': ''}
# _LOGICS['param']['di'] = {'units': ''}

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
            'idx': 0,
            'title': 'Classic variables of a Goodwin Keen',
            'lw': 1},
        {
            'x': 'time',
            'y': [['CO2AT', 'CO2UP', 'CO2LO'],
                  ['T', 'T0'],
                  ['F'],
                  ['Emission', 'Eind', 'Eland']],
            'idx': 0,
            'title': 'All climatic variables',
            'lw': 1
        },
        {
            'x': 'time',
            'y': [['L', 'N'],
                  ['Y', 'Y0', 'Pi', 'I'],
                  ['c', 'p'],
                  ['pcarbon', 'pbackstop']],
            'idx': 0,
            'title': 'Twin variables',
            'lw': 1
        },
        {
            'x': 'time',
            'y': [['lambda', 'omega'],
                  ['d'],
                  ['g'],
                  ['T'],
                  ['Emission']],
            'idx': 0,
            'title': 'Relevant variables',
            'lw': 1
        }
    ],
    'XY': [],
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

# Dictionnary of fields for preset
df = {

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
    'time': 2015,

    # parameters
    'n': 0.0305,
    'Nmax': 7.056,
    'prop_i': 0.02,
    'alpha': 0.02,
    'delta': 0.04,
    'nu': 2.7,
    'mu': 1.875,
    'eta': 0.192,
    'r': 0.01,
    'gammai': 0.25,

    # carbon policy dynamics
    'convexitycost': 2.6,
    'deltapbackstop': -0.005,
    'conv10to15': 1.160723971 / 1000.,

    # parametric curves
    'philinSlope': 0.469,
    'philinConst': -0.292,
    # 'divlinconst': 0.138,
    # 'divlinSlope': 0.473,
    # 'divlinMin': 0.,
    # 'divlinMax': 0.3,
    # 'kappalinSlope': 0.575,
    # 'kappalinConst': 0.0318,
    # 'kappalinMin': 0.,
    # 'kappalinMax': 0.3,

    # Atmosphere parameters
    'deltaEland': -0.022,
    'deltagsigmaEm': -0.001,
    'gammaAtmo': 0.0176,  # old value is 0.0176 (to fit with ILOVECLIM: 1)
    'F2CO2': 3.681,
    'CAT': 588.,
    'CUP': 360.,
    'CLO': 1720.,
    'phi12': 0.024,
    'phi23': 0.001,
    'Capacity': 1. / 0.098,
    'Capacity0': 3.52,  # old value is 3.52 (to fit with ILOVECLIM: 80)

    # variables for scenarios
    'apc': 0.,
    'bpc': 0.,
    'pi1': 0.,
    'pi2': 0.,
    'pi3': 0.,
    'zeta3': 6.754,
    'fk': 1. / 3,
}

# dictionnary of fields value that are not explicitly in the model but used for calibration
df0 = {
    'df': 1.53,
    'dw': 0.5,
    'di': 0.5,
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
Nw = (1. - df['prop_i']) * df['N']
df0['L'] = df0['lambda'] * Nw
df0['Abattement'] = 1. / (1. + ((1. - df0['emissionreductionrate']) * df0['Y'] *
                                df['convexitycost']) / (0.001 * df0['Eind'] * df['pbackstop'] *
                                                        df0['emissionreductionrate']**df['convexitycost'] * (1. - df0['Dy'])))
df0['Y0'] = df0['Y'] / (1. - df0['Dy']) / (1. - df0['Abattement'])
df0['sigmaEm'] = df0['Eind'] / (1. - df0['emissionreductionrate']) / df0['Y0']
df0['Y2'] = (1. - df0['Abattement']) * (1. - df0['Dy']) * df0['Y0']

# We integrate our second order initial condition
df['K'] = df['nu'] * df0['Y0']
# df['Df'] = df0['df'] * df['p'] * df0['Y']
df['Dw'] = df0['dw'] * df['p'] * df0['Y']
df['Di'] = df0['di'] * df['p'] * df0['Y']
df['w'] = df0['omega'] * df['p'] * df0['Y'] / df0['L']
df['a'] = df0['Y0'] / df0['L']
df['rhoAtmo'] = 3.681 / df0['climate_sens']

df['sigmaEm'] = df0['Eind'] / (1. - df0['emissionreductionrate']) / df0['Y0']

# Scenarios
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
        'com': 'Transition scenario with Climate impacts and carbon price policies',
        'plots': dict(plots),
    },
}
