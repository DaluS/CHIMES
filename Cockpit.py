# -*- coding: utf-8 -*-
'''
Contains all the possibilities of each _core interaction
'''

import _core
import _plots as plots

_core._class_checks.models.get_available_models()
_core._class_checks.models.describe_ALL_available_models()

# %% Choice of parameters ####################################################
'''
* To change a parameter :  `sol.set_dparam(key='alpha', value=0.01)`


sol.load_field({'a' : [1,2,'lin']})
sol.load_field({'a' : [1,2,'log'],
                'alpha' : 0.03})
sol.load_field({'nx': 100})
sol.load_field({'a': [1,2,3]})
'''


# %% DEEPER ANALYSIS ##########################################################
'''
sol.getCycleAnalysis(key='lambda')
sol.getCycleAnalysis(key=False)
'''

'''Output_MODELNAME_name_USER_DATE.npz
'''
# Solver.save(path=...)
# sol_load = _core._saveload.load(' ')


# %% Test that the system is still doing great ################################
# !pytest tests/test_01_Hub.py -v


# #############################################################################
# #############################################################################
# #############################################################################
'''
hub = _core.Hub('G_Reduced')
hub.get_summary()
hub.run(verb=1.1)
hub.plot()
Result = hub.get_dparam(returnas=dict)
'''
# #############################################################################
hub = _core.Hub('GK')
#hub.set_dparam(key='alpha', value=2.5)
# hub.get_summary()
hub.run(verb=1.1)
hub.plot()
#Result = hub.get_dparam(returnas=dict)
plots.plotVar(hub, 'K', idx=0)
plots.plotphasespace(hub, x='omega', y='lambda', idx=0)
