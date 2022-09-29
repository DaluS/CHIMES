"""
DESCRIPTION :
    It is a two-sector model ( Household and Firm ), with salary negociation.
    There is no "money" explicitely (money and real units are equivalent), and there is no debt mechanism possible :
every sector is spending what they recieve

    The interesting things :
        * growth is an emergent propertie
        * Economic cycles (on employement and wage share) are an emergent propertie
        * trajectories are closed in the phasespace (lambda, omega) employement - wageshare

LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np
from pygemmes._models import Funcs


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'employment': {
            'func' : lambda employment, alpha,beta,delta,omega,nu: employment*( (1-omega)/nu - alpha - beta - delta),
            'com' : "reduced 2-var system",
        },
        'omega': {
            'func' : lambda omega, phillips,alpha: omega*(phillips-alpha),
            'com' : 'reduced 2-var system',
        },
    },

    # Intermediary relevant functions
    'statevar': {
        'phillips': Funcs.Phillips.div,
    },
    'parameter': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
