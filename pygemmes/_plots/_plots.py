# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021
@author: Paul Valcke

"""

from ._plot_timetraces import plot_timetraces
from ._plot_tools import _multiline

import copy
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec


_LS = [
    (0, ()),
    (0, (1, 1)),
    (0, (5, 1)),  # densely dashed
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (5, 5)),
    (0, (3, 5, 1, 5)),
    (0, (3, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
    (0, (1, 5)),  # dotted
    (0, (5, 10)),
    (0, (5, 5))
]

matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
plt.rcParams.update({'font.size': 15})


__all__ = [
    'slices_wholelogic',
    'plot_variation_rate',
    'plot_timetraces',
    'plotnyaxis',
    'phasespace',
    'plot3D',
    'plotbyunits',
    'Var',
    'cycles_characteristics'
]

# ############################################################################
# ############## IMPORTANT PLOTS #############################################


def slices_wholelogic(hub, key='', axes=[[]], N=100, tid=0, idx=0):
    '''
    Take the logic of a field, and calculate a slice given two of the argument fields that are modified

    Example :
        plotfunction(hub,key='Hid',axes=[['Omega',0,2]],N=100,tid=0,idx=0)
        plotfunction(hub,key='Hid',axes=[['Omega',0,2],['x',0,100]],N=100,tid=0,idx=0)

    Parameters
    ----------
    key  : str. name of the field you are introspecting
    axes : [[str,valmin,valmax]] or [[str,valmin,valmax],[str,valmin,valmax]] for 2D
    N    : int, number of points in grid
    tid  : index of
    idx : TYPE, optional
        DESCRIPTION. The default is 0.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    R = hub.get_dparam()

    if len(axes) > 2:
        raise Exception('Too many dimensions to plot !')
    elif len(axes) == 2:
        axx = axes[0]
        axy = axes[1]
        XX, YY = np.meshgrid(np.linspace(axx[1], axx[2], N),
                             np.linspace(axy[1], axy[2], N))

        keys = [axes[0][0], axes[1][0]]
        defaultkeys = [k for k in R[key]['kargs'] if k not in keys]

        defaultval = {k: R[k]['value'] for k in defaultkeys if k in hub.dmisc['parameters']}
        defaultval.update({k: R[k]['value'][tid, idx]
                          for k in defaultkeys if k in hub.dmisc['dfunc_order']['statevar']})
        defaultval0 = copy.deepcopy(defaultval)
        defaultval[keys[0]] = XX
        defaultval[keys[1]] = YY

        Z = R[key]['func'](**defaultval)

        plt.figure(f'Function: {key} 2D')
        plt.pcolormesh(XX, YY, Z, cmap='jet')
        plt.xlabel(R[axes[0][0]]['symbol'])
        plt.ylabel(R[axes[1][0]]['symbol'])
        plt.title(R[key]['symbol']+f'\n {defaultval0}')
        plt.colorbar()
        plt.show()
    elif len(axes) == 1:
        XX = np.linspace(axes[0][1], axes[0][2], N)
        defaultkeys = [k for k in R[key]['kargs'] if k not in [key]]

        defaultval = {k: R[k]['value'] for k in defaultkeys if k in hub.dmisc['parameters']}

        defaultval.update({k: R[k]['value'][tid, idx]
                          for k in defaultkeys if k in hub.dmisc['dfunc_order']['statevar']})
        defaultval0 = copy.deepcopy(defaultval)
        defaultval[axes[0][0]] = XX

        Z = R[key]['func'](**defaultval)

        plt.figure(f'Function: {key} 1D')
        plt.plot(XX, Z)
        plt.xlabel(R[axes[0][0]]['symbol'])
        plt.ylabel(R[key]['symbol'])
        plt.title(f'{defaultval0}')
        plt.show()


def plot_variation_rate(hub, varlist, title='', idx=0):
    '''
    Allow one to observe the time variation and the contribution of each dependency.
    Useful for debugging or understanding where are the main loops

    THE SYSTEM NEEDS :
        1) a run
        2) calculate_variation_rate

    for each field in varlist (ex : ['Y','L','w']) it will :
        * Print the variable time evolution
        * Print its relative growth rate
        * if it is a Statevar, its time derivate, and the contribution of each of its dependency to its time derivate
        * if it is an ODE, its second time derivate and the contribution of each of its dependency
    '''
    R = hub.get_dparam()

    fig = plt.figure()
    fig.set_size_inches(15, 5*len(varlist))
    t = R['time']['value'][:, 0]
    gs = GridSpec(len(varlist), 3)

    # Axis for value and relative growth
    ax0 = {key: fig.add_subplot(gs[i, 0]) for i, key in enumerate(varlist)}
    ax02 = {key: ax0[key].twinx() for key in varlist}

    # Axis for derivative and their contributions
    ax = {key: fig.add_subplot(gs[i, 1:]) for i, key in enumerate(varlist)}

    for key in varlist:
        # ##################################
        # Left Curves (y, relative growth)
        ax02[key].plot(t, R[key]['value'][:, idx], c='b')
        ax0[key].plot(t[1:-1], R[key]['time_log_derivate'][1:-1, idx], ls='--', c='g')
        ax0[key].axhline(y=0, color='k', lw=0.5)

        # Ylim management
        sort = np.sort(R[key]['time_log_derivate'][1:-1, idx])[int(0.05*len(t)):-int(0.05*len(t))]
        ax0[key].set_ylim([1.3*np.amin(sort), 1.3*np.amax(sort)])
        # Left side axis management
        ax02[key].set_ylabel(R[key]['symbol'])
        ax02[key].spines['left'].set_position(('outward',  80))

        ax02[key].yaxis.tick_left()
        ax02[key].yaxis.set_label_position('left')
        ax02[key].spines['left'].set_color('blue')
        ax02[key].tick_params(axis='y', colors='blue')
        symb = R[key]['symbol'].replace('$', '')
        label = r'$\dfrac{\dot{'+symb+r'}}{'+symb+'}$'
        ax0[key].spines['left'].set_color('green')
        ax0[key].tick_params(axis='y', colors='green')
        ax0[key].set_ylabel(label)

        # ##################################
        # Right side (Derivates)

        # Full curve
        if R[key]['eqtype'] == 'ode':
            ax[key].plot(t[2:-2], R[key]['time_dderivate'][2:-2, idx],
                         c='black', label=r'$\dfrac{d^2 '+symb+r'}{dt^2}$')
            label = r'$\ddot{'+R[key]['symbol'].replace('$', '')+r'}$'
        else:
            ax[key].plot(t[1:-1], R[key]['time_derivate'][1:-1, idx],
                         c='black', label=r'$\dfrac{d '+symb+r'}{dt}$')
            label = r'$\dot{'+R[key]['symbol'].replace('$', '')+r'}$'
        ax[key].spines['right'].set_color('black')
        ax[key].axhline(y=0, color='k', lw=0.5)

        #  Contribution
        vv = R[key]['partial_contribution']
        for i, k2 in enumerate(vv.keys()):
            symb2 = R[k2]['symbol'].replace('$', '')
            if R[key]['eqtype'] == 'ode':
                lab = r'$\dfrac{\partial \dot{'+symb+r'}}{\partial '+symb2+'}\dot{'+symb2+r'}$'
            else:
                lab = r'$\dfrac{\partial '+symb+r'}{\partial '+symb2+'}\dot{'+symb2+r'}$'
            ax[key].plot(t[1:-1], vv[k2][1:-1, idx],
                         label=lab)

        # Axis management
        ax[key].yaxis.tick_right()
        ax[key].yaxis.set_label_position('right')
        ax[key].set_ylabel(label)
        ax[key].legend()

    # Figure management
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.suptitle(title)
    plt.show()


def plotbyunits(hub, title='', lw=1, idx=0, color='k', sharex=True):
    '''
    generate one subfigure per set of units existing
    '''
    groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])
    Nax = len(groupsoffields)

    Ncol = 2
    Nlin = Nax // Ncol + Nax % Ncol
    allvars = [item for sublist in groupsoffields.values() for item in sublist]

    R = hub.get_dparam(keys=[allvars], returnas=dict)
    vy = {}

    vx = R['time']['value'][:, idx]
    units = r'$  '+R['time']['units'].replace('$', '\$')+'  $'

    fig = plt.figure()
    fig.set_size_inches(10*Ncol, 3*Nlin)
    dax = {key: plt.subplot(Nlin, Ncol, i+1)
           for i, key in enumerate(groupsoffields.keys())}

    index = 0
    for key, vvar in groupsoffields.items():

        ax = dax[key]

        vy[key] = {yyy: R[yyy]['value'][:, idx] for yyy in vvar}
        ymin = np.amin([np.amin(v) for v in vy[key].values()])
        ymax = np.amax([np.amax(v) for v in vy[key].values()])

        units = r'$\  '+key.replace('$', '\$')+'  \ $'
        ylabel = units
        dax[key].set_ylabel(ylabel)
        #dax[key].set_ylim(ymin, ymax)
        #ax.set_xlabel(R['time']['symbol']+' (years)')
        ax.set_xlim(vx[0], vx[-1])
        ax.axhline(y=0, color='k', lw=0.5)
        if 1 < index < Nax-2:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(r'$time (y)$')
        if index < 2:
            ax.xaxis.tick_top()
            # ax.xaxix.label_top()
        ax.grid(axis='x')
        if index % 2 == 1:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        for j, key2 in enumerate(vvar):
            if key2 != 'time':
                dax[key].plot(vx,
                              vy[key][key2],
                              color=color,
                              label=R[key2]['symbol'],
                              ls=_LS[j % (len(_LS)-1)],
                              lw=lw)
        dax[key].legend()
        index += 1
    plt.suptitle(title)
    fig.tight_layout()

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()


def plotnyaxis(hub, x='time', y=[[]], idx=0, title='', lw=2):
    '''
    x must be a variable name (x axis organisation)
    y must be a list of list of variables names (each list is a shared axis)

    example :
        pgm.plots.plotnyaxis(hub, x='time',
                     y=[['lambda', 'omega'],
                        ['d'],
                        ['kappa', 'pi'],
                        ],
                     idx=0,
                     title='',
                     lw=2)
    '''
    allvarname = [x]+[item for sublist in y for item in sublist]
    R = hub.get_dparam(keys=[allvarname], returnas=dict)

    fig = plt.figure()
    fig.set_size_inches(10, 5)
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
        units = r'$(  '+R[y[ii][-1]]['units'].replace('$', '\$')+'  $)'
        ylabel = r''.join([R[xx]['symbol']+', ' for xx in y[ii]]) + units
        dax[ii].set_ylabel(ylabel)
        dax[ii].set_ylim(ymin, ymax)
        color = np.array(plt.cm.hsv(ii/Nyaxis))
        color[:-1] *= 0.8
        color = tuple(color)
        # Add the curves
        for j, key in enumerate(y[ii]):
            p[key], = dax[ii].plot(vx, vy[ii][key],    color=color,
                                   label=R[key]['symbol'], ls=_LS[j % (len(_LS)-1)], lw=lw)
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


def phasespace(hub, x='omega', y='lambda', color='time', idx=0):
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

    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax, label=color)
    plt.xlabel(allvars[x]['symbol'])
    plt.ylabel(allvars[y]['symbol'])
    plt.xlim([np.amin(xval), np.amax(xval)])
    plt.ylim([np.amin(yval), np.amax(yval)])
    plt.axis('scaled')
    plt.title('Phasespace ' + x + '-' + y + ' for model : '
              + hub.dmodel['name'] + '| system number' + str(idx))

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

    fig = plt.figure()
    fig.set_size_inches(10, 10)
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
    # plt.legend()
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
    fig = plt.figure()
    fig.set_size_inches(10, 5)

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


def cycles_characteristics(hub, xaxis='omega', yaxis='lambda', ref='lambda'):
    '''
    Plot frequency and harmonicity for each cycle found in the system
    '''
    ####
    fig = plt.figure()
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)

    AllX = []
    AllY = []
    AllC1 = []
    AllC2 = []
    R = hub.get_dparam()
    cycs = R[ref]['cycles_bykey']

    for i in range(hub.dmisc['dmulti']['shape'][0]):  # loop on parrallel system
        for j, ids in enumerate(cycs['period_indexes'][i]):  # loop on cycles decomposition
            AllX.append(R[xaxis]['value'][ids[0]:ids[1], i])
            AllY.append(R[yaxis]['value'][ids[0]:ids[1], i])
            AllC1.append(cycs['frequency'][i][j])
            AllC2.append(cycs['Harmonicity'][i][j])

    lc1 = _multiline(AllX, AllY, AllC1, ax=ax1, cmap='jet', lw=2)
    lc2 = _multiline(AllX, AllY, AllC2, ax=ax2, cmap='jet', lw=2)

    ax1.set_xlabel(R[xaxis]['symbol'])
    ax1.set_ylabel(R[yaxis]['symbol'])
    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(lc1, cax=cax1, orientation='vertical')
    ax1.set_title('frequency')

    ax2.set_xlabel(R[xaxis]['symbol'])
    ax2.set_ylabel(R[yaxis]['symbol'])
    divider2 = make_axes_locatable(ax2)
    cax2 = divider2.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(lc2, cax=cax2, orientation='vertical')
    ax2.set_title('Harmonicity')

    plt.suptitle('Period analysis on : '+R[ref]['symbol'])
    plt.show()


_DPLOT = {
    'Slice_logic': slices_wholelogic,
    'variation_rate': plot_variation_rate,
    'timetrace': plot_timetraces,
    'nyaxis': plotnyaxis,
    'phasespace': phasespace,
    '3D': plot3D,
    'byunits': plotbyunits,

    'Onevariable': Var,
    'cycles_characteristics': cycles_characteristics}
