import pygemmes as pgm
from copy import deepcopy
import numpy as np

# %% Small check for pleasure
hub= pgm.Hub('LorenzSystem',preset='Canonical example')
hub.run()
pgm.plots.plot3D(hub, 'x', 'y', 'z', 'time')

# %% INTERACTION SCHEMES ################################
# Goodwin interaction scheme, Goodwin-reduced interaction scheme
hub= pgm.Hub('Goodwin')
hub.get_Network()
hub.get_Network(params=True,filters=('pi','W','GDP','I','g'),auxilliary=False,redirect=True)

hubR= pgm.Hub('reduced_G')
hubR.get_Network()

# %% RUNS ###################################
# 3 system in parrallel with small difference in
hub= pgm.Hub('Goodwin')
hub.set_dparam(**{'nx':3,
                  'K':[2.7,2.3,1]})
hub.get_summary()
hub.run(N=1000)

# Loop on all indexes
for idx in range(3):
    hub.plot(separate_variables={'':'pi'},idx=idx)
    pgm.plots.plotnyaxis(hub,[['employment'],['omega'],['pi'],['g']],idx=idx)
    pgm.plots.phasespace(hub,'omega','employment','pi',idx=idx)

# %% GOODWIN CLOSED CYCLES ANALYSIS ####################################
hub= pgm.Hub('Goodwin')
hub.set_dparam(**{'Tmax':30,
                  'nx':30,
                  'K':np.linspace(.5,2.75,30)})
hub.run(N=1000)
hub.calculate_Cycles(ref='employment')
pgm.plots.Var(hub,'omega',mode='cycles')
pgm.plots.Var(hub,'g',mode='sensitivity')
pgm.plots.cycles_characteristics(hub,'omega','employment',
                                 ref='g',
                                 type1='frequency',
                                 type2='meanval')

# %% GOODWIN REDUCED #################################################
hub= pgm.Hub('reduced_G')
hub.get_summary()
hub.run()
hub.plot()

# %% VAN DER PLOECK aka GOODWIN CES ##################################
hub= pgm.Hub('Goodwin_CES')
hub.set_dparam(**{'nx':4,
                  'K':2.5,
                  'Tmax':300,
                  'CESexp':[18,100,500,1000]})
hub.get_summary()
hub.run()
pgm.plots.phasespace(hub, 'omega', 'employment', 'time', idx=1)
pgm.plots.phasespace(hub, 'omega', 'l', 'time', idx=0)
pgm.plots.Var(hub,'omega',mode='cycles')

hub= pgm.Hub('Goodwin_CES')
hub.set_dparam(**{'nx':1,#10,
                  'K':2.4,#np.linspace(2.4,2.85,10),
                  'Tmax':100,
                  'CESexp':100})
hub.run()
pgm.plots.Var(hub,'l',mode='cycles')
pgm.plots.cycles_characteristics(hub,'omega','employment',
                                 ref='l',
                                 type1='frequency',
                                 type2='meanval')

# %% GOODWIN-KEEN ####################################################
hub= pgm.Hub('GK',preset='default')
hub.get_summary()
hub.run()
hub.plot()

hub= pgm.Hub('GK',preset='farfromEQ')
hub.get_summary()
hub.run()
hub.plot()
pgm.plots.plot3D(hub,'omega','employment','d','time')

#
hub= pgm.Hub('GK',preset='farfromEQ')
hub.set_dparam(**{'D':0})
hub.get_summary()
hub.run()
hub.plot()
pgm.plots.plot3D(hub,'omega','employment','d','time')

# How inflation here stabilize
hub= pgm.Hub('GK',preset='farfromEQ')
hub.set_dparam(**{'eta':0})
hub.get_summary()
hub.run()
hub.plot()
pgm.plots.plot3D(hub,'omega','employment','d','time')

# Crisis with inflation
hub= pgm.Hub('GK',preset='crisis')
hub.get_summary()
hub.run()
hub.plot()
pgm.plots.plot3D(hub,'omega','employment','d','time')

# %% GK REDUCED #####################################################
hub= pgm.Hub('reduced_GK')
hub.get_summary()
hub.run()
hub.plot()


hub= pgm.Hub('reduced_GK')
hub.set_dparam(**{'employment':0.5,
                  'd':7})
hub.get_summary()
hub.run()
hub.plot()

# %% ################################################################
# ###################################################################
pgm.get_available_models('GEMMES_Coping2018',details=True)
hub=pgm.Hub('GEMMES_Coping2018',preset='BAU_DAM')
hub.get_summary()
hub.run()
hub.plot()
hub.plot_preset()

hub=pgm.Hub('GEMMES_Coping2018',preset='TRANSITION')
hub.get_summary()
hub.run()
hub.plot()

#####################################################################
# %% Goodwin KVL
hub=pgm.Hub('reduced_G_KVL',preset='GoodwinL')
hub.run()
hub.plot_preset()



















hub=pgm.Hub('CHIMES')

dict={
### MONOSECTORAL
'Tmax':40,
'Nprod': ['Consumption','Capital'],
'nx':10,

'alpha' : np.linspace(0,0.02,10),
'n'     : 0.025,
'phinull':0.1,
'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[0,0],
'K': [2.2,0.6],
'D':[0,0],
'u':[.9,.9],
'p':[1,3],
'V':[10,15],
'z':[1,1],

'Cpond':[1.1,0],

'mu0':[1.3,2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[0.,0.3],
'b':1,
'nu':3,

## MATRICES
'Gamma': [[0.0 ,0.0],
          [0.0 ,0.0]],
'Xi': [['Consumption','Capital','Consumption','Capital'],
       ['Consumption','Capital','Capital','Consumption'],[0,2,1,0]],
}


dictMONOGOODWIN={
# Numerical structural
'Tmax'  : 100,
'Nprod' : ['Mono'],
'Tini'  : 0,

# Population
'n'     : 0.025, # MONOSECT
'N'     : 1    , # MONOSECT

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7,
'Gamma': 0,
'Xi'   : 1,
'nu'   : 3,
'delta': 0.05,
'b'    : 1,
'a'    : 1, # MONOSECT
'alpha': 0.02, # MONOSECT
'u'    : 1,

# Inventory-related dynamics
'V'     : 1000,
'sigma' : 0,  # use variation
'chi'   : 0,    # inflation variation

# Debt-related
'Dh'    : 0, # MONOSECT
'D'     : [0],
'r'     : 0.03, # MONOSECT

# Wages-prices
'w'     : 0.6, # MONOSECT
'p'     : 1,
'z'     : 1,
'mu0'   : 1.3,
'eta'   : 0.0,
'gammai': 0, # MONOSECT
'phinull':0.1, # MONOSECT

# Consumption theory
'Cpond' : [1],
}



dict3={
# Numerical structural
'Tmax'  : 50,
'Nprod' : 10,

# Population
'n'     : 0.025,
'N'     : 10,

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7/3,
'Gamma': np.eye(10)*0.1,
'Xi'   : np.eye(10)*3,
'nu'   : 1,
'delta': 0.05,
'b'    : 1,
'a'    : 1,
'alpha': 0.02,
'u'    : .95,

# Inventory-related dynamics
'V'     : 1000,
'sigma' : 1,  # use variation
'chi'   : 0,    # inflation variation

# Debt-related
'Dh'    : 0,
'D'     : [0],
'r'     : 0.03,

# Wages-prices
'w'     : 0.6,
'p'     : 1,
'z'     : 1,
'mu0'   : 1.3,
'eta'   : 0.1,
'gammai': 0,
'phinull':0.1,

# Consumption theory
'Cpond' : [1],
}


hub.set_dparam(**dictMONOGOODWIN)
hub.get_summary()
hub.run()
hub.reinterpolate_dparam(N=200)
hub.calculate_Cycles()
hub.calculate_StatSensitivity()

pgm.plots.plotbyunits(hub,
                            filters_key=('kappa','a','w','basket'),
                            filters_units=['$.y^{-1}','$.units^{-1}','','y^{-1}'],
                            filters_sector=(),
                            separate_variables={'':['pi','xi','gamma','rd','omega']})
#pgm.plots.plotnyaxis(hub,y=[[['K','Consumption'],['K',"Capital"],['V','Consumption']],['employment'],])