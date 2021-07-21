# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:56:37 2021

@author: Paul Valcke
"""

import _core
import matplotlib.pyplot as plt 

HUB = _core.Hub('G_Reduced') 
solvers = ['eRK2-scipy','eRK4-scipy','eRK8-scipy']
Vecdt = [1, 0.1, 10**(-2),10**(-3)]
k0 = 'lambda'

t={}
lambd = {}
plt.figure()
for dt in Vecdt :
    for s in solvers :
        HUB.reset()
        #HUB.set_dparam() ###
        
        HUB.run(solver=s)

        t     = HUB.get_dparam(returnas=dict)['time']['value']
        lambd = HUB.get_dparam(returnas=dict)['lambda']['value']


    
        plt.plot(t, lambd, '-k', label=s)
plt.legend(); 
plt.gca().axhline(0.97, c='k', ls='--'); 
plt.gca().axhline(0.94675, c='k', ls='--')

HUB.set_dparam({'dt':0.1})


