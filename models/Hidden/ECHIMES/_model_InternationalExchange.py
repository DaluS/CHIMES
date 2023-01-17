'''Extensions for international trades, applied to ECHIMES'''

_DESCRIPTION = ''' '''
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O
import numpy as np


def dotDinternational( MtransactI, MtransactY, wL, rD, pC,MonetaryExchanges):
    return rD \
         + wL -pC \
         + O.ssum2(MtransactI - O.transpose(MtransactI)) \
         + O.ssum2(MtransactY - O.transpose(MtransactY)) \
         + O.ssumR(MonetaryExchanges - O.transpose(MonetaryExchanges))
def dotVinternational( Y, Gamma, Ir, C, Xi,PhysicalExchanges):
    return Y \
         - O.matmul(O.transpose(Gamma), Y) \
         - C \
         - O.matmul(O.transpose(Xi), Ir) \
         + O.ssumR(O.transposeR(PhysicalExchanges)) \
         - O.ssumR(PhysicalExchanges)

def phyfunc(p,pInter,chiM,sigmaRQ, PhysicalExchanges):
    return PhysicalExchanges*np.log(p/pInter)*chiM*sigmaRQ

 
_LOGICS = {
    'size': {'Nprod': {'list': ['MONO'],},},
    'differential': {
        'ExchangeRate': {
            'func': lambda Excedent,Mass,chiM,ExchangeRate:ExchangeRate*chiM*(O.transposeR(Excedent/Mass)-Excedent/Mass),
            'size':['nr'],
            'initial':1,
        },
        'PhysicalExchanges': {
            'func': phyfunc,
            'com':'log-price dynamics',
            'definition': 'X_{rqi} Exchange of item i From R to Q',
            'units':'Units.y^{-1}',
            'size': ['nr','Nprod'],
            'initial':0,
        },
    },
    'statevar': {
        'Excedent': {
            'func': lambda MonetaryExchanges: 0,
            'definition':'Commercial excedent in region'},
        'MonetaryExchanges': {
            'func': lambda PhysicalExchanges,p: 0,
            'definition': 'Money associated to the physical exchange',
            'com': 'conversion from physical',
            'size': ['nr','Nprod'],
        },
        'dotV': {
            'func': dotVinternational,
            'com': 'Added international',
            'size': ['Nprod'],
        },
        'dotD': {
            'func': dotDinternational,
            'com': 'Added international',
            'size': ['Nprod'],
        },
        'pInter': {
            'func': lambda p,ExchangeRate :O.transposeR(p),
            'com': 'No taxes',
            'definition': 'p_{rqi} price in region r of good i from region q',
            'size':['nr','Nprod']
        },
    },
    'parameter':{
        'sigmaRQ':      {'value': 1},
        'chiM':         {'value': 1},
        'Mass':         {'value': 1},
        'Y':            {'value': 0,'size':['Nprod'],},
        'I':            {'value': 0,'size': ['Nprod'],},
        'Ir':           {'value': 0,'size': ['Nprod'],},
        'C':            {'value': 0,'size': ['Nprod'],},
        'V':            {'value': 10,'size': ['Nprod'],},
        'Gamma':        {'value': 0,'size': ['Nprod','Nprod']},
        'Xi':           {'value': 0,'size': ['Nprod','Nprod']},
        'MtransactI':   {'value': 0,'size': ['Nprod','Nprod']},
        'MtransactY':   {'value': 0,'size': ['Nprod', 'Nprod']},
        'p':            {'value': 1,'size': ['Nprod']}
    },
}

NR = ['Region1','Region2']
Nprod = ['sY','sI','sC']
exR = np.zeros((1,2,2,1))
exR[0,:,:,0]=[[1,1/2],[2,1]]
physeX = np.zeros((1,2,2,3))+1


_PRESETS={
    '3by2': {
        'fields': {'dt':1,
                   'Tmax':20,
                   'nr': ['Region1','Region2'],
                   'Nprod':['sY','sI','sC'],
                   'p':1,
                   'ExchangeRate': exR,
                   'PhysicalExchanges': physeX,
                   },
        'com': ('Check of the structure working as intended'),
        'plots': {},
    },
}