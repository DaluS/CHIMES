# -*- coding: utf-8 -*-
"""
import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import pygemmes as pgm
import numpy as np
import os

'''
Always use tab on pgm or hub, and ? on each functions
'''
# ########################################################################### #
# %%#####################  LEVEL 1 : USER ################################### #
# ########################################################################### #
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
hub = pgm.Hub('GK')
hub = pgm.Hub('GK', verb=True)

# EXPLORING IT
hub.get_summary()  # definition concern the field definition, com the way it is calculated
hub.get_equations_description()

hub.get_Network()
hub.get_Network(params=True)


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
hub.reinterpolate_dparam(1000)
R = hub.get_dparam()
np.shape(R['lambda']['value'])


# %% Get more subtle criterias ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
R1 = hub.get_dparam(key=['lambda', 'omega'])
R2 = hub.get_dparam(key=('lambda', 'omega'))
R1.keys()
R2.keys()

groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])


# %% STUDY OF CYCLES
hub = pgm.Hub('GK')
hub.run()
hub.calculate_Cycles(ref='lambda')
dax4 = hub.plot(mode='cycles', key=['lambda', 'omega', 'd', 'phillips'])

# && ####################### ACCESS TO INDIVIDUAL PLOTS ######################
hub = pgm.Hub('GK')

# Plots that are not related to a run but to a function
pgm.plots.slices_wholelogic(hub, key='kappa', axes=[['pi', 0, 0.3]], N=100, tid=0, idx=0)
pgm.plots.slices_wholelogic(hub, key='L', axes=[['a', 1, 3], ['K', 1, 5]], N=100, tid=0, idx=0)

# Plots related to a run
hub.run()

pgm.plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)
pgm.plots.phasespace(hub, x='lambda', y='pi', color='d', idx=0)
pgm.plots.plotnyaxis(hub, x='time',
                     y=[['lambda', 'omega'],
                        ['d'],
                        ['kappa', 'pi'],
                        ],
                     idx=0,
                     title='',
                     lw=2)
pgm.plots.plot_timetraces(hub, key=['lambda', 'omega', 'd'])
pgm.plots.plot3D(hub, x='lambda',
                 y='omega',
                 z='d',
                 cinf='pi',
                 cmap='jet',
                 index=0,
                 title='')
pgm.plots.plotbyunits(hub)


# Plots about derivates
hub.calculate_variation_rate()

pgm.plots.plot_variation_rate(hub, ['omega', 'lambda', 'd', 'D']
                              )

# plots about cycles
hub.calculate_Cycles(ref='omega')

pgm.plots.cycles_characteristics(hub, xaxis='omega',
                                 yaxis='lambda',
                                 ref='omega')
# %% CHANGING VALUES ########################################################
'''
Order of loading values/status (latest in the one kept) :
    * the fields library (by default)
    * the values inside _LOGICS of the model
    * the values of the loaded preset
    * the values of set_dparam
'''


# %% Using presets
pgm.get_available_models(model='GK', details=True)
hub = pgm.Hub(model='GK', preset='default')
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
hub = pgm.Hub('GK')
hub.set_dparam(alpha=[0,
                      0.01,
                      0.02,
                      0.03])
hub.get_summary()
hub.run()
dax = hub.plot(key=['lambda',
                    'omega'])


# %% CALCULATING SENSIVITY ##################################################
'''
Instead of doing one run, we do N run in parrallel, with each field having a
value in its distribution
'''

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

presetSimple = pgm.generate_dic_distribution(
    {'alpha': {'mu': 0.02,
               'sigma': .2,
               'type': 'log'}, }, N=10)

presetCoupled = pgm.generate_dic_distribution(SensitivityDic,
                                              N=10,
                                              grid=False)

hub = pgm.Hub('GK')
hub.set_dparam(**presetCoupled)
hub.run()
dax = hub.plot()

hub.reinterpolate_dparam(1000)
hub.calculate_StatSensitivity()
dax = hub.plot(key=['lambda', 'omega'], mode='sensitivity')


# %% GENERATE DPRESET AND USE IT
_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }
hub = pgm.Hub('GK', preset='SensitivityCoupled', dpresets=_DPRESETS)
hub.run()
hub.reinterpolate_dparam(1000)
hub.calculate_StatSensitivity()
dax = hub.plot(mode='sensitivity')

# %% BASIN OF ATTRACTIONS ####################################################
'''
This is an example on how someone can do more complex analysis
'''


# Initialisation of the system with 1000 points in a box
hub = pgm.Hub('Reduced_GK', preset='default')

BasinDomain = {
    'lambda': {'mu': 0.5,
               'sigma': 0.99,
               'type': 'uniform'},
    'omega': {'mu': 0.5,
              'sigma': .98,
              'type': 'uniform'},
    'd': {'mu': -1,
          'sigma': 1,
          'type': 'uniform'},
}
initcond = pgm.generate_dic_distribution(BasinDomain,
                                         N=1000,
                                         grid=False)

hub.set_dparam(**initcond)
hub.run()
hub.reinterpolate_dparam(N=1000)


# Point we are trying to reach
finalpoint = {
    'lambda': 0.967297870750419,
    'omega': 0.84547946985534,
    'd': -0.0771062162051694,
}

# We get the convergence rate
ConvergeRate = hub.calculate_ConvergeRate(finalpoint)
R = hub.get_dparam(key=[k for k in finalpoint]+['time'], returnas=dict)


# Plot of everything ####################
fig = plt.figure('3D', figsize=(10, 10))
cmap = mpl.cm.jet_r
ax = plt.axes(projection='3d')
ax.set_xlabel(r'$\lambda$')
ax.set_ylabel(r'$\omega$')
ax.set_zlabel('d')
t = R['time']['value'][:, 0]

# All the final points
ax.scatter(finalpoint['lambda'],
           finalpoint['omega'],
           finalpoint['d'],
           s=50,
           c='k')

# Scatter plot
R = hub.get_dparam(key=[k for k in finalpoint]+['time'], returnas=dict)
scat = ax.scatter(R['lambda']['value'][0, ConvergeRate > 0.001],
                  R['omega']['value'][0, ConvergeRate > 0.001],
                  R['d']['value'][0, ConvergeRate > 0.001],
                  c=ConvergeRate[ConvergeRate > 0.001],
                  cmap=cmap,
                  norm=mpl.colors.LogNorm(vmin=10**(-3)))
plt.axis('tight')

# Add trajectory of converging points
'''
for i in range(len(ConvergeRate)):
    if ConvergeRate[i]:
        ax.plot(R['lambda']['value'][:, i],
                R['omega']['value'][:, i],
                R['d']['value'][:, i], c='k', lw=0.1)
'''
# Add colobar
cbar = fig.colorbar(scat)
cbar.ax.set_ylabel(r'$f_{carac}^{stab} (y^{-1})$')
plt.show()


# %% FORKING A LOADED MODEL ##################################################
hub = pgm.Hub('GK')
hub2 = hub.copy()


# %% SAVING AND LOADING ######################################################
hub = pgm.Hub('Reduced_GK', preset='default')
hub.run()
hub.save()

loaddic = pgm.get_available_output(returnas=dict)
hub = pgm.load(pgm.get_available_output(returnas=list)[0])[0]


# %% EXERCICES ###############################################################
'''
Exercise 1 : execute by yourself
    1. Loading library "From scratch", load pygemmes
    2. Access lists get the list of models, the list of solvers
    3. Load a model, then with a preset directly loaded
    4. change value : Run it with different timestep
    5. change solver : Run it with different solvers
    6. Plots : Plot only lambda, then everything but lambda, then with cycles analysis activated
    7. Exploring dparam structure : print all the keys of one field in dparam, then all their values
    8. Getting dparam values : Get the values of omega over time as an array, plot it manually
    9. Creating multiple process : Create a preset with 5 values of the rate of productivity progres
'''


# ########################################################################### #
# %%#####################  LEVEL 2 : MODELLER ############################### #
# ########################################################################### #
'''
Exercise 2 : editing
    1. Copy-paste a file Copy the file model GK-CES name it GK-NEW then reload
pygemmes to see if you can load id
    2. Modify the equations Use the equations for "lambda, omega, d" you find in McIsaac et al,
Minskyan classical growth cycles, Mathematics and Financial Economics with the introduction
of new parameters in _def_fields
    3. See the impact of a parameter : Do an ensemble of run with different elasticity values
    4. See the impact on cycles : Show the impact of the elasticity value on the cycles
    5. See the impact on stability : Do a stability analysis with different values

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


listofsolver = pgm.get_available_solvers(returnas=list)
listofsolver = [listofsolver[i] for i in [0,3]]
listofmodels = pgm.get_available_models(returnas=list)
for model in listofmodels:
    presets = pgm.get_available_models(returnas=dict)[model]['presets']
    for preset in [None]+presets:
        hub = pgm.Hub(model, preset=preset)
        hub.set_dparam(Tmax=10, verb=False)
        for solver in listofsolver:
            print(model, preset, solver)
            hub.run()
