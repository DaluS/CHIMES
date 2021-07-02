# -*- coding: utf-8 -*-
"""
PARAMETERS FOR GOODWIN-KEEN LIKE MODELS
"""


import numpy as np


_PARAMSET = 'v0'
_FLATTEN = True


# ---------
# NUMERICAL

# # -----------------
# # INITAL CONDITIONS 
# _DINIT = {
    # ### INTENSIVE VARIABLES 
    # 'd'      : v1*1.,
    # 'omega'  : v1*p['omega0'],
    # 'lambda' : v1*p['lambdamax'],
    # 't'      : v1*0,

    # ### INITIAL EXTENSIVE VARIABLES 
    # 'Y' : v1*1 , # GDP
    # 'N' : v1*1 , # Population
    # 'a' : v1*1 , # productivity
    # 'p' : v1*1 , # Price
# }
# ### DEDUCED FROM PREVIOUS ONES 
# ic['D'] = ic['d']*ic['Y']
# ic['K'] = ic['Y']*p['nu']
# ic['L'] = ic['lambda']*ic['N']
# ic['W'] = ic['omega']*ic['a']


# ##########################################
# PARAMETERS PARAMETERS 
_DEF_PARAM = {

    # --------------
    # Numerical
    'Tmax': {
        'value': 100,
        'com': 'Duration of simulation',
        'units': 't',
        'group': 'Numerical',
    },
    'Nx': {
        'value': 1,
        'com': 'Number of similar systems evolving in parrallel',
        'units': None,
        'group': 'Numerical',
    },
    'dt': {
        'value': 0.01,
        'com': 'Timestep (fixed timestep method)',
        'units': 't',
        'group': 'Numerical',
    },
    'Tstore': {
        'value': None,  # Dynamically allocated
        'com': 'Time between storages (if StorageMode=full, it goes to dt)',
        'units': None,
        'group': 'Numerical',
    },
    'Nt': {
        'value': None,  # Dynamically allocated
        'com': 'Number of temporal iteration',
        'units': None,
        'group': 'Numerical',
    },
    'Ns': {
        'value': None,  # Dynamically allocated
        'com': 'Number of elements stored',
        'units': None,
        'group': 'Numerical',
    },
    'verb': {
        'value': True,
        'com': 'flag indicating whether to print intermediate info',
        'units': None,
        'group': 'Numerical'
    },
    'storage': {
        'value': 'full',
        'com': 'flag indicating which time steps to store',
        'units': None,
        'group': 'Numerical'
    },
    'save': {
        'value': True,
        'com': 'flag indicating whether to save output data',
        'units': None,
        'group': 'Numerical'
    },

    # --------------
    # Population evolution 
    'beta': {
        'value': 0.025,
        'com': 'Rate of population growth',
        'units': 'y^-1',
        'group': 'Population',
    },
    'alpha': {
        'value': 0.02,
        'com': 'Rate of productivity increase',
        'units': 'y^-1',
        'group': 'Population',
    },

    # --------------
    # Capital properties
    'delta': {
        'value': 0.005,
        'com': 'Rate of capital depletion',
        'units': 'y^-1',
        'group': 'Capital',
    },

    # --------------
    # Production
    'nu': {
        'value': 3,
        'com': 'Kapital to output ratio', #' !! IN CES its 1/A !!',
        'units': None,
        'group': 'Production',
    },
    'eta': {
        'value': 1000,
        'com': '1/(1+substituability)', #CES parameter 
        'units': None,
        'group': 'Production',
    },
    'b': {
        'value': .5,
        'com': 'capital part of the production', #CES parameter 
        'units': None,
        'group': 'Production',
    },
    'z': {
        'value': 1,
        'com': 'Markup on salary estimation by employer',
        'units': None,
        'group': 'Production',
    },

    # --------------
    # INTEREST / Price
    'r': {
        'value': .03,
        'com': 'Interest at the bank',
        'units': 'y^{-1}',
        'group': 'Prices',
    },
    'etaP': {
        'value': .192,
        'com': 'Typical rate for inflation',
        'units': 'y^{-1}',
        'group': 'Prices',
    },
    'muP': {
        'value': 1.3,
        'com': 'Mark-up of price',
        'units': None,
        'group': 'Prices',
    },
    'gammaP': {
        'value': 1,
        'com': 'Money-illusion',
        'units': None,
        'group': 'Prices',
    },

    # --------------
    # PHILIPS CURVE (employement-salary increase)
    'phinul': {
        'value': 0.04,
        'com': (
            'Unemployement rate at which there is no salary increase '
            + 'with no inflation'
        ),
        'units': None,
        'group': 'Philips',
    },

    # --------------
    # KEEN INVESTMENT FUNCTION (profit-investment function)
    'k0': {
        'value': -0.0065,
        'com': '',
        'units': None,
        'group': 'Keen',
    },
    'k1': {
        'value': np.exp(-5),
        'com': '',
        'units': None,
        'group': 'Keen',
    },
    'k2': {
        'value': 20,
        'com': '',
        'units': None,
        'group': 'Keen',
    },

    # --------------
    # LINEAR DIVIDENT PROFITS 
    'div0': {
        'value': 0.138,
        'com': 'Part of GDP as dividends when pi=0',
        'units': None,
        'group': 'Dividends',
    },
    'div1': {
        'value': 0.473,
        'com': 'Slope',
        'units': None,
        'group': 'Dividends',
    },

    # --------------
    # Coupling Effets (EDP)
    'g1': {
        'value': .0,
        'com': 'GLOBAL EFFECTS OF LAMBDA (Mean field)',
        'units': None,
        'group': 'Coupling',
    },
    'g2': {
        'value': .00,
        'com': 'WITH NEIGHBORS EFFECTS OF LAMBDA (field)',
        'units': None,
        'group': 'Coupling',
    },
    'muI': {
        'value': 0.,
        'com': '',
        'units': "NOTDONEYET",
        'group': 'Coupling',
    },
    'muN': {
        'value': 0.,
        'com': '',
        'units': "NOTDONEYET",
        'group': 'Coupling',
    },

    # --------------
    # RELAXATION-BUFFER DYNAMICS
    'tauR': {
        'value': 2.0,
        'com': 'Typical time for recruitement',
        'units': 'y',
        'group': 'RelaxBuffer',
    },
    'tauF': {
        'value': 0.1,
        'com': 'Typical time for firing',
        'units': 'y',
        'group': 'RelaxBuffer',
    },
    'tauL': {
        'value': 2.,
        'com': 'Typical time for employement information',
        'units': 'y',
        'group': 'RelaxBuffer',
    },
    'tauK': {
        'value': 2.,
        'com': 'Typical time on new capital integration',
        'units': 'y',
        'group': 'RelaxBuffer',
    },

    # --------------
    # GEMMES PARAMETERS
    'theta': {
        'value': 2.6,
        'com': 'Convexity on abattement cost function',
        'units': None,
        'group': 'Gemmes',
    },
    'dsigma': {
        'value': -0.001,
        'com': 'Variation rate of the growth of emission intensity',
        'units': 'y^{-1}',
        'group': 'Gemmes',
    },
    'dPBS': {
        'value': -0.005,
        'com': 'Growth rate of back-stop technology price',
        'units': 'y^{-1}',
        'group': 'Gemmes',
    },
    'dEland': {
        'value': -0.022,
        'com': 'Growth rate of land use change in CO2 emission',
        'units': 'y^{-1}',
        'group': 'Gemmes',
    },

    # --------------
    # Damage function (on GDP)
    # D = 1 - (1 + p['pi1']*T + p['pi2']*T**2 + p['pi3']*T**p['zeta'] )**(-1)
    'pi1': {
        'value': 0.,
        'com': 'Linear temperature impact',
        'units': 'T^{-1}',
        'group': 'Damage',
    },
    'pi2': {
        'value': .00236,
        'com': 'Quadratic temperature impact',
        'units': 'T^{-2}',
        'group': 'Damage',
    },
    'pi3' : {
        'value': .00000507,
        'com': 'Weitzmann Damage temperature impact',
        'units': 'T^{-zeta}',
        'group': 'Damage',
    },
    'zeta': {
        'value': 6.754,
        'com': 'Weitzmann impact',
        'units': None,
        'group': 'Damage',
    },
    'fk': {
        'value': 1./3.,   # Dangerous not to put points 1./3. (Python 2 vis 3)
        'com': 'Fraction of environmental damage',
        'units': None,
        'group': 'Damage',
    },
                                # allocated to the stock of capital
    # --------------
    # Climate model
    'Phi12': {
        'value': .024,
        'com': 'Transfer of carbon from atmosphere to biosphere',
        'units': None,
        'group': 'Climate',
    },
    'Phi23': {
        'value': .001,
        'com': 'Transfer from biosphere to stock',
        'units': None,
        'group': 'Climate',
    },
    'C': {
        'value': 1/.098,
        'com': 'Heat capacity of fast-paced climate',
        'units': "SI",
        'group': 'Climate',
    },
    'C0': {
        'value': 3.52,
        'com': 'Heat capacity of inertial component of climate',
        'units': "SI",
        'group': 'Climate',
    },
    'gammaHEAT': {
        'value': 0.0176,
        'com': 'Heat exchange coefficient between layer',
        'units': None,
        'group': 'Climate',
    },
    'Tsens': {
        'value': 3.1,
        'com': 'Climate sensitivity (deltaT/log2CO2)',
        'units': 'T',
        'group': 'Climate',
    },

    'FexoMax': {
        'value': 0.7,
        'com': 'Maximal exougenous radiative forcing',
        'units': 'W M^{-2}',
        'group': 'Climate',
    },
    'F2CO2': {
        'value': 3.681,
        'com': 'doubling CO2 impact on forced radiations',
        'units': 'W/m2',
        'group': 'Climate',
    },

    'PopSat': {
        'value': 12,
        'com': 'Maximal population (billions)',
        'units': 'Humans',
        'group': 'Population',
    },

}


# #############################################################################
# #############################################################################
#                       Default  pre-sets of parameters
# #############################################################################


_DPARAM = {
    'v0': {k0: dict(v0) for k0, v0 in _DEF_PARAM.items()},
    'v1': {k0: dict(v0) for k0, v0 in _DEF_PARAM.items()},
    'GreatAuthor2019': {k0: dict(v0) for k0, v0 in _DEF_PARAM.items()},
}


# Modify
v0 = 'GreatAuthor2019'
_DPARAM[v0]['b'] = 0.
_DPARAM[v0]['eta'] = 0.192


# #############################################################################
# #############################################################################
#                       Utilities 
# #############################################################################


def _check_inputs(paramset=None):

    # paramset
    if paramset is None:
        paramset = _PARAMSET
    c0 = isinstance(paramset, str) and paramset in _DPARAM.keys()
    if not c0:
        ls = ['\t- {}'.format(kk) for kk in sorted(_DPARAM.keys())]
        msg = (
            "Arg paramset must be a valid predefined parameter set!\n"
            + "\n".join(ls)
            + "\nYou provided: {}".format(paramset)
        )
        raise Exception(msg)

    return paramset


# #############################################################################
# #############################################################################
#           Choose which version of the dict of parameters to use 
# #############################################################################


def get_params(paramset=None):
    """
    Create a dictionnary containing all the parameters necessary for simulation
    Their description is in comments.

    parameters
    ----------
    paramset:   None / str
        Flag indicating which predefined set of parameter to pick
        Defaults to 'v0'
    flatten:    None / bool
        Flag indicating whether to flatten the param dict
        Used for retro-compatibility
        Default to True

    """

    # ------------
    # Check inputs
    paramset = _check_inputs(
        paramset=paramset,
    )

    # ------------
    # Dictionnary of parameters (copy to avoid modifying the original)
    param = {k0: dict(v0) for k0, v0 in _DPARAM[paramset].items()}

    return param
