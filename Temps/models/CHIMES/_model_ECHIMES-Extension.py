'''ECHIMES: adding extensions on the core'''

##########################################################################
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions#
from pygemmes._models import Operators as O                              #
import numpy as np                                                       #
##########################################################################

# IMPORTATION OF ECHIMES 
_LOGICS,_PRESETS,_SUPPLEMENTS,_DESCRIPTION= importmodel('ECHIMES')

#_LOGICSAGG,_PRESETSAGG= importmodel('MultisectoralAggregates')          ### ADDING AUXILLIARY AGGREGATES
#_LOGICSACCES,_PRESETACCES = importmodel('Accessibility')                   ### ADDING ACCESSIBILITY
#_LOGICSEXCHANGE, _PRESETEXCHANGE = importmodel('InternationalExchange') ### ADDING INTERNATIONAL EXCHANGE

# KAPPA-PHILLIPS #################
#_LOGICS['statevar']['kappa'] = {'func': lambda pi, k0, k1, k2: k0 + k1 * np.exp(k2 * pi),
#                                'com': 'exponential param curve'},
#_LOGICS['statevar']['Phillips'] = {'func': lambda employmentAGG, phi0, phi1: -phi0 + phi1 / (1 - employmentAGG) ** 2},

# TRANSFORMING INTO GOODWIN-KEEN #
#_LOGICS['statevar']['Cpond']= {'func': lambda kappa,Gamma,nu,delta,omega: (1-kappa-Gamma-delta*nu)/omega},

# ADDING UTILITY CONSUMPTION #####


# ADDING ACCESSIBILITY ###########
#_LOGICS_ACC,_PRESETS0,_SUPPLEMENTSACC= importmodel('Accessibility')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_ACC, verb=False) 

# ADDING CES #####################
#_LOGICS_CES,_PRESETS0,_SUPPLEMENTSCES= importmodel('CESprod')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_CES, verb=False) 

# CHANGING INFLATION #############
#_LOGICS_INF,_PRESETS0= importmodel('inflationU')
#_LOGICS = mergemodel(_LOGICS, _LOGICS_INF, verb=False)

#########################################################################
'''
Dimensions = { 
    'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W',
               'alpha', 'Nprod', 'Phillips', 'rDh', 'gammai',
               'n', 'ibasket', 'Dh'],
    'matrix': [ 'Gamma','Xi','Mgamma','Mxi','Minter',
                'Minvest','MtransactY','MtransactI']
    #'vector': will be deduced by filldimensions 
}
DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
_LOGICS=filldimensions(_LOGICS,Dimensions,DIM)
'''