# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


def plotbasic(sol, rows=1, idx=0):
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
    for i in range(len(lkeys)-1):
        lk = lkeys[i]
        val = array[:, i, idx]
        plt.subplot(len(lkeys)-1, rows, i+1)

        plt.plot(t, val)
        plt.ylabel(lk)
    plt.suptitle(list(sol.model.keys())[0]+'||| system number :'+str(idx))
    plt.show()
    # else:
    #    print('Plot simple could not be done as the simulation did not run')


def plotVar(sol, key, idx=0):
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
    plt.figure('key :'+key+'| system idx'+str(idx), figsize=(10, 5))

    allvars = sol.get_dparam(returnas=dict)
    y = allvars[key]['value']
    t = allvars['time']['value']

    plt.plot(t, y)
    plt.ylabel(key)
    plt.xlabel('time')
    plt.show()


def plotphasespace(sol, x='omega', y='lambda', idx=0):

    allvars = sol.get_dparam(returnas=dict)
    yval = allvars[y]['value'][:, idx]
    xval = allvars[x]['value'][:, idx]
    t = allvars['time']['value'][:, idx]

    points = np.array([xval, yval]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(t)
    lc.set_linewidth(2)

    plt.figure('Phasespace'+x+' '+y+'for system :'+str(idx), figsize=(10, 10))
    fig = plt.gcf()
    ax = plt.gca()
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax, label='time (y)')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xlim([np.amin(xval), np.amax(xval)])
    plt.ylim([np.amin(yval), np.amax(yval)])
    plt.axis('scaled')
    plt.title('Phasespace '+x+'-'+y+' for model : ' +
              list(sol.model.keys())[0]+'| system number'+str(idx))

    plt.show()
