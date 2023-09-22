'''Multiple types of capital'''

_DESCRIPTION = """
# Putty-Clay capital dynamics
* **Article :**    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
"""

from chimes._models import Funcs, importmodel,mergemodel,filldimensions
from chimes._models import Operators as O
import numpy as np

_LOGICS = {
    'size': {'Ntechno': {'list': ['MONO']}},
    'differential': {
        'K'             :{'func': lambda Ir, delta, K: Ir - delta * K},

        'a0'            :{'func': lambda a0, alpha: a0 * alpha,
                          'definition': 'Capital unit per worker'},
        'w0'            :{'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket)},
        'N'             :{'func': lambda N, n: N * n},
        'p'             :{'func': lambda p: 0},
    },
    'statevar': { 
        'w'             :{'func': lambda w0,z: w0*z,},
        'a'             :{'func': lambda a0,apond : a0*apond},
        'nu'            :{'func': lambda A : 1/A},

        'Y'             :{'func': lambda K,A: K*A},
        'L'             :{'func': lambda K,a: K/a},
        'omega'         :{'func': lambda L,Y,w,p:  w*L / (p* Y)},     

        'Phillips'      :{'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG},

        'Pi'            :{'func': lambda p,Y,w,L,Gamma,delta,K : p*Y-w*L-Gamma*Y*p-p*delta*K},
        'SumPi'         :{'func': lambda Pi: O.ssum(Pi),
                          'units' : r'$.y^{-1}',
                          'symbol': r'$\sum \Pi $'  },
        'pi'            :{'func': lambda omega, gamma, delta,nu: 1 - omega - gamma - delta*nu },
        'ROC'           :{'func': lambda pi, A : pi*A},
        'Iweight'       :{'func': lambda ROC,beta: np.exp(ROC*beta)/O.ssum(np.exp(ROC*beta))},
        'Ir'            :{'func': lambda Iweight, SumPi,delta,K : Iweight*SumPi + delta*K},

        'employment'    :{'func': lambda L,N        : L/N},
        'employmentAGG' :{'func': lambda employment: O.ssum(employment),},
    },
    'parameter': {
        'beta' : {'value':100},
        'apond': {'value':3},
        'A'    : {'value':1/3}, 
    }
}




_LOGICS_AGG = {
    'statevar': {
        'KAGG'      : {'func': lambda K         : O.ssum(K), 
                       'symbol': r'$K^{\bigcirc}$',
                       'units': 'Units' }, 
        'YAGG'      : {'func': lambda K,A       : O.ssum(K*A), 
                       'symbol': r'$Y^{\bigcirc}$',
                       'units': 'Units.y^{-1}' },  
        'deltaAGG'  : {'func': lambda KAGG,K,delta: O.ssum(K*delta)/KAGG , 
                       'symbol': r'$\delta^{\bigcirc}$',
                       'units': 'Units' }, 
        'AAGG'      : {'func': lambda K,A,KAGG  : O.ssum(A*K)/KAGG, 
                       'symbol': r'$a^{\bigcirc}$',
                       'units': 'y^{-1}' }, 
        'LAGG'      : {'func': lambda K,A,KAGG  : O.ssum(A*K)/KAGG, 
                       'symbol': r'$L^{\bigcirc}$',
                       'units': 'Humans' },                     
        'GammaAGG'  : {'func': lambda K,Gamma,A : O.ssum(K*Gamma*A)/O.ssum(K*A) , 
                       'symbol': r'$\Gamma^{\bigcirc}$',
                       'units': '' },  
        'aAGG'      : {'func': lambda K,KAGG,a  : KAGG/O.ssum(K/a), 
                       'symbol': r'$K^{\bigcirc}$',
                       'units': 'Units' }, 
        'omegaAGG'  : {'func': lambda K,w,a,A   : O.ssum(K*w/a)/O.ssum(A*K), 
                       'symbol': r'$K^{\bigcirc}$',
                       'units': 'Units' }, 
        'gAGG'      : {'func': lambda g,A       : O.ssum(g*A)/O.ssum(A), 
                       'symbol': r'$K^{\bigcirc}$',
                       'units': 'Units' }, 
    }
}

print(_LOGICS_AGG['statevar'].keys())
_LOGICS = mergemodel(_LOGICS,_LOGICS_AGG)

Dimensions = { 
    'scalar': ['phinull', 'N', 'employmentAGG', 'w0', 'W',
               'alpha', 'a0', 'Nprod', 'Phillips','n',
               'beta','SumPi',
               'KAGG', 'YAGG', 'deltaAGG', 'AAGG', 'GammaAGG', 'aAGG', 'omegaAGG', 'gAGG'
               ],
    'matrix': [],
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Ntechno'],
      'matrix':['Ntechno','Ntechno']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)

_PRESETS={}
