'''
Adding accessibility into the system
'''

from pygemmes._models import Funcs, importmodel,mergemodel
import numpy as np

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


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'statevar': {
        ### ACCESSIBILITY
        'AcY': {
            'func': lambda V,Gamma,kY,softmin :  1-np.exp(-kY*V/(Gamma+0.0001)),
            #'func': lambda V,Gamma,kY,softmin :  ssum2(1-np.exp(-kY*V/(Gamma+0.0001)**(-softmin) ))**(-1/softmin),
            'com': 'Softmin with Gamma',
            'definition': 'Accessibility to intermediate production',
            'symbol': r'$\mathcal{A}^Y',
            'size': ['Nprod']
        },
        'AcI': {
            'func': lambda V,Xi,kI,softmin : 1-np.exp(-kI*V/(Xi+0.0001)),
            #'func': lambda V,Xi,kI,softmin : ssum2( 1-np.exp(-kI*V/(Xi+0.0001))**(-softmin) )**(-1/softmin),
            'com': 'Softmin with Xi',
            'definition': 'Accessibility to Investment',
            'symbol': r'$\mathcal{A}^Y',
            'size': ['Nprod']
        },
        'AcC': {
            'func': lambda V,Gamma,kC,softmin : 1-np.exp(-kC*V),
            'com': 'Softmin',
            'definition': 'Accessibility to consumption',
            'symbol': r'$\mathcal{A}^Y',
            'size': ['Nprod']
        },
        ### USE AND ACCESSIBILITY
        'u': {'func': lambda u0,AcY,softmin: AcY,
              #(u0**(-softmin)+AcY**(-softmin))**(-1/softmin),
              'com': 'for the moment only voluntary limitation',
              'definition': 'Effective use of capital',
              'size': ['Nprod']},

        ### CONSUMPTION
        'C': {
            'func': lambda W, Cpond, p,AcC: AcC*Cpond * W / p,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },

        ### INVESTMENT
        'I': {
            'func': lambda p, Y, kappa, Mxi,AcI: AcI * p * Y * (kappa + ssum2(Mxi)),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
    },
    'parameter':{
        'kC': {'value':10,
               'definition': 'accessibility to consumption'},
        'kI': {'value': 10,
               'definition': 'accessibility to consumption'},
        'kY': {'value': 10,
               'definition': 'accessibility to consumption'},
        'softmin': {'value':100},
        'Gamma': {'value':0.01,
                  'size':['Nprod','Nprod']},
        'Xi': {'value':0.01,
                  'size':['Nprod','Nprod']},
        'u0': {'value':1}
    },
}

_PRESETS={}