# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""


import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from ._plot_timetraces import plot_timetraces

_LS = [
    (0, ()),  # solide
    (0, (1, 1)),  # densely dotted
    (0, (5, 5)),  # dashed
    (0, (3, 5, 1, 5)),  # dashdotted
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
    (0, (1, 5)),  # dotted
    (0, (5, 1)),  # densely dashed
    (0, (3, 1, 1, 1)),
    (0, (3, 1, 1, 1, 1, 1))
]


def _plotbyunits(hub, title='', lw=1, idx=0, color='k'):
    '''
    generate one subfigure per set of units existing
    '''
    groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])
    Nax = len(groupsoffields)

    Ncol = 2
    Nlin = Nax // Ncol + 1
    allvars = [item for sublist in groupsoffields.values() for item in sublist]

    R = hub.get_dparam(keys=[allvars], returnas=dict)
    vy = {}

    vx = R['time']['value'][:, idx]
    units = r'$  '+R['time']['units'].replace('$', '\$')+'  $'

    fig = plt.figure('Plots by units', figsize=(5*Ncol, 3*Nlin))

    dax = {key: plt.subplot(Nlin, Ncol, i+1) for i, key in enumerate(groupsoffields.keys())}

    for key, vvar in groupsoffields.items():
        if vvar != 'time':
            ax = dax[key]

            vy[key] = {yyy: R[yyy]['value'][:, idx] for yyy in vvar}
            ymin = np.amin([np.amin(v) for v in vy[key].values()])
            ymax = np.amax([np.amax(v) for v in vy[key].values()])

            units = r'$\  '+key.replace('$', '\$')+'  \ $'
            ylabel = units
            dax[key].set_ylabel(ylabel)
            #dax[key].set_ylim(ymin, ymax)
            ax.set_xlabel(R['time']['symbol']+' (years)')
            ax.set_xlim(vx[0], vx[-1])

            for j, key2 in enumerate(vvar):
                dax[key].plot(vx,
                              vy[key][key2],
                              color=color,
                              label=key2,
                              ls=_LS[j],
                              lw=lw)
            dax[key].legend()
    plt.suptitle(title)
    fig.tight_layout()
    plt.show()


def _plotnyaxis(hub, x='time', y=[[]], idx=0, title='', lw=1):
    '''
    x must be a variable name (x axis organisation)
    y must be a list of list of variables names (each list is a shared axis)
    '''
    allvarname = [x]+[item for sublist in y for item in sublist]
    R = hub.get_dparam(keys=[allvarname], returnas=dict)
    fig = plt.figure('NyAxis', figsize=(10, 5))
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
        ymin = np.amin([np.amin(v) for v in vy[ii].values()])
        ymax = np.amax([np.amax(v) for v in vy[ii].values()])
        units = r'$(  '+R[y[ii][-1]]['units']+'  )$'
        ylabel = ''.join([R[xx]['symbol']+', ' for xx in y[ii]]) + units
        dax[ii].set_ylabel(ylabel)
        dax[ii].set_ylim(ymin, ymax)
        color = np.array(plt.cm.hsv(ii/Nyaxis))
        color[:-1] *= 0.8
        color = tuple(color)
        # Add the curves
        for j, key in enumerate(y[ii]):
            p[key], = dax[ii].plot(vx, vy[ii][key],    color=color,
                                   label=R[key]['symbol'], ls=_LS[j], lw=lw)
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


def _phasespace(hub, x='omega', y='lambda', color='time', idx=0):
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
    allvars = hub.get_dparam(returnas=dict)
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
              + hub.dmodel['name'] + '| system number' + str(idx))

    plt.show()


def _plot3D(hub, x, y, z, cinf, cmap='jet', index=0, title=''):
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

    fig = plt.figure('3D', figsize=(10, 10))
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


def Var(hub, key, idx=0, cycles=False, log=False):
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
    allvars = hub.get_dparam(returnas=dict)
    y = allvars[key]['value'][:, idx]
    t = allvars['time']['value'][idx]

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
              + hub.dmodel['name'] + '| system number' + str(idx))
    plt.ylabel(key)
    plt.xlabel('time')
    plt.show()


_DPLOT = {
    'timetrace': plot_timetraces,
    'plotnyaxis': _plotnyaxis,
    'phasespace': _phasespace,
    'plot3D': _plot3D,
    'plotbyunits': _plotbyunits, }
