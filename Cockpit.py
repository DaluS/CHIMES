# -*- coding: utf-8 -*-
# !pytest tests/test_01_Solver.py -v To test the system 

import _core
import matplotlib.pyplot as plt

### Get the list of models already existing 
print('#### LIST OF ALL MODELS ####')
_core._class_checks.models.get_available_models()
print(' ')
print('#### MORE INFORMATIONS ON EACH ')

Solvers = ['eRK4-homemade', 
            'eRK2-scipy',
            'eRK4-scipy',
            'eRK8-scipy',
          ]

verb = [ 0,
         1,
         2, 
         .5, 
       ]

### THE LOOP FOR V1 THAT HAS TO WORK WELL
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

plt.figure()
plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()

# #############################################################################
NameOfTheModel = 'GK'
sol = _core.Hub(NameOfTheModel)
sol.get_summary()
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)

plt.figure()
plt.subplot(411);plt.plot(Result['time']['value'],Result['W']['value']);plt.ylabel('W')
plt.subplot(412);plt.plot(Result['time']['value'],Result['L']['value']);plt.ylabel('L')
plt.plot(Result['time']['value'],Result['N']['value'])
plt.subplot(413);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(414);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()
