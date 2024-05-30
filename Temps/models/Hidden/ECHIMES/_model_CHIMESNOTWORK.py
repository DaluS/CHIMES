'''Numerical core for multisectoral models'''

_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY
* **Article :** https://www.overleaf.com/project/62fbdce83176c9784e52236c    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

## Description
The goal of **E-CHIMES** is:
* description of production with physical variables
* behavior of agents (price, investment) based on economic values
* Connexion to ecological systems through physical coupling (emissions, land use...)

It integrates :
* Nprod productive sector, by activity
* Material flow analysis integrated inside
* Loans dynamics for investment and cross-sector expanses
* Inventory fluctuations
* Inflation
* Adaptive use of capital

## What should be done ?
* Check u and i mechanism
"""
from chimes._models import Funcs, importmodel,mergemodel
from chimes._models import Operators as O
import numpy as np

def dotD( MtransactI, MtransactY, wL, rD, pC):
    return rD \
         + wL -pC \
         + O.ssum2(MtransactI - O.transpose(MtransactI)) \
         + O.ssum2(MtransactY - O.transpose(MtransactY))



_LOGICS = {
    'size': {'Nprod': {'list': ['MONO'],},},
    ###################################################################
    'differential': {
        ### MONETARY STOCK-FLOW CONSISTENCY
        'D':  {'func': lambda dotD: dotD},
        'Dh': {'func': lambda W, p, C: -W + O.sprod(p, C)},

        ### PHYSICAL STOCK-FLOW CONSISTENCY
        'V': {'func': lambda dotV: dotV},
        'K': {'func': lambda Ir, delta, K: Ir - delta * K},

        ### PRICES
        'p':  {'func': lambda p, inflation: p * inflation},
        'w0': {'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket),},

        ### BEHAVIOR
        'u0': {'func': lambda u0, sigma, V, dotV: -sigma * (1 - u0) * (dotV / V),},
              #'func': lambda u0, sigma, Y, dotV: -sigma * (1 - u0) * (dotV / Y),
              #'func': lambda u0, sigma, v0: -sigma * (1 - u0) * (1-1/v0),
              # 'func': lambda u: 0,      

        ### EXOGENOUS SCALING
        'a0':{'func': lambda a0, alpha: a0 * alpha,},
        'N': {'func': lambda N, n: N * n,},
    },
    'statevar': {
        ### BY-SECTOR PRODUCTIVITY AND WAGE
        'w':        {'func': lambda w0,z: w0*z},
        'a':        {'func': lambda a0, b,nu,u : u*a0*b/nu},

        ### USE AND ACCESSIBILITY
        'u':        {'func': lambda u0: u0},
        'nu':       {'func': lambda nu0, u: nu0/u},

        ### COST COMPONENTS
        'omega':    {'func': lambda a, w, p:  w / (p* a)},
        'Mgamma':   {'func': lambda Gamma,p : Gamma*O.transpose(p)/p},
        'Mxi':      {'func': lambda Xi, p,nu,delta: nu*delta*Xi * O.transpose(p) / p},
        'c':        {'func': lambda omega, Mgamma, Mxi, p: p * (omega + O.ssum2(Mgamma) + O.ssum2(Mxi))},

        ### Inflations
        'inflation':        {'func': lambda inflationMarkup,inflationdotV: inflationMarkup+inflationdotV},
        'inflationMarkup':  {'func': lambda p, eta, mu0, c,: eta * np.log(mu0 * c / p)},
        'inflationdotV':    {'func': lambda chi, dotV, V: - chi *( dotV / V)},
        'basket':           {'func': lambda p, C: p * C / O.sprod(p, C)},
        'ibasket':          {'func': lambda inflation, basket: O.sprod(inflation, basket)},

        'L': {'func': lambda Y,a : Y/a},

        ### PHYSICAL FLUXES
        'Y': {'func': lambda nu, K: K / nu},
        'Ir':{'func': lambda I,Xi,p: I/O.matmul(Xi,p)},
        'C': {'func': lambda W,Cpond,p: Cpond*W/p},
        'dotV': {'func': lambda Y, Gamma, Ir, C, Xi: Y - O.matmul(O.transpose(Gamma), Y) - C - O.matmul(O.transpose(Xi), Ir)},
        'deltaK':       {'func': lambda K,delta : delta*K},
        
        # Matrix approach
        'Minter':       {'func': lambda Y, Gamma: O.transpose(Gamma*Y)},
        'Minvest':      {'func': lambda Ir, Xi:  O.transpose(Xi* Ir)},
        'MtransactY':   {'func': lambda p, Y, Gamma: Y * Gamma * O.transpose(p)},
        'MtransactI':   {'func': lambda I, Xi, p: I * Xi * O.transpose(p) / (O.matmul(Xi, p))},

        ### MONETARY FLUXES
        'wL':           {'func': lambda w,L : w*L},
        'pC':           {'func': lambda p,C: p *C,},
        'I':            {'func': lambda p, Y, kappa, Mxi: p * Y * (kappa + O.ssum2(Mxi)),},

        'rD':           {'func': lambda r,D: r*D,},
        'dotD':         {'func': dotD,},

        ### LABOR-SIDE THEORY
        'W':            {'func': lambda w, L, r, Dh: O.sprod(w, L) - r * Dh},
        'rDh':          {'func': lambda r,Dh : r*Dh},
        'employmentAGG':{'func': lambda employment: O.ssum(employment)},
        'Phillips':     {'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG},
        #'func': lambda employmentAGG, phi0, phi1: -phi0 + phi1 / (1 - employmentAGG) ** 2,
            
        ### PROFITS AND INVESTMENTS
        'kappa':        {'func': lambda pi, k0: k0 * pi},
        'pi':           {'func': lambda omega, Mgamma, Mxi, r, D, p, Y: 1 - omega - O.ssum2(Mgamma) - O.ssum2(Mxi) - r * D / (p * Y)},
        'rd':           {'func': lambda r,D,p,Y : r*D/(p*Y)},
        ################################################
        'gK':           {'func': lambda Ir,K,delta : Ir/K - delta},
        'ROC':          {'func': lambda pi, nu,Xi,p: pi/(nu*O.matmul(Xi,p)/p)},
        'employment':   {'func': lambda L,N: L/N},
        'gamma':        {'func': lambda Gamma, p: O.matmul(Gamma, p) / p},
        'xi':           {'func': lambda delta, nu, b, p, Xi: (delta * nu / b) * O.matmul(Xi, p) / p},
        'reldotv':      {'func': lambda dotV, Y, p, c: (c - p) * dotV / (p * Y)},
        'reloverinvest':{'func': lambda kappa, pi: pi - kappa},
    },
    'parameter': {
    },
}

Monosectoral = ['Dh','w0','a0','N','ibasket','W','rDh','employmentAGG','Phillips','alpha','n','phinull','r','gammai']
Matrix= ['Mgamma','Mxi','Minter','Minvest','MtransactY','MtransactI','Gamma','Xi']

for k in _LOGICS.keys():
    for key in _LOGICS[k]:
        if 'size' not in _LOGICS[k][key].keys():
            if key in Matrix: _LOGICS[k][key]['size']=['Nprod','Nprod']
            elif key not in Monosectoral: _LOGICS[k][key]['size']=['Nprod','__ONE__']

############################ SUPPLEMENTS ################################################
'''
Specific parts of code that are accessible
'''
def funcs(test):
    print(test)

_SUPPLEMENTS= {'Test':funcs}



############################ PRESETS #####################################################

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
#'Gamma': [[0.05 ,0],
#          [0    ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
#'Xi': [[0.01,1],
#       [0.1,1]],
#'rho': np.eye(2),
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

########################################################################################
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



Removed={### SCALARS
        'alpha'  :{'value': 0.02,},
        'n'      :{'value': 0.025,},
        'phinull':{'value': 0.1,},
        'r'      :{'value': 0.03, },

        ### VECTORS
        'z': {'value':1,
              'definition': 'local wage ponderation',
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
        'delta': {'value': 0.005,
                  'size': ['Nprod']
                  },
        'deltah': {'value': 0.1,
                  'size': ['Nprod']
                  },
        'sigma': {'value': 1,
                  'size': ['Nprod']
                  },
        'gammai': {'value': 1,
                  },
        'eta': {'value': 0.5,
               'size': ['Nprod']
               },
        'chi': {'value': 1.5,
               'size': ['Nprod']
               },
        'b': {'value': 1,
              'size': ['Nprod']
              },
        'nu': {'value': 3,
               'size': ['Nprod']
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
        },}