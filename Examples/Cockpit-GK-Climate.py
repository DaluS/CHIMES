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
print(150*'#')


# Exploring the library
pgm.get_dfields_overview()
print(150*'#')


# Exploring the models already coded (without running them)
pgm.get_available_models(details=True, verb=True)
print(150*'#')


# Having the graphs for each moddel
for model in pgm.get_available_models(details=False, verb=False, returnas=list):
    print(model)
    pgm.showVariableGraph(model)
    print(50*'#')

# Showing the graph of interaction for each models

# Canonical examples with simple toolbox

# A chaotic system : Lorenz Attractor

# Multiple type of trajectories : Dampened oscillator

# A simple economy : A Goodwin-Keen system

# Extensive Goodwin-keen system

# Logics

# Scheme of interaction

# Run straight from the library

# Run a preset

# Writing your own preset

# Looking at sensitivity in parameters or initial conditions

# One-field sensitivity

# Multiple fields sensitivity

# Reduced Goodwin-Keen system

# Bridging both

# Frequency analysis of trajectories

###
