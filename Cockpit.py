# -*- coding: utf-8 -*-
'''
Cockpit is the perfect place to learn how to use GEMMES.
Please execute it with a ipython notebook to try and see each section
'''

import _core


# Get the list of models already existing

# %% Choice of models ########################################################
'''
* To get the list of all models : `_core._class_checks.models.get_available_models()`

* To get the description of a model : `_core._class_checks.models.describe_available_model(model)`
* To get the description of all models : `_core._class_checks.models.describe_ALL_available_models()`

* To get the description of the library :
* To get the description of specific fields :
'''

_core._class_checks.models.get_available_models()
_core._class_checks.models.describe_ALL_available_models()

# %% Choice of parameters ####################################################
'''
* To load a model : `sol = _core.Solver('G_Reduced')`
* To get the presets ` `
* To load a presets :

* To change a parameter :  `sol.set_dparam(key='alpha', value=0.01)`


sol.load_field({'a' : [1,2,'lin']})
sol.load_field({'a' : [1,2,'log'],
                'alpha' : 0.03})
sol.load_field({'nx': 100})
sol.load_field({'a': [1,2,3]})
'''

hub = _core.Hub('G_Reduced')
hub.set_dparam(key='alpha', value=2.5)

# PARAMETRISATION OF THE SOLVER #############################################
'''
Solvers = ['eRK4-homemade',
           'eRK2-scipy',
           'eRK4-scipy',
           'eRK8-scipy',
           ]

verb = [0,  # None,False
        1,  # True
        2,
        .5,
        ]

Compute_auxiliaries = [True, False],  # compute_auxiliary

atol = None,
atol = None,
max_time_step = None
'''
hub.run(solver='eRK2-scipy')

# %%GET INFORMATION OF THE MODEL ##############################################
'''
# EXPLANATIONS
There are four ways to get informations about the loaded system through the hub

1. just calling the hub `sol` that gives you:
    * the model name
    * its source location
    * the number of parameters and functions loaded
    * the flag if it has run or not
    *  # NOTICE THAT nb. model param and nb.function is bigger than the real
    number of variable and parameters. Do not worry: )
2. `sol.get_summary()` that gives you all useful informations
    * The numerical parameters
    * The model parameters and their value
    * The functions, their expression, their initial value
3. `sol.get_dparam()` will return or print all the data of the model. Should
be controlled through keywords
4. `sol.get_variables_compact()` will return an array of the time evolution and
the corresponding keys

* sol.get_summary is good practice before launching the run,
* sol.get_dparam(returnas = dict) is good practice for solution exploration
* sol.get_variable_compact is good practice for simple plots
'''

'''
# GENERAL USE
lcrit={'dimension': [],
         'units': [],
         'type': [],
         'group': [],
         'eqtype': []}
lprint = [
    'parameter',
    'value',
    'units',
    'dimension',
    'symbol',
    'type',
    'eqtype',
    'group',
    'comment', ]
Returnas = [dict,           # dictionnary
            'DataGFrame',   # a pandas DataFrame
            np.ndarray,     # a dict of np.ndarrays
            False           # return nothing(useful of verb=True)
            ]
Verb2 = [True,   # pretty-print the chosen parameters
         False,  # print nothing
         ]

for ve in Verb2:
    for re in Returnas:
        sol.(verb=ve, returnas=re, **kwdargs)

# 4 sol.get_variables_compact()
lkeys, array = sol.get_variables_compact()
'''

# %% DEEPER ANALYSIS ##########################################################
'''
sol.getCycleAnalysis(key='lambda')
sol.getCycleAnalysis(key=False)
'''


# %% GET PLOTS ################################################################
hub.plot()

# SAVING ######################################################################

'''Output_MODELNAME_name_USER_DATE.npz
'''
# Solver.save(path=...)
# sol_load = _core._saveload.load(' ')


# %% Test that the system is still doing great ################################
# !pytest tests/test_01_Hub.py -v


# #############################################################################
# #############################################################################
# #############################################################################
sol = _core.Hub('G_Reduced')
sol.get_summary()
sol.run(verb=1.1)
sol.plot()
Result = sol.get_dparam(returnas=dict)

# #############################################################################
sol = _core.Hub('GK')
sol.run(verb=0)
sol.plot()
Result = sol.get_dparam(returnas=dict)
