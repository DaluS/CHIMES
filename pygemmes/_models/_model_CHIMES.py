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

"""
        'H': {
            'func': lambda H,deltah,rho,C: C-deltah*H-matmul(rho,H),
            'com': 'explicit stock-flow',
            'definition': 'Possessions',
            'units': 'units',
            'size': ['Nprod']
        },
"""
_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['Consumption','Capital'],
        },
    },
    'differential': {
        'K': {
            'func': lambda Ir,delta,u,K: Ir-delta*u*K,
            'com': 'depreciation proportional to u',
            'definition': 'Productive capital in physical units',
            'units': 'Units',
            'size': ['Nprod'],
            'initial': 2.7*0.5,
        },
        'D': {
            'func': Debtvariation,
            'com': 'no shareholding',
            'definition': 'Debt of local sector',
            'units': '$',
            'size': ['Nprod'],
        },
        'Dh': {
            'func': lambda W,p,C: -W+sprod(p,C),
            'com': '',
            'definition': 'debt of households',
            'units': '$',
            'symbol':r'$D_{household}$'
        },
        'u': {
            'func': lambda u: 0,
            #'func': lambda u,sigma,V,dotV: -sigma*(1-u)*dotV/V,
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
            'units': '$.Units^{-1}',
        },
        'V': {
            'func': lambda dotV : dotV,
            'com': 'dynamics in dotV',
            'size': ['Nprod'],
            'units': 'units',
            'symbol': '$V$'
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
            'units': 'y^{-1}',
            'symbol': 'i'
        },
        'pi': {
            'func': lambda c,p,r,d : 1 - c/p -r*d,
            'com': 'explicit form',
            'size': ['Nprod'],
            'units':'',
        },
        'c': {
            'func': lambda omega,epsilon,xi,p : p*(omega + epsilon+xi),
            'com':'explicit form',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },
        'xi': {
            'func': lambda delta,nu,b,p,Xi: (delta*nu/b)*matmul(Xi,p)/p,
            'definition': 'relative capex weight',
            'com': 'explicit calculation',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\xi$',
        },
        'ibasket': {
            'func': lambda inflation,basket : sprod(inflation,basket),
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
            'units': 'y^{-1}',
            'symbol': r'$i_{Basket}$',
        },
        'basket': {
            'func': lambda Nprod : 1/Nprod,
            'com': 'EQUATION IS SENSELESS',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
            'units': '',
        },

        ### Purchasing power
        'W': {
            'func': lambda w,z,L,r,Dh: sprod(w*z,L)-r*Dh,
            'definition': 'Total income of household',
            'com': 'no shareholding, no bank possession',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'
        },
        #'Omega': {
        #    'func': lambda N,W,e,p,basket: (W/N)/(e*p+(1-e)*(sprod(basket,p))) ,
        #    'definition': 'Percieved purchasing power',
        #    'com': 'no shareholding, no bank possession',
        #    'size': ['Nprod'],
        #},
        #'Hid': {
        #    'func': lambda N,hid0,Omega,Omega0,x: N*hid0/(1+np.exp(-x*(Omega/Omega0-1))),
        #    'definition': 'Ideal goods for purchasing power',
        #    'com':'deduced from Omega',
        #    'size': ['Nprod'],
        #},
        'L': {
            'func': lambda a,b,Y: Y/(a*(2-b)),
            'com': 'instant recruitment on leontiev',
            'size': ['Nprod'],
        },
        'employment': {
            'func': lambda L,N: ssum(L)/N,
            'com': 'Calculation with L',
            'units': 'y^{-1}',
            'symbol': r'$\lambda$'
        },
        'philips':  {
            'func': lambda employment, phi0, phi1: -phi0 + phi1 / (1 - employment)**2,
            'com': 'diverging (force omega \leq 1)',
            'units': 'y^{-1}',
            'symbol': r'$\Phi(\lambda)$',
        },



        ### Physical fluxes
        'Y': {
            'func': lambda K,u,b,nu: u*K*b/nu,
            'com': 'Leontiev with variable use',
            'size': ['Nprod'],
            'units': 'Units.y^{-1}',
        },
        'Ir': {
            'func': lambda I,Xi,p: I/matmul(Xi,p),
            'com': 'deduced from monetary investment',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },
        'C': {
            'func': lambda W,Cpond,p: Cpond*W/p,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },

        'dotV':{
            'func': lambda Y,Gamma,Ir,C,Xi: Y-matmul(transpose(Gamma),Y)-C-matmul(transpose(Xi),Ir),
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'units': 'y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$\dot{V}$'
        },

        ### Explicit monetary flux
        'I': {
            'func': lambda p,Y,kappa,xi: p*Y*(kappa+xi),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'd': {
            'func': lambda D,p,Y: D/(p*Y),
            'com': 'deduced from D',
            'definition': 'relative weight debt',
            'units': 'y^{-1}',
            'size': ['Nprod'],
        },
        'kappa': {
            'func': lambda pi: pi,
            'com': 'no external investment (but inventory)',
            'units': '',
            'size': ['Nprod'],
        },

        ### AUXILLIARY VECT STATEVAR
        'epsilon': {
            'func': lambda Gamma,p: matmul(Gamma,p)/p,
            'definition': 'share of intermediary consumption',
            'com': 'raw definition',
            'units': '',
            'size': ['Nprod'],
        },
        'omega': {
            'func': lambda a,b,w,p,z: z*b*w/(p*a*(2-b)),
            'com': 'raw def',
            'units': '',
            'size': ['Nprod'],
        },
        'employment_local': {
            'func': lambda L,N : L/N,
            'com': 'raw def',
            'definition': 'part of population working in sector',
            'size': ['Nprod'],
            'units': '',
        },


        ### AUXILLIARY STATEVAR
        #'GDP_nominal': 0,
        #'GDP': 0,

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
        #'e': {'value': 1,
        #      'definition': 'weight of other consumptions',
        #      'size': ['Nprod']
        #      },
        'Cpond': {'value': 0,
              'definition': 'part of salary into consumption of the product',
              'size': ['Nprod']
              },
        #'f': {'value': 1,
        #      'definition': 'consumption adjustment rate',
        #      'size': ['Nprod']
        #      },
        #'hid0': {'value': 1,
        #      'definition': 'willed quantity of goods',
        #      'size': ['Nprod']
        #      },
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

        #'sigma': {'value': 1,
        #          'size': ['Nprod']
        #          },
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
        #'Omega0': {'value': 1,
        #           'size': ['Nprod']
        #           },
        #'x': {'value': 1,
        #      'size': ['Nprod']
        #      },

        ### MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
        'Xi': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
        #'rho': {
        #    'value': 0.01,
        #    'size': ['Nprod', 'Nprod']
        #},
    },
}

"""
'C': {
    'func': lambda f, Hid,rho,H: f*(Hid-H)+matmul(rho,H),
    'com': 'consumption as relaxation',
    'definition': 'flux of goods for household',
    'size': ['Nprod'],
},
"""

_PRESETS = {
    'default': {
        'fields': {},
        'com': (''),
        'plots': {},
    },
}
# Check size consistent in operations
# If only one dimension, transform string into list
