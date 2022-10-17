import pygemmes as pgm
import numpy as np
hub=pgm.Hub('CHIMES')

dict={
### MONOSECTORAL
'Tmax':10,
'Nprod': ['Consumption','Capital'],
'alpha':0.02,
'n':0.025,
'phinull':0.1,
'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[10,10],
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


dict2={
# Numerical structural
'Tmax'  : 50,
'Nprod' : ['Mono'],

# Population
'n'     : 0.025,
'N'     : 1,

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7/3,
'Gamma': 0.1,
'Xi'   : 3,
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


dict3={
# Numerical structural
'Tmax'  : 50,
'Nprod' : 10,

# Population
'n'     : 0.025,
'N'     : 10,

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7/3,
'Gamma': np.eye(10),
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


hub.set_dparam(**dict3)
hub.get_summary()
hub.run()
pgm.plots.plotbyunits_multi(hub,
                            filters_key=('kappa','a','w','basket'),
                            filters_units=['$.y^{-1}','$.units^{-1}','','y^{-1}'],
                            filters_sector=(),
                            separate_variables={'':['pi','xi','gamma','rd','omega']})