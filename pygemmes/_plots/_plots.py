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
from mpl_toolkits.mplot3d.art3d import Line3DCollection

_LS = [(0, ()),  # solide
       (0, (1, 1)),  # densely dotted
       (0, (5, 5)),  # dashed
       (0, (3, 5, 1, 5)),  # dashdotted
       (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
       (0, (1, 5)),  # dotted
       (0, (5, 1)),  # densely dashed
       (0, (3, 1, 1, 1)),
       (0, (3, 1, 1, 1, 1, 1))]

__all__ = ['plot3yaxis',
           'phasespace',
           'plot3D']


def plotnyaxis(hub, x, y, idx=0, title=''):
    '''
    x must be a variable name (x axis organisation)
    y must be a list of list of variables names (each list is a shared axis)
    '''
    allvarname = [x]+[item for sublist in y for item in sublist]
    R = hub.get_dparam(keys=[allvarname], returnas=dict)
    fig = plt.figure(figsize=(10, 5))
    ax = plt.gca()
    p = {}  # dictionnary of curves

    # Prepare x axis
    vx = R[x]['value'][:, idx]
    units = r'$(  '+R[x]['units']+'  )$'
    ax.set_xlabel(R[x]['symbol']+units)
    ax.set_xlim(vx[0], vx[-1])

    # set ax dictionnary
    Nyaxis = len(y)
    dax = {0: ax}
    for i in range(1, Nyaxis):
        dax[i] = ax.twinx()

    # set for each y
    vy = {}
    for ii, vlist in enumerate(y):
        yy = y[ii]
        vy[ii] = {yyy: R[yyy]['value'][:, idx] for yyy in yy}

        # y axis
        ymin = np.min([np.min(v) for v in vy[ii].values()])
        ymax = np.max([np.max(v) for v in vy[ii].values()])
        units = r'$(  '+R[y[ii][-1]]['units']+'  )$'
        ylabel = ''.join([R[x]['symbol']+', ' for x in y[ii]]) + units
        dax[ii].set_ylabel(ylabel)
        dax[ii].set_ylim(ymin, ymax)
        color = np.array(plt.cm.hsv(ii/Nyaxis))
        color[:-1] *= 0.8
        color = tuple(color)
        # Add the curves
        for j, key in enumerate(y[ii]):
            p[key], = dax[ii].plot(vx, vy[ii][key],    color=color,
                                   label=R[key]['symbol'], ls=_LS[j])
        side = 'right' if ii % 2 else 'left'

        dax[ii].spines[side].set_position(('outward', np.amax((0, 60*(ii//2)))))
        if side == 'left':
            dax[ii].yaxis.tick_left()
            dax[ii].yaxis.set_label_position('left')
        dax[ii].yaxis.label.set_color(color)
        dax[ii].tick_params(axis='y', colors=color)

    dax[ii].legend(handles=p.values(), loc='best')
    plt.title(title)
    plt.show()


def plot3yaxis(hub, x, y1, y2, y3=[], idx=0):
    '''
    plot variables on multiple y axis (up to 3)
    x must be a variable name
    y must be a list of variable names

    for the moment only 9 variables are accepted per list !
    '''
    color1 = plt.cm.jet(0)
    color2 = plt.cm.jet(0.3)
    color3 = plt.cm.jet(.9)

    #########
    allvarname = [x]+y1+y2+y3
    R = hub.get_dparam(keys=[allvarname], returnas=dict)

    fig, host = plt.subplots(figsize=(8, 5))
    p = {}
    host.set_xlabel(R[x]['symbol']+r'($ '+R[x]['units'].replace('$', '\$')+'$)')
    vx = R[x]['value'][:, idx]
    host.set_xlim(vx[0], vx[-1])

    vy1 = {y: R[y]['value'][:, idx] for y in y1}
    y1min = np.min([np.min(v) for v in vy1.values()])
    y1max = np.max([np.max(v) for v in vy1.values()])
    units = r'($'+R[y1[-1]]['units']+'$)'
    ylabel1 = ''.join([R[x]['symbol']+' ' for x in y1])  # +units

    host.set_ylabel(ylabel1)
    for i, key in enumerate(y1):
        p[key], = host.plot(vx, vy1[key],    color=color1, label=R[key]['symbol'], ls=_LS[i])
    host.yaxis.label.set_color(color1)
    host.set_ylim(y1min, y1max)

    par1 = host.twinx()
    vy2 = {y: R[y]['value'][:, idx] for y in y2}
    y2min = np.min([np.min(v) for v in vy2.values()])
    y2max = np.max([np.max(v) for v in vy2.values()])
    ylabel2 = ''.join([R[x]['symbol']+' ' for x in y2]) + \
        r'($ '+R[y2[-1]]['units'].replace('$', '\$')+'$)'
    par1.set_ylabel(ylabel2)
    for i, key in enumerate(y2):
        p[key], = par1.plot(vx, vy2[key],    color=color2, label=R[key]['symbol'], ls=_LS[i])
    par1.yaxis.label.set_color(color2)
    par1.set_ylim(y2min, y2max)

    if len(y3):
        par2 = host.twinx()
        vy3 = {y: R[y]['value'][:, idx] for y in y3}
        y3min = np.min([np.min(v) for v in vy3.values()])
        y3max = np.max([np.max(v) for v in vy3.values()])
        ylabel3 = ''.join([R[x]['symbol']+' ' for x in y3]) + \
            r'($ '+R[y3[-1]]['units'].replace('$', '\$')+'$)'
        par2.set_ylabel(ylabel3)
        for i, key in enumerate(y3):
            p[key], = par2.plot(vx, vy3[key],    color=color3, label=R[key]['symbol'], ls=_LS[i])

        # right, left, top, bottom
        par2.spines['right'].set_position(('outward', 60))
        par2.xaxis.set_ticks([])
        par2.yaxis.label.set_color(color3)
        par2.set_ylim(y3min, y3max)
        # Sometimes handy, same for xaxis
        # par2.yaxis.set_ticks_position('right')

        # Move "Velocity"-axis to the left
        # par2.spines['left'].set_position(('outward', 60))
        # par2.spines['left'].set_visible(True)
        # par2.yaxis.set_label_position('left')
        # par2.yaxis.set_ticks_position('left')

    host.legend(handles=p.values(), loc='best')

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


def plot3D(hub, x, y, z, cinf, cmap='jet', index=0, title=''):
    '''
    Plot a 3D curve, with a fourth information on the colour of the curve

    x,y,z,cinf are names of your variables
    cmap your colormap
    title is your graph title
    '''
    R = hub.get_dparam(key=[x, y, z, cinf], returnas=dict)
    vx = R[x]['value'][:, index]
    vy = R[y]['value'][:, index]
    vz = R[z]['value'][:, index]
    vc = R[cinf]['value'][:, index]

    points = np.array([vx, vy, vz]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(vc.min(), vc.max())

    fig = plt.figure('', figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.plot(vx,
            vy,
            vz, lw=0.01, c='k')
    lc = Line3DCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(vc)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    cbar = fig.colorbar(lc, ax=ax)
    cbar.ax.set_ylabel(R[cinf]['symbol'])
    ax.set_xlabel(R[x]['symbol'])
    ax.set_ylabel(R[y]['symbol'])
    ax.set_zlabel(R[z]['symbol'])

    plt.tight_layout()
    plt.legend()
    plt.title(title)
    plt.show()


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
    t = allvars['time']['value'][idx]
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
            print(car)
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
