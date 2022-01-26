#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:20:03 2021

@author: camille
"""

import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt

_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')

### MODELS LIST ##############################################################
#Choix d'un modèle 
#dmodels donne la liste des modèles et presets
#dmodels = pgm.get_available_models(returnas=dict, details=False, verb=True,)
#_MODEL = 'ResourcesOnlySimple'
_MODEL = 'GKResourcesSimple'

# SOLVER #####################################################################
#choix d'un solveur
#dsolvers = pgm.get_available_solvers(returnas=dict, verb=False,)
_SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4)


# LOADING MODEL IN HUB #######################################################
hub = pgm.Hub(_MODEL)#chargement du modèle
# hub.load_preset('crisis')
hub.set_dparam(key='dt', value=0.001)
hub.run(verb=1.1, solver=_SOLVER)
hub.plot()

plots.phasespace(hub, x='R', y='M', color='time', idx=0)

R = hub.get_dparam(returnas=dict)