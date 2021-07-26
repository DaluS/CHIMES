# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""

import matplotlib.pyplot as plt


def printbasic(sol, rows=2):
    lkeys, array = sol.get_variables_compact()

    t = array[:, -1]
    plt.figure('All variables', figsize=(20, 10))
    for i in range(len(lkeys)-1):
        lk = lkeys[i]
        val = array[:, i]
        plt.subplot(len(lkeys)-1, rows, i+1)

        plt.plot(t, val)
        plt.ylabel(lk)
    plt.suptitle(list(sol.model.keys())[0])
    plt.show()
