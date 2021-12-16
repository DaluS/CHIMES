# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle


def Var(sol, key, idx=0, cycles=False, log=False):
    '''
    Parameters
    ----------
    sol : TYPE
        DESCRIPTION.
    key : TYPE
        DESCRIPTION.
    idx : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    None.

    '''
    plt.figure('key :' + key + '| system idx' + str(idx), figsize=(10, 5))
    fig = plt.gcf()
    ax = plt.gca()

    # PLOT OF THE BASE
    allvars = sol.get_dparam(returnas=dict)
    y = allvars[key]['value'][:, idx]
    t = allvars['time']['value']
    print('y', np.shape(y))
    print('t', np.shape(t))
    plt.plot(t, y, lw=2, ls='-', c='k')

    # PLOT OF THE CYCLES
    if cycles:
        cyclvar = allvars[key]['cycles']
        tmcycles = cyclvar['t_mean_cycle']

        # Plot of each period by a rectangle
        miny = np.amin(y)
        maxy = np.amax(y)

        for car in cyclvar['period_T_intervals'][::2]:
            # print(car)
            ax.add_patch(
                Rectangle((car[0], miny), car[1]-car[0], maxy-miny, facecolor='k', alpha=0.1))

        # Plot of enveloppe (mean-max)
        vmin = cyclvar['minval']
        vmax = cyclvar['maxval']
        plt.plot(tmcycles, vmin, '--', label='min value')
        plt.plot(tmcycles, vmax, '--', label='max value')

        # Plot of the mean value evolution
        meanv = np.array(cyclvar['meanval'])
        plt.plot(tmcycles, cyclvar['meanval'], ls='dotted', label='mean value')
        plt.plot(tmcycles, cyclvar['medval'],
                 ls='dashdot', label='median value')

        # Plot of the standard deviation around the mean value
        stdv = np.array(cyclvar['stdval'])
        ax.fill_between(tmcycles, meanv - stdv, meanv + stdv, alpha=0.2)
        plt.legend()

    if log is True:
        ax.set_yscale('log')
    plt.title('Evolution of :' + key + ' in model : '
              + sol.dmodel['name'] + '| system number' + str(idx))
    plt.ylabel(key)
    plt.xlabel('time')
    plt.show()


def phasespace(sol, x='omega', y='lambda', color='time', idx=0):
    '''
    Plot of the trajectory of the system in a 2dimensional phase-space

    Parameters
    ----------
    sol : hub after a run
    x   : key for the variable on x axis, The default is 'omega'.
    y   : key for the variable on y axis, The default is 'lambda'.
    idx : number of the system taken to be plot, The default is 0

    Returns
    -------
    None.

    '''
    allvars = sol.get_dparam(returnas=dict)
    yval = allvars[y]['value'][:, idx]
    xval = allvars[x]['value'][:, idx]
    t = allvars[color]['value'][:, idx]

    points = np.array([xval, yval]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(t)
    lc.set_linewidth(2)

    fig = plt.figure('Phasespace' + x + ' ' + y + 'for system :' + str(idx),
                     figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax, label=color)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xlim([np.amin(xval), np.amax(xval)])
    plt.ylim([np.amin(yval), np.amax(yval)])
    plt.axis('scaled')
    plt.title('Phasespace ' + x + '-' + y + ' for model : '
              + sol.dmodel['name'] + '| system number' + str(idx))

    plt.show()


# #############################################################################
# #############################################################################
#                       DEPRECATED
# #############################################################################


# DEPRECATED ?
def AllVar(
    hub,
    ncols=None,
    idx=None,
    sharex=None,
    tit=None,
    wintit=None,
    dmargin=None,
    fs=None,
    show=None,
):
    '''
    Plot all the variables in the system on a same figure

    Parameters
    ----------
    hub : The hub of the system
        DESCRIPTION.
    ncols : the number of column in the figure
        DESCRIPTION. The default is 2.
    idx : the index of the system you want to print
        DESCRIPTION. The default is 0.
    dmargin: dict
        dict defining the margins to be used for defining the axes

    Returns
    -------
    None.

    '''

    # -----------
    # Check inputs

    if ncols is None:
        ncols = 3
    if idx is None:
        idx = 0
    if dmargin is None:
        dmargin = {
            'left': 0.05, 'right': 0.98,
            'bottom': 0.06, 'top': 0.90,
            'wspace': 0.15, 'hspace': 0.20,
        }
    if sharex is None:
        sharex = True
    if tit is None:
        model = hub.dmodel['name']
        preset = hub.dmodel['preset']
        solver = hub.dmisc['solver']
        tit = f'{model} - {preset} - {solver}\nsystem number: {idx}'
    if wintit is None:
        wintit = 'All variables'
    if fs is None:
        fs = (20, 20)
    if show is None:
        show = True

    # -----------
    # Prepare data to be plotted

    dpar = hub.get_dparam(returnas=dict)
    t = dpar['time']['value'][:, idx]
    lkeys_notime = hub.get_dparam(
        returnas=list,
        eqtype=['ode', 'statevar'],
        key=('time',),
    )
    nkeys = len(lkeys_notime)

    # derive nrows
    nrows = nkeys // ncols + 1

    # -----------
    # Prepare figure and axes dict

    fig = plt.figure(figsize=fs)
    fig.canvas.set_window_title(wintit)
    fig.suptitle(tit)

    # axes coordinates array
    gs = gridspec.GridSpec(ncols=ncols, nrows=nrows, **dmargin)

    dax = {}
    shx = None
    for ii, key in enumerate(lkeys_notime):

        # create axes and store in dict
        row = ii % nrows
        col = ii // nrows
        dax[key] = fig.add_subplot(gs[row, col], sharex=shx)

        # sharex if relevant
        if ii == 0 and sharex is True:
            shx = dax[key]

        # set ylabels
        if dpar[key]['symbol'] is None:
            ylab = key
        else:
            ylab = dpar[key]['symbol']
        if dpar[key]['units'] not in [None, '']:
            ylab += f" ({dpar[key]['units']})"
        dax[key].set_ylabel(ylab)

        # set xlabel if at bottom
        if row == nrows - 1 or ii == nkeys - 1:
            xlab = f"time ({dpar['time']['units']})"
            dax[key].set_xlabel(xlab)

    # -----------
    # plot data on axes

    for ii, key in enumerate(lkeys_notime):
        dax[key].plot(t, dpar[key]['value'][:, idx])

    # -----------
    # show and return axes dict

    if show is True:
        plt.show()
    return dax


# DEPRECATED ?
def AllPhaseSpace(sol, variablesREF, idx=0):
    plt.figure('All Phasespace', figsize=(10, 7))
    fig = plt.gcf()
    leng = len(variablesREF)
    NumbOfSubplot = int(leng * (leng - 1) / 2)

    idd = 1
    for ii, var1 in enumerate(variablesREF):
        for var2 in variablesREF[ii + 1:]:

            allvars = sol.get_dparam(returnas=dict)
            xval = allvars[var1]['value'][:, idx]
            yval = allvars[var2]['value'][:, idx]
            t = allvars['time']['value'][:, idx]

            points = np.array([xval, yval]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            norm = plt.Normalize(t.min(), t.max())
            lc = LineCollection(segments, cmap='viridis', norm=norm)
            lc.set_array(t)
            lc.set_linewidth(2)

            plt.subplot(2, NumbOfSubplot, idd)
            ax = plt.gca()
            line = ax.add_collection(lc)
            plt.xlabel(var1)
            plt.ylabel(var2)
            plt.xlim([np.amin(xval), np.amax(xval)])
            plt.ylim([np.amin(yval), np.amax(yval)])
            plt.axis('scaled')
            idd += 1
    fig.colorbar(line, ax=ax, label='time')
    suptit = (
        f"All Phasespace for model {sol.dmodel['name']}, system {idx}"
    )
    plt.suptitle(suptit)
    plt.show()
