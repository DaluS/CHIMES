# -*- coding: utf-8 -*-
"""
FUNCTIONS POOL FOR SIMULATIONS

All the functions are stocked in _DFUNC.
None is the default value if the key has no meaning for the parameter
    Each parameter is a dictionary, with the following keys :
    'KEY': {                            # KEY THE CODE WILL USE TO CALL IT
        'func': callable,               # the function itself
        'com': '',                      # Comment about what it means
        'dimension': 'time',            # Physical dimension if relevant
        'units': 'y',                   # Physical units if relevant
        'type': None,                   # Intensive or extensive
        'symbol': None,                 # Plot-friendly name (Latex)
    },

###############################

PARAMETERS :
    _FUNCSET     : Name of the set of default parameter set taken by the system. 
    _DALLOWED    : List of types and dimensions accepted by the system (with None)
    _DEF_FUNC    : All the informations about useful parameters
    _dfail       : Parameters that couldn't get loaded because incomplete
    _lkeys       : List of attributes necessary for a parameter to be added
    _DFUNC       : Presets of parameters !!! NOT CODED FOR THE MOMENT

FUNCTIONS:
    _check_inputs: Check if the the input of the user is in term of format
    get_function   : Description linked to the function

"""


import numpy as np


_FUNCSET = 'v0'


# ##########################################
# ##########################################
#       Default functions
# ##########################################


# !!! All function must have keyword arguments, no positional arguments !!!


def pi(omega=None, r=None, d=None):
    """  """
    return 1 - omega - r*d


def Pi(Y=None, W=None, L=None, r=None, D=None):
    """  """
    return Y - W*L - r*D


def g(omega=None, nu=None, delta=None):
    """ """
    return (1 - omega) / nu - delta


def philips(phi0=None, phi1=None, lambd=None):
    """ """
    return - phi0 + phi1 / (1-lambd)**2


def worker(K=None, a=None, nu=None):
    """ """
    return K / (a * nu)


def lambd(L=None, N=None):
    """ """
    return L / N


def omega(W=None, L=None, Y=None):
    """ """
    return W * L / Y


def d(D=None, Y=None):
    """ """
    return D / Y


def GDP(K=None, nu=None):
    """ """
    return K / nu


def invest(Y=None, kappa=None):
    """ """
    return Y * kappa


def kappa(k0=None, k1=None, k2=None, pi=None):
    """ """
    return k0 + k1 * np.exp(k2*pi)


# ##########################################
# ##########################################
#       Dict of functions
# ##########################################


_DFUNC = {
    'GK': {
        'pi': {
            'func': pi,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$\pi$',
        },
        'Pi': {
            'func': Pi,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$\Pi$',
        },
        'g': {
            'func': g,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$g$',
        },
        'philips': {
            'func': philips,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$\phi$',
        },
        'worker': {
            'func': worker,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': '',
        },
        'lambd': {
            'func':lambd ,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': '',
        },
        'omega': {
            'func': omega,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$\omega$',
        },
        'd': {
            'func': d,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$d$',
        },
        'GDP': {
            'func': GDP,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$GDP$',
        },
        'invest': {
            'func': invest,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': '',
        },
        'kappa': {
            'func': kappa,
            'com': '',
            'dimension': '',
            'units': '',
            'type': '',
            'symbol': r'$\kappa$',
        },
    },
}


# #############################################################################
# #############################################################################
#                       Getting the choosen set of functions
# #############################################################################


def get_functions(funcset=None):
    """ Return a dict of variables """
    c0 = funcset in _DFUNC.keys()
    if c0 is not True:
        lstr = [
            "\t- '{}': {}".format(k0, sorted(v0.keys()))
            for k0, v0 in _DFUNC.items()
        ]
        msg = (
            "Arg varset must be a valid key to an existing set of functions!\n"
            + "\n".join(lstr)
            + "\nYou provided: {}".format(funcset)
        )
        raise Exception(msg)
    return _DFUNC[funcset]
