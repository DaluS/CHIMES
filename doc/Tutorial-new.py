# -*- coding: utf-8 -*-
"""
import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`
"""
import pygemmes as pgm


import matplotlib.pyplot as plt
import matplotlib as mpl
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

# %% OVERVIEW #################################################################
# Fields :
'''
Give you an overview of what fields (quantities existing in the universe) exist in pygemmes
show a default value, a definition, units, and can show which models are inside
'''
pgm.get_available_fields?
pgm.get_available_field()
pgm.get_available_fields(exploreModels=False ,
                         showModels=False,
                         returnas=None)
pgm.get_available_fields(exploreModels=True ,
                         showModels=True,
                         returnas=None)
fields_list= pgm.get_available_fields(exploreModels=True ,
                                      showModels=True,
                                      returnas=list)

# models
"""
Check all models available in pygemmes, and gives back the information that are asked.
if details=False, just gives names and preset names
"""
pgm.get_available_models?
pgm.get_available_models()
pgm.get_available_models(details=True)
modeldict=pgm.get_available_models(returnas=dict)
listofmodels = pgm.get_available_models(returnas=list)

# Functions
"""
Functions coded in a shared library for each models
"""
pgm.get_available_functions?
pgm.get_available_functions()

# PLOTS
"""
Show the list, properties and 
"""
pgm.get_available_plots?
pgm.get_available_plots()

# %% OVERVIEW #################################################################
# %% LOADING A MODEL

pgm.Hub?
hub = pgm.Hub('GK')
hub = pgm.Hub('GK', verb=False)

# EXPLORING IT
hub.get_summary()  # definition concern the field definition, com the way it is calculated
hub.get_equations_description()

hub.get_Network()
hub.get_Network(params=True)
hub.get_Network(auxilliary=False,params=True)


# %% MISC SUPPLEMENTARY INFORMATION
hub.dmodel  # Gives the content of the model file
hub.dmisc   # gives multiple informations on the run and the variables
hub         # Minimalist informations


# %% Calculation ###
hub.run()
hub.run(verb=1.1)
hub.get_summary()

# %% Basic Plots
dax = hub.plot()
dax2 = hub.plot(key=['employment', 'omega', 'd'])  # Select the variables
dax3 = hub.plot(key=('GDP', 'a', 'Pi', 'kappa'))  # Remove some variables
hub.plot_preset(preset='default')


# %% Get access to data
R = hub.get_dparam()
R.keys()
R['employment'].keys()
import numpy as np
np.shape(R['employment']['value'])


# %% Get more subtle criterias ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
R1 = hub.get_dparam(key=['employment', 'omega'])
R2 = hub.get_dparam(key=('employment', 'omega'))
R1.keys()
R2.keys()

groupsoffields = hub.get_dparam_as_reverse_dict(
    crit='units', eqtype=['ode', 'statevar'])

# && ####################### ACCESS TO INDIVIDUAL PLOTS ######################
hub = pgm.Hub('GK')

# Plots that are not related to a run but to a function
#pgm.plots.slices_wholelogic(hub, key='kappa', axes=[
#                            ['pi', 0, 0.3]], N=100, tid=0, idx=0)
#pgm.plots.slices_wholelogic(hub, key='L', axes=[['a', 1, 3], [
#                            'K', 1, 5]], N=100, tid=0, idx=0)

# Plots related to a run
hub.run()

pgm.plots.phasespace(hub, x='omega', y='employment', color='d', idx=0)
pgm.plots.phasespace(hub, x='employment', y='pi', color='d', idx=0)
pgm.plots.plotnyaxis(hub, x='time',
                     y=[['employment', 'omega'],
                        ['d'],
                        ['kappa', 'pi'],
                        ],
                     idx=0,
                     title='',
                     lw=2)
pgm.plots.plot_timetraces(hub, key=['employment', 'omega', 'd'])
pgm.plots.plot3D(hub, x='employment',
                 y='omega',
                 z='d',
                 cinf='pi',
                 cmap='jet',
                 index=0,
                 title='')
pgm.plots.plotbyunits(hub)


# Plots about derivates
#hub.calculate_variation_rate()
#pgm.plots.plot_variation_rate(hub, ['omega', 'employment', 'd', 'D']
#                              )

# plots about cycles
#hub.calculate_Cycles(ref='omega')
#pgm.plots.cycles_characteristics(hub, xaxis='omega',
 #                                yaxis='employment',
 #                                ref='omega')
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
hub.set_preset('default')

# Changing one parameter
hub = pgm.Hub('GK')
hub.set_dparam('dt',0.02)
hub.set_dparam(Tmax=50)

# Put a dictionnary
dparam = {'alpha': 0, 'n': 1}
hub.set_dparam(**dparam)

# Create N system in parrallel with different values
hub = pgm.Hub('GK')
hub.set_dparam(**{'nx':4,
                  'alpha':[0,
                      0.01,
                      0.02,
                      0.03]})
hub.get_summary()
hub.run()
dax = hub.plot(key=['employment',
                    'omega'],idx=0)
dax = hub.plot(key=['employment',
                    'omega'],idx=1,dax=dax)
dax = hub.plot(key=['employment',
                    'omega'],idx=2,dax=dax)
dax = hub.plot(key=['employment',
                    'omega'],idx=3,dax=dax)



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
presetCoupled['nx']=10
hub = pgm.Hub('GK')
hub.set_dparam(**presetCoupled)
hub.run()
dax = hub.plot()

'''
hub.reinterpolate_dparam(1000)
hub.calculate_StatSensitivity()
dax = hub.plot(key=['employment', 'omega'], mode='sensitivity')


# %% GENERATE DPRESET AND USE IT
_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }
hub = pgm.Hub('GK', preset='SensitivityCoupled', dpresets=_DPRESETS)
hub.run()
hub.reinterpolate_dparam(1000)
hub.calculate_StatSensitivity()
dax = hub.plot(mode='sensitivity')
'''
# %% BASIN OF ATTRACTIONS ####################################################
'''
This is an example on how someone can do more complex analysis
'''

'''
# Initialisation of the system with 1000 points in a box
hub = pgm.Hub('Reduced_GK', preset='default')

BasinDomain = {
    'employment': {'mu': 0.5,
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
    'employment': 0.967297870750419,
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
ax.scatter(finalpoint['employment'],
           finalpoint['omega'],
           finalpoint['d'],
           s=50,
           c='k')

# Scatter plot
R = hub.get_dparam(key=[k for k in finalpoint]+['time'], returnas=dict)
scat = ax.scatter(R['employment']['value'][0, ConvergeRate > 0.001],
                  R['omega']['value'][0, ConvergeRate > 0.001],
                  R['d']['value'][0, ConvergeRate > 0.001],
                  c=ConvergeRate[ConvergeRate > 0.001],
                  cmap=cmap,
                  norm=mpl.colors.LogNorm(vmin=10**(-3)))
plt.axis('tight')
'''
# Add trajectory of converging points
'''
for i in range(len(ConvergeRate)):
    if ConvergeRate[i]:
        ax.plot(R['employment']['value'][:, i],
                R['omega']['value'][:, i],
                R['d']['value'][:, i], c='k', lw=0.1)
'''
'''
# Add colobar
cbar = fig.colorbar(scat)
cbar.ax.set_ylabel(r'$f_{carac}^{stab} (y^{-1})$')
plt.show()
'''

# %% FORKING A LOADED MODEL ##################################################
hub = pgm.Hub('GK')
hub2 = hub.copy()


# %% SAVING AND LOADING ######################################################
hub = pgm.Hub('GK', preset='default')
hub.run()
hub.save()

loaddic = pgm.get_available_output(returnas=dict)
#hub = pgm.load(pgm.get_available_output(returnas=list)[0])[0]


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



# solvers
"""
Solvers are desactivated : there is only one for the moment
"""

# %% Reinterpolate data to be lighter
hub.reinterpolate_dparam(1000)
R = hub.get_dparam()
np.shape(R['employment']['value'])
# %% STUDY OF CYCLES
hub = pgm.Hub('GK')
hub.run()
hub.calculate_Cycles(ref='employment')
dax4 = hub.plot(mode='cycles', key=['employment', 'omega', 'd', 'phillips'])




Dictoftests = {
    #### NUMERICAL/DIMENSIONS TESTS ####
    'nx' : {'nx': 4},
    'nr_num' : {'nr': 5},
    'nr_list' : {'nr': ['Paris','Berlin']},
    'Nprod_num' : {'Nprod': 5},
    'Nprod_list' :{'Nprod': ['Capital','Consommation']},
    'dt': {'dt':0.001},
    'Tmax': {'Tmax':120},

    #### MONOSECTORAL VALUE CHANGE
    'initial value alone': {'a': 0.9},
    'parameter value alone' : {'alpha': 0.05},
}

print('BASIC TESTS ON NUMERICAL SIZES')
for k,v in Dictoftests.items():
    print('#################',k,'##########')
    hub=pgm.Hub('test_multisect2',verb=False)

    hub.set_dparam(verb=False,**{'Tmax':0.1})
    hub.set_dparam(**v)
    hub.run()


### LISTE DES CHANGEMENTS A POUVOIR APPORTER :

# Changement de tailles
hub=pgm.Hub('test_multisect2');
hub=pgm.Hub('test_multisect2');hub.set_dparam()
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr': 5})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr': ['Paris','Berlin']})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'Nprod': ['Capital','Consommation']})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'Nprod': 5})
hub.set_dparam(**{'dt':1})
hub.set_dparam()

# Changement de valeur monosect #########
hub.set_dparam(**{'a': 0.9})          # valeur initiale
hub.set_dparam(**{'alpha': 0.05})     # valeur de parametre

# Changement monosect sur vecteur #######

hub.set_dparam(**{'nx':3,
                  'a': [0.5,.1,3]})     # Si non explicite, automatiquement sur nx
hub.set_dparam(**{'nx':2,
                  'alpha': [0.5,.1,4]}) # Si non explicite, automatiquement sur nx
hub.set_dparam(**{'nr':2,
                  'alpha': ['nr',[0.5,.1]]})                # need nr=2, change on all nx
hub.set_dparam(**{'alpha': [['nr','France'],0.5]})        # change on region 0, nx 1
hub.set_dparam(**{'nr'   : ['France','USA'],                # Two named regions
                'alpha': [['nr','France'],['nx',1],0.5]}) # Change in region France
hub.set_dparam(**{'nr'   : ['France','USA','China'],        # Three regions, change in France and USA
                'alpha': [['nr','France','USA'],['nx',1],0.5]})
hub.set_dparam(**{'nx':5,
                'alpha': [['nr',0],['nx',0,4],[0.5,0.2]]})
hub.set_dparam(**{'alpha': [['nr',0],['nx',1],0.5]})

# FOR VECTOR OR MATRICES, THE SYSTEM WILL AUTOMATICALLY RECOGNIZE THE FIRST ENTRIES
hub.set_dparam(**{'Z': [['energy','capital'],['nr',0],[0.5,0.22]]})
hub.set_dparam(**{'MATRIX': {'first':['energy','capital'],
                             'second':['mine','consumption'],
                             'nr':0,
                             'value':[0.5,0.22]}})
hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],['nr',0],[0.5,0.22]]})
hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],[0.5,0.22]]})
hub.set_dparam(**{'MATRIX': [['energy','capital'],0.22]})



# dpreset, puis preset
preset= {
    'name1': {
        'fields': {
            'dt': 0.01,
            'nx': 3,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'w': .85*1.2,
            'alpha': 0.02,
            'n': 0.025,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['lambda', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2},
                       {'x': 'time',
                        'y': [['K', 'Y', 'I', 'Pi'],
                              ['inflation', 'g'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                    'y': 'omega',
                    'z': 'd',
                    'cinf': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         'color': 'k'},  # optional
                        ],
            'cycles_characteristics': [{'xaxis': 'omega',
                                        'yaxis': 'lambda',
                                        'ref': 'lambda'}
                                       ]
        },
    }
}
hub.set_dpreset(preset)
hub.set_preset('name1')
