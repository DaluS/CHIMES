# -*- coding: utf-8 -*-
'''
THIS COCKPIT ALLOW ONE TO TEST IF HIS MODEL IS GIVING BACK
'''

import imageio
import cv2
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt


##############################################################################
_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')
### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=True,
)

_MODEL = 'GK'
_MODEL_REDUCED = _MODEL+"-Reduced"

# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=False,
)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
_SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# PRESET ####################################################################
_DPRESET = {'default': {
    'fields': {
        'dt': 0.01,
        'a': 1,
        'N': 1,
        'K': 2.7,
        'D': 0.2,
        'w': .85,
        'p': 1,
        'eta': 0.01,
        'gammai': 0.5,
        'alpha': 0.02,
        'beta': 0.025,
        'nu': 3,
        'delta': .005,
        # 'phinull': .04,
        'k0': -0.0065,
        'k1': np.exp(-5),
        'k2': 20,
        'r': 0.03,
    },
    'com': (
        'This is a run that should give simple '
        'convergent oscillations'),
    'plots': [],
},
}


# %% LOADING AND COPYING MODELS #############################################

blueprint = 'GK'
model = 'GK-Reduced'
preset = 'default'

hub = pgm.Hub(blueprint, preset='default', dpresets=_DPRESET, verb=False)
hub_reduced = pgm.Hub(model, verb=False)

# COPY OF THE PARAMETERS INTO A NEW DICTIONNARY
FieldToLoad = hub_reduced.get_dparam(returnas=dict, eqtype=[None, 'ode'],
                                     group=('Numerical',),)
R = hub.get_dparam(returnas=dict)
tdic = {}
for k, v in FieldToLoad.items():
    val = R[k]['value']
    if 'initial' in v.keys():
        tdic[k] = val[0][0]
    else:
        tdic[k] = val

_DPRESETS = {'Copy'+_MODEL: {'fields': tdic, }, }

# LOADING THE MODEL WITH A NEW MODEL
hub_reduced = pgm.Hub(_MODEL_REDUCED, preset='Copy'+_MODEL,
                      dpresets=_DPRESETS)

# RUNS
hub_reduced.run(verb=0, solver=_SOLVER)
hub.run(verb=0, solver=_SOLVER)

# PLOTS
R = hub.get_dparam(returnas=dict)
Rr = hub_reduced.get_dparam(returnas=dict)

Tocompare = ['lambda', 'omega', 'd',
             'phillips', 'kappa', 'inflation', 'pi', 'g']

plt.figure()
for i, k in enumerate(Tocompare):
    plt.subplot(4, 2, i+1)
    plt.plot(R['time']['value'], R[k]['value'], label='Full')
    plt.plot(Rr['time']['value'], Rr[k]['value'], ls='--', label='Reduced')
    plt.ylabel(k)
plt.suptitle('Comparison model GK Full and Reduced')
plt.show()
