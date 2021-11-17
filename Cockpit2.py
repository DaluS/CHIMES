# -*- coding: utf-8 -*-
# !pytest pygemmes/tests/test_01_Hub.py -v
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots


def groupofvariables(hub):
    ''' Gives from the hub a dictionnary of all the variables that shares the same units'''
    groupsoffields = hub.get_dparam_as_reverse_dict(crit='units')
    hub.get_dparam_as_reverse_dict(crit='eqtype')
    return {k: [v for v in vals if v in hub.dargs.keys()]
            for k, vals in groupsoffields.items()}


### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=True,
)
_MODEL = 'DampOscillator'
_MODEL = 'LorenzSystem'

# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=True,
)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy' #(an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy' #(an Runge Kutta solver of order 8)

# PRESETS ###################################################################
_DPRESETS = {'BasinOfAttraction':
             {'fields': {'Tmax': 20,
                         'dt': 0.0001,
                         'd': 5,
                         'lambda': np.linspace(.5, .99, 15),
                         'omega': {'value': np.linspace(.5, .99, 15),
                                   'grid': False},
                         },
              },
             }


# %% SHORT RUN ###############################################################
for preset in dmodels[_MODEL]['presets']:
    hub = pgm.Hub(_MODEL, preset=preset)
    # hub = pgm.Hub(_MODEL, preset='BasinOfAttraction', dpresets=_DPRESETS)
    # hub.set_dparam(key='alpha', value=10)
    # hub.load_preset('crisis')
    hub.run(verb=1.1, solver=_SOLVER)
    hub.plot()
    #plots.phasespace(hub, x='theta', y='thetap', color='time', idx=1)
# hub.FillCyclesForAll(ref='lambda')
# hub.FillCyclesForAll(ref=None)

   # plots.Var(hub, 'lambda', idx=0, cycles=True, log=False)

R = hub.get_dparam(returnas=dict)


fig = plt.figure('', figsize=(20, 20))
ax = plt.axes(projection='3d')
for idx in range(1):
    ax.plot(R['x']['value'][:, idx], R['y']['value']
            [:, idx], R['z']['value'][:, idx])
plt.show()


# %% LOAD/ Saved run available ###############################################
'''
dout = pgm.get_available_output(
    path=_PATH_OUTPUT_REF, returnas=dict, verb=True,
)
# sol_load = _core._saveload.load(' ')
# hub.save()#path=...)
'''


# %% Informations
'''
hub.get_summary(idx=0)
hub.dfunc_order
hub.dmodel
hub.dargs
hub.dparam
hub.dmisc
allkey, allvars = hub.get_variables_compact(eqtype=None)
'''
Result = hub.get_dparam(returnas=dict)


# %% DEEPER ANALYSIS
hub.FillCyclesForAll(ref='lambda')


# %% PLOTS
# dax = hub.plot(eqtype='ode', label='homemade', color='b')
hub.plot()

plots.Var(hub, 'K', idx=0, cycles=True, log=True)
plots.Var(hub, 'lambda', idx=0, cycles=True, log=False)


# plots.AllPhaseSpace(hub, groupsofvariable['undefined'], idx=0)

plots.ForEachUnitsGroup(hub)

plots.phasespace(hub, x='omega', y='lambda', color='time', idx=0)
plots.phasespace(hub, x='omega', y='d', idx=0)
plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)

#plots.AllPhaseSpace(hub, dimensionlessnumbers, idx=0)
