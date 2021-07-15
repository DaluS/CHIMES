# -*- coding: utf-8 -*-
import _class
import matplotlib.pyplot as plt
### Get the list of models already existing 
print('#### LIST OF ALL MODELS ####')
_class._class_checks.models.get_available_models()
print(' ')
print('#### MORE INFORMATIONS ON EACH ')





# #############################################################################
NameOfTheModel = 'G_Reduced' 
sol = _class.Solver()
sol
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)
sol.get_summary()

plt.figure()
plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()

# #############################################################################
NameOfTheModel = 'GK' 
sol = _class.Solver(NameOfTheModel)
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)
sol.get_summary()

plt.figure()
plt.subplot(411);plt.plot(Result['time']['value'],Result['W']['value']);plt.ylabel('W')
plt.subplot(412);plt.plot(Result['time']['value'],Result['L']['value']);plt.ylabel('L')
plt.plot(Result['time']['value'],Result['N']['value'])
plt.subplot(413);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(414);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()
