'''
State variables, monosectoral, calculated on a productive multisectoral
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


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'statevar': {
        'pAGG': { 'func': lambda p,basket: sprod(p,basket),
                  'definition': 'price deflator',
                  'units': '',
                  'symbol': r'$p_{\bigcirc}$'
        },
        'GDPnomY': { 'func': lambda p,Gamma,Y: sprod(p,Y-matmul(transpose(Gamma),Y)),
                     'com': 'calculated on Y',
                     'definition': 'nominal expected GDP',
                     'symbol': r'$Y^{NY}_{\bigcirc}$',
                     'units': '$.y^{-1}'
        },
        'GDPnom2': {'func': lambda C,p,I,c,dotV: sprod(C,p)+ssum(I)+sprod(c,dotV),
                    'com': 'calculated on C+I+cdotV',
                    'definition': 'Inventory accountability nominal GDP',
                    'symbol': r'$Y^{NV}_{\bigcirc}$',
                    'units': '$.y^{-1}'
                    },
        'GDP': { 'func': lambda GDPnomY,pAGG: GDPnomY/pAGG ,
                 'com': 'GDP on production deflated',
                 'definition': 'deflated expected GDP',
                 'symbol': r'$Y_{\bigcirc}$',
                 'units': 'y^{-1}'
        },
        'CAGG': { 'func': lambda p,C: sprod(p,C) ,
                  'com': 'Nominal consumption',
                  'symbol': r'$C_{\bigcirc}$',
                  'units': '$.y^{-1}',
        },
        'IAGG': { 'func': lambda I: ssum(I) ,
                  'com' : 'nominal investment',
                  'symbol': r'$I_{\bigcirc}$',
                  'units': '$.y^{-1}',
        },
        'VAGG': {'func': lambda V,c: sprod(V,c),
                 'com': 'nominal inventory',
                 'symbol': r'$V_{\bigcirc}$',
                 'units': '$.y^{-1}',
                 },
        'KAGGpass': { 'func': lambda Xi,p,K: sprod(matmul(Xi,p),K) ,
                      'com': 'capital value on its creation',
                      'definition': 'nominal passive capital value',
                      'symbol': r'$K^{\Xi}_{\bigcirc}$',
                      'units': '$',
        },
        'LAGG': { 'func': lambda L: ssum(L) ,
                  'definition': 'total workers',
                  'symbol': r'$L_{\bigcirc}$',
                  'units': 'Humans'
        },
        'aAGG': { 'func': lambda GDP,LAGG: GDP/LAGG,
                  'definition': 'aggregated productivity',
                  'symbol': r'$a_{\bigcirc}$',
                  'units': 'Humans^{-1}.y^{-1}'
        },
        'DAGG': {'func': lambda D: ssum(D),
                 'definition': 'sum of private debt',
                 'symbol': r'$D_{\bigcirc}$',
                 'units': '$'
                 },
        'omegaAGG': { 'func': lambda w,L,z,GDPnomY: sprod(w*z,L)/GDPnomY  ,
                      'definition': 'aggregated wage share',
                      'symbol': r'$\omega_{\bigcirc}$',
                       'units': ''
        },
        'uAGG': { 'func': lambda u,K,b,nu : sprod(u,K*b/nu)/sprod(K,b/nu),
                  'definition': 'agregated use rate of capital',
                    'symbol': r'$u_{\bigcirc}$',
                       'units': ''
        },
        'nuAGG': { 'func': lambda KAGGpass,GDPnomY: KAGGpass/GDPnomY ,
                   'com': 'On active capital',
                   'definition': 'agregated return on capital',
                    'symbol': r'$\nu_{\bigcirc}$',
                       'units': 'y'
        },
        'deltaAGG': { 'func': lambda delta,Xi,p,K, KAGGpass: sprod(delta,matmul(Xi,p)*K)/KAGGpass ,
                      'definition': 'agregated capital degradation rate',
                    'symbol': r'$\delta_{\bigcirc}$',
                       'units': 'y^{-1}'
        },
        'dAGG': { 'func': lambda D,GDPnomY: ssum(D)/GDPnomY ,
                  'com': 'on YGDP',
                  'definition': 'relative agregated debt',
                  'symbol': r'$d_{\bigcirc}$',
                  'units': 'y'
        },
        'rdAGG': {'func': lambda r,D, GDPnomY: r*ssum(D) / GDPnomY,
                 'com': 'on YGDP',
                 'definition': 'relative private debt weight',
                 'symbol': r'$d_{\bigcirc}$',
                 'units': ''
                 },
        'gammaAGG': { 'func': lambda p,Gamma,Y : sprod(p,matmul(transpose(Gamma),Y))/sprod(p,Y),
                      'definition': 'agregated part of intermediary consumption',
                      'symbol': r'$\gamma_{\bigcirc}$',
                      'units': ''
        },
        'XiAGG': { 'func': lambda p,nu,delta,b,Xi,Y: sprod(p ,matmul(transpose(Xi),Y)*nu*delta/b)/sprod(p ,Y*nu*delta/b) ,
                   'definition': 'agregated relative size of capital',
                    'symbol': r'$\Xi_{\bigcirc}$',
                    'units': ''
        },
        'xiAGG': { 'func': lambda deltaAGG,nuAGG,XiAGG : deltaAGG*nuAGG*XiAGG,
                   'definition': 'aggregated relative weight of capital destruction',
                    'symbol': r'$\xi_{\bigcirc}$',
                    'units': ''
        },
        'piAGG': { 'func': lambda omegaAGG,gammaAGG,xiAGG,r,dAGG: 1-omegaAGG-gammaAGG-xiAGG-r*dAGG,
                   'definition': 'aggregated relative profit',
                   'com': 'on expected',
                   'symbol': r'$\pi_{\bigcirc}$',
                   'units': ''
        },
        'ROCAGG': {'func': lambda piAGG,nuAGG, XiAGG : piAGG/(nuAGG*XiAGG) ,
                  'definition': 'aggregated relative profit',
                  'com': 'on expected',
                  'symbol': r'$\pi_{\bigcirc}$',
                  'units': ''
                  },
        'cAGG': { 'func': lambda omegaAGG,gammaAGG,xiAGG, pAGG : (omegaAGG+gammaAGG+xiAGG)* pAGG ,
                  'definition': 'aggregated relative cost',
                  'symbol': r'$c_{\bigcirc}$',
                  'units': '$'
        },
    },
}

_PRESETS={}