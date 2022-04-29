

import os
import warnings


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as img
from mpl_toolkits.mplot3d import Axes3D


_PATH_HERE = os.path.dirname(__file__)


_DARTICLE = {
    'ref_short': "D. Bastidas et al., Math. and Financial Economics, 2018",
    'ref_full': (
        "Daniel Bastidas, Adrien Fabre, Florent Mc Isaac"
        "Minskyan classical growth cycles: "
        "stability analysis of a stock-flow consistent macrodynamic model, "
        "Mathematics and Financial Economics,"
        "2018, issue 13, pages 359-391"
    ),
    'doi': 'https://doi.org/10.1007/s11579-018-0231-6',

    # dict for figures (key, link to png, name of routine)
    'dfigures': {
        1: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': 'Trajectory 3d',
            'png': 'fig02_Trajectory.png',
            'func': 'plot_fig01',
        },
        2: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': 'Trajectory 3d',
            'png': 'fig02_Trajectory.png',
            'func': 'plot_fig02',
        },
        3: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': 'Trajectory 3d',
            'png': 'fig02_Trajectory.png',
            'func': 'plot_fig03',
        },
        4: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': 'Time evolution',
            'png': 'fig02_Trajectory.png',
            'func': 'plot_fig04',
        },
        5: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': 'Time evolution',
            'png': 'fig02_Trajectory.png',
            'func': 'plot_fig04',
        },
    },
}
'''
        6: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig06',
        },
        7: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig07',
        },
        8: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig08',
        },
        9: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig09',
        },
        10: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig10',
        },
        11: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig11',
        },
        12: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': '',
            'com': '',
            'png': '',
            'func': 'plot_fig12',
        },
        13: {
            'model': 'GK-CES',
            'preset': 'CES',
            'caption': 'Trajectories of debt for different values of initial speculation and for (ω0, λ0, d0) = (0.85, 0.85, 1)',
            'com': '',
            'png': '',
            'func': 'plot_fig13',
        },

'''

# #############################################################################
# #############################################################################
#                   Plotting routines (one per figure)
# #############################################################################


# ##############################
#       plot fig01
# ##############################


def plot_fig01(hub=None):
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

    pfe_im = os.path.join(_PATH_HERE, 'fig02_Trajectory.png')
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
#       plot fig04
# ##############################


def plot_fig04(hub=None):
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

    pfe_im = os.path.join(_PATH_HERE, 'fig02_Trajectory.png')
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

    indsys = hub.dparam['eta']['value'] == 100
    dkeys = {
        'omega': {
            'props': {'color': 'k', 'ls': '-'},
        },
        'lambda': {
            'props': {'color': 'b', 'ls': '-'},
        },
        'pi': {
            'props': {'color': 'g', 'ls': '-'},
        },
        'd': {
            'props': {'color': 'r', 'ls': '-'},
        },
        'nu': {
            'props': {'color': 'o', 'ls': '-'},
        },
        'Y/N': {
            'props': {'color': 'm', 'ls': '-'},
            'keys': ['Y', 'N'],
        },
    }

    # extract
    time = hub.dparam['time']['value'][:, indsys]
    for k0, v0 in dkeys.items():
        if v0.get('keys') is None:
            dkeys[k0]['value'] = hub.dparam[k0]['value'][:, indsys]
        else:
            lv = [hub.dparam[vv]['value'][:, indsys] for vv in v0['keys']]
            dkeys[k0]['value'] = lv[0] / lv[1]
        dkeys[k0]['props']['label'] = k0

    # --------------------
    # Prepare plot parameters

    # x_label = hub.dparam[kx]['symbol'] + f" ({hub.dparam[kx]['units']})"
    # y_label = hub.dparam[ky]['symbol'] + f" ({hub.dparam[ky]['units']})"

    # dmargin = {
        # 'left': 0.05, 'right': 0.95,
        # 'bottom': 0.3, 'top': 0.80,
        # 'wspace': 0.15, 'hspace': 0.05,
    # }

    # --------------------
    # Load original figure

    pfe_im = os.path.join(_PATH_HERE, 'fig02_Trajectory.png')
    im = img.imread(pfe_im)

    # --------------------
    # prepare fig and axes

    fig = plt.figure(figsize=(15, 5))
    # gs = gridspec.GridSpec(ncols=2, nrows=1, **dmargin)

    # axe for reproduction
    ax0 = fig.add_axes([0.01, 0.01, 0.46, 0.98], frameon=False)
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.set_title('original', size=12, fontweight='bold')

    # axe for original image
    ax1 = fig.add_axes([0.53, 0.18, 0.40, 0.76])
    ax1.set_xlabel('Time (y)')
    ax1.set_ylabel('')
    ax1.set_title('pygemmes', size=12, fontweight='bold')
    ax1.set_xlim(-5, 205)
    ax1.set_ylim(-0.2, 2.4)

    # store both in a dict
    dax = {'original': ax0, 'pygemmes': ax1}

    # ---------
    # plot data

    kax = 'original'
    if dax.get(kax) is not None:
        ax = dax[kax]
        ax.imshow(im)

    kax = 'pygemmes'
    if dax.get(kax) is not None:
        ax = dax[kax]
        for kk in ['omega', 'lambda', 'pi']:
            ax.plot(
                time,
                dkeys[kk]['value'],
                **dkeys[kk]['props']
            )
        ax.legend(loc='upper center', ncol=2)

    return dax


# #############################################################################
# #############################################################################
#                   Update plotting routines in dict
# #############################################################################


for k0, v0 in _DARTICLE['dfigures'].items():
    _DARTICLE['dfigures'][k0]['func'] = eval(v0['func'])
