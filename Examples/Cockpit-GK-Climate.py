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

# A simple economy : A Goodwin-Keen system

# Extensive Goodwin-keen system

# Logics


pgm.GenerateIndividualSensitivity()
pgm.GenerateCoupledSensitivity()


# Run straight from the library

# Run a preset

# Writing your own preset

# Looking at sensitivity in parameters or initial conditions

# One-field sensitivity

# Multiple fields sensitivity

# Reduced Goodwin-Keen system

# Bridging both
pgm.create_preset_from_model_preset(targetmodel, outputmodel)

# Frequency analysis of trajectories

###

# Loading-saving
pgm.get_available_output()
