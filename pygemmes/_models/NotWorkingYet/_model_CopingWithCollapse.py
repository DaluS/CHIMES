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

# ---------------------------
# user-defined function order (optional)
_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        # ATMOSPHERE ODE
        'CO2AT': {
            'func': lambda Emission=0, phi12=0, CO2UP=0, CUP=1, CAT=1, itself = 0: Emission - phi12*itself + phi12*CAT/CUP*CO2UP,
            'com': '3Layer Matrix coupling + Emission',
        },
        'CO2UP': {
            'func': lambda phi12=0, phi23=0, CAT=1, CUP=1, CLO=1, CO2AT=0, itself=0, CO2LO=0: phi12*CO2AT - itself*(phi12*CAT/CUP-phi23) + phi23*CUP/CLO*CO2LO,
            'com': '3Layer Matrix coupling',
        },
        'CO2LO': {
            'func': lambda phi23=0, CO2UP=0, CUP=1, CLO=1, itself = 0: phi23*CO2UP - phi23*CUP/CLO*itself,
            'com': '3Layer Matrix coupling',
        },
        'T': {
            'func': lambda F=0, rhoAtmo=0, itself=0, gammaAtmo=0, T0=0, Capacity=1: (F - rhoAtmo*itself - gammaAtmo*(itself-T0))/Capacity,
            'com': 'Forcing + dissipation + transfert to lower',
        },
        'T0': {
            'func': lambda gammaAtmo=0, T=0, itself=0, Capacity0=1: (gammaAtmo*(T-itself))/Capacity0,
            'com': 'Transfer from atmosphere',
        },
        # 'pseudot': {
        #    'func': lambda: 1,
        #    'com': 'false time because practical',
        #    'initial': 0,
        #    'units': 'y'
        # },

        # COUPLING ODE
        'gsigmaEm': {
            'func': lambda itself=0, deltagsigmaEm=0: itself*deltagsigmaEm,
            'com': 'Evolution of emission rate growth rate',
        },
        'sigmaEm': {
            'func': lambda itself=0, gsigmaEm=0: itself*gsigmaEm,
            'com': 'Emission intensity dynamics',
        },
        'Eland': {
            'func': lambda itself=0, deltaEland=0: itself*deltaEland,
            'com': 'Exogenous land emission'
        },

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
            'func': lambda I=0, itself=0, delta=0, p=1: I/p - itself * delta,
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

        # Prices
        'pbackstop': {
            'func': lambda itself=0, deltapbackstop=0: itself*deltapbackstop,
            'com': 'exogenous backstop price on exponential'
        },
        'pcarbon': {
            'func': lambda itself=0, deltapcarbon=0: itself*deltapcarbon,
            'com': 'Exogenous carbon price on exponential'
        },
        'p': {
            'func': lambda itself=0, inflation=0: itself * inflation,
            'com': 'price defined by inflation',
        },
    },





    'statevar': {
        # ATMOSPHERE STATE VARIABLES
        'F': {
            'func': lambda F2CO2=0, CO2AT=1, CAT=1: F2CO2 / np.log(2) * np.log(CO2AT/CAT),
            'com': 'Temperature forcing from CO2 + sensitivity',
        },

        # ECONOMIC STATE VARIABLES
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
        'GDP': {
            'func': lambda Y=0, p=0: Y * p,
            'com': 'Output with selling price ',
        },
        'inflation': {
            'func': lambda mu=0, eta=0, c=0: eta*(mu*c-1),
            'com': 'markup dynamics',
        },
        'c': {
            'func': lambda Abattement=0, Dy=0, omega=0: omega/((1-Abattement)*(1-Dy)),
            'com': 'Unitary cost taking loss of production'
        },
        'lambda': {
            'func': lambda L=0, N=1: L / N,
            'com': 'employement rate as statevar by ratio',
        },
        'omega': {
            'func': lambda w=0, L=0, Y=1, p=1: (w * L) / (Y*p),
            'com': 'wage share by ratio as statevar',
        },
        'I': {
            'func': lambda GDP=0, kappa=0: GDP * kappa,
            'com': 'Investment value from kappa function',
        },
        'd': {
            'func': lambda D=0, GDP=1: D / GDP,
            'com': 'private debt ratio as statevar',
        },
        'pi': {
            'func': lambda Pi=0, GDP=1: Pi/GDP,
            'com': 'relative profit by ratio as statevar',
        },


        # BEHAVIORAL PARAMETRIC FUNCTIONS
        'phillips': {
            'func': lambda philinConst=0, philinSlope=0, lamb=0: philinConst + philinSlope * lamb,
            'com': 'Linear Philips curve',
        },
        'kappa': {
            'func': lambda kappalinConst=0, kappalinSlope=0, pi=0, kappalinMin=0, kappalinMax=0: np.clip(kappalinConst + kappalinConst * pi, kappalinMin, kappalinMax),
            'com': 'Relative GDP investment through relative profit',
        },
        'Sh': {
            'func': lambda divlinSlope=0, divlinconst=0, pi=0, GDP=0, divlinMin=0, divlinMax=0: np.clip(GDP*(divlinSlope*pi+divlinconst), divlinMin, divlinMax),
            'com': 'Affine shareholding dividends dependency'
        },
        'Emission': {
            'func': lambda Eind=0, Eland=0: Eind+Eland,
            'com': 'Total CO2 emission',
        },
        'Eind': {
            'func': lambda Y0=0, sigmaEm=0, n=0: Y0*sigmaEm*(1-n),
            'com': 'Emission of the industry',
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
        'Abattement': {
            'func': lambda sigmaEm=0, pbackstop=0, emissionreductionrate=0, convexitycost=1: sigmaEm*pbackstop*(emissionreductionrate**convexitycost)/convexitycost,
            'com': 'emission reduction rate Abattement'
        },
        'emissionreductionrate': {
            'func': lambda pcarbon=0, pbackstop=1, convexitycost=1: np.minimum((pcarbon/pbackstop)**(1/(convexitycost)), 1),
            'com': 'choice of emission reduction rate weird',
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
