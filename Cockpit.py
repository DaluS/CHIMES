# -*- coding: utf-8 -*-
#!pytest tests/test_01_Hub.py -v


import _core
import matplotlib.pyplot as plt
# Get the list of models already existing
print('#### LIST OF ALL MODELS ####')
_core._class_checks.models.get_available_models()
print(' ')
print('#### MORE INFORMATIONS ON EACH ')

# PARAMETRISATION OF THE SOLVER #############################################
Solvers = ['eRK4-homemade',
           'eRK2-scipy',
           'eRK4-scipy',
           'eRK8-scipy',
           ]
verb = [0,
        1,
        2,
        .5,
        ]

# A few other options to parameteriize the scipy solvers are available
# (absolute and relative tolerance for convergence atol and rtol,
# and the maximum time step size max_time_step).

# PARAMETRISATION OF THE MODEL ##############################################

# sol.get_presetlist()
# sol.get_currentpreset()
# sol.set_preset()
# sol.set_dparam(key='alpha', value=0.01)

'''
Do two runs with just one different parameter
sol = _core.Solver('G_Reduced')
sol.run()
sol2 = sol.copy()
sol2.set_dparam(key='alpha', value=0.015)
sol2.run()
'''

# SAVING ####################################################################

'''Output_MODELNAME_name_USER_DATE.npz
'''
# Solver.save(path=...)
# sol_load = _core._saveload.load(' ')


# THE LOOP FOR V1 THAT HAS TO WORK WELL
"""
for NameOfTheModel in ListOfModels :
    sol = _core.Hub(NameOfTheModel)
    PRESETS = []
    for preset in PRESETS :
        sol = _core.Hub(NameOfTheModel)

        #sol.load_preset(preset)

        sol.load_field({'a' : 1})
        sol.load_field({'a' : [1,2,'lin']})
        sol.load_field({'a' : [1,2,'log'],
                        'alpha' : 0.03})
        sol.load_field({'nx': 100})
        sol.load_field({'a': [1,2,3]})

        sol.get_summary()
        sol.run(solver='eRK4-homemade', verb=1.1)

        sol.getCycleAnalysis(key='lambda')
        sol.getCycleAnalysis(key=False)

        Result = sol.get_dparam(returnas=dict)

        plt.figure()
        plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
        plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
        plt.suptitle(NameOfTheModel+' '+preset)
        plt.show()
"""

# #############################################################################
NameOfTheModel = 'G_Reduced'
sol = _core.Hub(NameOfTheModel)
sol.get_summary()
sol.run(verb=0.1)

Result = sol.get_dparam(returnas=dict)
#

plt.figure()
plt.subplot(211)
plt.plot(Result['time']['value'], Result['omega']['value'])
plt.ylabel('Omega')
plt.subplot(212)
plt.plot(Result['time']['value'], Result['lambda']['value'])
plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()

# #############################################################################
NameOfTheModel = 'GK'
sol = _core.Hub(NameOfTheModel)
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)
# sol.get_summary()

plt.figure()
plt.subplot(411)
plt.plot(Result['time']['value'], Result['W']['value'])
plt.ylabel('W')
plt.subplot(412)
plt.plot(Result['time']['value'], Result['L']['value'])
plt.ylabel('L')
plt.plot(Result['time']['value'], Result['N']['value'])
plt.subplot(413)
plt.plot(Result['time']['value'], Result['omega']['value'])
plt.ylabel('Omega')
plt.subplot(414)
plt.plot(Result['time']['value'], Result['lambda']['value'])
plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()
