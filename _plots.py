# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


def AllVar(sol, rows=1, idx=0):
    '''
    Plot all the variables in the system on a same figure

    Parameters
    ----------
    sol : The hub of the system
        DESCRIPTION.
    rows : the number of column on the plot
        DESCRIPTION. The default is 2.
    idx : the index of the system you want to print
        DESCRIPTION. The default is 0.

    Returns
    -------
    None.

    '''
    # if sol.__dmisc['run']:
    lkeys, array = sol.get_variables_compact()

    t = array[:, -1]
    plt.figure('All variables', figsize=(20, 20))
    for i in range(len(lkeys) - 1):
        lk = lkeys[i]
        val = array[:, i, idx]
        plt.subplot(len(lkeys) - 1, rows, i + 1)

        plt.plot(t, val)
        plt.ylabel(lk)
    plt.suptitle(sol.model['name'] + '||| system number :' + str(idx))
    plt.show()
    # else:
    #    print('Plot simple could not be done as the simulation did not run')


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
    plt.figure(f"key : {key} | system idx : {idx}", figsize=(10, 5))
    fig = plt.gcf()
    ax = plt.gca()

    # PLOT OF THE BASE
    allvars = sol.get_dparam(returnas=dict)
    y = allvars[key]['value']
    t = allvars['time']['value']
    plt.plot(t, y, lw=2, ls='-', c='k')

    # PLOT OF THE CYCLES
    if cycles:
        cyclvar = allvars[key]['cycles']
        tmcycles = cyclvar['t_mean_cycle']

        # Plot of each period by a rectangle

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
    plt.title("Evolution of {key} in model #{idx}"
              + sol.model['name'] + '| system number' + str(idx))
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
              + sol.model['name'] + '| system number' + str(idx))

    plt.show()


def AllPhaseSpace(sol, variablesREF, idx=0):
    plt.figure('All Phasespace for system :'+str(idx)+' for model : ' +
               sol.model['name'], figsize=(10, 7))
    fig = plt.gcf()
    leng = len(variablesREF)
    NumbOfSubplot = int(leng*(leng-1)/2)

    idd = 1
    for ii, var1 in enumerate(variablesREF):
        for var2 in variablesREF[ii+1:]:

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
    plt.suptitle('All Phasespace for system :'+str(idx)+' for model : ' +
                 sol.model['name'])
    plt.show()
