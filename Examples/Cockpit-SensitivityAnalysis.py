# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:12:57 2022

@author: Paul Valcke
"""

import os
import numpy as np
import pygemmes as pgm

# Load the model
_MODEL = 'GK-Reduced'
hub = pgm.Hub(_MODEL)

# Generate the list of everything we can tweak for sensibility
AllFieldsKeys = hub.dmisc['parameters']+hub.dmisc['dfunc_order']['ode']


# Generate a dictionary of dictionary, with for each key : { 'mean value", 'std' , 'distribution' }
SensitivityDic = {
    'alpha': {'mu': .02,
              'sigma': .2,
              'type': 'log'},
    'k2': {'mu': 20,
           'sigma': .2,
           'type': 'log'},
    'mu': {'mu': 1.3,
           'sigma': .2,
           'type': 'log'},
}


preset = pgm.Toolbox.GenerateIndividualSensitivity(
    'alpha', 0.02, .2, disttype='log', N=10)
preset = pgm.Toolbox.GenerateCoupledSensitivity(SensitivityDic, N=10)
