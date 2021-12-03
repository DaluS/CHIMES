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

##############################################################################
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
#_MODEL = 'MonoGEM'


# SOLVER #####################################################################
dsolvers = pgm.get_available_solvers(returnas=dict, verb=False,)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy' #(an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# LOADING MODEL IN HUB #######################################################
'''
hub = pgm.Hub(model=None,
              preset=None,
              dpresets=None,
              verb=None)
'''
hub = pgm.Hub(_MODEL)


# CHANGING VALUES AND PRESETS ################################################
'''
set_dparam(
        self,
        dparam=None,
        key=None,
        value=None,
        grid=None,
        verb=None,
        )
'''


hub.set_dparam({'Tmax': 20,
                'dt': 0.005,
                'lambda': np.linspace(.5, .99, 20),
                'omega': {'value': np.linspace(.5, .99, 20), 'grid': True},
                'd': {'value': np.linspace(10, 20, 11), 'grid': True},
                },)

# hub.load_preset('crisis')


# %% SOLVER ##################################################################
'''
solver =
'eRK4-homemade' (One we created by ourself, that we can tweak)
'eRK2-scipy' (an Runge Kutta solver of order 2)
'eRK4-scipy' (an Runge Kutta solver of order 4)
'eRK8-scipy' (an Runge Kutta solver of order 8)

verb =
0 print nothing
1 print all steps number but on the same line
2 print all steps each time on the same line
1.1 (or any float) will print the number of the iteration every time this value
    of time is spent (1.1 will give a print every 1.1 seconds)
    When using an IDE, use either 0 or a float
    (IDE don't work well with 1 and 2)

compute_auxiliary=None,
solver=None,
verb=None,
rtol=None,
atol=None,
max_time_step=None)
'''
hub.run(verb=1.1, solver=_SOLVER)
hub.get_summary(idx=None)


# GETTING VALUES #############################################################
'''
get_dparam(self,
           condition=None,
           verb=None,
           returnas=None,
           **kwdargs):
        """
        Return a copy of the input parameters dict as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)
        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing
        """
        lcrit = ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
        lprint = ['parameter', 'value', 'units', 'dimension', 'symbol',
            'type', 'eqtype', 'group', 'comment',
        ]
'''

R = hub.get_dparam(returnas=dict)
FieldToLoad = hub_reduced.get_dparam(returnas=dict,
                                     eqtype=[None, 'ode'],
                                     group=('Numerical',),)

'''
get_dparam_as_reverse_dict(
        self,
        crit=None,
        returnas=None,
        verb=None,
        **kwdargs,
    ):
        """ Return/prints a dict of units/eqtype... with a list of keys

        if crit = 'units', return a dict with:
            - keys: the unique possible values of field 'units'
            - values: for each unique unit, the corresponding list of keys

        Restrictions on the selection can be imposed by **kwdargs
        The selection is done using self.get_dparam() (single-sourced)
        """
'''
hub.get_dparam_as_reverse_dict(crit='units', eqtype=(None,))
hub.get_dparam_as_reverse_dict(crit='units', eqtype=None)
groupsoffields = hub.get_dparam_as_reverse_dict(crit='units')
hub.get_dparam_as_reverse_dict(crit='eqtype')


# %% Saved run available
dout = pgm.get_available_output(
    path=_PATH_OUTPUT_REF, returnas=dict, verb=True,
)


# %% Load a file
# sol_load = _core._saveload.load(' ')


# %% SAVE
# hub.save()#path=...)


# %% Informations
hub.get_summary(idx=0)  # Summary of all variables, definitions and values
hub.dfunc_order  # Order of equation resolutions
hub.dmodel  # Informations from the model file
hub.dargs  # All dependencies values for each
hub.dparam  # Full fields informations
hub.dmisc  # Miscallenous informations

allkey, allvars = hub.get_variables_compact(eqtype=None)


# %% SHORT RUN ###############################################################

for _MODEL in dmodels.keys():
    for _SOLVER in dsolvers.keys():
        for preset in dmodels[_MODEL]['presets']:
            hub = pgm.Hub(_MODEL)  # , preset=preset, verb=False)
            # hub = pgm.Hub(_MODEL, preset='BasinOfAttraction', dpresets=_DPRESETS)
            # hub.set_dparam(key='alpha', value=10)
            # hub.load_preset('crisis')
            hub.run(verb=0, solver=_SOLVER)
            # hub.plot()


# %% DEEPER ANALYSIS
hub.FillCyclesForAll(ref='lambda')
# hub.FillCyclesForAll(ref=None)


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


groupsofvariables = {k: [v for v in vals if v in hub.dargs.keys()]
                     for k, vals in groupsoffields.items()}


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
