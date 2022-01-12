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


def groupofvariables(hub):
    ''' Gives from the hub a dictionnary of all the variables that shares the same units'''
    groupsoffields = hub.get_dparam_as_reverse_dict(crit='units')
    hub.get_dparam_as_reverse_dict(crit='eqtype')
    return {k: [v for v in vals if v in hub.dargs.keys()]
            for k, vals in groupsoffields.items()}


##############################################################################
_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')
### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=True,
)

_MODEL = 'MonoGEM'
#_MODEL = 'DampOscillator'
#_MODEL = 'LorenzSystem'
#_MODEL = 'GK-Reduced'
#_MODEL = 'GK'

# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=False,
)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy' #(an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# %% SHORT RUN ###############################################################
hub = pgm.Hub(_MODEL)  # , preset=preset, verb=False)
hub.run(verb=0, solver=_SOLVER)
hub.plot()

'''
hub.run(verb=0, solver=_SOLVER)
hub.plot()


R = hub.get_dparam(returnas=dict)
# %% Saved run available
dout = pgm.get_available_output(
    path=_PATH_OUTPUT_REF, returnas=dict, verb=True,
)


# %% Load a model

hub = pgm.Hub(_MODEL)  # , preset='default')
# hub.set_dparam(preset='crisis')


# %% Load a file
# sol_load = _core._saveload.load(' ')


# %% Change a parameter

* To change a parameter :  `hub.set_dparam(key='alpha', value=0.01)`


hub.set_dparam(**{'a' : [1,2,'lin']})
hub.set_dparam(**{'a' : [1,2,'log'],
                  'alpha' : 0.03})
hub.set_dparam(**{'nx': 100})
hub.set_dparam(**{'a': [1,2,3]})


# %% Runs


'eRK4-homemade' (One we created by ourself, that we can tweak)
'eRK2-scipy' (an Runge Kutta solver of order 2)
'eRK4-scipy' (an Runge Kutta solver of order 4)
'eRK8-scipy' (an Runge Kutta solver of order 8)
We can also ask the solver to give more or less information about where it is
    in the resolution :

0 print nothing
1 print all steps number but on the same line
2 print all steps each time on the same line
1.1 (or any float) will print the number of the iteration every time this value
    of time is spent (1.1 will give a print every 1.1 seconds)
    When using an IDE, use either 0 or a float
    (IDE don't work well with 1 and 2)

hub.run(verb=1.1)

# %% Informations
hub.get_summary(idx=0)
hub.dfunc_order
hub.dmodel
hub.dargs
hub.dparam
hub.dmisc
allkey, allvars = hub.get_variables_compact(eqtype=None)

Result = hub.get_dparam(returnas=dict)


# %% DEEPER ANALYSIS
hub.FillCyclesForAll(ref='lambda')
# hub.FillCyclesForAll(ref=None)

# %% SAVE
# hub.save()#path=...)

# %% PLOTS

# dax = hub.plot(eqtype='ode', label='homemade', color='b')

hub.plot()

plots.Var(hub, 'K', idx=0, cycles=True, log=True)
plots.Var(hub, 'lambda', idx=0, cycles=True, log=False)


# plots.AllPhaseSpace(hub, groupsofvariable['undefined'], idx=0)

plots.ForEachUnitsGroup(hub)

plots.phasespace(hub, x='omega', y='lambda', color='time', idx=7)
plots.phasespace(hub, x='omega', y='d', idx=0)
plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)


# dimensionlessnumbers = ['omega', 'lambda', 'd']
# plots.AllPhaseSpace(hub, dimensionlessnumbers, idx=0)


hub.get_dparam_as_reverse_dict(crit='units', eqtype=(None,))
hub.get_dparam_as_reverse_dict(crit='units', eqtype=None)


groupsoffields = hub.get_dparam_as_reverse_dict(crit='units')
hub.get_dparam_as_reverse_dict(crit='eqtype')
groupsofvariables = {k: [v for v in vals if v in hub.dargs.keys()]
                     for k, vals in groupsoffields.items()}
'''
