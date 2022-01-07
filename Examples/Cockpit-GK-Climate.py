# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 17:32:09 2022
@author: Paul Valcke
"""

'''
# Demonstration of Pygemmes : A look on economy-climate dynamic coupling

This jupyter notebook provide :
* A tutorial on how to use Pygemmes
* An explanation on the way we model
* An analysis of coupled systems in economy and climate
'''

# Short Overview of Pygemmes
'''
Pygemmes is an ensemble of tools put together in a user/modeler friendly way,
to study dynamical systems in general.

Pygemmes has three main components :
    * `def_fields`, a library of quantities with their definition (a comment, an unit, a typical value...)
    * `_models_` files, an ensemble of logical expression linking fields
    * `_core` an ensemble of routines that read models and extract the information the user is looking for

The user will typically pilot Pygemmes with a cockpit that contains typical instructions.
'''


# Exploring the solvers coded

import pygemmes as pgm
pgm.get_available_solvers()
'''
Each solver will have a different behavior. Here is an example of all solvers on the same system, same parameters
'''

print(150*'#')
pgm.comparesolver_Lorenz(dt=0.01, Npoints=1000)
pgm.plot_one_run_all_solvers('LorenzSystem', preset='Canonical example')
pgm.plot_one_run_all_solvers('GK')
#pgm.testConvergence_DampOsc([1, 0.1, 0.01, 0.001], solver='eRK4-homemade')

# Exploring the library
pgm.get_dfields_overview()
print(150*'#')


# Exploring the models already coded (without running them)
pgm.get_available_models(details=True, verb=True)
print(150*'#')

# Showing the graph of interaction for each models
'''
for model in pgm.get_available_models(details=False, verb=False, returnas=list):
    print(model)
    pgm.showVariableGraph(model)
    print(50*'#')
'''

# Multiple type of trajectories : Dampened oscillator
lpreset = ['Perfect Oscillations',
           'FirstOrder',
           'Overdamp',
           'Critical',
           'Underdamped']
hub = pgm.Hub('DampOscillator')
hub.run()
dax = hub.plot()
for preset in lpreset:
    hub = pgm.Hub('DampOscillator', preset=preset)
    hub.run()
    dax = hub.plot(dax=dax, label=preset)

# An in-depth example : A Goodwin-Keen system
hub = pgm.Hub('GK')

# Extensive Goodwin-keen system

# Logics and model description
hub.dmodel
hub.equations_description()
pgm.showVariableGraph('GK')
hub.dmisc
hub.get_summary()


# Often less useful
hub.dparam
hub.dargs
hub.dfunc_order


# Run straight from the library

# Run a preset
hub.dmodel['preset']

# Writing your own preset
hub.set_dparam


# Looking at sensitivity in parameters or initial conditions
pgm.GenerateIndividualSensitivity()
pgm.GenerateCoupledSensitivity()

# Accessing data
hub.get_variables_compact
hub.run()
hub.reinterpolate_dparam()
hub.plot()

# One-field sensitivity

# Multiple fields sensitivity

# Reduced Goodwin-Keen system

# Bridging both
pgm.create_preset_from_model_preset(targetmodel, outputmodel)

# Frequency analysis of trajectories
hub.findCycles
###

# Loading-saving
pgm.get_available_output()
