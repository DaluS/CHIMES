# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""

import matplotlib.pyplot as plt


def plotbasic(sol, rows=2, idx=0):
    '''
    Parameters
    ----------
    sol : The hub of the system
        DESCRIPTION.
    rows : TYPE, optional
        DESCRIPTION. The default is 2.
    idx : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    None.

    '''
    # if sol.__dmisc['run']:
    lkeys, array = sol.get_variables_compact()

    t = array[:, -1]
    plt.figure('All variables', figsize=(20, 10))
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
