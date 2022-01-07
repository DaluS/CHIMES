

import os
import warnings


import matplotlib.pyplot as plt


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
            'model': 'Goodwin-Reduced',
            'preset': 'smallcycle',
            'caption': '',
            'com': 'Trajectory',
            'png': 'fig02.png',
            'func': 'plot_fig02',
        },
        3: {
            'model': 'Goodwin-Reduced',
            'preset': 'bigcycle',
            'caption': '',
            'com': 'Basin of attraction',
            'png': 'fig03.png',
            'func': 'plot_fig03',
        },
        5: {
            'model': 'Goodwin',
            'preset': 'default',
            'caption': '',
            'com': 'Blablabla',
            'png': 'fig05.png',
            'func': 'plot_fig05',
        },
        6: {
            'model': 'Goodwin',
            'preset': 'default',
            'caption': '',
            'com': 'Blablabla',
            'png': 'fig05.png',
            'func': 'plot_fig06',
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


def plot_fig02(hub=None):
    """ The objective here is to reproduce the original figure
    """

    # --------------------
    # Get data of interest

    x = hub.dparam['lambda']['value'][:, 0]
    y = hub.dparam['omega']['value'][:, 0]

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(8, 5))

    ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8], aspect='equal')
    ax0.set_xlabel('x (units)')
    ax0.set_ylabel('y (units)')
    ax0.set_title('title', size=12, fontweight='bold')

    dax = {'blabla': ax0}

    # ---------
    # plot data

    kax = 'blabla'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.plot(x, y)

    return dax


# ##############################
#       plot fig03
# ##############################


def plot_fig03(hub=None):


    dax = None

    return dax


# ##############################
#       plot fig05
# ##############################


def plot_fig05(hub=None):


    dax = None

    return dax


# ##############################
#       plot fig06
# ##############################


def plot_fig06(hub=None):


    dax = None

    return dax


# #############################################################################
# #############################################################################
#                   Update plotting routines in dict
# #############################################################################


for k0, v0 in _DARTICLE['dfigures'].items():
    _DARTICLE['dfigures'][k0]['func'] = eval(v0['func'])
