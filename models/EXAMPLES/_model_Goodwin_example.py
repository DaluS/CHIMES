"""A Goodwin model of an economy. Independant model file"""

from chimes.libraries import importmodel      # Import another model _LOGICS, _PRESETS
from chimes.libraries import Operators as O   # Prewritten operators for multisectoral and multiregional coupling. `chm.get_available_Operators()`
from chimes.libraries import fill_dimensions   # When using multisectoral dynamics, fill automatically the sizes of fields
from chimes.libraries import merge_model       # Merge two model logics into each others
from chimes.libraries import Funcs            # Prewritten functions from CHIMES use `chm.get_available_Functions()`
import numpy as np                    


_DESCRIPTION = """
## What is this model ?
A Goodwin is a two-sector model of an economy : household and firms. 
The growth is endogenous, but eventually driven by technical automatization and population growth
It share many points with a Solow and and Ramsay model of growth. 
The main difference is that this model is able to explore out of equilibrium without exploding.
To do so, the wages (and thus consumption) is driven by a long causal chain: a short-run Phillips curve.
The higher the employment, the faster wages grows. 

## Expected behavior
* When looking at the causal variables (K,w) it looks like an exponential with oscillations.
* When looking at the dimensionless state variables (employment,wage share "omega"), it is just sustaining oscillations.
* The further from the equilibrium, the bigger and slower the oscillations
* The dimensionless oscillations should not grow or shrink

## Why is it interesting ? 
The Goodwin model has been over the years an excellent platform for more complex models, as it can be:
* Stock-flow consistent both physically and nominally
* Have inventory and debt fluctuations
* Naturally englobe business cycles
* Work out of equilibrium 
* Add sectors, be disaggregated... 
* Any endogenization effect can be easily read as it either stabilize, destabilize, change the cycles and equilibrium point
* None of the hypothesis is central and they can all be changed

## The predatory-prey aspect
One can study the "reduced" form of the system, rewriting the equations with the derivatives on employment and wage share is 
giving a system of 2 equations, similar to a Lotka-Volterra system in population dynamics, also called "predatory-prey".
In consequence, a part of the community assumed that some where the predators (capital) and prey (workers), giving the model 
a "class struggle" political coloration and making it overlooked by many. 
A Lotka-Volterra system is a non-linear oscillator that do not know what is his equilibrium. 

## What is different from the paper ?
We use a slightly different variable convention. There is a constant inflation, and productivity is here a/nu. 
a is used for labor efficiency (number of capital unit per worker)

## What is particular with this model file ? 
It has been written to have a full description inside the model file, and thus is not using the default library inside CHIMES. 
It is a good example to follow if you want to do something fully commented and fully independant.
You can check the file `_model_Goodwin.py` for the short version relying on the library


"""

_TODO = ['Write the equilibrium position in supplements']
_ARTICLE = "https://link.springer.com/chapter/10.1007/978-1-349-05504-3_12"
_DATE = "2023/11/17"
_CODER = "Paul Valcke"
_KEYWORDS = ['Tutorial', 'Documentation', 'Goodwin', 'Economics', 'Oscillations', 'Monosectoral']
_UNITS = ['y',        # Time
          '$',        # Money
          'Units',    # Physical
          'Humans']   # Humans

_LOGICS = {
    'differential': {  # Differential variables are defined by their time derivative and not their value
        'p': {
            'initial': 1.0,
            'func': lambda p, inflation: p*inflation,  # equivalent to dp/dt = p*inflation
            'definition': 'nominal value per physical unit produced',
            'com': 'Consequence of causal inflation',
            'units': '$.Units^{-1}',
            'symbol': '$p$', },
        'a': {
            'func': lambda a, alpha: a*alpha,
            'initial': 3.0,
            'definition': 'Automatisation level',
            'com': 'exogenous',
            'units': 'Units.Humans^{-1}',
            'symbol': '$a$', },
        'N': {
            'func': lambda N, n: N*n,
            'initial': 1.0,
            'definition': 'Worker pool',
            'com': 'exogenous exponential',
            'units': 'Humans',
            'symbol': '$N$', },
        'K': {
            'func': lambda K, Ir, delta: Ir-delta*K,
            'initial': 2,
            'definition': 'Capital in real units',
            'com': 'Investment - dpreciation dynamics',
            'units': 'Units',
            'symbol': '$K$', },
        'w': {
            'func': lambda w, phillips: w*phillips,
            'initial': 0.85,
            'definition': 'individual wage value',
            'com': 'short-run Phillips dynamics',
            'units': '$.Humans^{-1}.y^{-1}',
            'symbol': '$w$', },
    },
    'statevar': {  # State variables value are defined by their logic
        'pi': {
            'func': lambda p, Y, Pi: Pi / (p*Y),
            'definition': 'relative profit',
            'com': 'its definition',
            'units': '',
            'symbol': r'$\pi$', },
        'omega': {
            'func': lambda p, Y, w, L: w*L/(p*Y),
            'definition': 'wage share',
            'com': 'its definition',
            'units': '',
            'symbol': r'$\omega$', },
        'employment': {
            'func': lambda L, N: L/N,
            'definition': 'employment rate',
            'com': 'its definition',
            'units': '',
            'symbol': r'$\lambda$', },
        'g': {
            'func': lambda Ir, K, delta: Ir/K-delta,
            'definition': 'Relative growth of GDP',
            'com': 'manually calculated',
            'units': 'y^{-1}',
            'symbol': '$g$', },
        'Y': {
            'func': lambda K, nu: K/nu,
            'definition': 'GDP in real units',
            'com': 'Leontiev optimized on labor',
            'units': 'Units.y^{-1}',
            'symbol': '$Y$', },
        'Pi': {
            'func': lambda p, Y, w, L: p*Y-w*L,
            'definition': 'Absolute profit',
            'com': 'definition without depreciation',
            'units': '$.y^{-1}',
            'symbol': r'$\Pi$', },
        'C': {
            'func': lambda Y, Ir: Y-Ir,
            'definition': 'flux of goods for household',
            'com': 'Consumption as full salary',
            'units': 'Units.y^{-1}',
            'symbol': '$C$', },
        'Ir': {
            'func': lambda Pi, p: Pi/p,
            'definition': 'Number of real unit from investment',
            'com': 'Profit reinvested',
            'units': 'Units.y^{-1}',
            'symbol': '$Ir$', },
        'L': {
            'func': lambda K, a: K/a,
            'definition': 'Workers',
            'com': 'from automatisation definition',
            'units': 'Humans',
            'symbol': '$L$', },

        'phillips': {
            'func': lambda Phi0, Phi1, employment: Phi0+Phi1/(1-employment)**2,
            'definition': 'Wage inflation rate',
            'com': 'DIVERGING PHILLIPS CURVE',
            'units': 'y^{-1}',
            'symbol': r'$\phi$', },
    },
    'parameter': {
        'inflation': {
            'value': 0,
            'definition': 'inflation rate',
            'units': 'y^{-1}',
            'symbol': '$i$', },
        'alpha': {
            'value': 0.02,
            'definition': 'Rate of productivity increase',
            'units': 'y^{-1}',
            'symbol': r'$\alpha$', },
        'n': {
            'value': 0.025,
            'definition': 'Rate of population growth',
            'units': 'y^{-1}',
            'symbol': '$n$', },
        'delta': {
            'value': 0.005,
            'definition': 'Rate of capital depletion',
            'units': 'y^{-1}',
            'symbol': r'$\delta$', },
        'nu': {
            'value': 3,
            'definition': 'Capital to output ratio',
            'units': 'y',
            'symbol': r'$\nu$', },

        'Phi0': {
            'value': -0.292,
            'definition': 'wage reduction rate when full unemployement',
            'units': 'y^{-1}',
            'symbol': r'$\Phi_0$', },
        'Phi1': {
            'value': 0.05,
            'definition': 'wage rate dependance to unemployement',
            'units': 'y^{-1}',
            'symbol': r'$\Phi_1$', },
    },
}


def Equilibrium_fromparam(hub):
    """
    For a Goodwin model, will analytically find the equilibrium position
    """
    R = hub.get_dfields()

    nu = R['nu']['value'][:, 0, 0, 0]
    delta = R['delta']['value'][:, 0, 0, 0]
    alpha = R['alpha']['value'][:, 0, 0, 0]
    n = R['n']['value'][:, 0, 0, 0]

    Phi1 = R['Phi1']['value'][:, 0, 0, 0]
    Phi0 = R['Phi0']['value'][:, 0, 0, 0]
    inflation = R['inflation']['value'][:, 0, 0, 0]

    omegaeq = 1 - nu*(delta + alpha + n)

    def fm1(x): return np.sqrt(1-x)
    lambdaeq = fm1(-Phi1/(Phi0+alpha+inflation))

    return {'employment': lambdaeq,
            'omega': omegaeq}


def K_w_for_lambdaomega(hub, employment, omega):
    """ 
    One might want to initiate its system at a certain value of employment(lambda) and wage share(omega).
    The system deduces the right value of K and w to ensure such characteristics
    """
    R = hub.get_dfields()

    a = R['a']['value'][0, :, 0, 0, 0]
    N = R['N']['value'][0, :, 0, 0, 0]
    nu = R['nu']['value'][:, 0, 0, 0]
    p = R['p']['value'][0, :, 0, 0, 0]

    return {'K': employment*N*a,
            'w': omega*p*a/nu}


_SUPPLEMENTS = {
    'Equilibrium_fromparam': Equilibrium_fromparam,
    'K_w_for_lambdaomega': K_w_for_lambdaomega
}

_PRESETS = {
    'startatequilibrium': {
        'fields': {
            'K': 1.84955252,
            'w': .85,
        },
        'com': """equilibrium is here when the employemnt and wage share are constant.
        On this case, we force the system to naturally start there. Only exponential growth should be observed
        """,
        'plots': {'nyaxis': [{'x': 'time',
                              'y': [['employment', 'omega'],
                                    ['K'],
                                    ],
                              'idx': 0,
                              'title': '',
                              'lw': 1}],
                  'byunits': [{}],
                  },
    },
    'Farfromequilibrium': {
        'fields': {
            'K': 2.6,
            'w': .85,
        },
        'com': """This run start far from the equilibrium point, and the will oscillate slowly""",
        'plots': {'nyaxis': [{'x': 'time',
                              'y': [['employment', 'omega'],
                                    ['K'],
                                    ],
                              'idx': 0,
                              'title': '',
                              'lw': 1}],
                  'XYZ': [{'x': 'employment',
                           'y': 'omega',
                           'z': 'time',
                           'color': 'pi',
                           'idx': 0,
                           'title': ''}],
                  'byunits': [],
                  },
    },
    'Parrallel runs': {
        'fields': {
            'nx': 10,
            'K': np.linspace(1.84955252, 2.6, 10),
            'w': .85
        },
        'com': """This run makes 10 system in parrallel, that do not interact. 
        The first is the "startatequilibrium and the last "Farfromequilibrium".
        The one in the middle are linear combination of the two initial conditions.""",
        'plots': {'byunits': [{'idx': 0, 'filters_units': ['']},
                              {'idx': 5, 'filters_units': ['']},
                              {'idx': 9, 'filters_units': ['']}],
                  'var': [{'key': 'omega', 'mode': 'sensitivity'}],
                  'cycles_characteristics': [{}]}
    }
}
