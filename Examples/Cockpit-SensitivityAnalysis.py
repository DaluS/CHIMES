# -*- coding: utf-8 -*-
"""
# THIS IS AN EXAMPLE ON HOW TO


Created on Wed Jan  5 11:12:57 2022

@author: Paul Valcke
"""

import os
import numpy as np
import pygemmes as pgm


import matplotlib.pyplot as plt
from pygemmes._plots import _plot_timetraces


# Load the model
_MODEL = 'GK-Reduced'
hub = pgm.Hub(_MODEL)

# Generate the list of everything we can tweak for sensibility
AllFieldsKeys = hub.dmisc['parameters']+hub.dmisc['dfunc_order']['ode']


# Generate a dictionary of dictionary, with for each key : { 'mean value", 'std' , 'distribution' }
SensitivityDic = {
    'alpha': {'mu': .02,
              'sigma': .12,
              'type': 'log'},
    'k2': {'mu': 20,
           'sigma': .12,
           'type': 'log'},
    'mu': {'mu': 1.3,
           'sigma': .12,
           'type': 'log'},
}


presetSimple = pgm.GenerateIndividualSensitivity(
    'alpha', 0.02, .2, disttype='log', N=10)
presetCoupled = pgm.GenerateCoupledSensitivity(SensitivityDic, N=10, grid=False)

_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }

hub = pgm.Hub(_MODEL, preset='SensitivityCoupled', dpresets=_DPRESETS)
hub.run(verb=1.1)
hub.reinterpolate_dparam(1000)
hub.CalculateStatSensitivity()
dax = _plot_timetraces.plot_timetraces(hub, SENSITIVITY=True)


hub = pgm.Hub('Noise')
hub.set_dparam(key='sigmanoise', value=np.linspace(.1, .1, 50))
hub.run()
hub.CalculateStatSensitivity()
hub.plot(SENSITIVITY=True)
