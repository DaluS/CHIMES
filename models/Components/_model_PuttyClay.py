'''Multiple types of capital'''

_DESCRIPTION = """
# Putty-Clay capital dynamics
* **Article :**    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
"""

from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O
import numpy as np

_LOGICS = {}

"""
    'size': {
        'Ntechno': {'list':['One']},
    },
    'differential': {
    }

    'statevar': { 
        'w'             :{'func': lambda w0,z: w0*z,},
        'a'             :{'func': lambda a0,apond : a0*apond},
        'nu'            :{'func': lambda A : 1/A},

        'Y'             :{'func': lambda K,A: K*A},
        'L'             :{'func': lambda K,a: K/a},
        'omega'         :{'func': lambda L,Y,w,p:  w*L / (p* Y)},     

        'Phillips'      :{'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG},

        'Pi'            :{'func': lambda p,Y,w,L,Gamma,delta,K : p*Y-w*L-Gamma*Y*p-p*delta*K},
        'pi'            :{'func': lambda omega, gamma, delta,nu: 1 - omega - gamma - delta/A },
        'ROC'           :{'func': lambda pi, A : pi*A},

        'Iweight'       :{'func': lambda ROC,beta: np.exp(ROC*beta)/(O.ssum(np.exp(ROC*beta)))},
        'Ir'            :{'func': lambda Iweight, Pi : Iweight*O.ssum(Pi) + delta*K},

        'employment'    :{'func': lambda L,N        : L/N},
        'employmentAGG' :{'func': lambda employment: O.ssum(employment),},
    }
}


        'K'             :{'func': lambda Ir, delta, K: Ir - delta * K},

        'a0'            :{'func': lambda a0, alpha: a0 * alpha,
                          'definition': 'Capital unit per worker'},
        'w0'            :{'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket)},
        'N'             :{'func': lambda N, n: N * n},
        'p'             :{'func': lambda p: 0},


Dimensions = { 
    'scalar': ['phinull', 'N', 'employmentAGG', 'w0', 'W',
               'alpha', 'a0', 'Nprod', 'Phillips', 
               'n'],
    'matrix': [],
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Ntechno'],
      'matrix':['Ntechno','Ntechno']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)
"""
_PRESETS={}