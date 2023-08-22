"""Goodwin-Keen with investment solvability and bank possessions"""


_DESCRIPTION ="""
This is a modificaiton of Goodwin-Keen. The labour productivity (parameter a in our basic model) is still exogenous. 
Assume we can  we can restrict attention to firms aggregate debt, and simply assume that, as it grows closer to its upper-bound, pK,
here we set p=1, a growing number of companies presumably go bankrupt, following complex micro-economic patterns whose nitty gritty here. 
Rather, as a proxy, we posit that the production sector no longer invests whenever D = pK, i.e., d = nu. 
Default is accompanied by a transfer of ownership over the collateral from borrowers to lenders.

The capital accumulation equation reads:
    dot(K) = I - (delta + Γ(d)) * K, where where Γ(d) ∈ [0, 1]
The evolution of private debt is:
    dot(D) = I - Pi_r - (Γ(d)) * K,
Real gross investment, I, is then driven by the return on assets, pi_K, capturing the risk appetite of the productive sector:
    I = kappa(pi_K) * Y * (1 - d/nu)^(1/4),
    where kappa() is an increasing function (depending here on our state variables, omega, d and r through the return on capital) taking values in [0; 1], and d := D/Y .

* **Article :** 
* **Author  :** Weiye Zhu
* **Coder   :** Weiye Zhu, Paul Valcke
* **Date    :** 2023/08/21

"""


# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
#from pygemmes._models import Operators as O


_LOGICS= {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha,
        'com': 'ODE exogenous, exponential', },
        'N': {'func': lambda N,n        : N*n,
        'com': 'ODE exogenous, exponential', },
        #'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'K': {
            'func': lambda Ir, delta, Gamma, K: Ir- (delta + Gamma ) * K,
            'com': 'Capital accumulation',
            },
        'w': {'func': lambda w,phillips : w*phillips,
        'com': 'Phillips impact (no negociation)',
         },
        'p': {'func': lambda p,inflation: p*inflation,
        'com': 'through inflation',
        },
        #'D': {'func': lambda w,L,C,r,D,p: r*D + w*L - p*C },
        'D': {
            'func': lambda I, Pi, Gamma, K,p: p*I - Pi - Gamma *p* K ,
            'com': '',
            },
        'Dh':{'func': lambda w,L,C,r,D,p:-r*D - w*L + p*C ,
        'com': 'Debt',
        },
    },
    'statevar': {
        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) ,
        'com': 'profit ratio',
        },
        'd'  :   {'func': lambda p,Y,D  : D  /(p*Y) ,
        'com': 'debt ratio',
        },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) ,
        'com': 'wage',
        },
        'employment' :{'func': lambda L,N: L/N ,
        'com': 'e',
        },
        'c' :{'func': lambda p,omega: p*omega,
        'com': 'comsumption rate',
        },
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta ,
        'com': 'relative growth rate',
        },      
        
        'Y' :{'func': lambda K,nu: K/nu ,
        'com': 'prod with use rate',
        },
        'Pi':{'func': lambda p,Y,w,L,r,D: p*Y-w*L-r*D ,
        'com': 'Profit for production-Salary',
        },
        'solvability' : {'func': lambda d, nu : (1-(d/nu)),
                         'definition': "debt/asset" },
        #'I' :{'func': lambda kappa,p,Y: kappa*p*Y },
        'I': {
            'func': lambda kappa, Y, solvability,p: p*kappa * Y * solvability**(1/4),
            'com': 'Investment driven by the return on assets capturing the risk appetite of the productive sector', 
            },
        'C' :{'func': lambda Y,Ir,Gamma: Y*(1+Gamma)-Ir ,
              'units': 'Units.y^{-1}'  
        },
        'Ir':{'func': lambda p,I: I/p ,
        'com': 'Real Interest rate',
        },
        'L' :{'func': lambda Y,a: Y/a ,
        },

        'GDP':{'func': lambda Y,p:Y*p,
        },

        'inflation' :{'func': lambda c,p, eta,mu : eta*(mu*c/p -1) ,
        },
        'kappa'     :{'func': lambda pi, k0, k1, k2: k0 + k1 * np.exp(k2 * pi),
        },
        'Gamma': {
            'func': lambda A,d,nu :  np.maximum(0,1 - np.exp(A/(1-(nu/d)**2))),
            'definition': 'Fraction of capital seized by the banking sector',
            'com': 'exponential form'
        },
        'phillips'  :{'func': lambda employment, phi0, phi1: -phi0 + phi1 / (1 - employment)**2,
        'com': '',
        },
    },
    'parameter': {
        'Agamma' : {
            'value': 0.05,
            'definition': 'seizing parameter'
        }
    },
    'size': {},
}


plotdict= {
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ['Gamma'],
                              ['solvability']
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2},
                       {'x': 'time',
                        'y': [['K', 'Y', 'I', 'Pi'],
                              ['inflation', 'g'],
                              ],
                        'idx':0,
                        'log':[False,False],
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'd',
                    'color': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         },  # optional
                        ],
        }
        
_SUPPLEMENTS = {}
_PRESETS = {
    'default': {
        'fields': {
            'A': 0.05,
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .85*1.19,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 3.01,
            'delta': .008,
            'k0': -0.00651,
            'k1': np.exp(-5.01),
            'k2': 20.01,
            'r': 0.031,
            'p': 1.31,
            'eta': 0.11,
            'gammai': 0.51,
        },
        'plots': plotdict,
        'com':'Good Equilibrium '
    },
    'infinity_debt': {
        'fields': {
            'A': 0.05,
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 1.01,
            'D': 0.01,
            'w': 0.75,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 3.01,
            'delta': .008,
            'k0': -0.00651,
            'k1': np.exp(-5.01),
            'k2': 20.01,
            'r': 0.031,
            'p': 1.31,
            'eta': 0.11,
            'gammai': 0.51,
        },
        'plots': plotdict,
        'com':''
    },
}