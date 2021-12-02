# -*- coding: utf-8 -*-
'''
Contains all the possibilities of each _core interaction
# !pytest pygemmes/tests/test_01_Hub.py -v
'''

import imageio
import cv2
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt

_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')


### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(returnas=dict, details=False, verb=True,)

# NON-ECONOMIC MODEL
#_MODEL = 'DampOscillator'
#_MODEL = 'LorenzSystem'
#_MODEL = 'DoublePendulum'

# ECONOMIC MODEL
_MODEL = 'GK-Reduced'
#_MODEL = 'GK'


# SOLVER #####################################################################
dsolvers = pgm.get_available_solvers(returnas=dict, verb=False,)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy' #(an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# LOADING MODEL IN HUB #######################################################

for _MODEL in dmodels.keys():
    for _SOLVER in dsolvers.keys():
        for preset in dmodels[_MODEL]['presets']:
            print(_MODEL, _SOLVER, preset)
            hub = pgm.Hub(_MODEL, preset=preset, verb=False)
            hub.run(verb=1.1, solver=_SOLVER)
            hub.plot()


# CHANGING VALUES AND PRESETS ################################################
hub.set_dparam({'Tmax': 20,
                'dt': 0.005,
                'lambda': np.linspace(.5, .99, 20),
                'omega': {'value': np.linspace(.5, .99, 20), 'grid': True},
                'd': {'value': np.linspace(10, 20, 11), 'grid': True},
                },)
# hub.load_preset('crisis')

hub.get_summary(idx=None)
R = hub.get_dparam(returnas=dict)


# %% DEEPER ANALYSIS
hub.FillCyclesForAll(ref='lambda')
plots.Var(hub, 'K', idx=0, cycles=True, log=True)


# %% ########################
dax = plots.plot(hub)
dax = plots.AllVar(hub, ncols=4, wintit='blabla', tit='test', fs=(12, 8))

dax = hub.plot(eqtype='ode', label='homemade', color='b')
dax = hub.plot(eqtype='ode', label='scipy', color='r', dax=dax)
dax = hub.plot(key=('phillips',), eqtype='statevar')  # All but Phillips
dax = hub.plot(key='phillips')     # only 'phillips'

dax = hub.plot(eqtype='ode', label='eRK4-homemade')
dax = hub.plot(eqtype='ode', label='eRK2-scipy', dax=dax)
dax = hub.plot(eqtype='ode', label='eRK4-scipy', dax=dax)
dax = hub.plot(eqtype='ode', label='eRK8-scipy', dax=dax)
