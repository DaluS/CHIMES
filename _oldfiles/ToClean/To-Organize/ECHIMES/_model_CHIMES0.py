"""
ECONOMIC CORE for HOLISTIC INTERDISCIPLINARY MODEL assessing ECOLOGICAL SUSTAINABILITY

The goal of CHIMES is :
    * description of production with physical variables
    * behavior of agents (price, investment) based on economic values
    * Connexion to ecological systems through physical coupling (emissions, land use...)

It integrates :
    * N productive sector, by activity
    * Material flow analysis integrated inside
    * Loans dynamics for investment and cross-sector expanses
    * Inventory fluctuations
    * Inflation
    * Adaptive use of capital
"""

from pygemmes._models import Funcs, importmodel,mergemodel
import numpy as np


# ######################## OPERATORS ####################################
'''
Those are operators that can be used to do multisectoral operations : 
coupling, transposition, sums... 
'''
def sprod(X,Y):
    ''' Scalar product between vector X and Y.
    Z=sprod(X,Y) so Z_i=\sum X_i Y_i'''
    return np.matmul(np.moveaxis(X,-1,-2),Y)
def ssum(X):
    ''' Scalar product between vector X and Y.
    Z=ssum(X) so Z_i=\sum X_i'''
    return np.matmul(np.moveaxis(X,-1,-2),X*0+1)
def ssum2(X):
    '''
    Z_i=ssum_j(X_{ij}) so Z_i=\sum_j X_{ij}'''
    return np.sum(X, axis=-1)[...,np.newaxis]
def transpose(X):
    '''Transposition of X :
    Y=transpose(X)  Y_ij=X_ji'''
    return np.moveaxis(X, -1, -2)
def matmul(M,V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M,V)
def distXY(x,y):
    '''x and y vector of position, z=distXY(x,y) is the matrix of distance
     between each particle of position x,y :
     z_ij= \sqrt{ (x_i-x_j)^2 + (y_i-y_j)^2}'''
    return np.sqrt((x - transpose(x)) ** 2 + (y - transpose(y)) ** 2)
def Identity(X):
    '''generate an identity matrix of the same size a matrix X'''
    return np.eye(np.shape(X)[-1])
# ########################################################################

def dotD( MtransactI, MtransactY, wL, rD, pC,Sh):
    return rD \
         + Sh + wL - pC \
         + ssum2(MtransactI - transpose(MtransactI)) \
         + ssum2(MtransactY - transpose(MtransactY))


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    ###################################################################
    'differential': {
        ### MONETARY STOCK-FLOW CONSISTENCY
        'D': {
            'func': lambda dotD: dotD,
            'com': 'logics in field dotD',
            'definition': 'Debt of local sector',
            'units': '$',
            'size': ['Nprod'],
        },
        'Dh': {
            'func': lambda W, p, C: -W + sprod(p, C),
            'com': 'consumption minus Augmented wage',
            'definition': 'Debt of households',
            'units': '$',
            'symbol': r'$D_{household}$'
        },

        ### PHYSICAL STOCK-FLOW CONSISTENCY
        'V': {
            'func': lambda dotV: dotV,
            'com': 'dynamics in dotV',
            'size': ['Nprod'],
            'units': 'units',
            'symbol': '$V$'
        },
        'K': {
            'func': lambda Ir, delta, K: Ir - delta * K,
            'com': 'depreciation proportional to u',
            'definition': 'Productive capital in physical units',
            'units': 'units',
            'size': ['Nprod'],
            'initial': 2.7,
        },

        ### PRICES
        'p': {
            'func': lambda p, inflation: p * inflation,
            'com': 'price deduced from inflation',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },
        'w0': {'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket),
              'com': 'Inflation-awareness + a Phillips',
               'definition': 'Wage caracteristic level',
               'units':'$.Humans^{-1}.y^{-1}',
               'initial':0.75,
              },

        ### BEHAVIOR
        'u0': {
            #'func': lambda u0, sigma, V, dotV: sigma * (1 - u0) * (-dotV / V ),
            #'com': 'signal on inventory variation',
            'func': lambda u0, sigma, v: sigma * (1 - u0) * (v - 1 ),
            'com': 'signal on target inventory',
            'definition': 'voluntary use of productive capital',
            'units': '',
            'size': ['Nprod'],
            'initial': 1,
        },

        ### EXOGENOUS SCALING
        'a0': {'func': lambda a0, alpha: a0 * alpha,
               'com': 'Capital per person',
               'initial':1,
              },
        'N': {'func': lambda N, n: N * n,
              'com': 'exogenous',
              'initial':1,
              },
    },
    'statevar': {
        ### BY-SECTOR PRODUCTIVITY, WAGE, USE AND ACCESSIBILITY
        'w': {'func': lambda w0,z: w0*z,
              'com': 'Sector-adjusted wage',
              'size':['Nprod']},
        'a': {'func': lambda a0, b,nu,u : u*a0*b/nu,
              'com': 'Sector-adjusted productivity',
              'size':['Nprod']},
        'u': {'func': lambda u0: u0,
              'com': 'for the moment only voluntary limitation',
              'definition': 'Effective use of capital',
              'size': ['Nprod']},
        'nu': {'func': lambda nu0, u: nu0/u,
               'com': 'Adjusted by use of capital',
               'size': ['Nprod']},

        ### PRODUCTION FUNCTION
        'L': {'func': lambda Y,a : Y/a,
              'com': 'logics in a',
              'size': ['Nprod'],
              },
        'employment': {
            'func': lambda L, N: L / N,
            'com': 'Calculation with L',
            'units': '',
            'symbol': r'$\lambda$',
            'size': ['Nprod'],
            },
        'Y': {'func': lambda nu, K: K / nu,
              'com': 'logics in nu',
              'size': ['Nprod'],
              },
        'v': {
            'func': lambda K, epsinV, nu0,V: epsinV*K/(V*nu0),
            'definition': 'relative inventory to target',
            'com': 'epsilon of year share',
            'units':'',
            'symbol': r'$v$',
            'size': ['Nprod'],
        },

        ### COST COMPONENTS
        'omega': {
            'func': lambda a, w, p:  w / (p* a),
            'com': 'By definition',
            'units': '',
            'size': ['Nprod'],
        },
        'Mgamma': {
            'func': lambda Gamma,p : Gamma*transpose(p)/p,
            'definition': 'weight of intermediate consumption from j',
            'units': '',
            'com': 'Matrix version',
            'size': ['Nprod','Nprod'],
        },
        'Mxi': {
            'func': lambda Xi, p,nu,delta: nu*delta*Xi * transpose(p) / p,
            'definition': 'weight of capital destruction from j',
            'units': '',
            'com': 'Matrix version',
            'size': ['Nprod', 'Nprod'],
        },
        'c': {
            'func': lambda omega, Mgamma, Mxi, p: p * (omega + ssum2(Mgamma) + ssum2(Mxi)),
            'com': 'sum of components',
            'size': ['Nprod'],
            'units': r'$.Units^{-1}',
        },

        ### Inflations
        'inflation': {
            'func': lambda inflationMarkup,inflationdotV: inflationMarkup+inflationdotV,
            'com': 'sum of inflation contributions',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i$'
        },
        'inflationMarkup': {
            'func': lambda p, eta, mu0, c,: eta * np.log(mu0 * c / p),
            'com': 'log on markup',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': r'$i^{\mu}$'
        },
        'inflationdotV': {
            #'func': lambda chi, dotV, V: - chi * dotV / V,
            'func': lambda chi, dotV, Y: - chi * dotV / Y,
            'com': 'price adjustment to demand-offer',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': r'$i^{\dot{V}}$'
        },
        'basket': {
            'func': lambda p, C: p * C / sprod(p, C),
            'com': 'cannot be non-auxilliary',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
            'units': '',
        },
        'ibasket': {
            'func': lambda inflation, basket: sprod(inflation, basket),
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
            'units': 'y^{-1}',
            'symbol': r'$i_{Basket}$',
        },


        ### PHYSICAL FLUXES
        'Ir': {
            'func': lambda I,Xi,p: I/matmul(Xi,p),
            'com': 'deduced from monetary investment',
            'units': 'Units.y^{-1}',
            'symbol': r'$I^R$',
            'size': ['Nprod'],
        },
        'C': {
            'func': lambda W,Cpond,p: Cpond*W/p,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },
        'dotV': { 
            'func': lambda Y, Gamma, Ir, C, Xi: Y - matmul(transpose(Gamma), Y) - C - matmul(transpose(Xi), Ir),
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$\dot{V}$'
        },
        'MGammaY': {
            'func': lambda Y, Gamma : Gamma*transpose(Y),
            'definition': 'intermediate physical flux from i to j',
            'com' : 'Matrix version','units': 'Units.y^{-1}',
            'size': ['Nprod','Nprod'],
        },
        'MIrXi': {
            'func': lambda Ir, Xi : Xi*transpose(Ir),
            'definition': 'investment physical flux from i to j',
            'com' : 'Matrix version',
            'units': 'Units.y^{-1}',
            'size': ['Nprod','Nprod'],
        },


        ### MONETARY FLUXES
        'wL': {
            'func': lambda w,L : w*L,
            'com': 'wage bill per sector',
            'definition': 'wage bill per sector',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'pC': {
            'func': lambda p,C: p *C,
            'com': 'explicit monetary flux',
            'definition': 'monetary consumption',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'I': {
            'func': lambda p, Y, kappa, Mxi: p * Y * (kappa + ssum2(Mxi)),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'MtransactY': {
            'func': lambda p, Y, Gamma: Y * Gamma * transpose(p),
            'definition': 'Money from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^Y$'
        },
        'MtransactI': {
            'func': lambda I, Xi, p: I * Xi * transpose(p) / (matmul(Xi, p)),
            'definition': 'Money from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^I$'
        },
        'rD': {
            'func': lambda r,D: r*D,
            'com': 'explicit monetary flux',
            'definition': 'debt interests',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'dotD': {
            'func': dotD,
            'com': 'explicit monetary flux',
            'definition': 'debt variation',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },


        ### HOUSEHOLD-SIDE THEORY
        'W': {
            'func': lambda w, L, rDh, r,D, Sh,DeltaB: sprod(w, L)+Sh+DeltaB*(rDh+ssum(r*D))-rDh,
            'definition': 'Total income of household',
            'com': 'With bank possession and shareholding',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'
        },
        'Sh': {
            'func': lambda p,Y,pi,divlinconst,divlinSlope: ssum(p*Y*(divlinconst+divlinSlope*pi)),
            'com': 'affine coefficients',
            'units':  '$.y^{-1}',
            'symbol': r'$\Delta \Pi $'
        },
        'rDh':{
            'func': lambda r,Dh : r*Dh,
            'definition': 'bank interests for household',
            'units': '$.y^{-1}',
        },
        'employmentAgg': {
            'func': lambda L, N: ssum(L) / N,
            'com': 'Calculation with L',
            'units': '',
            'symbol': r'$\Lambda$'
        },

        'Phillips': {
            'func': lambda employmentAgg, phi0, phi1: -phi0 + phi1 / (1 - employmentAgg) ** 2,
            'com': 'diverging (force omega \leq 1)',
            'units': 'y^{-1}',
            'symbol': r'$\Phi(\lambda)$',
        },

        ### PROFITS AND INVESTMENTS
        'kappa': {
            'func': lambda pi, k0: np.maximum(k0 * pi,0),
            'com': 'LINEAR KAPPA FUNCTION',
            'units': '',
            'size': ['Nprod'],
        },
        'pi': {
            'func': lambda omega, Mgamma, Mxi, r, D, p, Y: 1 - omega - ssum2(Mgamma) - ssum2(Mxi) - r * D / (p * Y),
            'com': 'explicit form',
            'size': ['Nprod'],
            'units': '',
        },
        'rd': {'func': lambda r,D,p,Y : r*D/(p*Y),
               'com': 'explicit form',
               'definition': 'relative weight debt',
               'size': ['Nprod'],
               'units': ''
        },
        'ROC': {
            'func': lambda pi, nu,Xi,p: pi/(nu*matmul(Xi,p)/p),
            'definition': 'return on capital',
            'com': 'raw definition',
            'size': ['Nprod'],
            'units': 'y^{-1}',
        },
    },
    'parameter': {
        ### SCALARS
        'alpha'  :{'value': 0.02 ,},
        'n'      :{'value': 0.025,},
        'phinull':{'value': 0.1  ,},
        'r'      :{'value': 0.03 ,},

        ### VECTORS
        'z': {'value':1,
              'definition': 'local wage ponderation',
              'size': ['Nprod']
              },
        'b': {'value':1,
                'definition': 'local productivity ponderation',
                'size':['Nprod']
                },
        'nu0': {'value':3,
                'definition': 'characteristic capital-to-output',
                'size':['Nprod']
                },
        'Cpond': {'value': .5,
              'definition': 'part of salary into consumption of the product',
              'size': ['Nprod']
              },
        'mu0': {'value': 1.3,
              'definition': '',
              'size': ['Nprod']
              },
        'DeltaB': {'value': 1,},
        'delta': {'value': 0.005,
                  'size': ['Nprod']
                  },
        'deltah': {'value': 0.1,
                  'size': ['Nprod']
                  },
        'sigma': {'value': 1,
                  'size': ['Nprod']
                  },
        'divlinconst':{'value': 0},
        'divlinSlope':{'value': 0},
        'gammai': {'value': 1,
                  },
        'eta': {'value': 0.5,
               'size': ['Nprod']
               },
        'chi': {'value': 1,
               'size': ['Nprod']
               },
        'b': {'value': 0.5,
              'size': ['Nprod']
              },
        'nu': {'value': 3,
               'size': ['Nprod']
               },
        'epsinV' : {'value':0.05,
                    'size':['Nprod']
                    },

        ### MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod'],
            'units':'',
        },
        'Xi': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
        'rho': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
    },
}


        #'Omega': {
        #    'func': lambda N,W,p,basket: (W/N)/(sprod(basket,p)) ,
        #    'definition': 'MONOSECTORAL Percieved purchasing power',
        #    'com': 'no shareholding, no bank possession',
        #    'units':'Units.Humans^{-1}.y^{-1}'
        #},


dictMONOGOODWIN={
# Numerical structural
'Tmax'  : 50,
'Nprod' : ['Mono'],
'Tini'  : 0,

# Population
'n'     : 0.025, # MONOSECT
'N'     : 1    , # MONOSECT

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7,
'Gamma': 0.05,
'Xi'   : 1,
'nu'   : 3,
'delta': 0.05,
'b'    : 3,
'a0'    : 1, # MONOSECT
'alpha': 0.02, # MONOSECT
'u'    : 1,

# Inventory-related dynamics
'V'     : 1,
'sigma' : 0,  # use variation
'chi'   : 0,  # inflation variation

# investment
'k0': 1.,

# Debt-related
'Dh'    : 0, # MONOSECT
'D'     : [0],
'r'     : 0.03, # MONOSECT

# Wages-prices
'w0'     : 0.6, # MONOSECT
'p'     : 1,
'z'     : 1,
'mu0'   : 1.3,
'eta'   : 0.0,
'gammai': 0, # MONOSECT
'phinull':0.1, # MONOSECT

# Consumption theory
'Cpond' : [1],
}

preset_basis = {
'Tmax':50,
'dt':0.1,
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

'sigma':[1,5],
'K': [2.,0.5],
'D':[0,0],
'u':[.95,.7],
'p':[1.5,3],
'V':[1,1],
'z':[1,.3],
'k0': 1.,

'Cpond':[1,0],

'mu0':[1.2,1.2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[1,1],
'b':3,
'nu':3,

## MATRICES
'Gamma': [[0.05 ,0],
          [0    ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.01,1],
       [0.1,1]],
'rho': np.eye(2),
}

preset_basis2=preset_basis.copy()
preset_basis2['K'] = [2.3,0.5]
preset_basis2['u'] = [1,1]
preset_basis2['p'] = [1,1]
preset_basis2['z'] = [1,1]
#preset_basis2['Tmax'] = 50


preset_TRI = {
'Tmax':50,
'dt':0.1,
'Nprod': ['Consumption','Intermediate','Capital'],
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

'sigma':[1,5,5],
'K': [2.1,0.4,0.4],
'D':[0,0,0],
'u':[.95,.95,.95],
'p':[1,1,1],
'V':[1,1,1],
'z':1,
'k0': 1.,
'Cpond':[1,0,0],
'mu0':1.2,
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':1,
'b':3,
'nu':3,

## MATRICES
'Gamma': [[0.0,0.1 ,0],
          [0  ,0.1 ,0],
          [0.0,0.1 ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.0,0,1],
       [0.0,0,1],
       [0.0,0,1]],
'rho': np.eye(3),
}

Nsect=4
#A=np.diag([0.1 for i in range(Nsect-1)],1)
#A[Nsect-2,Nsect-1]=0

A=np.diag([0.1 for i in range(Nsect-1)],-1)
A[Nsect-1,Nsect-2]=0

preset_N = {
'Tmax':8,
'dt':0.1,
'Nprod': ['Consumption']+['Inter'+str(i) for i in range(Nsect-2)]+['Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':4,
'Dh':0,
'w':0.8,

'sigma':5,
'K': [4]+[0.4 for i in range(Nsect-2)]+[5],
'D':0,
'u':.95,
'p':1,
'V':1,
'z':1,
'k0': 1.,
'Cpond':[1]+[0 for i in range(Nsect-1)],
'mu0':1.3,
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':1,
'b':3,
'nu':3,

## MATRICES
'Gamma': A,
'Xi':    [[0 for j in range(Nsect-1)]+[1] for i in range(Nsect)],
'rho': np.eye(Nsect),
}


_PRESETS = {
    'Goodwin': {
        'fields': dictMONOGOODWIN,
        'com': ('A monosectoral system that behaves just as a Goodwin'),
        'plots': {},
    },
    'Bisectoral': {
        'fields': preset_basis,
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting for VERY far from equilibrium'),
        'plots': {},
    },
    'SimpleBi': {
        'fields': preset_basis2, 
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting close to equilibrium'),
        'plots': {},
    },
    'SimpleTri': {
        'fields': preset_TRI,
        'com': 'Trisectoral',
        'plots': {},
    },
    'SimpleN': {
        'fields': preset_N,
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting close to equilibrium'),
        'plots': {},
    },
}