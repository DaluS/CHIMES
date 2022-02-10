# -*- coding: utf-8 -*-
"""

import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`
"""




import pygemmes as pgm
import numpy as np

'''
Always use tab on pgm or hub, and ? on each functions
'''

# ############################################################################
# #######################  LEVEL 1 : USER ####################################
# ############################################################################
'''
A user is someone who do not write his own models, but use the one of others for
analysis.
'''

# %% OVERVIEW OF PYGEMMES
pgm.get_available_fields()
pgm.get_available_models(details=False)
pgm.get_available_solvers()
pgm.get_available_functions()

pgm.get_available_models(details=True)

listofsolver = pgm.get_available_solvers(returnas=list)
listofmodels = pgm.get_available_models(returnas=list)



# %% LOADING A MODEL
Modelname = 'GK'

hub = pgm.Hub('GK')
hub = pgm.Hub('GK',verb=True)

# EXPLORING IT
hub.get_summary()
hub.equations_description()

hub.Network()
hub.Network(params=True)

# %% MISC SUPPLEMENTARY INFORMATION
hub.dmodel  # Gives the content of the model file
hub.dmisc   # gives multiple informations on the run and the variables
hub         # Minimalist informations

# %% Calculation
hub.run()
hub.run(verb=1.1)
hub.run(solver=listofsolver[3])

hub.get_summary()

# %% Plots
dax = hub.plot()
dax2 = hub.plot(key=['lambda', 'omega', 'd'])  # Select the variables
dax3 = hub.plot(key=('GDP', 'a', 'Pi', 'kappa'))  # Remove some variables
hub.plot_preset(preset='default')


# %% Get your data accessible
R = hub.get_dparam()
R.keys()
R['lambda'].keys()
np.shape(R['lambda']['value'])

# %% Reinterpolate data to be lighter
hub.reinterpolate_dparam(100)
R = hub.get_dparam()
np.shape(R['lambda']['value'])

# %% Get more subtle criterias ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
R1= hub.get_dparam(key=['lambda','omega'])
R2= hub.get_dparam(key=('lambda','omega'))
R1.keys()
R2.keys()

groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])

# %% STUDY OF CYCLES
hub.FillCyclesForAll(ref='lambda')
dax4 = hub.plot(mode='cycles',key=['lambda','omega','d','phillips'])


# %% ##################### CHANGING VALUES ###################################

# %% Using presets
pgm.get_available_models(model='GK',details=True)
hub = pgm.Hub(model='GK',preset='default')
hub.run()
hub.plot_preset(preset='default')
# dpreset use will be explained later

# %% Using  set_dparam
hub = pgm.Hub('GK')
hub.set_dparam(preset='default')

# Changing one parameter
hub = pgm.Hub('GK')
hub.set_dparam(key='dt', value=0.01)
hub.set_dparam(Tmax=50)

# Put a dictionnary
dparam = {'alpha': 0, 'n': 1}
hub.set_dparam(**dparam)

# Create N system in parrallel with different values
hub.set_dparam(alpha=[0, 0.01, 0.02, 0.03])
hub.get_summary()
hub.run()
dax= hub.plot(key=['lambda','omega'])

# %% ################### CALCULATING SENSIVITY ###############################
SensitivityDic = {
    'alpha': {'mu': .02,
              'sigma': .12,
              'type': 'log'},
    'k2': {'mu': 20,
           'sigma': .12,
           'type': 'log'},
    'mu': {'mu': 1.3,
           'sigma': .12,
           'type': 'log'},
}

presetSimple = pgm.GenerateIndividualSensitivity(
    'alpha', 0.02, .2, disttype='log', N=10)
presetCoupled = pgm.GenerateCoupledSensitivity(SensitivityDic, N=10, grid=False)

hub = pgm.Hub('GK')
hub.set_dparam(**presetCoupled)
hub.run()
dax = hub.plot()

hub.CalculateStatSensitivity()
dax = hub.plot(mode='sensitivity')

# %% GENERATE DPRESET AND USE IT
_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }
hub = pgm.Hub('GK', preset='SensitivityCoupled', dpresets=_DPRESETS)



# %% EXERCICES ##########################################
'''
Exercise 1 : execute by yourself
    1. Loading library "From scratch", load pygemmes
    2. Access lists get the list of models, the list of solvers
    3. Load a model, then with a preset directly loaded
    4. change value Run it with different timestep
    5. change solver Run it with different solvers
    6. Plots Plot only lambda, then everything but lambda, then with cycles analysis activated
    7. Exploring dparam structure print all the keys of one field in dparam, then all their values
    8. Getting dparam values Get the values of omega over time as an array, plot it manually
    9. Creating multiple process Create a preset with 5 values of the rate of productivity progres

Exercise 2 : editing
    1. Accessing your personal folder find your personal folder where all models are
    2. Copy-paste a file Copy the file model GK-Reduced, name it GK-CES-Reduced then reload
pygemmes to see if you can load id
    3. Modify the equations Use the equations for "lambda, omega, d" you find in McIsaac et al,
Minskyan classical growth cycles, Mathematics and Financial Economics with the introduction
of new parameters in _def_fields
    4. See the impact of a parameter (1) Do an ensemble of run with different elasticity values
    5. See the impact on cycles Show the impact of the elasticity value on the cycles
    6. See the impact on stability Do a stability analysis with different values

Exercise 3 : add on github
    1. Create an issue on the github page
    2. Once your model is ready, put it in pygemmes/_models
    3. Create a branch with your modifications and push it
    4. Create a Pull Request with it

'''

# %% TESTS ##########################################
# TO TEST THAT EVERYTHING IS WORKING WELL
# !pytest pygemmes/tests/test_01_Hub.py -v
# !pytest pygemmes/tests/test_00_get -v
# !pytest pygemmes/tests/test_02_Hub_Multiple -v
# !pytest pygemmes/tests/test_03_articles -v
