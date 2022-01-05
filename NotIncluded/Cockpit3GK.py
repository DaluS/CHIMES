# -*- coding: utf-8 -*-
# !pytest pygemmes/tests/test_01_Hub.py -v
import matplotlib.pyplot as plt
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots

### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=True,
)
_MODEL = 'DampOscillator'
_MODEL = 'LorenzSystem'
_MODEL = 'GK-Reduced'
_MODEL = 'GK'

# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=True,
)
# _SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy' #(an Runge Kutta solver of order 4)
_SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)

# PRESETS ###################################################################
lambdavec = np.linspace(.75, .99, 10)
omegavec = np.linspace(.75, .99, 5)
_DPRESETS = {'BasinOfAttraction':
             {'fields': {'Tmax': 20,
                         'dt': 0.0005,
                         'd': 5,
                         'lambda': lambdavec,
                         'omega': {'value': omegavec,
                                   'grid': True},
                         },
              },
             }


# %% SHORT RUN ###############################################################
# for preset in dmodels[_MODEL]['presets']:
# hub = pgm.Hub(_MODEL)#, preset=preset)
hub = pgm.Hub(_MODEL, preset='BasinOfAttraction', dpresets=_DPRESETS)
# hub.set_dparam(key='alpha', value=10)
# hub.load_preset('crisis')
hub.run(verb=1.1, solver=_SOLVER)
hub.plot()
R = hub.get_dparam(returnas=dict)
#plots.phasespace(hub, x='theta', y='thetap', color='time', idx=1)
# hub.FillCyclesForAll(ref='lambda')
# hub.FillCyclesForAll(ref=None)

# plots.Var(hub, 'lambda', idx=0, cycles=True, log=False)


# 2D Plot for lambda,omega phase-space


lambdaXYZ = R['lambda']['value']
omegaXYZ = R['omega']['value']
dXYZ = R['d']['value']

Step = 0.1
Pause = 0.01
plt.figure('', figsize=(10, 10))
for i in range(0, R['nt']['value'], int(Step/R['dt']['value'])):
    plt.clf()
    date = R['time']['value'][i, -1, -1]
    plt.title("t ="+f"{date:.2f}"+" years")
    plt.pcolormesh(omegavec, lambdavec,
                   dXYZ[i, :, :], vmin=0, vmax=5, cmap='jet', shading='auto')
    plt.xlabel('$\lambda(t=0)$')
    plt.ylabel('$\omega(t=0)$')
    plt.colorbar()
    plt.pause(Pause)
plt.show()

#### 3D Plot on Lorenz ####
if _MODEL == "LorenzSystem":

    R = hub.get_dparam(returnas=dict)
    fig = plt.figure('', figsize=(10, 10))
    ax = plt.axes(projection='3d')
    for idx in range(3):
        ax.plot(R['x']['value'][:, idx], R['y']['value']
                [:, idx], R['z']['value'][:, idx])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.tight_layout()
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
