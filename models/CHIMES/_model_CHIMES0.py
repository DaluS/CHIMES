'''Numerical core for multisectoral models'''

_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY
* **Article :** https://www.overleaf.com/project/62fbdce83176c9784e52236c    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

## Description
The goal of **E-CHIMES** is:
* description of production with physical variables
* behavior of agents (price, investment) based on economic values
* Connexion to ecological systems through physical coupling (emissions, land use...)

It integrates :
* Nprod productive sector, by activity
* Material flow analysis integrated inside
* Loans dynamics for investment and cross-sector expanses
* Inventory fluctuations
* Inflation
* Adaptive use of capital

## What should be done ?
* Check u and i mechanism


# DEALING WITH INVENTORY VARIATION (1) Starting close enough to the equilibrium

$$ \dot{V} = Y - [\Gamma^T Y] - \Xi^T I^r - C $$ 

With : 
$$Y = K/\nu$$
$$L = K/a$$
$$\Pi = pY  - w L- Y [\Gamma p] - \delta K  [\Xi p]$$
$$I^r = \delta K + \Pi$$ 
$$C = C^{pond} \sum(w L)$$

What this program does is, given : $\lambda$,$w$, $\Gamma$,$\Xi$,$C^{pond}$,$\delta$,$\nu$,$p$,$a$ returns the value of $K$ so that we have market-clearing conditions respecting the employment

"""
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O
import numpy as np

def dotD( MtransactI, MtransactY, wL, rD, pC):#,Shareholding):
    return rD \
         + wL -pC \
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

        ### PRICES
        'p'             :{'func': lambda p, inflation: p * inflation},
        'w0'            :{'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket)},

        ### BEHAVIOR
        #'u0'            :{'func': lambda u0, sigma, V, dotV: -sigma * (1 - u0) * (dotV / V),},
        #                  'com': 'On dotV/V',},
        #'u0'            :{'func': lambda u0, sigma, Y, dotV: -sigma * (1 - u0) * (dotV / Y),},
        'u0'            :{'func': lambda u0, sigma, v: sigma * (1 - u0) * (1-v),},
        #'func': lambda u: 0,

        ### EXOGENOUS SCALING
        'a0'            :{'func': lambda a0, alpha: a0 * alpha,
                          'definition': 'Capital unit per worker'},
        'N'             :{'func': lambda N, n: N * n},
    },
    'statevar': {
        ### BY-SECTOR PRODUCTIVITY AND WAGE
        'w'             :{'func': lambda w0,z: w0*z,},
        'a'             :{'func': lambda a0,apond : a0*apond},

        ### PROFITS AND COSTS
        'xi'            :{'func': lambda delta, nu, Mxi: (delta * nu)*O.ssum2(Mxi)},
        'omega'         :{'func': lambda L,Y,w,p:  w*L / (p* Y)},
        'gamma'         :{'func': lambda Mgamma:  O.ssum2(Mgamma)},
        'rd'            :{'func': lambda r,D,p,Y    : r*D/(p*Y)},
        'pi'            :{'func': lambda omega, gamma, xi, rd: 1 - omega - gamma - xi - rd,},
        
        'ROC'           :{'func': lambda pi, nu,Xi,p : pi / (nu*O.matmul(Xi,p)/p)},
        'c'             :{'func': lambda omega, gamma, xi, p: p * (omega + gamma + xi)},
        'mu'            :{'func': lambda p,c: p/c,
                          'units': ''},

        ### USE AND ACCESSIBILITY
        'u'             :{'func': lambda u0: u0,
                          'com' : 'just u0'},

        ### COST COMPONENTS
        
        'Mgamma'        :{'func': lambda Gamma,p : Gamma*O.transpose(p)/p},
        'Mxi'           :{'func': lambda Xi, p,nu,delta: nu*delta*Xi * O.transpose(p) / p},

        ### Inflations
        'inflation'     :{'func': lambda inflationMarkup,inflationdotVv,inflationdotVY,inflationdotVV: inflationMarkup+inflationdotVY+inflationdotVv+inflationdotVV,},
        'inflationMarkup':{'func': lambda eta, mu0, mu: eta* np.log(mu0/mu),},#eta * (mu0/mu -1 )},#

        'inflationdotVv' :{'func': lambda chiv,v: chiv *(v-1),
                    'com': 'V0/V'},
        'inflationdotVY' :{'func': lambda chiY, dotV, Y: - chiY *( dotV / Y),
                          'com': 'dotV/Y'},
        'inflationdotVV' :{'func': lambda chiV, dotV, V: - chiV *( dotV / V),
                          'com': 'dotV/V'},

        'basket'        :{'func': lambda p, C: p * C / O.sprod(p, C)},
        'ibasket'       :{'func': lambda inflation, basket: O.sprod(inflation, basket)},
        'L'             : {'func': lambda u,K,a : u*K/a},

        ### PHYSICAL FLUXES
        'Y'             :{'func': lambda u,nu, K: u*K / nu,},
        'Ir'            :{'func': lambda I,Xi,p: I/O.matmul(Xi,p),},
        'C'             :{'func': lambda W,Cpond,p: Cpond*W/p,},
        'dotV'          :{'func': dotV},
        'v'             :{'func': lambda epsilonV,Y,V: epsilonV*Y/V},
        'Kdelta'        :{'func': lambda K,delta : delta*K,},
        'GammaY'        :{'func': lambda Gamma,Y : O.matmul(O.transpose(Gamma), Y),
                          'definition': 'flux to intermediate consumption',
                          'units': 'Units.y^{-1}',
                          'symbol': '$(\Gamma^T Y)$'},
        'TakenforIr'    :{'func': lambda Xi,Ir : O.matmul(O.transpose(Xi), Ir),
                          'units':  'Units.y^{-1}',
                          'symbol': '$(\Xi^T I^r)$'},
        
        # Matrix approach
        'Minter'        :{'func': lambda Y, Gamma: O.transpose(Gamma*Y)},
        'Minvest'       :{'func': lambda Ir, Xi:  O.transpose(Xi* Ir)},
        'MtransactY'    :{'func': lambda p, Y, Gamma: Y * Gamma * O.transpose(p)},
        'MtransactI'    :{'func': lambda I, Xi, p: I * Xi * O.transpose(p) / (O.matmul(Xi, p))},

        ### MONETARY FLUXES
        'wL'            :{'func': lambda w,L : w*L},
        'Shareholding'  :{'func': lambda Delta,p,Y,pi: Delta*p*Y*pi },
        'pC'            :{'func': lambda p,C: p *C},
        'Idelta'        :{'func': lambda xi,p,Y : p * Y * xi},
        'Ilever'        :{'func': lambda p, Y, kappa: p * Y * kappa },
        'I'             :{'func': lambda Idelta,Ilever: Idelta+ Ilever},
        'rD'            :{'func': lambda r,D: r*D},
        'dotD'          :{'func': dotD},

        ### LABOR-SIDE THEORY
        'W'             :{'func': lambda w, L, r, Dh, : O.sprod(w, L)  - r * Dh}, #+ O.ssum(Shareholding)
        'rDh'           :{'func': lambda r,Dh : r*Dh,},
        'employmentAGG' :{'func': lambda employment: O.ssum(employment),},


        'Phillips'      :{'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG,
                          'com': 'LINEAR',},
        'kappa'         :{'func': lambda pi, k0, k1 : k0 +k1 * pi,
                          'com': 'AFFINE KAPPA FUNCTION'},

        ### PROFITS AND INVESTMENTS
        'g'             :{'func': lambda Ir,K,delta : Ir/K - delta },
        'employment'    :{'func': lambda L,N        : L/N},
        'reldotv'       :{'func': lambda dotV, Y, p, c: (c - p) * dotV / (p * Y)}, #'com': 'calculated as inventorycost on production',
        'reloverinvest' :{'func': lambda kappa, pi: pi - kappa}, #'com': 'difference between kappa and pi',
    },
    'parameter': {
        'apond' :   { 'value' : 1,
                      'definition': 'sector-ponderation of production'},
        'CESexp':   { 'value' : 1000},
        'b':        { 'value' : 0.5},
        'epsilonV': { 'value' : 0.1},
        'chiv' :    { 'value' : 0  },
        'chiV' :    { 'value' : 0  },
        'chiY' :    { 'value' : 0  },
    },
}

########################### CHANGING PROPERTIES ############################
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


##########################################################################
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
#########################################################################


def generategoodwin(Nsect,gamma=0.1,xi=1):
    '''Generate a dparam to generate N Goodwin in parrallel'''
    GOODWIN_PRESET= { 
        
        
        ### Numerical values 
        'Tmax':100.,    'Tini':0.,     'dt': 0.1, 
        'Nprod': [''],    
        #'nx': [''],     'nr': [''],

        # Monosectoral initial 
        'N':1/.9,     'w0':0.7,     'a0':3., 
        # Initial multisectoral
        'D':0.,     'Dh':0.,   
        'K':2.7,     'p':1., 



        # Multisectoral ponderation
        'z': 1.,     # On wage 
        'apond': 1., # On productivity

        # Characteristic frequencies
        'alpha':0.025,     'n':0.02,    'delta':0.005, 
        'eta': 0.,     'mu0': 1.,     'chi': 0., 

        # Prices, inflation, negociation
        'gammai':0.,    
        'r':0.03, 
        #'phinull':0.1, 
        'philinConst': -0.292,    'philinSlope':  0.469, 
        'Delta': 0.,             #shareholding 

        # Kappa investment 
        'k0':0.,    'k1':1.,

        # CES production function
        'A': 1/3,    'CESexp':1000.,    'b' :.5,

        # MATRICES 
        'Xi': xi,     'Gamma': gamma, 

        'Cpond': 1., 
        'sigma': 0, 

        # ACCESSIBILITY AND INVENTORY
        'V' : 100,
        'kY': 1000,
        'kI': 1000,
        'kC': 1000,        
        'softmin':1000,  
        'epsilonV': 0.1, 
    }


    GOODWIN_N= GOODWIN_PRESET.copy()
    GOODWIN_N['w0'] = 1 -GOODWIN_N['Gamma'] - 1/GOODWIN_N['A']*GOODWIN_N['Xi']*(GOODWIN_N['alpha']
                                                                                    +GOODWIN_N['n']
                                                                                    +GOODWIN_N['delta'])
    print(GOODWIN_N['w0'])
    GOODWIN_N['Nprod']=[str(i) for i in range(Nsect)]
    GOODWIN_N['Gamma']=np.eye(Nsect)*gamma
    GOODWIN_N['Xi'   ]=np.eye(Nsect)*xi
    
    GOODWIN_N['N']*=Nsect
    GOODWIN_N['Cpond']=1/Nsect


    #useful statevar for calculation that will not be loaded in set_dparam
    GOODWIN_N['a'] = GOODWIN_N['a0']*GOODWIN_N['apond']
    GOODWIN_N['w'] = GOODWIN_N['w0']*GOODWIN_N['z']
    return {k : np.array([v]) if type(v) not in [np.array,np.ndarray,list] else v for k,v in GOODWIN_N.items()}

def pForROC(dic):
    '''Find the price vector so that the natural return on capital is the growth rate of society
    ROC = pi / (nu*xi'''
    from scipy.optimize import fsolve
    def ecart(p,dic):
        nu = 1/dic['A']
        omega = dic['w0']*dic['z']*nu/(dic['a0']*dic['apond']*p)
        gamma = O.matmul(dic['Gamma'],p)/p
        xi = O.matmul(dic['Xi'],p)/p
            
        return  1 - gamma - omega - nu*xi*(  dic['alpha'] 
                                           + dic['n'] 
                                           + dic['delta'] )  
                                         
    p = fsolve(ecart,np.array([1.]*len(dic['Nprod'])),args=dic)
    return p

def Kfor0dotV(params):
    '''
    Given the value of parameters (Gamma,Xi,Cpond,delta,nu,p,a,w),
    Find the vector of capital that ensure dotV=0 at the first iteration, only for a GOODWIN.
    You can then multiply it in order to have the right GDP or employment
    '''
    from scipy.optimize import fsolve
    def dotV(K,params):
        Gamma   =np.array(params['Gamma'])
        Xi      =np.array(params['Xi'])
        Cpond   =np.array(params['Cpond'])
        delta   =np.array(params['delta'])  +0*K
        A       =np.array(params['A'])      +0*K
        p       =np.array(params['p'])      +0*K
        a       =np.array(params['a'])      +0*K
        w       =np.array(params['w'])      +0*K

        #### Deriving equations 
        Y = K*A
        L = K/a
        Inter = np.matmul(np.transpose(Gamma),Y) 
        C = Cpond*sum(w*L)/p
        Pi = p*Y 
        Pi-= w*L 
        Pi-= Y*np.matmul(Gamma,p)  
        Pi-= delta*K* np.matmul(Xi,p)
        Ir = Pi/(np.matmul(Xi,p)) + K*delta
    
        ### Returning dotV
        return Y - Inter - C - np.matmul(np.transpose(Xi),Ir)
    K = fsolve(dotV,np.array([1.]*len(params['Nprod'])),args=params)
    return K

def Leontievinverse(params,Eigenvalues=False):
    LeontievInverse = np.linalg.inv(np.eye(params['Nsect'])
                                    -params['Gamma']
                                    -params['delta']/params['A']*params['Xi'])
    Eigenvalues,Eigenvectors = np.linalg.eig(LeontievInverse)
    return LeontievInverse,Eigenvalues,Eigenvectors


###################### LOCAL SPECIAL PLOTS ################
def PiRepartition(hub,tini=False,tend=False):
    for sector in hub.dparam['Nprod']['list'] :
        hub._DPLOT['repartition'](hub,
                            ['pi','omega','Mxi','Mgamma','rd','reloverinvest','reldotv'],
                            sign= [1,1,1,1,1,1,-1],
                            sector=sector,
                            title=f'Expected relative budget $\pi$ for sector {sector}',
                                    tini=tini,
                                    tend=tend)
def PhysicalFluxes(hub,tini=False,tend=False):
    for sector in hub.dparam['Nprod']['list'] :
        hub._DPLOT['repartition'](hub,
                            ['dotV','Minter','Minvest','C'],
                            ref='Y',
                            stock='V',
                            sector=sector,
                            title=f'Physical Fluxes for sector {sector}',
                                  tini=tini,
                                  tend=tend)
def MonetaryFluxes(hub,tini=False,tend=False):
    for sector in hub.dparam['Nprod']['list'] :
        hub._DPLOT['repartition'](hub,
                          ['MtransactY','MtransactI','wL','pC','rD'],
                          sign=[1, 1, 1, -1, 1],
                          ref='dotD',
                          sector=sector,
                          title=f'Monetary Fluxes for sector {sector}',
                          removetranspose=True,
                                  tini=tini,
                                  tend=tend)


_SUPPLEMENTS = {
    # Generating Set_dparam
    'generateNgoodwin': generategoodwin,
    'Kfor0dotV' : Kfor0dotV,
    'pForROC' : pForROC,

    # Exploring Leontiev Inverse
    'LeontievInverse': Leontievinverse,

    # Plots 
    'PiRepartition' : PiRepartition,
    'PhysicalFluxes': PhysicalFluxes,
    'MonetaryFluxes': MonetaryFluxes,
}








preset_TRI = {
'Tmax':50,
'dt':0.1,
'Nprod': ['Consumption','Intermediate','Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':3,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[1,5,5],
'K': [2.1,0.4,0.4],
'D':[0,0,0],
'u':[.95,.95,.95],
'p':[1,1,1],
'V':[1,1,1],
'z':1,
'k0': 1.,
'Cpond':[1,0,0],
'mu0':1.2,
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':1,
'b':.5,
'A':1/3,

## MATRICES
'Gamma': [[0.0,0.1 ,0],
          [0  ,0.1 ,0],
          [0.0,0.1 ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.0,0,1],
       [0.0,0,1],
       [0.0,0,1]],
'rho': np.eye(3),
}

preset_basis = {
    ### Numerical values 
    'Tmax':100,    'Tini':0,     'dt': 0.1, 
    'Nprod': [''],#['Consumption','Capital'],     
    'nx': [''],     'nr': [''],

    # Monosectoral initial 
    'N':1,     'w0':0.75,     'a0':3, 
    'Dh':0,
    # Monosectoral parameters
    'alpha' : 0.02,
    'n'     : 0.025,
    'gammai':0,    
    'r':0.03, 
    'philinConst': -0.292,    'philinSlope':  0.469, 

    # Multisectoral Initial condition
    'p':[1,  ],#     1],  
    'K':[2., ],#   0.5],
    'D':[0,  ],#     0],
    'V':[1000],#,  1000],

    'b':.5,
    'A':1/3,
    'CESexp':10,

    #'sigma':[1,5],
    
    #'u':[.95,.7],

    'z':[1],#,1],
    'apond':[1],#,1],
    'k0': 1.,

    'Cpond':[1],#,0],

    'mu0':[1.5],#,1.2],
    'delta':0.05,
    'deltah':0.05,
    'eta':0.1,
    'chi':0,#[1],#1],


    ## MATRICES
    'Gamma': .05,# [[0.05 ,0],
            #[0    ,0]],
    #'Xi': [['Consumption','Capital','Consumption','Capital'],
    #       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
    'Xi': 1,# [[0.01,1],
        #[0.1,1]],
    #'rho': np.eye(2),
    }

preset_basis2=preset_basis.copy()
preset_basis2['K'] = [2]#.3,0.5]


_PRESETS = {
    'Goodwin': {
        'fields': _SUPPLEMENTS['generateNgoodwin'](1),
        'com': (''),
        'plots': {'XY':[{'x':'omega',
                         'y':'employment',
                         'color':'time'}]},
    },
    '2Goodwin': {
        'fields':  _SUPPLEMENTS['generateNgoodwin'](2),
        'com': (''),
        'plots': {},
    },
    '5Goodwin': {
        'fields': _SUPPLEMENTS['generateNgoodwin'](5),
        'com': (''),
        'plots': {},
    },
    'SimpleBi':{
        'fields': preset_basis2,
        'com':'',
        'plots':{}
    },
    'SimpleTri':{
        'fields': preset_TRI,
        'com':'',
        'plots':{}
    }
}



