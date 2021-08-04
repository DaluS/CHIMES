# -*- coding: utf-8 -*-
'''
Contains all the possibilities of each _core interaction
'''

import _core
import _plots as plots

# _core._class_checks.models.get_available_models()
_core._class_checks.models.describe_ALL_available_models()
# _core._class_checks.models.PrintDFIELDS()


# %% Start the hub ###########################################################

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


# %% Test that the system is still doing great #############################
# !pytest tests/test_01_Hub.py -v
hub = _core.Hub(model='GK-NEWFORMALISM')

hub.run(verb=1.1)
hub.FillCyclesForAllVar(ref='lambda', idx='all')
plots.Var(hub, 'lambda', idx=0, cycles=True, log=False)
# ##########################################################################
# ##########################################################################
# ##########################################################################
'''
hub = _core.Hub('G_Reduced')
hub.get_summary()
hub.run(verb=1.1)
hub.plot()
Result = hub.get_dparam(returnas=dict)
'''
# #############################################################################
# hub.set_dparam(key='alpha', value=2.5)
# hub.get_summary()
'''
for model in ['GK']:  # , 'G_Reduced']:
    for solver in ['eRK4-homemade', 'eRK2-scipy', 'eRK4-scipy', 'eRK8-scipy']:
        print('######################################')
        hub2 = _core.Hub(model=model)
        hub.run(verb=1.1)
        # hub.save()
        # hub.get_summary()

# hub.FillCyclesForAll(ref=None)
hub.reset()
hub.run()
hub.FillCyclesForAllVarOneIDX(ref='lambda')

Result = hub.get_dparam(returnas=dict)

plots.AllVar(hub)
'''
"""
    #plots.Var(hub, 'K', idx=0, cycles=True, log=True)

    plots.phasespace(hub, x='omega', y='d', idx=0)
    plots.phasespace(hub, x='omega', y='lambda', color='time', idx=0)
    plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)

    dimensionlessnumbers = ['omega', 'lambda', 'd', 'g']
    plots.AllPhaseSpace(hub, dimensionlessnumbers, idx=0)
    """,
