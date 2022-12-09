'''

Extensions for international trades, applied to ECHIMES
'''
from pygemmes._models import Funcs, importmodel,mergemodel
import numpy as np

##################################################################################
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
def ssumR(X):
    return np.sum(X,axis=-2)[...,np.newaxis]
def transpose(X):
    '''Transposition of X :
    Y=transpose(X)  Y_ij=X_ji'''
    return np.moveaxis(X, -1, -2)
def transposeR(X):
    '''Transposition of X :
    Y=transpose(X)  Y_ijk=X_jik'''
    return np.moveaxis(X, -2, -3)

def Identity(X):
    '''generate an identity matrix of the same size a matrix X'''
    return np.eye(np.shape(X)[-1])
def matmul(M,V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M,V)
def distXY(x,y):
    '''x and y vector of position, z=distXY(x,y) is the matrix of distance
     between each particle of position x,y :
     z_ij= \sqrt{ (x_i-x_j)^2 + (y_i-y_j)^2}'''
    return np.sqrt((x - transpose(x)) ** 2 + (y - transpose(y)) ** 2)
#################################################################################

def dotDinternational( MtransactI, MtransactY, wL, rD, pC,MonetaryExchanges):
    return rD \
         + wL -pC \
         + ssum2(MtransactI - transpose(MtransactI)) \
         + ssum2(MtransactY - transpose(MtransactY)) \
         + ssumR(MonetaryExchanges - transpose(MonetaryExchanges))
def dotVinternational( Y, Gamma, Ir, C, Xi,PhysicalExchanges):
    return Y \
         - matmul(transpose(Gamma), Y) \
         - C \
         - matmul(transpose(Xi), Ir) \
         + ssumR(transposeR(PhysicalExchanges)) \
         - ssumR(PhysicalExchanges)

def phyfunc(p,pInter,chiM,sigmaRQ, PhysicalExchanges):
    return PhysicalExchanges*np.log(p/pInter)*chiM*sigmaRQ

 
_LOGICS = {
    'size': {'Nprod': {'list': ['MONO'],},},
    'differential': {
        'ExchangeRate': {
            'func': lambda Excedent,Mass,chiM,ExchangeRate:ExchangeRate*chiM*(transposeR(Excedent/Mass)-Excedent/Mass),
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
            'func': lambda p,ExchangeRate :transposeR(p),
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