# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 12:18:18 2021

@author: Paul Valcke
"""
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt

_MODEL = 'GK'
Basefields = {
    'dt': 0.01,
    'a': 1,
    'N': 1,
    'K': 2.9,
    'w': .85*1.2,
    'alpha': 0.02,
    'n': 0.025,
    'nu': 3,
    'delta': .005,
    'k0': -0.0065,
    'k1': np.exp(-5),
    'k2': 20,
    'r': 0.03,
    'p': 1.3,
    'eta': 0.1,
    'gammai': 0.5,
}

_DPRESET = {'default': {
    'fields': Basefields,
    'com': '',
    'plots': [],
},
}


dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=False,
)


def comparesolvers(_MODEL, preset=False, _DPRESET=False):
    '''
    Will compare up to seven solver that exist in pygemmes, using the model and preset you provide
    * if no preset, nor dictionary of preset the system takes default values
    * if preset and not dictionary preset, preset must be the name of one of the model preset
    * if preset and _dpreset, the system will load the preset in _dpreset

    Parameters
    ----------
    _MODEL : TYPE
        Name of the model for test
    preset : TYPE, optional
        Name of the preset. if none default value
    _DPRESET : TYPE, optional
        preset dictionary. if none/false, presets from the model

    Returns
    -------
    Print of all solvers super-imposed
    '''

    colors = ['y', 'k', 'm', 'r', 'g', 'b', 'c']

    dhub = {}
    for ii, solver in enumerate(dsolvers):
        print('Solver :', solver)

        # LOADING OF THE MODEL WITH THE CORRESPONDING PRESET
        # IF PRESET AND PRESET FILE GIVEN
        if preset and _DPRESET:
            dhub[solver] = pgm.Hub(_MODEL, preset=preset,
                                   dpresets=_DPRESET, verb=False)

        # ELIF PRESET NAME GIVEN
        elif preset:
            dhub[solver] = pgm.Hub(_MODEL, preset=preset, verb=False)

        # ELSE USE OF BASIC VALUES
        else:
            dhub[solver] = pgm.Hub(_MODEL, verb=False)

        # RUN
        dhub[solver].run(verb=1.1, solver='eRK4-homemade')

        # PRINT
        # If first solver, creation of dax
        if ii == 0:
            dax = dhub[solver].plot(
                label=solver, color=colors[ii], wintit='Solver comparison on model'+_MODEL, tit='Solver comparison on model'+_MODEL)
        # Else use of dax
        else:
            dax = dhub[solver].plot(label=solver, ls='--',
                                    color=colors[ii], dax=dax)
    plt.show()


comparesolvers('GK', preset='default', _DPRESET=_DPRESET)
