'''Goodwin-Keen with Endogenous technical progress'''

from chimes.libraries import Funcs, importmodel, merge_model
from chimes.libraries import Operators as O
import numpy as np
_DESCRIPTION = """
DESCRIPTION :

    This is a small modificaiton of Goodwin-Keen. Assume that labour productivity (parameter a in our basic model) is not exogenous
    but depends upon the growth rate of investment (in R & D). This leads to adding the following equation:
    dot(a) / a = alpha + beta * g

TYPICAL BEHAVIOR: Locally Unstable, the good equilibrium is an unstable focuse

@author: Weiye Zhu
"""


# ######################## PRELIMINARY ELEMENTS #########################

# ######################## LOGICS #######################################
_LOGICS, _PRESETS0, _SUPPLEMENTS_GK = importmodel('GK')
_GKEndo_LOGICS = {
    'differential': {
        # Endogenous Labor Productivity
        'a': {
            'func': lambda a, alpha, beta, g: a * (alpha + beta * g),
            'com': 'Labor Productivity depends on investment', },
    }
}

_LOGICS = merge_model(_LOGICS, _GKEndo_LOGICS, verb=False)

_SUPPLEMENTS = {}
_PRESETS = _PRESETS0
