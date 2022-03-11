# -*- coding: utf-8 -*-

"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

----
This file contains :
    _DFIELDS the big dictionnary with basic information on
        * Variables
        * Parameters
        * Numerical parameters

    _DALLOWED_FIELDS : Contains all the restrictions on each field for each
    element in _DFIELD
    _DEFAULTFIELDS : The value that will be added if none are

    __DOTHECHECK Flag to check or not the dictionnary
    __FILLDEFAULTVALUES Flag to fill the defaultfields
"""
import numpy as np


__DOTHECHECK = True
__FILLDEFAULTVALUES = True


# #############################################################################
# #############################################################################
#                   Library (new formalism)
# #############################################################################


_LIBRARY = {
    'Numerical': {
        'Tmax': {
            'value': 100,
            'units': 'y',
            'definition': 'Total simulated time',
        },
        'Tini': {
            'value': 2015,
            'definition': 'Initial time',
            'units': 'y',
        },
        'dt': {
            'value': 0.01,
            'units': 'y',
            'definition': 'time between two steps',
        },
        'nt': {
            'func': lambda Tmax=0, dt=1: int(Tmax / dt),
            'units': '',
            'definition': 'Number of timestep',
            'com': 'Constant dt',
            'eqtype': 'param',
        },
        'nx': {
            'value': 1,
            'units': 'y',
            'definition': 'Number of system in parrallel',
        },
        'time': {
            'initial': 0.,
            'func': lambda dt=0: 1.,
            'definition': 'Time vector',
            'com': 'dt/dt=1, time as ODE',
            'units': 'y',
            'eqtype': 'ode',
        },
        # 't': {
        #    'value': 0,
        #    'definition': 'time inside equations'}
    },


    'Ressources': {
        'K_R': {
            'value': 1.,
            'definition': 'Kapital for ressource extraction',
            'units': 'Units',
        },
        'D_R': {
            'value': 1.,
            'definition': 'Debt of ressource sector',
            'units': '$',
        },
        'p_R': {
            'value': 1.,
            'definition': 'price of ressources',
            'units': '$.Units^{-1}',
        },
        'kappa_R': {
            'value': 1.,
            'definition': 'Investment func for ressource sector',
            'units': '',
        },
        'pi_R': {
            'value': 1.,
            'definition': 'relative profit of ressource sector',
            'units': '',
        },
        'Pi_R': {
            'value': 1.,
            'definition': 'Absolute profit for ressource sector',
            'units': '$.Units^{-1}',
        },
        'R': {
            'value': 1.,
            'definition': 'Available ressources',
            'units': 'Units',
        },
        'Y_R': {
            'value': 1.,
            'definition': 'Flux of extracted ressources',
            'units': 'Units.y^{-1}',
        },
        'I_R': {
            'value': 1.,
            'definition': 'Investment (real) for ressources',
            'units': 'Units.y^{-1}',
        },
        'Kstar': {
            'value': 1.,
            'definition': "Equivalent capital for services",
            'units': 'Units',
        },
        'd_R': {
            'value': 1.,
            'definition': 'debt ratio ressources',
            'units': 'y',
        },
        'inflation_R': {
            'value': 1.,
            'definition': 'inflation for ressources',
            'units': 'y^{-1}',
        },
    },

    'Household': {
        # VARIABLES
        'N': {
            'value': 1.,
            'definition': 'Population',
            'units': 'Humans',
        },
        'L': {
            'value': None,
            'definition': 'Workers',
            'units': 'Humans',
        },
        'a': {
            'value': 1,
            'units': 'Units.Humans^{-1}.y^{-1}',
            'definition': 'Productivity',
        },
        'w': {
            'value': 0.85,
            'definition': 'Wage value',
            'units': '$.Humans^{-1}.y^{-1}'
        },
        'Omega': {
            'value': 1,
            'definition': 'Individual purchasing power',
            'units': 'Units.y^{-1}.Humans^{-1}',
            'symbol': r'$\Omega$', },
        'lambda': {
            'value': .97,
            'definition': 'employement rate',
            'units': '',
            'symbol': r'$\lambda$',
        },
        'omega': {
            'value': .85,
            'definition': 'wage share',
            'units': '',
            'symbol': r'$\omega$',
        },


        # PARAMETERS
        'n': {
            'value': 0.025,
            'definition': 'Rate of population growth',
            'units': 'y^{-1}',
        },
        'alpha': {
            'value': 0.02,
            'definition': 'Rate of productivity increase',
            'units': 'y^{-1}',
        },
        'Nmax': {
            'value': 12,
            'definition': 'Saturating population',
            'units': 'Humans',
        },
    },


    'Recipies': {
        'gamma': {
            'value': 0.1,
            'definition': 'Input-output production recipy',
            'units': '',
        },
        'Xi': {
            'value': 0.1,
            'definition': 'Input-output capital recipy',
            'units': '',
        },
        'rho': {
            'value': 0.1,
            'definition': 'Capital consumption recipy',
            'units': 'y^{-1}',
        },
    },


    'Production': {
        'A': {
            'value': 1/3.,
            'definition': 'Efficiency in CES prod',
            'units': 'y^{-1}',
        },
        'nu': {
            'value': 3,
            'definition': 'Kapital to output ratio',
            'units': '',
            'symbol': r'$\nu$',
        },
        'b': {
            'value': 0.5,
            'definition': 'part of capital in prod intensity',
            'units': '',
        },
        'CESexp': {
            'value': 100,
            'definition': 'exponent in CES function',
            'units': '',
        },
        'cesLcarac': {
            'func': lambda A=0, K=0, a=1, b=0.5, CESexp=100: A*(K/a) * (2*(1-b))**(1/CESexp),
            'definition': 'Typical Labor from capital',
            'com': 'Extracted from YCES',
            'units': 'Humans',
            'eqtype': 'param',
        },
        'cesYcarac': {
            'func': lambda K=0, A=0, b=0.5, CESexp=100: K*A*(2*b)**(-1/CESexp),
            'definition': 'Typical Y from capital',
            'com':  'Extracted from YCES',
            'units': 'Units.y^{-1}',
            'eqtype': 'param',
        },
        'omegacarac': {
            'func': lambda w=0, cesLcarac=0, p=1, cesYcarac=1: w*cesLcarac/(p*cesYcarac),
            'definition': 'Typical omega without substituability',
            'com':  'Extracted from YCES',
            'units': '',
            'eqtype': 'param',
        },
        'l': {
            'func': lambda omegacarac=0.5, CESexp=100: (omegacarac**(-CESexp/(1+CESexp)) - 1)**(1/CESexp),
            'definition': 'ratio btwn effective workers and typical worker',
            'com': 'deduced from Pi optimisation',
            'units': '',
            'eqtype': 'param',
        },
        # VARIABLES
        'K': {
            'value': 2.7,
            'units': 'Units',
            'definition': 'Capital',
        },
        'K_0': {
            'value': 1,
            'units': 'Units',
            'definition': 'Intermediary capital in case of Cobb-Douglas arbitrage with matter',
        },
        'Y': {
            'value': 1,
            'definition': 'GDP in output quantity',
            'units': 'Units.y^{-1}',
        },
        'Y0': {
            'value': 1,
            'definition': 'Yearly Production without climate damage and abatment',
            'units': 'Units.y^{-1}',
        },
        'GDP': {
            'value': 1,
            'definition': 'GDP in output quantity',
            'units': '$.y^{-1}',
        },
        'V': {
            'value': 1,
            'definition': 'Inventory of Goods',
            'units': 'Units',
        },
        'u': {
            'value': .85,
            'definition': 'Use intensity of capital',
            'units': '',
        },


        # INTERMEDIARY VARIABLES
        'g': {
            'value': None,
            'definition': 'Relative growth of GDP',
            'units': 'y^{-1}',
        },
        'pi': {
            'value': None,
            'definition': 'relative profit',
            'units': '',
            'symbol': r'$\pi$',
        },
        'Pi': {
            'value': None,
            'definition': 'Absolute profit',
            'units': '$.y^{-1}',
            'symbol': r'$\Pi$',
        },
        'c': {
            'value': None,
            'definition': 'production price',
            'units': '$.Units^{-1}'
        },

        # PARAMETERS
        'delta': {
            'value': 0.005,
            'definition': 'Rate of capital depletion',
            'units': 'y^{-1}',
            'symbol': r'$\delta$',
        },
        'gammai': {
            'value': 1,
            'definition': 'inflation awareness',
            'units': '',
            'symbol': r'$\Gamma$',
        },
        'sigma': {
            'value': 1,
            'definition': 'rate of use adjustment',
            'units': 'y^{-1}',
            'symbol': r'$\sigma$',
        },
    },


    'Salary Negociation': {
        'phillips': {
            'value': None,
            'definition': 'Wage inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$\phi$',
        },

        # Diverging Philips
        'phinull': {
            'value': 0.1,
            'definition': 'Unemployment rate with no salary increase',
            'units': '',
        },
        'phi0': {
            'func': lambda phinull=0: phinull / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'param',
        },
        'phi1': {
            'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'param',
        },

        # Linear Phillips (from Coping article)
        'philinConst': {
            'value': -0.292,
            'definition': 'wage rate when full unemployement',
            'units': 'y^{-1}',
        },
        'philinSlope': {
            'value': 0.469,
            'definition': 'wage rate dependance to unemployement',
            'units': 'y^{-1}',
        },

        # Exponential Philips (from CES article)
        'phiexp0': {
            'value': -0.01,
            'definition': 'Constant in expo phillips',
            'units': 'y^{-1}',
        },
        'phiexp1': {
            'value': 2.35*10**(-23),
            'definition': 'slope in expo phillips',
            'units': 'y^{-1}',
        },
        'phiexp2': {
            'value': 50,
            'definition': 'exponent in expo phillips',
            'units': '',
        },

        # Additional parameter
        'zphi': {
            'value': 0.1,
            'definition': 'nonlinearity on profit in negociation',
            'com': '',
            'units': ''
        }
    },

    'Speculation': {
        's': {
            'value': 0,
            'definition': 'share of GDP going to financial market',
            'units': ''
        },
        'Speculation': {
            'value': 0,
            'definition': 'flux of money going from firm to finance',
            'units': '$.y^{-1}'
        },
        'SpecExpo1': {
            'value': -0*0.25,
            'definition': 'Speculation constant (expo)',
            'units': '$.y^{-1}',
        },
        'SpecExpo2': {
            'value': 0*0.25,
            'definition': 'Speculation expo slope (expo)',
            'units': '$.y^{-1}',
        },
        'SpecExpo3': {
            'value': 0*0.36,
            'definition': 'Speculation attenuation in exp (expo)',
            'units': '',
        },
        'SpecExpo4': {
            'value': 0*12,
            'definition': 'Speculation sensitivity to growth',
            'units': 'y',
        },
    },

    'Shareholding': {
        'Sh': {
            'value': 0,
            'definition': 'Shareholding dividends',
            'units': '$.y^{-1}',
        },

        # Dividend fit from copingwithcollapse
        'divlinSlope': {
            'value': 0.473,
            'definition': 'Shareholding dependency to profits (affine)',
            'units': '$.y^{-1}',
        },
        'divlinconst': {
            'value': 0.138,
            'definition': 'Shareholding dividends when no profits (affine)',
            'units': '$.y^{-1}',
        },
        'divlinMin': {
            'value': 0,
            'definition': 'Shareholding minimum part',
            'units': '$.y^{-1}',
        },
        'divlinMax': {
            'value': 3,
            'definition': 'Shareholding maximum part',
            'units': '$.y^{-1}',
        },
    },


    'Investment': {
        'I': {
            'value': None,
            'definition': 'Investment in money',
            'units': '$.y^{-1}',
        },
        'Ir': {
            'value': None,
            'definition': 'Number of real unit from investment',
            'units': 'Units.y^{-1}',
        },
        'kappa': {
            'value': None,
            'definition': 'Part of GDP in investment',
            'units': '',
            'symbol': r'$\kappa$',
        },
        'k0': {
            'value': -0.0065,
            'definition': 'GDP share investedat zeroprofit (expo)',
            'units': '',
        },
        'k1': {
            'value': np.exp(-5),
            'definition': 'Investment slope (expo)',
            'units': '',
        },
        'k2': {
            'value': 20,
            'definition': 'Investment power in kappa (expo)',
            'units': '',
        },
        'kappalinSlope': {
            'value': 0.575,
            'definition': 'Investment slope kappa (affine)',
            'units': '',
        },
        'kappalinConst': {
            'value': 0.0318,
            'definition': 'Investment no profit (affine)',
            'units': '',
        },
        'kappalinMin': {
            'value': 0,
            'definition': 'Minimum value of kappa (affine)',
            'units': '',
        },
        'kappalinMax': {
            'value': 0.3,
            'definition': 'Maximum value of kappa (affine)',
            'units': '',
        },
        'zsolv': {
            'value': 0.1,
            'definition': 'nonlinearity solvability investment',
            'com': '',
            'units': ''
        }
    },


    'Debt': {
        'r': {
            'value': .03,
            'definition': 'Interest on debt',
            'units': 'y^{-1}',
        },
        'D': {
            'value': 0.1,
            'definition': 'Debt of private sector',
            'units': '$',
        },
        'Dh': {
            'value': 0.1,
            'definition': 'Debt of household',
            'units': '$',
        },
        'd': {
            # 'func': lambda GDP=0, D=0: D/GDP,
            'value': 0.1,
            'definition': 'relative debt',
            'units': 'y',
        },
        'solvability': {
            'definition': 'capital compared to debt',
            'units': ''
        },
        'M': {
            'value': 1,
            'definition': 'amount of money in the system',
            'units': '$'},
        'm': {
            'value': 1,
            'definition': 'money per unit of GDP',
            'units': 'y'},
        'v': {
            'value': 1,
            'definition': 'money circulation speed',
            'units': 'y^{-1}'},
    },


    'Prices': {
        # VARIABLES
        'inflation': {
            'value': None,
            'definition': 'inflation rate',
            'units': 'y^{-1}',
        },
        'p': {
            'value': 1,
            'definition': 'price of goods',
            'units': '$.Units^{-1}'
        },

        # PARAMETERS
        'mu': {
            'value': 1.3,
            'definition': 'Markup on prices',
            'units': '',
        },
        'eta': {
            'value': 0.5,
            'definition': 'timerate of price adjustment',
            'units': 'y^{-1}',
        },
        'chi': {
            'value': 1,
            'definition': 'inflation rate on inventory',
            'units': 'y^{-1}',
        },
        'chiY': {
            'value': 1,
            'definition': 'inflation sensibility on dot{V}/Y',
            'units': ''}
    },


    'Consumption': {
        # VARIABLES
        'G': {'value': None,
              'definition': 'Purchased good flow',
              'units': 'Units.y^{-1}',
              'symbol': r'$C$',
              },
        'H': {'value': 0,
              'definition': 'Household possessions',
              'units': 'Units',
              'symbol': r'$H$', },
        'Hid': {'value': None,
                'definition': 'Household optimal possessions',
                'units': 'Units',
                'symbol': r'$H^{id}$', },

        # PARAMETERS
        'deltah': {'value': 0.1,
                   'definition': 'possessions deterioration rate',
                   'units': 'y^{-1}',
                   'symbol': r'$\delta^h$', },
        'fC': {'value': 1,
               'definition': 'rate for consumption optimisation',
               'units': 'y^{-1}',
               'symbol': r'$f$', },
        'Omega0': {'value': 1,
                   'definition': 'Purchasing power of inflexion',
                   'units': 'Units.Humans^{-1}.y^{-1}',
                   },
        'x': {'value': 1,
              'definition': 'Inflexion effectiveness',
              'Units': None},
        'h': {'value': 1,
              'definition': 'saturated p per person',
              'units': None},
    },


    'Coping-Damages': {
        'deltad': {
            'value': 0.005,
            'definition': 'Rate of capital depletion with CC',
            'units': 'y^{-1}',
        },
        'Dy': {
            'value': 0,
            'definition': 'Damage on production',
            'units': '',
        },
        'DK': {
            'value': 0,
            'definition': "Intermediary damage on capital",
            'units': '',
        },
        'Damage': {
            'value':  0,
            'definition': 'Damage function',
            'units': '',
        },
        'deltaD': {
            'value':  0,
            'definition': 'Climate induced destruction rate',
            'units': 'Units.y^{-1}',
        },
        'pi1': {
            'value': 0,
            'definition': 'Linear damage parameter',
            'units': 'Tc^{-1}',
        },
        'pi2': {
            'value': 0.00236,
            'definition': 'quadratic damage parameter',
            'units': 'Tc^{-2}',
        },
        'pi3': {
            'value': 0.00000507,
            'definition': 'Weitzman damage parameter',
            'units': None,
        },
        'zeta3': {
            'value': 6.754,
            'definition': 'Weitzmann dmg temp exponent',
            'units': '',
        },
        'fk': {
            'value': 1/3,
            'definition': 'Fraction of damage allocated to capital',
            'units': '',
        },
    },


    'Emissions': {
        'Eind': {
            'value': 38.85,
            'definition': 'Emission from the society',
            'units': 'C.y^{-1}',
        },
        'Eland': {
            'value': 2.6,
            'definition': 'Natural Emission',
            'units': 'C.y^{-1}',
        },
        'deltaEland': {
            'value': 0,
            'definition': 'timerate of natural emission reduction',
            'units': 'y^{-1}',
        },
        'sigmaEm': {
            'value': 0,
            'definition': 'current emission intensity of the economy',
            'units': 'C.Units^{-1}.y^{-1}',
        },
        'gsigmaEm': {
            'value': -0.0152,
            'definition': 'Growth rate economic emission intensity',
            'units': 'y^{-1}',
        },
        'deltagsigmaEm': {
            'value': -0.001,
            'definition': 'growth rate of the emission growth rate',
            'units': 'y^{-1}',
        }
    },


    'Coping-Technologies': {
        'pbackstop': {
            'value': 547,
            'definition': 'Magic backstop technology price',
            'units': '',
        },
        'pcarbon': {
            'value': 100,
            'definition': 'aggregated real price of carbon',
            'units': '',
        },
        'pcarbon_pot': {
            'value': 100,
            'definition': 'aggregated potential price of carbon',
            'units': '',
        },
        'carbontax': {
            'value': 100,
            'definition': 'aggregated carbon tax paid by private sector',
            'units': '',
        },
        'apc': {
            'value': 0,
            'definition': 'parameter apc for ex. carbon price',
            'units': '',
        },
        'bpc': {
            'value': 0,
            'definition': 'parameter bpc for ex. carbon price',
            'units': '',
        },
        'deltapbackstop': {
            'value': -0.005,
            'definition': 'growth rate of backstop price',
            'units': '',
        },
        'deltapcarbon': {
            'value': 0,
            'definition': 'Growth rate of carbon price',
            'units': '',
        },
        'conv10to15': {
            'value': 1.160723971/1000,
            'definition': 'conversion factor',
            'units': '',
        },
        'emissionreductionrate': {
            'value': 0.03,
            'definition': 'Emission reduction rate',
            'units': 'y^{-1}',
        },
        'Abattement': {
            'value': 0,
            'definition': 'Redirection of production',
            'units': '',
        },
        'convexitycost': {
            'value': 2.6,
            'definition': 'Convexity of cost function for reduction',
            'units': '',
        },
    },


    '3Layer-Climate': {
        'Emission0': {
            'value': 38.85,
            'definition': 'CO2 Emission per year (Gt) at t=0',
            'units': 'C.y^{-1}',
        },
        'Emission': {
            'value': 38,
            'definition': 'CO2 Emission per year (Gt)',
            'units': 'C.y^{-1}',
        },
        'deltaEmission': {
            'value': 0.01,
            'definition': 'Diminution rate of carbon emission',
            'units': 'y^{-1}',
        },
        'F2CO2': {
            'value': 3.681,
            'definition': 'Forcing when doubling CO2',
            'units': None,
        },
        'CO2AT': {
            'value': 851,
            'definition': 'CO2 in atmosphere',
            'units': 'C',
        },
        'CO2UP': {
            'value': 460,
            'definition': 'CO2 in upper ocean',
            'units': 'C',
        },
        'CO2LO': {
            'value': 1740,
            'definition': 'CO2 in lower ocean',
            'units': 'C',
        },
        'CUP': {
            'value': 460,
            'definition': 'Historical CO2 in upper ocean',
            'units': 'C',
        },
        'CAT': {
            'value': 588,
            'definition': 'Historical CO2 in atmosphere',
            'units': 'C',
        },
        'CLO': {
            'value': 1720,
            'definition': 'Historical CO2 in lower ocean',
            'units': 'C',
        },
        'phi12': {
            'value': 0.024,
            'definition': 'Transfer rate atmosphere-ocean',
            'units': 'y^{-1}',
        },
        'phi23': {
            'value': 0.001,
            'definition': 'Transfer rate upper-lower ocean',
            'units': 'y^{-1}',
        },
        'Capacity': {
            'value': 1/0.098,
            'definition': 'Heat capacity atmosphere+upper ocean',
            'units': None,
        },
        'Capacity0': {
            'value': 3.52,
            'definition': 'Heat capacity lower ocean',
            'units': None,
        },
        'rhoAtmo': {
            'value': 3.681/3.1,
            'definition': 'radiative feedback parameter',
            'units': None,
        },
        'gammaAtmo': {
            'value': 0.0176,
            'definition': 'Heat exchange between layers',
            'units': None,
        },
        'T': {
            'value': 1,
            'definition': 'temperature anomaly of atmosphere',
            'units': 'Tc',
        },
        'T0': {
            'value': 1,
            'definition': 'temperature anomaly of ocean',
            'units': 'Tc',
        },
        'F': {
            'value': 3.6,
            'com': 'Radiative Forcing',
            'units': None,
        },
    },


    'GK-Improvements': {
        'B': {
            'value': 0,
            'definition': 'Capital in a buffer before being productive',
            'units': 'Units',
        },
        'lamb0': {
            'value': .95,
            'definition': 'Characteristic employement',
            'units': '',
        },
        'tauK': {
            'value': 0.01,
            'definition': 'typical time for capital to be effective',
            'units': 'y',
        },
        'taulamb': {
            'value': 0.01,
            'definition': 'typical time for capital to be effective',
            'units': '',
        },
        'flamb': {
            'value': 3.6,
            'definition': 'employement perception rate adjustment',
            'units': 'y^{-1}',
        },
        'beta': {
            'value': 0.1,
            'definition': 'Endogenous technical progress from growth',
            'units': '',
        },
        'zpi': {
            'value': 1,
            'definition': 'Influence of profit on salary negociation',
            'units': '',
        },
        'zsolv': {
            'value': 3.6,
            'definition': 'Influence of solvability on investment',
            'units': '',
        },
    },

}

# #############################################################################
# #############################################################################
#                   FIELDS OF FIELDS AND EXPECTED VALUES
# #############################################################################
# dict of default value in fields


__DEFAULTFIELDS = {
    'value': {
        'default': None,
        'type': (int, float, np.int_, np.float_, np.ndarray, list),
        'allowed': None,
    },
    'definition': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'com': {
        'default': 'No comment',
        'type': str,
        'allowed': None,
    },
    'dimension': {
        'default': 'undefined',
        'type': str,
        'allowed': None,
    },
    'units': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'Units',   # Any physical quantity of something (capital, ressources...)
            'y',       # Time
            '$',       # Money
            'C',       # Carbon Concentration
            'Tc',      # Temperature (Celsius)
            'Humans',  # Population
            'W',       # Energy
            'L',       # Length
            '',        # Dimensionless
        ],
    },
    'type': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'intensive',
            'extensive',
            'dimensionless',
        ],
    },
    'symbol': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'group': {
        'default': '',
        'type': str,
        'allowed': None,
    },
}


# --------------------
# Make sure the default is allowed
for k0, v0 in __DEFAULTFIELDS.items():
    if v0.get('allowed') is not None:
        __DEFAULTFIELDS[k0]['allowed'].append(v0['default'])


# ------------------------------------
# Derive new _DFIELDS from _LIBRARY

__LKLIB = [dict.fromkeys(v0.keys(), k0) for k0, v0 in _LIBRARY.items()]
for ii, dd in enumerate(__LKLIB[1:]):
    __LKLIB[0].update(dd)

_DFIELDS = {
    k0: dict(_LIBRARY[v0][k0]) for k0, v0 in __LKLIB[0].items()
}

for k0, v0 in __LKLIB[0].items():
    _DFIELDS[k0]['group'] = v0


# #############################################################################
# #############################################################################
#               Conformity checks (for safety, to detect typos...)
# #############################################################################


def _complete_DFIELDS(
    dfields=_DFIELDS,
    default_fields=__DEFAULTFIELDS,
    complete=__FILLDEFAULTVALUES,
    check=__DOTHECHECK,
):
    """ Complete dfields from default"""

    # --------------
    # run loop

    dfail = {}
    for k0, v0 in dfields.items():
        for k1, v1 in default_fields.items():

            # ---------
            # complete
            if complete and v0.get(k1) is None:
                # set symbol to key if not defined
                if k1 == 'symbol':
                    dfields[k0][k1] = k0
                else:
                    dfields[k0][k1] = default_fields[k1]['default']

            # ---------
            # check
            if check and v0.get(k1) is not None:

                # check type
                if not isinstance(v0[k1], default_fields[k1]['type']):
                    dfail[k0] = (
                        f"wrong type for {k1} "
                        f"({default_fields[k1]['type']} vs {type(v0[k1])})"
                    )

                # check allowed values
                elif default_fields[k1].get('allowed') is not None:

                    # treat units spearately
                    if k1 == 'units':
                        unit = v0[k1].split('.') if '.' in v0[k1] else [v0[k1]]

                        c0 = True
                        lok = default_fields[k1]['allowed']
                        for uu in unit:

                            # simple case
                            if '^{' not in uu:
                                if uu not in lok:
                                    c0 = False
                                    break
                                else:
                                    continue

                            # case with '^{'
                            if not uu.endswith('}'):
                                c0 = False
                                break

                            # check u0 is ok and u1 is a number
                            u0, u1 = uu.split('^{')
                            u1 = u1[:-1].split('.')
                            c0 = (
                                u0 in lok
                                and all([
                                    u11.strip('-').isdigit() for u11 in u1
                                ])
                            )
                            if not c0:
                                break

                    else:
                        c0 = v0[k1] in default_fields[k1]['allowed']

                    if not c0:
                        dfail[k0] = (
                            f"Non-allowed value for {k1} "
                            f"({default_fields[k1]['allowed']} vs {v0[k1]})"
                        )

    # --------------
    # Raise exception if relevant
    if len(dfail) > 0:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
        msg = (
            "The followinbg entries in _DFIELDS are not valid:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)


_complete_DFIELDS()
