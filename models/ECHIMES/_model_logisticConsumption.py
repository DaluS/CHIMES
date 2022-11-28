"""
Consumption dynamics for a logistic distribution

"""

from pygemmes._models import Funcs, importmodel,mergemodel
import numpy as np

# ######################## OPERATORS ####################################
'''
Those are operators that can be used to do multisectoral operations : 
coupling, transposition, sums... 
'''
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
# ##########################################################################

_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'differential': {
        'H': {
            'func': lambda H, deltah, rho, C: C - deltah * H - matmul(rho, H),
            'com': 'explicit stock-flow',
            'definition': 'Possessions',
            'units': 'units',
            'size': ['Nprod'],
            'initial': 1,
        },
    },
    'statevar':{
        'Hid': {
            'func': lambda N,hid0,Omega,Omega0,x: N*hid0/(1+np.exp(-x*(Omega/Omega0-1))),
            'definition': 'Ideal goods for purchasing power',
            'com':'deduced from Omega',
            'size': ['Nprod'],
        },
        'HidAGG': { 'func': lambda Hid,p: sprod(Hid,p) ,
                   'definition': 'nominal household expected possessions',
                    'units': '$',
        },
        'C': {
            'func': lambda f, Hid,rho,H: f*(Hid-H)+matmul(rho,H),
            'com': 'consumption as relaxation',
            'definition': 'flux of goods for household',
            'size': ['Nprod'],
        'Omega': {
            'func': lambda N, W, p, basket: (W / N) / (sprod(basket, p)),
            'definition': 'MONOSECTORAL Percieved purchasing power',
            'com': 'no shareholding, no bank possession',
            'units': 'Units.Humans^{-1}.y^{-1}'
        },
    },
    'parameter': {
        'rho': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
        'Omega0': {'value': 1,
                   'size': ['Nprod']
                   },
        'x': {'value': 1,
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
    },
}