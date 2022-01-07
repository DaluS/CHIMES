

import os
import warnings


_PATH_HERE = os.path.dirname(__file__)


_DARTICLE = {
    'ref_short': "Great author, Coping 2015, A very famous journal",
    'ref_full': (
        "Author1, author 2, author3..., "
        "Very famous journal, "
        "year, issue, page"
    ),

    # dict for figures (key, link to png, name of routine)
    'dfigures': {
        2: {
            'model': 'model 1',
            'preset': 'a',
            'caption': '',
            'com': 'Trajectory',
            'png': 'fig02.png',
            'func': 'plot_fig02',
        },
        3: {
            'model': 'model 1',
            'preset': 'a',
            'caption': '',
            'com': 'Basin of attraction',
            'png': 'fig03.png',
            'func': 'plot_fig03',
        },
        5: {
            'model': 'model 2',
            'preset': 'c',
            'caption': '',
            'com': 'Blablabla',
            'png': 'fig05.png',
            'func': 'plot_fig05',
        },
    },
}


# #############################################################################
# #############################################################################
#                   Plotting routines (one per figure)
# #############################################################################


# ##############################
#       plot fig02
# ##############################


def plot_fig02(Hub=None):


    dax = None

    return dax


# ##############################
#       plot fig03
# ##############################


def plot_fig03(Hub=None):


    dax = None

    return dax


# ##############################
#       plot fig05
# ##############################


def plot_fig05(Hub=None):


    dax = None

    return dax


# #############################################################################
# #############################################################################
#                   Update plotting routines in dict
# #############################################################################


for k0, v0 in _DARTICLE['dfigures'].items():
    _DARTICLE['dfigures'][k0]['func'] = eval(v0['func'])
