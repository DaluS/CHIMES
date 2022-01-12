# -*- coding: utf-8 -*-
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
#_MODEL = '3Layerclimate'

# ECONOMIC MODEL
#_MODEL = 'GK-Reduced'
#_MODEL = 'GK'
_MODEL = 'Goodwin'
#_MODEL = 'Goodwin-Reduced'


# SOLVER #####################################################################
dsolvers = pgm.get_available_solvers(returnas=dict, verb=False,)
_SOLVER = 'eRK1-homemade'  # (One we created by ourself, that we can tweak)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# LOADING MODEL IN HUB #######################################################
hub = pgm.Hub(_MODEL)
# hub.set_dparam(preset='crisis')
hub.set_dparam(key='dt', value=0.001)
hub.run(verb=1.1, solver=_SOLVER)
hub.plot()

R = hub.get_dparam(returnas=dict)
