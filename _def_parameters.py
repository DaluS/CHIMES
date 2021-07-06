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

_DALLOWED = {
    'dimension': ['time', 'time rate', 'temperature rate'],
    'type': ['intensive', 'extensive'],
}


# ##########################################
# PARAMETERS PARAMETERS
_DEF_PARAM = {

    # --------------
    # Numerical
    'Tmax': {
        'value': 100,
        'name': 'time steps',
        'com': 'Duration of simulation',
        'dimension': 'time',
        'units': 'y',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'Nx': {
        'value': 1,
        'name': None,
        'com': 'Number of similar systems evolving in parrallel',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'dt': {
        'value': 0.01,
        'name': None,
        'com': 'Time step (fixed timestep method)',
        'dimension': 'time',
        'units': 't',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'Tstore': {
        'value': None,  # Dynamically allocated
        'name': None,
        'com': 'Time between storages (if StorageMode=full, it goes to dt)',
        'dimension': 'time',
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'Nt': {
        'value': None,  # Dynamically allocated
        'name': None,
        'com': 'Number of temporal iteration',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'Ns': {
        'value': None,  # Dynamically allocated
        'name': None,
        'com': 'Number of elements stored',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'verb': {
        'value': True,
        'name': None,
        'com': 'flag indicating whether to print intermediate info',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical'
    },
    'storage': {
        'value': 'full',
        'name': None,
        'com': 'flag indicating which time steps to store',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical'
    },
    'save': {
        'value': True,
        'name': None,
        'com': 'flag indicating whether to save output data',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical'
    },

    # --------------
    # Population evolution
    'beta': {
        'value': 0.025,
        'name': None,
        'com': 'Rate of population growth',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$beta$',
        'group': 'Population',
    },
    'alpha': {
        'value': 0.02,
        'name': None,
        'com': 'Rate of productivity increase',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$alpha$',
        'group': 'Population',
    },

    # --------------
    # Capital properties
    'delta': {
        'value': 0.005,
        'name': None,
        'com': 'Rate of capital depletion',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta$',
        'group': 'Capital',
    },

    # --------------
    # Production
    'nu': {
        'value': 3,
        'name': None,
        'com': 'Kapital to output ratio',   # !! IN CES its 1/A !!',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'\nu',
        'group': 'Production',
    },
    'eta': {
        'value': 1000,
        'name': None,
        'com': '1/(1+substituability)',     # CES parameter
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },
    'b': {
        'value': .5,
        'name': None,
        'com': 'capital part of the production',    # CES parameter
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },
    'z': {
        'value': 1,
        'name': None,
        'com': 'Markup on salary estimation by employer',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },

    # --------------
    # INTEREST / Price
    'r': {
        'value': .03,
        'name': None,
        'com': 'Interest at the bank',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'etaP': {
        'value': .192,
        'name': None,
        'com': 'Typical rate for inflation',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'muP': {
        'value': 1.3,
        'name': None,
        'com': 'Mark-up of price',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'gammaP': {
        'value': 1,
        'name': None,
        'com': 'Money-illusion',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },

    # --------------
    # PHILIPS CURVE (employement-salary increase)
    'phinul': {
        'value': 0.04,
        'name': None,
        'com': 'Unemployment rate that stops salary increase (no inflation)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },

    # --------------
    # KEEN INVESTMENT FUNCTION (profit-investment function)
    'k0': {
        'value': -0.0065,
        'name': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_0$',
        'group': 'Keen',
    },
    'k1': {
        'value': np.exp(-5),
        'name': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_1$',
        'group': 'Keen',
    },
    'k2': {
        'value': 20,
        'name': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_2$',
        'group': 'Keen',
    },

    # --------------
    # LINEAR DIVIDENT PROFITS
    'div0': {
        'value': 0.138,
        'name': None,
        'com': 'Part of GDP as dividends when pi=0',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$div_0$',
        'group': 'Dividends',
    },
    'div1': {
        'value': 0.473,
        'name': None,
        'com': 'Slope',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$div_1$',
        'group': 'Dividends',
    },

    # --------------
    # Coupling Effets (EDP)
    'g1': {
        'value': .0,
        'name': None,
        'com': 'GLOBAL EFFECTS OF LAMBDA (Mean field)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$g_1$',
        'group': 'Coupling',
    },
    'g2': {
        'value': .00,
        'name': None,
        'com': 'WITH NEIGHBORS EFFECTS OF LAMBDA (field)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$g_2$',
        'group': 'Coupling',
    },
    'muI': {
        'value': 0.,
        'name': None,
        'com': '',
        'dimension': None,
        'units': "NOTDONEYET",
        'type': 'intensive',
        'symbol': r'$_mu_I$',
        'group': 'Coupling',
    },
    'muN': {
        'value': 0.,
        'name': None,
        'com': '',
        'dimension': None,
        'units': "NOTDONEYET",
        'type': 'intensive',
        'symbol': r'$\mu_N$',
        'group': 'Coupling',
    },

    # --------------
    # RELAXATION-BUFFER DYNAMICS
    'tauR': {
        'value': 2.0,
        'name': None,
        'com': 'Typical time for recruitement',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_R$',
        'group': 'RelaxBuffer',
    },
    'tauF': {
        'value': 0.1,
        'name': None,
        'com': 'Typical time for firing',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_F$',
        'group': 'RelaxBuffer',
    },
    'tauL': {
        'value': 2.,
        'name': None,
        'com': 'Typical time for employement information',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$tau_L$',
        'group': 'RelaxBuffer',
    },
    'tauK': {
        'value': 2.,
        'name': None,
        'com': 'Typical time on new capital integration',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_K$',
        'group': 'RelaxBuffer',
    },

    # --------------
    # GEMMES PARAMETERS
    'theta': {
        'value': 2.6,
        'name': None,
        'com': 'Convexity on abattement cost function',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\theta$',
        'group': 'Gemmes',
    },
    'dsigma': {
        'value': -0.001,
        'name': None,
        'com': 'Variation rate of the growth of emission intensity',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{\sigma}$',
        'group': 'Gemmes',
    },
    'dPBS': {
        'value': -0.005,
        'name': None,
        'com': 'Growth rate of back-stop technology price',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{PBS}$',
        'group': 'Gemmes',
    },
    'dEland': {
        'value': -0.022,
        'name': None,
        'com': 'Growth rate of land use change in CO2 emission',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{Eland}$',
        'group': 'Gemmes',
    },

    # --------------
    # Damage function (on GDP)
    # D = 1 - (1 + p['pi1']*T + p['pi2']*T**2 + p['pi3']*T**p['zeta'] )**(-1)
    'pi1': {
        'value': 0.,
        'name': None,
        'com': 'Linear temperature impact',
        'dimension': 'temperature rate',
        'units': 'T^{-1}',
        'type': 'intensive',
        'symbol': r'$\pi_1$',
        'group': 'Damage',
    },
    'pi2': {
        'value': .00236,
        'name': None,
        'com': 'Quadratic temperature impact',
        'dimension': None,
        'units': 'T^{-2}',
        'type': 'intensive',
        'symbol': r'$\pi_2$',
        'group': 'Damage',
    },
    'pi3': {
        'value': .00000507,
        'name': None,
        'com': 'Weitzmann Damage temperature impact',
        'dimension': None,
        'units': 'T^{-zeta}',
        'type': 'intensive',
        'symbol': r'$\pi_3$',
        'group': 'Damage',
    },
    'zeta': {
        'value': 6.754,
        'name': None,
        'com': 'Weitzmann impact',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\zeta$',
        'group': 'Damage',
    },
    'fk': {
        'value': 1. / 3.,
        'name': None,
        'com': 'Fraction of environmental damage',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$f_K$',
        'group': 'Damage',
    },

    # allocated to the stock of capital

    # --------------
    # Climate model
    'Phi12': {
        'value': .024,
        'name': None,
        'com': 'Transfer of carbon from atmosphere to biosphere',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_{1\rightarrow2}$',
        'group': 'Climate',
    },
    'Phi23': {
        'value': .001,
        'name': None,
        'com': 'Transfer from biosphere to stock',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_{2\rightarrow3}$',
        'group': 'Climate',
    },
    'C': {
        'value': 1 / .098,
        'name': None,
        'com': 'Heat capacity of fast-paced climate',
        'dimension': None,
        'units': "SI",
        'type': 'intensive',
        'symbol': r'$C$',
        'group': 'Climate',
    },
    'C0': {
        'value': 3.52,
        'name': None,
        'com': 'Heat capacity of inertial component of climate',
        'dimension': None,
        'units': "SI",
        'type': 'intensive',
        'symbol': r'$C_0$',
        'group': 'Climate',
    },
    'gammaHEAT': {
        'value': 0.0176,
        'name': None,
        'com': 'Heat exchange coefficient between layer',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\gamma_{heat}$',
        'group': 'Climate',
    },
    'Tsens': {
        'value': 3.1,
        'name': None,
        'com': 'Climate sensitivity (deltaT/log2CO2)',
        'dimension': None,
        'units': 'T',
        'type': 'intensive',
        'symbol': r'$T_{sens}$',
        'group': 'Climate',
    },

    'FexoMax': {
        'value': 0.7,
        'name': None,
        'com': 'Maximal exougenous radiative forcing',
        'dimension': None,
        'units': 'W M^{-2}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Climate',
    },
    'F2CO2': {
        'value': 3.681,
        'name': None,
        'com': 'doubling CO2 impact on forced radiations',
        'dimension': None,
        'units': 'W/m2',
        'type': 'intensive',
        'symbol': r'$F^2_{CO2}$',
        'group': 'Climate',
    },

    'PopSat': {
        'value': 12,
        'name': None,
        'com': 'Maximal population (billions)',
        'dimension': None,
        'units': 'Humans',
        'type': 'intensive',
        'symbol': r'$N_{sat}$',
        'group': 'Population',
    },

}


# #############################################################################
# #############################################################################
#       _DEF_PARAM: Fill in default values and check conformity
# #############################################################################

_dfail = {}
_lkeys = [
    'value', 'name', 'com', 'dimension', 'units', 'type', 'symbol', 'group',
]
for k0, v0 in _DEF_PARAM.items():

    # Check existence of keys
    lout = [ss for ss in _lkeys if ss not in v0.keys()]
    if len(lout) > 0:
        _dfail[k0] = f"missing keys: {lout}"
        continue

    # If com if filled but not name, use com to fill name (and vice-versa)
    if v0['name'] is None and v0['com'] is not None:
        _DEF_PARAM[k0]['name'] = v0['com']
    elif v0['name'] is not None and v0['com'] is None:
        _DEF_PARAM[k0]['com'] = v0['name']

    # Try to spot any typo / mistake
    if v0['dimension'] not in _DALLOWED['dimension'] + [None]:
        _dfail[k0] = f"Non-conform dimension! ({v0['dimension']})"
    if v0['type'] not in _DALLOWED['type'] + [None]:
        _dfail[k0] = f"Non-conform type! ({v0['type']})"


if len(_dfail) > 0:
    lstr = [f"\t- {k0}: {v0}" for k0, v0 in _dfail.items()]
    msg = (
        "The following non-conformities have been spotted:\n"
        + "\n".join(lstr)
    )
    raise Exception(msg)


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
