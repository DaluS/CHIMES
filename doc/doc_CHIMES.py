import pygemmes as pgm

hub=pgm.Hub('CHIMES')

dict={
### MONOSECTORAL
'Tmax':50,
'Nprod': ['Consumption','Capital'],
'alpha':0.02,
'n':0.025,
'phinull':0.1,
'gammai':0,
'r':0.0,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'K': [2.2,0.6],
'D':[0,0],
'u':[1,1],
'p':[1,5],
'V':[1000,1250],
'z':[1,1],

'Cpond':[1,0],

'mu0':1.3,
'delta':0.05,
'deltah':0.05,
'eta':0.1,
'chi':0.1,
'b':1,
'nu':3,

## MATRICES
'Gamma': [[0.1,0.01],[0.01,0.1]],
'Xi': [['Consumption','Capital','Consumption','Capital'],['Consumption','Capital','Capital','Consumption'],[0,2,1,0]],
}
hub.set_dparam(**dict)
hub.get_summary()
hub.run()
#hub.plot()

pgm.plots.plotbyunits_multi(hub)