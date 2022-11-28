# -*- coding: utf-8 -*-
"""
CORE for HOLISTIC INTERDISCIPLINARY MODEL assessing ECOLOGICAL SUSTAINABILITY

The goal of CHIMES is :
    * description of production with physical variables
    * behavior of agents (price, investment) based on economic values
    * Connexion to ecological systems through physical coupling (emissions, land use...)

It integrates :
    * N productive sector, by activity
    * Material flow analysis integrated inside
    * Loans dynamics for investment and cross-sector expanses
    * Inventory fluctuations
    * Inflation
    * Adaptive use of capital

WE ARE STILL ON A DUMMY CONSUMPTION THEORY
IF YOU WANT A LIGHT VERSION, OPEN THE MODEL FILE AND CHANGE __AUXIN and __AGGIN

More infos : https://www.overleaf.com/read/vywvyymcqwwk

CHIMES :
"""

# ######################## PRELIMINARY ELEMENTS #########################
__AUXIN = True # Add auxilliary variables
__AGGIN = True # Add Agregated variables
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

def Debtvariation(r,D,w,L,z,p,C,MtransactY,MtransactI):
    debt = r*D \
        +w*z*L \
        -p*C \
        +ssum2(MtransactY) \
        -ssum2(transpose(MtransactY)) \
        +ssum2(MtransactI) \
        -ssum2(transpose(MtransactI))
    return debt


# ######################## LOGICS ######################################
_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'differential': {
        'K': {
            'func': lambda Ir,delta,u,K: Ir-delta*u*K,
            'com': 'depreciation proportional to u',
            'definition': 'Productive capital in physical units',
            'units': 'units',
            'size': ['Nprod'],
            'initial': 2.7,
        },
        'D': {
            'func': lambda dotD:dotD,
            'com': 'no shareholding',
            'definition': 'Debt of local sector',
            'units': '$',
            'size': ['Nprod'],
        },
        'Dh': {
            'func': lambda W,p,C: -W+sprod(p,C),
            'com': '',
            'definition': 'debt of households',
            'units': '$',
            'symbol':r'$D_{household}$'
        },
        'u': {
            #'func': lambda u: 0,
            'func': lambda u,sigma,V,dotV: -sigma*(1-u)*dotV/V,
            'com': 'hardcapped at 1',
            'definition': 'use of productive capital',
            'units': '',
            'size': ['Nprod'],
            'initial':1,
        },
        'p': {
            'func': lambda p,inflation: p*inflation,
            'com': 'log on markup',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },
        'V': {
            'func': lambda dotV : dotV,
            'com': 'dynamics in dotV',
            'size': ['Nprod'],
            'units': 'units',
            'symbol': '$V$'
        },
        'w': {'func': lambda philips, w, gammai, ibasket: w * (philips + gammai * ibasket),
              'com': 'exogenous',
              },
        'a': {'func': lambda a, alpha : a*alpha,
              'com': 'exogenous',
             },
        'N': {'func': lambda N, n : N*n,
              'com': 'exogenous',
             },
    },
    'statevar': {
        ### price,profit,inflation ###
        'c': {
            'func': lambda omega,gamma,xi,p : p*( omega + gamma + xi),
            'com':'explicit form',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },
        'inflation': {
            # 'func': lambda inflationMarkup,inflationdotV: inflationMarkup+inflationdotV,
            # 'com': 'sum of inflation contributions',
            'func': lambda p, eta, mu0, c, chi, dotV, V: eta * np.log(mu0 * c / p) - chi * dotV / V,
            'com': 'costpush and inventoryvariation',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i$'
        },
        'ibasket': {
            'func': lambda inflation,basket : sprod(inflation,basket),
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
            'units': 'y^{-1}',
            'symbol': r'$i_{Basket}$',
        },
        'basket': {
            'func': lambda p,C: p*C/sprod(p,C),
            'com': 'cannot be non-auxilliary',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
            'units': '',
        },

        ### Purchasing power
        'W': {
            'func': lambda w,z,L,r,Dh: sprod(w*z,L)-r*Dh,
            'definition': 'Total income of household',
            'com': 'no shareholding, no bank possession',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'
        },
        'Omega': {
            'func': lambda N,W,p,basket: (W/N)/(sprod(basket,p)) ,
            'definition': 'MONOSECTORAL Percieved purchasing power',
            'com': 'no shareholding, no bank possession',
            'units':'Units.Humans^{-1}.y^{-1}'
        },
        'L': {
            'func': lambda a,b,Y: Y/(a*(2-b)),
            'com': 'instant recruitment on leontiev',
            'size': ['Nprod'],
        },
        'employment': {
            'func': lambda L,N: ssum(L)/N,
            'com': 'Calculation with L',
            'units': '',
            'symbol': r'$\Lambda$'
        },
        'philips':  {
            'func': lambda employment, phi0, phi1: -phi0 + phi1 / (1 - employment)**2,
            'com': 'diverging (force omega \leq 1)',
            'units': 'y^{-1}',
            'symbol': r'$\Phi(\lambda)$',
        },

        ### Physical fluxes ################
        'dotV': {
            'func': lambda Y, Gamma, Ir, C, Xi: Y - matmul(transpose(Gamma), Y) - C - matmul(transpose(Xi), Ir),
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$\dot{V}$'
        },
        'Y': {
            'func': lambda K,u,b,nu: u*K*b/nu,
            'com': 'Leontiev with variable use',
            'size': ['Nprod'],
            'units': 'Units.y^{-1}',
        },
        'Ir': {
            'func': lambda I,Xi,p: I/matmul(Xi,p),
            'com': 'deduced from monetary investment',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },
        'C': {
            'func': lambda W,Cpond,p: Cpond*W/p,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },

        ### Explicit monetary flux ###########
        'dotD': {
            'func': Debtvariation,
            'definition': 'debt variation',
            'com': '',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': "$\dot{D}$",
        },
        'I': {
            'func': lambda p,Y,kappa,xi: p*Y*(kappa+xi),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'MtransactY': {
            'func': lambda p, Y, Gamma: Y * Gamma * transpose(p),
            'definition': 'Money from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^Y$'
        },
        'MtransactI': {
            'func': lambda I, Xi, p: I * Xi * transpose(p) / (matmul(Xi, p)),
            'definition': 'Money from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^I$'
        },
        'checksumI': {
            'func' : lambda MtransactI, I : I - ssum2(MtransactI),
            'definition' : 'should be zero',
            'size': ['Nprod'],
        },

        ### investment curve
        'kappa': {
            'func': lambda pi,k0: k0*pi,
            'com': 'LINEAR KAPPA FUNCTION',
            'units': '',
            'size': ['Nprod'],
        },

        ### Non-dimensional statevar
        'gamma': {
            'func': lambda Gamma,p: matmul(Gamma,p)/p,
            'definition': 'share of intermediary consumption',
            'com': 'raw definition',
            'units': '',
            'symbol': r'$\gamma$',
            'size': ['Nprod'],
        },
        'omega': {
            'func': lambda a,b,w,p,z: z*b*w/(p*a*(2-b)),
            'com': 'raw def',
            'units': '',
            'size': ['Nprod'],
        },
        'xi': {
            'func': lambda delta, nu, b, p, Xi: (delta * nu / b) * matmul(Xi, p) / p,
            'definition': 'relative capex weight',
            'com': 'explicit calculation',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\xi$',
        },
        'pi': {
            'func': lambda omega, gamma, xi, r, D, p, Y: 1 - omega - gamma - xi - r * D / (p * Y),
            'com': 'explicit form',
            'size': ['Nprod'],
            'units': '',
        },
    },
    'parameter': {
        ### SCALARS
        'alpha'  :{'value': 0.02,},
        'n'      :{'value': 0.025,},
        'phinull':{'value': 0.1,},
        'r'      :{'value': 0.03, },

        ### VECTORS
        'z': {'value':1,
              'definition': 'local wage ponderation',
              'size': ['Nprod']
              },
        'Cpond': {'value': .5,
              'definition': 'part of salary into consumption of the product',
              'size': ['Nprod']
              },
        'mu0': {'value': 1.3,
              'definition': '',
              'size': ['Nprod']
              },
        'delta': {'value': 0.005,
                  'size': ['Nprod']
                  },
        'deltah': {'value': 0.1,
                  'size': ['Nprod']
                  },
        'sigma': {'value': 1,
                  'size': ['Nprod']
                  },
        'gammai': {'value': 1,
                  },
        'eta': {'value': 0.5,
               'size': ['Nprod']
               },
        'chi': {'value': 1,
               'size': ['Nprod']
               },
        'b': {'value': 0.5,
              'size': ['Nprod']
              },
        'nu': {'value': 3,
               'size': ['Nprod']
               },

        ### MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod'],
            'units':'',
        },
        'Xi': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
        'rho': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
    },
}

"""Not used in the dynamics but can be useful to check"""
_LOGICS_AUX = {
    'size': {
    },
    'differential': {
        'H': {
            'func': lambda H, deltah, rho, C: C - deltah * H - matmul(rho, H),
            'com': 'explicit stock-flow',
            'definition': 'Possessions',
            'units': 'units',
            'size': ['Nprod'],
            'initial':1,
        },
    },
    'statevar': {
        'inflationMarkup': {
            'func': lambda p, eta, mu0, c,: eta * np.log(mu0 * c / p),
            'com': 'log on markup',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i^{\mu}$'
        },
        'inflationdotV': {
            'func': lambda chi, dotV, V: - chi * dotV / V,
            'com': 'price adjustment to demand-offer',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i^{\dot{V}}$'
        },


        ### PROFITS
        'Pi': {
            'func' : lambda Y,p,pi : Y*p*pi,
            'com': 'from pi',
            'definition': 'expected Profit',
            'symbol': '$\Pi^{e}$',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'PiInstant': {
            'func': lambda Pi, dotV,c,p: Pi+(c-p)*dotV,
            'com': 'Pi+(c-p)\dot{V}',
            'definition': 'Profit corrected by inventory change',
            'symbol': '$\Pi^{inst}$',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'piInstant': {
            'func': lambda PiInstant,p,Y: PiInstant/(p*Y),
            'com': 'from PiInstant',
            'definition': 'instant relative profit',
            'symbol': '$\pi^{inst}$',
            'units': '',
            'size': ['Nprod'],
        },
        'Iaccontability':{
            'func': lambda I,p,Y,xi,c,dotV: I-p*Y*xi+c*dotV,
            'com': 'corrected I',
            #'definition': 'productive investment '
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': 'I^{acc}'
        },

        ### MONETARY FLUXES
        'TakenbyI': {
            'func': lambda Ir, Xi: matmul(transpose(Xi), Ir),
            'definition': 'physical flux removed through investment',
            'com': 'definition',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$(\Xi^T I^r)$'
        },
        'TakenbyY': {
            'func': lambda Y, Gamma: matmul(transpose(Gamma), Y),
            'definition': 'physical flux removed through intermediary consumption',
            'com': 'definition',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$(\Gamma^T Y)$'
        },
        'pY': {
            'func': lambda p, Y: p * Y,
            'definition': 'Brut nominal output',
            'com': '',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': "$(pY)$",
        },
        'TransactI': {
            'func': lambda MtransactI: ssum2(MtransactI)-ssum2(transpose(MtransactI)),
            'definition': 'Net money flux from investment',
            'com': 'component of dotD',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': '$\sum_j (\mathcal{T}^I_{ij}-\mathcal{T}^I_{ji})$'
        },
        'TransactInter': {
            'func': lambda MtransactY: ssum2(MtransactY)-ssum2(transpose(MtransactY)),
            'definition': 'Net money flux from intermediary consumption',
            'com': 'component of dotD',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': '$\sum_j (\mathcal{T}^Y_{ij}-\mathcal{T}^Y_{ji})$'
        },
        'Consumption': {
            'func': lambda p, C: -p * C,
            'definition': 'Consumption in monetary value',
            'com': 'Just to check',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'Interests': {
            'func': lambda r, D: r * D,
            'definition': 'interest volume',
            'com': 'Just to check',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': '$(rD)$',
        },
        'Wage': {
            'func': lambda w, z, L: w * z * L,
            'definition': 'local salaries',
            'com': 'Just to check',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol': "$(wzL)$",
        },


        ### NON-DIMENSIONAL QUANTITIES
        'employmentlocal': {
            'func': lambda L, N: L / N,
            'com': 'raw def',
            'definition': 'part of population working in sector',
            'size': ['Nprod'],
            'symbol': '$\lambda$',
            'units': '',
        },
        'growthK': {
            'func': lambda Ir, delta, u, K: Ir / K - u * delta,
            'definition': 'growth rate of capital',
            'com': 'no u variation',
            'units': 'y^{-1}',
            'size': ['Nprod'],
            'symbol': '$g^K$'
        },
        'reldotv': {
            'func': lambda dotV, Y, p, c: (c - p) * dotV / (p * Y),
            'com': 'calculated as inventorycost on production',
            'definition': 'relative budget weight of inventory change',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\dot{v}$',
        },
        'reloverinvest': {
            'func': lambda kappa, pi: pi - kappa,
            'com': 'difference between kappa and pi',
            'units': '',
            'symbol': r'$(\kappa-\pi)$',
            'size': ['Nprod'],
            'definition': 'relative overinstment of the budget',
        },
        'rd': {
            'func': lambda r, D, p, Y: r * D / (p * Y),
            'com': 'deduced from D',
            'definition': 'relative weight debt',
            'units': '',
            'size': ['Nprod'],
        },

        ### EQUITIES
        'Equity': {
            'func': lambda K,p,c,V,D,Xi: sprod(K,matmul(Xi,p))+sprod(c,V)-D,
            'definition' : 'per sector equity',
            'units': '$',
            'size': ['Nprod'],
        },
        'EquityHousehold': {
            'func': lambda H,p,Dh: sprod(H,p)+Dh,
            'definition' : 'Household equity',
            'units': '$',
            'symbol': r'Equity$_{H}$'

        },
    },
    'parameter':{
    },
}

"""ALL AGREGATED VALUES THAT CAN BE CALCULATED"""
_LOGICS_AGREGATES = {
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
        'KAGGact': {'func': lambda nu,delta, p, K: sprod(p/(nu*delta), K),
                    'com': 'capital value on its potential production',
                    'definition': 'nominal active capital value',
                    'symbol': r'$K^{\nu}_{\bigcirc}$',
                    'units': '$',
        },
        'HAGG': { 'func': lambda H,p: sprod(H,p),
                  'definition' : 'nominal household possessions',
                    'symbol': r'$H_{\bigcirc}$',
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
        'deltahAGG': { 'func': lambda p, deltah,rho,H : sprod(p,deltah*H+matmul(rho,H))/sprod(p,H) ,
                       'definition': 'agregated possessions degradation rate',
                       'symbol': r'$\delta^h_{\bigcirc}$',
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
        'cAGG': { 'func': lambda omegaAGG,gammaAGG,xiAGG, pAGG : (omegaAGG+gammaAGG+xiAGG)* pAGG ,
                  'definition': 'aggregated relative cost',
                  'symbol': r'$c_{\bigcirc}$',
                  'units': '$'
        },
    },
}


if __AUXIN or __AGGIN:  _LOGICS = mergemodel(_LOGICS, _LOGICS_AUX,       verb=True)
if __AGGIN:             _LOGICS = mergemodel(_LOGICS, _LOGICS_AGREGATES, verb=True)


# ####################### PRESETS #######################################
preset_basis = {
'Tmax':20,
'dt':0.1,
'Nprod': ['Consumption','Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[1,5],
'K': [2.2,0.6],
'D':[0,0],
'u':[.95,.7],
'p':[1.5,3],
'V':[10,10],
'z':[1,.3],
'k0': 1.,

'Cpond':[1,0],

'mu0':[1.2,1.2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[1,1],
'b':1,
'nu':3,

## MATRICES
'Gamma': [[0.05 ,0],
          [0    ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.01,1],
       [0.1,1]],
'rho': np.eye(2),
}

dictMONOGOODWIN={
# Numerical structural
'Tmax'  : 100,
'Nprod' : ['Mono'],
'Tini'  : 0,

# Population
'n'     : 0.025, # MONOSECT
'N'     : 1    , # MONOSECT

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7,
'Gamma': 0.05,
'Xi'   : 1,
'nu'   : 3,
'delta': 0.05,
'b'    : 1,
'a'    : 1, # MONOSECT
'alpha': 0.02, # MONOSECT
'u'    : 1,

# Inventory-related dynamics
'V'     : 1,
'sigma' : 0,  # use variation
'chi'   : 0,  # inflation variation

# investment
'k0': 1.,

# Debt-related
'Dh'    : 0, # MONOSECT
'D'     : [0],
'r'     : 0.03, # MONOSECT

# Wages-prices
'w'     : 0.6, # MONOSECT
'p'     : 1,
'z'     : 1,
'mu0'   : 1.3,
'eta'   : 0.0,
'gammai': 0, # MONOSECT
'phinull':0.1, # MONOSECT

# Consumption theory
'Cpond' : [1],
}

trisector={
'Nprod': ['Consumption', 'Capital','Intermediate'],
'K': [5.01426008,2.79580692,1],
'D': [ 0.75618537,-0.75618537,0],
'Dh': -2.03540888e-17,
'u': [0.94703658,0.7126253 ,0.9],
'p': [2.35968699,0.79685443,1],
'V': [10.59268384, 9.91437758,10],
'w': 2.88903052,
'a': 1.48884403,
'N': 1.64460462*3/2,
'H': [1.33837281e+00,0,0],
'alpha': 0.02,
'n': 0.025,
'phinull': 0.1,
'r': 0.03,
'z': [1. ,0.3,.7],
'Cpond': [1,0,0],
'mu0': [1.2,1.2,1.2],
'delta': [0.05,0.05,0.05],
'deltah': [0.05,0,0],
'sigma': [1,5,5],
'gammai': 0.,
'eta': [0.3,0.3,0.3],
'chi': [1,1,1],
'b': [1.,1.,1.],
'nu': [3.,3.,3.],
'Gamma': [[0, 0.  ,0.1],
          [0, 0.  ,0.1],
          [0, 0.  ,0.1]],
'Xi': [[0.01, 1.  ,0],
       [0.1 , 1.  ,0],
       [0   , 1.  ,0]],
'rho': [[0, 0.,1.],
        [0.,0.,1.],
        [0.,0.,1.]],
'Tmax': 20,
'Tini': 0,
'dt': 0.1,
'nx': 1,
'nr': 1,
'k0': 1.,
 }


_PRESETS = {
    'MonoSectoral': {
        'fields': dictMONOGOODWIN,
        'com': ('A monosectoral system that behaves just as a Goodwin'),
        'plots': {},
    },
    'Bisectoral': {
        'fields': preset_basis,
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting for VERY far from equilibrium'),
        'plots': {},
    },
    'Trisectoral': {
        'fields': trisector,
        'com': ('Three sectors : Consumption, investment, intermediary.'),
        'plots': {},
    },
}
