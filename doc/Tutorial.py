# -*- coding: utf-8 -*-
"""
THIS DOCUMENT IS A TUTORIAL ON HOW TO USE PYGEMMES AS A SIMPLE USER
EXECUTE THE DOCUMENT LINE BY LINE TO UNDERSTAND WHAT IS HAPPENING
"""


"""
# IF PYGEMMES IS NOT IN YOUR PATH, OR YOU DID NOT START YOUR TERMINAL IN PYGEMMES
import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`
"""

import pygemmes as pgm
import numpy as np


# ## BEST ADVICE EVER ####################################!#!#!#!#!#!#!#
# Always use tab and ? on pgm, hub, and each functions ###!#!#!#!#!#!#!#


# ########################################################################### #
# %%#####################  LEVEL 1 : USER ################################### #
# ########################################################################### #
'''
A user is someone who do not write his own models, but use the one of others for
analysis.
'''


# %% OVERVIEW OF PYGEMMES ########################################

# Content (practical functions will be shown later)
pgm.get_available_fields(exploreModels=True, showModels=True,) #returnas=list)
pgm.get_available_functions()
pgm.get_available_models() # details=True
pgm.get_available_plots()
#pgm.get_available_models(details=True)
#listofmodels = pgm.get_available_models(returnas=list)


# %% LOADING A MODEL
hub = pgm.Hub('GK')
hub = pgm.Hub('GK', verb=False)

# EXPLORING ITS CONTENT ######################
hub.get_summary()  # definition concern the field definition, com the way it is calculated
hub.get_equations_description()

# plot the causal network
hub.get_Network()                               # state variables, differential equations
hub.get_Network(params=True)                    # state,differential,parameters
hub.get_Network(auxilliary=False,params=True)   # remove auxilliary statevar and differential
hub.get_Network(filters=('Pi',))                # remove the variable Pi and its connexions
hub.get_Network(filters=('Pi',),redirect=True)  # all connexions from Pi are reconnected

# miscellaneous supplementary informations
hub.dmodel  # Gives the content of the model file
hub.dmisc   # gives multiple informations on the run and the variables
hub         # Minimalist informations


# %% RUN THE MODEL ########################################################
hub.run(verb=0)           # calculate all the runs
hub.run(verb=1.1)         # show how it is
hub.run(N=100)            # after the run, reinterpolate temporal data on 100 values
hub.get_summary()         # shows summary with latest values


# %% Plots ################################################################
hub.plot()
"""There are three layers of filters, each of them has the same logic :
if the filter is a tuple () it exclude the elements inside,
if the filter is a list [] it includes the elements inside.

Filters are the following :
filters_units      : select the units you want
filters_sector     : select the sector you want  ( '' is all monosetorial variables)
filters_sector     : you can put sector names if you want them or not. '' corespond to all monosectoral variables
separate_variables : key is a unit (y , y^{-1}... and value are keys from that units that will be shown on another graph,

Region             : is, if there a multiple regions, the one you want to plot
idx                : is the same for parrallel systems"""
hub.plot(filters_key =('p'),
         filters_units=('Units'),
         filters_sector=(),
         separate_variables={'':['employment','omega']},
         idx=0,
         Region=0,
         title='',
         lw=2)
hub.plot_preset(preset='default')


# %% Get your data accessible #############################################
R = hub.get_dparam()
R.keys()
R['employment'].keys()
np.shape(R['employment']['value'])

# %% Get more subtle criterias ############################################
# the criterias are : 'key', 'dimension', 'units', 'type', 'group', 'eqtype'
R1 = hub.get_dparam(key=['employment', 'omega'])
R2 = hub.get_dparam(key=('employment', 'omega'))
R1.keys()
R2.keys()

groupsoffields = hub.get_dparam_as_reverse_dict(
    crit='units',
    eqtype=['ode', 'statevar'])


# && ####################### ACCESS TO INDIVIDUAL PLOTS ######################
hub = pgm.Hub('GK')
hub.run()

pgm.plots.plotbyunits() # same as hub.plot()

pgm.plots.phasespace(hub,
                     x='omega',
                     y='employment',
                     color='d',
                     idx=0)
pgm.plots.phasespace(hub,
                     x='employment',
                     y='pi',
                     color='d',
                     idx=0)
pgm.plots.plot_timetraces(hub,
                          key=['employment', 'omega', 'd'])
pgm.plots.plot3D(hub, x='employment',
                 y='omega',
                 z='d',
                 color='pi',
                 cmap='jet',
                 index=0,
                 title='')
pgm.plots.Var(hub,'pi',log=True)

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


# %% Using  set_preset
hub = pgm.Hub('GK')
hub.set_preset('default')

# Changing one parameter
hub = pgm.Hub('GK')
hub.set_dparam('dt',0.02)
hub.set_dparam('Tmax',50)
hub.get_summary()

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
hub.reinterpolate_dparam(1000)

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
                                              N=10)
presetCoupled['nx']=10
hub = pgm.Hub('GK')
hub.set_dparam(**presetCoupled)
hub.run(N=1000)
hub.calculate_StatSensitivity()
pgm.plots.Var(hub,'employment',mode='sensitivity')
output_preset = hub.Extract_preset()
hub.set_dparam(**output_preset)

# %% CALCULATING CYCLES ######################################################
hub = pgm.Hub('GK')
hub.run()
hub.calculate_Cycles(ref='employment') # The ref will determine what variables are the begin and end of cycles calculated
pgm.plots.Var(hub,'employment',mode='cycles')
pgm.plots.cycles_characteristics(hub,'employment','omega',
                                 ref='g',
                                 type1='frequency',
                                 type2='meanval')



# TO BE REINTRODUCED ########################################################
#pgm.plots.slices_wholelogic(hub,key='g',axes=[['omega',0,2]],N=100,tid=0,idx=0,Region=0)

#calculate_Convergerate

#######################################################################################
##################### MULTISECTORIALITY ###############################################

hub=pgm.Hub('test_multisect2');
hub=pgm.Hub('test_multisect2');hub.set_dparam()
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr': 5})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr': ['Paris','Berlin']})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'Nprod': ['Capital','Consommation']})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'Nprod': 5})
hub.set_dparam(**{'dt':1})

# Changement de valeur monosect #########
hub.set_dparam(**{'a': 1.1})          # valeur initiale
hub.set_dparam(**{'alpha': 0.05})     # valeur de parametre

# Changement monosect sur vecteur #######

hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nx':3,
                  'a': [0.5,.1,3]})     # Si non explicite, automatiquement sur nx
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr':2,
                  'alpha': ['nr',[0.5,.1]]})                # need nr=2, change on all nx
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nx':4,'nr':['France','USA'],'alpha': [['nr','France'],0.5]})        # change on region 0, nx 1
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr'   : ['France','USA'], 'nx':3,               # Two named regions
                'alpha': [['nr','France'],['nx',1],0.5]}) # Change in region France
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr'   : ['France','USA','China'], 'nx':3,          # Three regions, change in France and USA
                'alpha': [['nr','France'],['nx',1],0.5]})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nx':5,
                'alpha': [['nr',0],['nx',0,4],[0.5,0.2]]})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'nr'   : ['France','USA','China'], 'nx':3,       'alpha': [['nr',0],['nx',1],0.5]})

# FOR VECTOR OR MATRICES, THE SYSTEM WILL AUTOMATICALLY RECOGNIZE THE FIRST ENTRIES
hub.set_dparam(**{'Z': [['energy','capital'],['nr',0],[0.5,0.22]]})
hub.set_dparam(**{'MATRIX': {'first':['energy','capital'],
                             'second':['mine','consumption'],
                             'nr':0,
                             'value':[0.5,0.22]}})
hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],['nr',0],[0.5,0.22]]})
hub.set_dparam(**{'MATRIX': [['energy','capital'],['mine','consumption'],[0.5,0.22]]})
hub=pgm.Hub('test_multisect2');hub.set_dparam(**{'MATRIX': [['energy','capital'],0.22]})



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


# %% BASIN OF ATTRACTIONS ####################################################
'''
This is an example on how someone can do more complex analysis



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

for i in range(len(ConvergeRate)):
    if ConvergeRate[i]:
        ax.plot(R['lambda']['value'][:, i],
                R['omega']['value'][:, i],
                R['d']['value'][:, i], c='k', lw=0.1)

# Add colobar
cbar = fig.colorbar(scat)
cbar.ax.set_ylabel(r'$f_{carac}^{stab} (y^{-1})$')
plt.show()
'''

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

