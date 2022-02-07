

import os
import warnings


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as img
from mpl_toolkits.mplot3d import Axes3D


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
            'model': 'G',
            'preset': 'default',
            'caption': '',
            'com': 'Trajectory',
            'png': 'fig02.png',
            'func': 'plot_fig02',
        },
        3: {
            'model': 'G',
            'preset': 'default',
            'caption': '',
            'com': 'Basin of attraction',
            'png': 'fig03.png',
            'func': 'plot_fig03',
        },
        5: {
            'model': 'G',
            'preset': 'default',
            'caption': '',
            'com': 'Blablabla',
            'png': 'fig05.png',
            'func': 'plot_fig05',
        },
        6: {
            'model': 'G',
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

    kx, ky, kz = 'lambda', 'omega', 'g'
    x = hub.dparam[kx]['value'][:, 0]
    y = hub.dparam[ky]['value'][:, 0]
    z = hub.dparam[kz]['value'][:, 0]

    # --------------------
    # Prepare plot parameters

    x_label = hub.dparam[kx]['symbol'] + f" ({hub.dparam[kx]['units']})"
    y_label = hub.dparam[ky]['symbol'] + f" ({hub.dparam[ky]['units']})"
    z_label = hub.dparam[kz]['symbol'] + f" ({hub.dparam[kz]['units']})"

    dmargin = {
        'left': 0.1, 'right': 0.95,
        'bottom': 0.1, 'top': 0.95,
        'wspace': 0.1, 'hspace': 0.05,
    }

    # --------------------
    # Load original figure

    pfe_im = os.path.join(_PATH_HERE, 'fig02_Trajectory.png')
    im = img.imread(pfe_im)

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(ncols=2, nrows=1, **dmargin)

    # axe for reproduction
    ax0 = fig.add_subplot(gs[0, 0], projection='3d')
    ax0.set_xlabel(x_label)
    ax0.set_ylabel(y_label)
    ax0.set_zlabel(z_label)
    ax0.set_title('title', size=12, fontweight='bold')

    # axe for original image
    ax1 = fig.add_subplot(gs[0, 1], frameon=False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # store both in a dict
    dax = {'reproduction': ax0, 'original': ax1}

    # ---------
    # plot data

    kax = 'reproduction'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.plot(x, y, z)

    kax = 'original'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.imshow(im)

    return dax


# ##############################
#       plot fig03
# ##############################


def plot_fig03(hub=None):
    """ The objective here is to reproduce the original figure
    """

    # --------------------
    # Get data of interest

    kx, ky = 'time', 'omega'
    x = hub.dparam[kx]['value'][:, 0]
    y = hub.dparam[ky]['value'][:, 0]

    # --------------------
    # Prepare plot parameters

    x_label = hub.dparam[kx]['symbol'] + f" ({hub.dparam[kx]['units']})"
    y_label = hub.dparam[ky]['symbol'] + f" ({hub.dparam[ky]['units']})"

    dmargin = {
        'left': 0.1, 'right': 0.95,
        'bottom': 0.1, 'top': 0.95,
        'wspace': 0.1, 'hspace': 0.05,
    }

    # --------------------
    # Load original figure

    pfe_im = os.path.join(_PATH_HERE, 'fig03_ProbabilityIntervals.png')
    im = img.imread(pfe_im)

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(ncols=2, nrows=1, **dmargin)

    # axe for reproduction
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_xlabel(x_label)
    ax0.set_ylabel(y_label)
    ax0.set_title('title', size=12, fontweight='bold')

    # axe for original image
    ax1 = fig.add_subplot(gs[0, 1], frameon=False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # store both in a dict
    dax = {'reproduction': ax0, 'original': ax1}

    # ---------
    # plot data

    kax = 'reproduction'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.plot(x, y)

    kax = 'original'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.imshow(im)

    return dax


# ##############################
#       plot fig05
# ##############################


def plot_fig05(hub=None):
    """ The objective here is to reproduce the original figure
    """

    # --------------------
    # Get data of interest

    kx, ky = 'time', 'lambda'
    x = hub.dparam[kx]['value'][:, 0]
    y = hub.dparam[ky]['value'][:, 0]

    # --------------------
    # Prepare plot parameters

    x_label = hub.dparam[kx]['symbol'] + f" ({hub.dparam[kx]['units']})"
    y_label = hub.dparam[ky]['symbol'] + f" ({hub.dparam[ky]['units']})"

    dmargin = {
        'left': 0.1, 'right': 0.95,
        'bottom': 0.1, 'top': 0.95,
        'wspace': 0.1, 'hspace': 0.05,
    }

    # --------------------
    # Load original figure

    pfe_im = os.path.join(_PATH_HERE, 'fig03_ProbabilityIntervals.png')
    im = img.imread(pfe_im)

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(ncols=2, nrows=1, **dmargin)

    # axe for reproduction
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_xlabel(x_label)
    ax0.set_ylabel(y_label)
    ax0.set_title('title', size=12, fontweight='bold')

    # axe for original image
    ax1 = fig.add_subplot(gs[0, 1], frameon=False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # store both in a dict
    dax = {'reproduction': ax0, 'original': ax1}

    # ---------
    # plot data

    kax = 'reproduction'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.plot(x, y)

    kax = 'original'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.imshow(im)

    return dax


# ##############################
#       plot fig06
# ##############################


def plot_fig06(hub=None):
    """ The objective here is to reproduce the original figure
    """

    # --------------------
    # Get data of interest

    kx, ky = 'lambda', 'K'
    x = hub.dparam[kx]['value'][:, 0]
    y = hub.dparam[ky]['value'][:, 0]

    # --------------------
    # Prepare plot parameters

    x_label = hub.dparam[kx]['symbol'] + f" ({hub.dparam[kx]['units']})"
    y_label = hub.dparam[ky]['symbol'] + f" ({hub.dparam[ky]['units']})"

    dmargin = {
        'left': 0.1, 'right': 0.95,
        'bottom': 0.1, 'top': 0.95,
        'wspace': 0.1, 'hspace': 0.05,
    }

    # --------------------
    # Load original figure

    pfe_im = os.path.join(_PATH_HERE, 'fig03_ProbabilityIntervals.png')
    im = img.imread(pfe_im)

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(ncols=2, nrows=1, **dmargin)

    # axe for reproduction
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_xlabel(x_label)
    ax0.set_ylabel(y_label)
    ax0.set_title('title', size=12, fontweight='bold')

    # axe for original image
    ax1 = fig.add_subplot(gs[0, 1], frameon=False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # store both in a dict
    dax = {'reproduction': ax0, 'original': ax1}

    # ---------
    # plot data

    kax = 'reproduction'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.plot(x, y)

    kax = 'original'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.imshow(im)

    return dax


# #############################################################################
# #############################################################################
#                   Update plotting routines in dict
# #############################################################################


for k0, v0 in _DARTICLE['dfigures'].items():
    _DARTICLE['dfigures'][k0]['func'] = eval(v0['func'])
