# -*- coding: utf-8 -*-
"""
DESCRIPTION :

CHIMES : Cor
"""

import numpy as np
from pygemmes._models import Funcs


# ######################## OPERATORS ####################################
def sprod(X,Y):
    return np.matmul(np.moveaxis(X,-1,-2),Y)
def ssum(X):
    return np.matmul(np.moveaxis(X,-1,-2),X*0+1)
def transpose(X):
    return np.moveaxis(X, -1, -2)
def matmul(M,V):
    return np.matmul(M,V)
# #######################################################################

def Debtvariation(r,D,w,L,z,p,Y,C,Ir,Gamma,Xi):
    debt = r*D+w*z*L-p*C \
        -matmul((Xi   -transpose(Xi)   ),p*Ir) \
        -matmul((Gamma-transpose(Gamma)),p*Y)
    return debt


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['energy'],
        },
    },
    'differential': {
        'K': {
            'func': lambda Ir,delta,u,K: Ir-delta*u*K,
            'com': 'depreciation proportional to u',
            'definition': 'Productive capital in physical units',
            'units': 'units',
            'size': ['Nprod'],
            'initial': 2.7*0.5,
        },
        'H': {
            'func': lambda H,deltah,rho,C: C-deltah*H-matmul(rho,H),
            'com': 'explicit stock-flow',
            'definition': 'Possessions',
            'units': 'units',
            'size': ['Nprod']
        },
        'D': {
            'func': Debtvariation,
            'com': 'no shareholding',
            'definition': 'Debt of local sector',
            'size': ['Nprod'],
        },
        'Dh': {
            'func': lambda W,p,C: -W+p*C,
            'com': '',
            'definition': 'debt of households',
        },
        'u': {
            'func': lambda u,sigma,V,dotV: -sigma*(1-u)*dotV/V,
            'com': 'hardcapped at 1',
            'definition': 'use of productive capital',
            'units': '',
            'size': ['Nprod'],
            'initial':1,
        },
        'p': {
            'func': lambda p,inflation: p*inflation,
            'com': 'log on markup',
            'size': ['Nprod'],
        },
        'V': {
            'func': lambda dotV : dotV,
            'com': 'dynamics in dotV',
            'size': ['Nprod'],
        },
        'w': {'func': lambda philips, w,gammai, ibasket : w*(philips+gammai*ibasket),
              'com': 'exogenous',
             },
        'a': {'func': lambda a, alpha : a*alpha,
              'com': 'exogenous',
             },
        'N': {'func': lambda N, n : N*n,
              'com': 'exogenous',
             },
    },
    'statevar': {
        ### price,profit,inflation ###
        'inflation': {
            'func': lambda p,eta,mu0,c,chi,dotV,V: eta*np.log(mu0*c/p)-chi*dotV/V,
            'com': 'log on markup',
            'size': ['Nprod'],
        },
        'pi': {
            'func': lambda c,p,r,d : 1 - c/p -r*d,
            'com': 'explicit form',
            'size': ['Nprod'],
        },
        'c': {
            'func': lambda w,a,b,Gamma,delta,nu,Xi,p : w/(a*2*(1-b)) + matmul(Gamma,p)+delta*nu/b * matmul(Xi,p),
            'com':'explicit form',
            'size': ['Nprod'],
        },
        'xi': {
            'func': lambda delta,nu,b,p,Xi: (delta*nu/b)*matmul(Xi,p)/p,
            'definition': 'relative capex weight',
            'com': 'explicit calculation',
            'size': ['Nprod'],
        },
        'ibasket': {
            'func': lambda inflation,basket : sprod(inflation,basket),
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
        },
        'basket': {
            'func': lambda Nprod : 1/Nprod,
            'com': 'EQUATION IS SENSELESS',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
        },

        ### Purchasing power
        'W': {
            'func': lambda w,z,L,r,Dh: sprod(w*z,L)-r*Dh,
            'definition': 'Total income of household',
            'com': 'no shareholding, no bank possession',
        },
        'Omega': {
            'func': lambda N,W,e,p,basket: (W/N)/(e*p+(1-e)*(sprod(basket,p))) ,
            'definition': 'Percieved purchasing power',
            'com': 'no shareholding, no bank possession',
            'size': ['Nprod'],
        },
        'Hid': {
            'func': lambda N,hid0,Omega,Omega0,x: N*hid0/(1+np.exp(-x*(Omega/Omega0-1))),
            'definition': 'Ideal goods for purchasing power',
            'com':'deduced from Omega',
            'size': ['Nprod'],
        },
        'L': {
            'func': lambda a,b,Y: Y/(a*(2-b)),
            'com': 'instant recruitment on leontiev',
            'size': ['Nprod'],
        },
        'employment': {
            'func': lambda L,N: ssum(L)/N,
            'com': 'Calculation with L',
        },
        'philips': Funcs.Phillips.div,



        ### Physical fluxes
        'Y': {
            'func': lambda K,u,b,nu: u*K*b/nu,
            'com': 'Leontiev with variable use',
            'size': ['Nprod'],
        },
        'Ir': {
            'func': lambda I,Xi,p: I/matmul(Xi,p),
            'com': 'deduced from monetary investment',
            'size': ['Nprod'],
        },
        'C': {
            'func': lambda f, Hid,rho,H: f*(Hid-H)+matmul(rho,H),
            'com': 'consumption as relaxation',
            'definition': 'flux of goods for household',
            'size': ['Nprod'],
        },
        'dotV':{
            'func': lambda Y,Gamma,Ir,C: Y-matmul(Gamma,Y)-C-Ir,
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'size': ['Nprod'],
        },

        ### Explicit monetary flux
        'I': {
            'func': lambda p,Y,kappa,xi: p*Y*(kappa+xi),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'size': ['Nprod'],
        },
        'd': {
            'func': lambda D,p,Y: D/(p*Y),
            'com': 'deduced from D',
            'definition': 'relative weight debt',
            'size': ['Nprod'],
        },
        'kappa': {
            'func': lambda pi: pi,
            'com': 'no external investment (but inventory)',
            'size': ['Nprod'],
        },
    },


    'parameter': {
        ### SCALARS
        'alpha'  :{'value': 0.02,},
        'n'      :{'value': 0.025,},
        'phinull':{'value': 0.1,},
        'r'      :{'value': 0.03, },

        ### VECTORS
        'z': {'value':1,
              'definition': 'local wage ponderation',
              'size': ['Nprod']
              },
        'e': {'value': 1,
              'definition': 'weight of other consumptions',
              'size': ['Nprod']
              },
        'f': {'value': 1,
              'definition': 'consumption adjustment rate',
              'size': ['Nprod']
              },
        'hid0': {'value': 1,
              'definition': 'willed quantity of goods',
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
                  'size': ['Nprod']
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
        'Omega0': {'value': 1,
                   'size': ['Nprod']
                   },
        'x': {'value': 1,
              'size': ['Nprod']
              },

        ### MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
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



_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
