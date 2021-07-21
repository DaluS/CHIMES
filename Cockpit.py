# -*- coding: utf-8 -*-
import _core
import matplotlib.pyplot as plt
### Get the list of models already existing 


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
ListOfModels = _core._class_checks.models.get_available_models(returnas=list)
_core._class_checks.models.describe_available_models()
# #############################################################################
NameOfTheModel = 'G_Reduced'
sol = _core.Hub(NameOfTheModel)
sol.get_summary()
sol.run(solver='eRK4-homemade', verb=0.1)

Result = sol.get_dparam(returnas=dict)
#

plt.figure()
plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()

# #############################################################################
NameOfTheModel = 'GK'
sol = _core.Hub(NameOfTheModel)
sol.run(solver='eRK4-homemade',verb=0.1)

Result = sol.get_dparam(returnas=dict)
#sol.get_summary()

plt.figure()
plt.subplot(411);plt.plot(Result['time']['value'],Result['W']['value']);plt.ylabel('W')
plt.subplot(412);plt.plot(Result['time']['value'],Result['L']['value']);plt.ylabel('L')
plt.plot(Result['time']['value'],Result['N']['value'])
plt.subplot(413);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(414);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()
