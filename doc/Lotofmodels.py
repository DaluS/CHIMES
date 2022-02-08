# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 13:29:18 2022

@author: Paul Valcke
"""

import pygemmes as pgm

#%% ######################### GOODWIN #########################################
hub = pgm.Hub('G', preset='default')
hub.run()
hub.plot_preset()

hub = pgm.Hub('G', preset='many-orbits')
hub.run()
hub.plot()


#%% ######################### GOODWIN WITH PI IN PHILLIPS #####################
hub = pgm.Hub('G-PiInPhi', preset='zpi')
hub.run(solver='eRK8-scipy')
R = hub.get_dparam(returnas=dict)


lab = r"$z_{\pi}=$"
dax = hub.plot(key=['lambda', 'omega', 'w'], idx=0,
               label=lab+f"{R['zpi']['value'][0]}",
               tit='Impact of profit sensibility in salary negociation in a Goodwin model : \n $ \dfrac{\partial w}{\partial t}= w \Phi(\lambda) \pi^{z_{\pi}}$')
for i in range(1, 4):

    dax = hub.plot(key=['lambda', 'omega', 'w'], idx=i,
                   label=lab+f"{R['zpi']['value'][i]}",
                   dax=dax)


#%% ######################## GOODWIN WITH KALDOORN PROGRESS ###################
hub = pgm.Hub('G-Kaldoorn', preset='beta-productivity')
hub.get_summary()
hub.run(verb=1.1)  # solver='eRK8-scipy', verb=1.1)
R = hub.get_dparam(returnas=dict)


Ntraj = hub.dmisc['dmulti']['shape'][0]
Graphs = ['lambda', 'omega', 'w', 'a', 'g']
lab1 = r"$\beta=$"
lab2 = r"$,\alpha=$"
dax = hub.plot(key=Graphs, idx=0,
               # +lab2+f"{R['alpha']['value'][0]:.2f}",
               label=lab1+f"{R['beta']['value'][0]:.2f}",
               tit=r'''Impact of endogenous productivity in a Goodwin model :
                   $\dfrac{\partial a}{\partial t} = a (\alpha + \beta g)$''')

for i in range(1, Ntraj):
    dax = hub.plot(key=Graphs, idx=i,
                   # +lab2+f"{R['alpha']['value'][i]:.2f}",
                   label=lab1+f"{R['beta']['value'][i]:.2f}",
                   dax=dax)

#%% #################### GOODWIN Kaldoorn, pi in phillips #####################
hub = pgm.Hub('G-PiInPhi-Kaldoorn', preset='coupledactivity')
hub.get_summary()
hub.run(verb=1.1)  # solver='eRK8-scipy', verb=1.1)
R = hub.get_dparam(returnas=dict)

Ntraj = hub.dmisc['dmulti']['shape'][0]
Graphs = ['lambda', 'omega', 'w', 'a', 'g']

lab1 = r"$\beta=$"
lab2 = r"$,z_{\pi}=$"
dax = hub.plot(key=Graphs,
               idx=0,
               label=lab1+f"{R['beta']['value'][0]:.2f}" +
               lab2+f"{R['zpi']['value']:.2f}",
               tit=r'''GOODWIN with two equations modified :
                   $ \dfrac{\partial w}{\partial t}= w \Phi(\lambda) \pi^{z_{\pi}}$
                   $\dfrac{\partial a}{\partial t} = a (\alpha + \beta g)$''')

for i in range(1, Ntraj):
    dax = hub.plot(key=Graphs,
                   idx=i,
                   label=lab1+f"{R['beta']['value'][i]:.2f}" +
                   lab2+f"{R['zpi']['value']:.2f}",
                   dax=dax)

#%% #################### GOODWIN Relax lambda #################################
hub = pgm.Hub('G-LambdaRelax-EndoProd-profitNego', preset='taulamb')
hub.get_summary()
hub.run(verb=1.1)  # solver='eRK8-scipy', verb=1.1)
R = hub.get_dparam(returnas=dict)
Graphs = ['lambda', 'omega', 'w', 'lambda0', 'phillips']
Ntraj = hub.dmisc['dmulti']['shape'][0]
lab1 = r"$\tau_{\lambda}=$"
dax = hub.plot(key=Graphs,
               idx=0,
               label=lab1+f"{R['taulamb']['value'][0]:.2f}",
               # lab2+f"{R['zpi']['value']:.2f}",
               tit=r'''GOODWIN with two equations modified :
                   $ \dfrac{\partial w}{\partial t}= w \Phi(\lambda) \pi$
                   $\dfrac{\partial \lambda }{\partial t} = \tau_{\lambda}^{-1} ( L/N - \lambda)$''')

for i in range(1, Ntraj):
    dax = hub.plot(key=Graphs,
                   idx=i,
                   label=lab1+f"{R['taulamb']['value'][i]:.2f}",
                   # lab2+f"{R['zpi']['value']:.2f}",
                   dax=dax)

#%% #################### GOODWIN CES ##########################################
hub = pgm.Hub('G-CES', preset='CES')
hub.get_summary()
hub.run(verb=1.1)  # solver='eRK8-scipy', verb=1.1)
hub.plot()


#%% ################### GOODWIN Buffer ########################################
hub = pgm.Hub('G-Kbuffer', preset='B')
hub.get_summary()
hub.run(verb=1.1)  # solver='eRK8-scipy', verb=1.1)
hub.plot()

#%% ################## GOODWIN MINE ###########################################
hub = pgm.Hub('MinePaul')
hub.get_summary()
hub = pgm.Hub('GMinePaul')
hub.get_summary()
hub.Network()
hub.run()

hub.set_dparam(intensity=0)
