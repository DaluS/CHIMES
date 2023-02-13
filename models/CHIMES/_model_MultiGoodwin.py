'''Minimal SFC model of a multisectoral structure'''

_DESCRIPTION = '''

Stock-flow consistent model with two coupling matrices between sectors.
There is as little behavior as possible : 
    * Price are fixed 
    * Profits are reinvested
    * Wage are fully going into consumption 
    * Wage are evolving with a Philips curve 

There is no market clearing, there is debt variation, there is no price adjustment.
'''

from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O
import numpy as np

def dotD( MtransactI, MtransactY, w,L, r,D, p,C):#,Shareholding):
    return r*D \
         + w*L -p*C \
         + O.ssum2(MtransactI - O.transpose(MtransactI)) \
         + O.ssum2(MtransactY - O.transpose(MtransactY)) # - Shareholding

def dotV(Y, Gamma, Ir, C, Xi):
    return  Y - O.matmul(O.transpose(Gamma), Y) - C - O.matmul(O.transpose(Xi), Ir)

_LOGICS = {
    'size': {'Nprod': {'list': ['MONO']}},
    ###################################################################
    'differential': {
        ### MONETARY STOCK-FLOW CONSISTENCY
        'D'             :{'func': lambda dotD : dotD},                  
        'Dh'            :{'func': lambda W, p, C: -W + O.sprod(p, C)},  

        ### PHYSICAL STOCK-FLOW CONSISTENCY
        'V'             :{'func': lambda dotV: dotV},
        'K'             :{'func': lambda Ir, delta, K: Ir - delta * K},

        ### PRICES AND WAGES 
        'w0'            :{'func': lambda Phillips, w0: w0*Phillips},
        'p'             :{'func': lambda p: 0},

        ### EXOGENOUS SCALING
        'a0'            :{'func': lambda a0, alpha: a0 * alpha,
                          'definition': 'Capital unit per worker'},
        'N'             :{'func': lambda N, n: N * n},
    },

    'statevar': {
        ### BY-SECTOR PRODUCTIVITY AND WAGE
        'w'             :{'func': lambda w0,z: w0*z,},
        'a'             :{'func': lambda a0,apond : a0*apond},

        ### PRODUCTION 
        'Y'             :{'func': lambda nu, K: K / nu,},
        'L'             :{'func': lambda K,a : K/a},

        ### Physical Fluxes
        'Y'             :{'func': lambda u,nu, K: u*K / nu,},
        'Pi'            :{'func': lambda p,Y,Gamma,nu,delta,Xi,w,L: p*Y-Y*O.matmul(Gamma,p)-Y*nu*delta*O.matmul(Xi,p)- w*L},

        'Idelta'        :{'func': lambda Y,nu,delta,Xi,p: Y*nu*delta*O.matmul(Xi,p)},
        'I'             :{'func': lambda Pi,Idelta: Pi+ Idelta},
        'Ir'            :{'func': lambda I,Xi,p: I/O.matmul(Xi,p),},

        'C'             :{'func': lambda W,Cpond,p: Cpond*W/p,},

        'MtransactY'    :{'func': lambda p, Y, Gamma: Y * Gamma * O.transpose(p)},
        'MtransactI'    :{'func': lambda I, Xi, p: I * Xi * O.transpose(p) / (O.matmul(Xi, p))},
        'dotV'          :{'func': dotV},
        'dotD'          :{'func': dotD},

        ### Consumption 
        'employment'    :{'func': lambda L,N        : L/N},
        'employmentAGG' :{'func': lambda employment: O.ssum(employment),},
        'Phillips'      :{'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG,
                          'com': 'LINEAR',},
        'W'             :{'func': lambda w, L, r, Dh, : O.sprod(w, L)  - r * Dh}, #+ O.ssum(Shareholding)

        ### CHECKS
        'pi'            :{'func': lambda Pi,p,Y: Pi/(p*Y)},
        'omega'         :{'func': lambda w,L,p,Y: w*L/(p*Y)},
        'd'             :{'func': lambda D,p,Y : D/(p*Y)},

    },
    'parameter': {
        'apond' :   { 'value' : 1,
                      'definition': 'sector-ponderation of production'},
        'wpond' :   { 'value' : 1,
                      'definition': 'sector-ponderation of wage'}

    }
}

Dimensions = { 
    'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W',
               'alpha', 'a0', 'Nprod', 'Phillips', 'rDh', 'gammai',
               'n', 'ibasket', 'Dh'],
    'matrix': [ 'Gamma','Xi','Mgamma','Mxi','Minter',
                'Minvest','MtransactY','MtransactI']
    #'vector': will be deduced by filldimensions 
}

DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)


