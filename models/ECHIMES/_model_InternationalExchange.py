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
def transpose(X):
    '''Transposition of X :
    Y=transpose(X)  Y_ij=X_ji'''
    return np.moveaxis(X, -1, -2)
def matmul(M,V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M,V)
def distXY(x,y):
    '''x and y vector of position, z=distXY(x,y) is the matrix of distance
     between each particle of position x,y :
     z_ij= \sqrt{ (x_i-x_j)^2 + (y_i-y_j)^2}'''
    return np.sqrt((x - transpose(x)) ** 2 + (y - transpose(y)) ** 2)
def Identity(X):
    '''generate an identity matrix of the same size a matrix X'''
    return np.eye(np.shape(X)[-1])
#################################################################################

def dotDinternational( MtransactI, MtransactY, wL, rD, pC):
    return rD \
         + wL -pC \
         + ssum2(MtransactI - transpose(MtransactI)) \
         + ssum2(MtransactY - transpose(MtransactY))
def dotVinternational( Y, Gamma, Ir, C, Xi):
    return Y \
         - matmul(transpose(Gamma), Y) \
         - C \
         - matmul(transpose(Xi), Ir)

_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },

    'differential': {
        'ExchangeRate': {
            'func': lambda p:0,
            'size':['nr'],
            'initial':1,
        },
        'PhysicalExchanges': {
            'func': lambda p,pInter,chiM,sigmaRQ, PhysicalExchanges:  PhysicalExchanges*np.log(p/pInter)*chiM*sigmaRQ,
            'com':'',
            'units':'Units.y^{-1}',
            'size': ['nr','Nprod'],
            'initial':0,
        },
    },
    'statevar': {
        'Excedent': {
            'func': lambda PhysicalExchanges,p:0,
        },
        'dotV': {
            'func': dotVinternational,
            'com': 'Added international',
        },
        'dotD': {
            'func': dotDinternational,
            'com': 'Added international'
        },
        'pInter': {
            'func': lambda p,ExchangeRate : 0,
            'com': 'No taxes',
            'definition': 'p_{qi} price of good i from region q',
            'size':['nr','Nprod']
        },
    },
    'parameter':{
        'sigmaRQ': {
            'value':1,
        },
        'chiM': {
            'value':1,
        },
    },
}

_PRESETS={}