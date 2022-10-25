import pygemmes as pgm
import numpy as np
hub=pgm.Hub('CHIMES')

dict={
'Tmax':80,
'Nprod': ['Consumption','Capital'],
'nx':1,

'alpha' : 0.02,
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
'u':[1,1],
'p':[1.5,3],
'V':[100,150],
'z':[1,1],
'k0': 1.3,

'Cpond':[1,0],

'mu0':[1.3,2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[1,1],
'b':1,
'nu':3,

## MATRICES
'Gamma': [[0.1 ,0.015],
          [0.015 ,0.1]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.01,.5],[1,0.02]],
'rho': np.eye(2),
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

# investment
'k0': 1.,

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

'k0': 1.,

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

hub=pgm.Hub('CHIMES')
hub.set_dparam(**dict,verb=False)
hub.get_summary()
hub.run()
#hub.reinterpolate_dparam(N=200)
#hub.calculate_Cycles()
#hub.calculate_StatSensitivity()


pgm.plots.plotbyunits(hub,
                            filters_key=('kappa','w','basket'),
                            filters_units=('$.y^{-1}'),#,'$.units^{-1}','','y^{-1}'],
                            filters_sector=(),
                            separate_variables={'':['pi','xi','gamma','rd','omega']})
pgm.plots.plotnyaxis(hub,y=[[['K','Consumption'],['K',"Capital"],['V','Consumption']],['employment'],])
'''
# Repartition relative pi
pgm.plots.repartition(hub,['xi','gamma','omega','pi','rd','reldotv','reloverinvest'],sector='Consumption',title='')
pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector='Consumption',dashboundary=False,title='')

# Repartition of physical fluxes
pgm.plots.repartition(hub,['xi','gamma','omega','pi','rd','reldotv','reloverinvest'],sector='Capital',title='')
pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector='Capital',dashboundary=False,title='')
'''
# Repartition of monetary fluxes
for sector in ['Consumption','Capital']:
    pgm.plots.repartition(hub,['xi','gamma','omega','pi','rd','reldotv','reloverinvest'],sector=sector,title=sector)
    pgm.plots.repartition(hub,['TakenbyY','TakenbyI','C','dotV'],ref='Y',sector=sector,dashboundary=False,title=sector)
    pgm.plots.repartition(hub,['TransactI','TransactInter','Consumption','Interests','Wage'],ref='dotD',sector=sector,dashboundary=False,title=sector)

