'''Economic Core for multisectoral models'''
##########################################################################
from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
from chimes.libraries import Operators as O                              #
import numpy as np                                                       #
##########################################################################

_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY

* **Article :** https://www.overleaf.com/read/thbdnhbtrbfx
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
* **Date    :** 14/09/23

## Description

E-CHIMES is an economic model with multiple productive sectors in co-dependency.
The model is fully stock-flow consistent on both the monetary and all physical plans.

It is a platform for endogenisation.
"""
_TODO = ['Debugging']
_ARTICLE = "https://link.springer.com/chapter/10.1007/978-1-349-05504-3_12"
_DATE = "2024/07/01"
_CODER = "Paul Valcke"
_KEYWORDS = ['Economic', 'Multisectoral', 'Core']


def dotD(MtransactI, MtransactY, wL, rD, pC, Shareholding):
    return rD \
        + wL \
        - pC \
        + Shareholding \
        + O.ssum2(MtransactI - O.transpose(MtransactI)) \
        + O.ssum2(MtransactY - O.transpose(MtransactY))


def dotV(Y, Gamma, I, C, Xi):
    return Y \
        - C \
        - O.matmul(O.transpose(Gamma), Y) \
        - O.matmul(O.transpose(Xi), I)


_LOGICS = dict(
    size={'Nprod': {'list': ['MONO']}},
    ###################################################################
    differential=dict(
        # MONETARY STOCK-FLOW CONSISTENCY
        D=lambda dotD: dotD,
        Dh=lambda W, p, C: -W + O.sprod(p, C),

        # PHYSICAL STOCK-FLOW CONSISTENCY
        V=lambda dotV: dotV,
        K=lambda I, delta, K: I - delta * K,

        # PRICES AND WAGES
        p=lambda p, inflation: p * inflation,
        w0=lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket),

        # EXOGENOUS SCALING
        a0=lambda a0, alpha: a0 * alpha,
        N=lambda N, n: N * n,
    ),
    statevar=dict(
        # BY-SECTOR PRODUCTIVITY AND WAGE
        w=lambda w0, zw: w0 * zw,
        a=lambda a0, za: a0 * za,

        # MONETARY FLUXES
        wL=lambda w, L: O.ssum(w * L),
        W=lambda wL, r, Dh, Shareholding: wL - r * Dh + O.ssum(Shareholding),
        rD=lambda r, D: r * D,
        Pi=lambda p, Y, Gamma, Idelta, r, D, wL: p*Y - r*D - wL - Y*O.matmul(Gamma, p) -Idelta,
        # Pi=lambda p, Y, pi: p * Y * pi,
        Shareholding=lambda Delta, Pi: Delta * Pi,
        pC=lambda p, C: p * C,
        Ilever=lambda Pi, kappaI: Pi * kappaI,
        In=lambda Idelta, Ilever: Idelta + Ilever,
        Idelta=lambda delta, K, Xi, p: delta*K*O.matmul(Xi, p),
        dotD=dotD,

        # PHYSICAL FLUXES
        Y=lambda u, nu, K: u * K / nu,
        I=lambda In, Xi, p: In / O.matmul(Xi, p),
        C=lambda W, kappaC, p: kappaC * W / p,

        # PROFITS AND COSTS
        omega=lambda Y, wL, p: wL / (p * Y),
        rd=lambda r, D, p, Y: r * D / (p * Y),
        pi=lambda p, Y, Pi: Pi/(p*Y),


        MtransactY=lambda p, Y, Gamma: Y * Gamma * O.transpose(p),
        MtransactI=lambda In, Xi, p: In * Xi * O.transpose(p) / (O.matmul(Xi, p)),

        # LABOR-SIDE
        L=lambda u, K, a: u * K / a,
        employmentAGG=lambda employment: O.ssum(employment),
        omegaAGG=lambda wL, p, Y: wL/O.ssum(p*Y),
        Phillips=lambda Phi0, Phi1, employmentAGG: Phi0 + Phi1 / (1 - employmentAGG)**2,
        employment=lambda L, N: L / N,
    ),
    parameter=dict(
        za=1,
        zw=1,
        ibasket=0,
        u=1,
        # 'CESexp':   { 'value' : 1000,
        # 'b':        { 'value' : 0.5 ,
        # 'epsilonV': { 'value' : 0.1 ,
        # 'chiv' :    { 'value' : 0   ,
        # 'chiV' :    { 'value' : 0   ,
        # 'chiY' :    { 'value' : 0   ,
        # 'inflation':{ 'value' : 0   ,
        Phi0=-0.1010101,
        Phi1=0.0010101,
        kappaI=1,
        kappaC=1,
    ),
)

##########################################################################
Dimensions = {
    'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W',
               'alpha', 'Nprod', 'Phillips', 'rDh', 'gammai',
               'n', 'ibasket', 'Dh', 'Phi0', 'Phi1','wL'],
    'matrix': ['Gamma', 'Xi', 'Mgamma', 'Mxi', 'Minter',
               'Minvest', 'MtransactY', 'MtransactI']
    # 'vector': will be deduced by fill_dimensions
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nprod'],
       'matrix': ['Nprod', 'Nprod']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)
#########################################################################


def Kfor0dotV(params):
    '''
    Given the value of parameters (Gamma,Xi,kappaC,delta,nu,p,a,w),
    Find the vector of capital that ensure dotV=0 at the first iteration, only for a GOODWIN.
    You can then multiply it in order to have the right GDP or employment
    '''
    from scipy.optimize import fsolve

    def dotV(K, params):
        Gamma = np.array(params['Gamma'])
        Xi = np.array(params['Xi'])
        kappaC = np.array(params['kappaC'])
        delta = np.array(params['delta']) + 0 * K
        A = np.array(params['A']) + 0 * K
        p = np.array(params['p']) + 0 * K
        a = np.array(params['a']) + 0 * K
        w = np.array(params['w']) + 0 * K

        # Deriving equations
        Y = K * A
        L = K / a
        Inter = np.matmul(np.transpose(Gamma), Y)
        C = kappaC * sum(w * L) / p
        Pi = p * Y
        Pi -= w * L
        Pi -= Y * np.matmul(Gamma, p)
        Pi -= delta * K * np.matmul(Xi, p)
        I = Pi / (np.matmul(Xi, p)) + K * delta

        # Returning dotV
        return Y - Inter - C - np.matmul(np.transpose(Xi), I)
    K = fsolve(dotV, np.array([1.] * len(params['Nprod'])), args=params)
    return K


def generategoodwin(Nsect, gamma=0.1, xi=1):
    '''Generate a dfields to generate N Goodwin in parrallel'''
    GOODWIN_PRESET = {
        # Numerical values
        'Tsim': 100., 'Tini': 0., 'dt': 0.1,
        'Nprod': [''],
        # 'nx': [''],     'nr': [''],

        # Monosectoral initial
        'N': 1,
        'w0': 0.7,
        'a0': 3.,
        # Initial multisectoral
        'D': 0.,
        'Dh': 0.,
        'K': 2.7,
        'p': 1.,

        # Wage negotiation properties
        'Phinull': 0.1,    # Employment rate at which wage is not increasing
        'Phi0': -1,     # "Almost" rate of wage decrease without employment

        # Multisectoral ponderation
        'zw': 1.,     # On wage
        'za': 1.,  # On productivity
        'z': 1.,     # On wage
        'apond': 1.,  # On productivity


        # Characteristic frequencies
        'alpha': 0.025, 'n': 0.02, 'delta': 0.005,
        'eta': 0., 'mu0': 1., 'chi': 0.,

        # Prices, inflation, negociation
        'inflation': 0.02,
        'gammai': 0.,
        'r': 0.03,
        'Delta': 0.,  # shareholding

        # Kappa investment
        'k0': 0., 'k1': 1.,

        # CES production function
        'A': 1 / 3, 'CESexp': 1000., 'b': .5,

        # MATRICES
        'Xi': xi, 'Gamma': gamma,

        'kappaC': 1.,
        'sigma': 0,

        # ACCESSIBILITY AND INVENTORY
        'V': 100000,
        # 'kY': 1000,
        # 'kI': 1000,
        # 'kC': 1000,
        # 'softmin':1000,
        # 'epsilonV': 0.1,


    }

    GOODWIN_N = GOODWIN_PRESET.copy()

    # Closing the Phillips curve
    GOODWIN_N['Phi1'] = -GOODWIN_N['Phi0'] * (GOODWIN_N['Phinull'])**2

    def fm1(x):
        return 1 - np.sqrt(x)
    GOODWIN_N['employment'] = fm1(-GOODWIN_N['Phi1'] / (GOODWIN_N['Phi0'] + GOODWIN_N['alpha'] + GOODWIN_N['inflation'] * (1 - GOODWIN_N['gammai'])))

    GOODWIN_N['w0'] = 1 - GOODWIN_N['Gamma'] - (1 / GOODWIN_N['A']) * GOODWIN_N['Xi'] * (GOODWIN_N['alpha'] + GOODWIN_N['n'] + GOODWIN_N['delta'])

    # Matrices and sectorial stuff
    GOODWIN_N['Nprod'] = [str(i) for i in range(Nsect)]
    GOODWIN_N['Gamma'] = np.eye(Nsect) * gamma
    GOODWIN_N['Xi'] = np.eye(Nsect) * xi
    GOODWIN_N['N'] *= Nsect
    GOODWIN_N['kappaC'] = 1 / Nsect

    # useful statevar for calculation that will not be loaded in set_fields
    GOODWIN_N['a'] = GOODWIN_N['a0'] * GOODWIN_N['za']
    GOODWIN_N['w'] = GOODWIN_N['w0'] * GOODWIN_N['zw']

    # Capital scaling
    K = Kfor0dotV(GOODWIN_N)
    GOODWIN_N['K'] = K * GOODWIN_N['employment'] * GOODWIN_N['N'] / np.sum(K / GOODWIN_N['a'])  # homotetic scaling for employment and N
    GOODWIN_N['p'] = pForROC(GOODWIN_N)
    return {k: np.array([v]) if type(v) not in [np.array, np.ndarray, list] else v for k, v in GOODWIN_N.items()}


def pForROC(dic):
    '''Find the price vector so that the natural return on capital is the growth rate of society
    ROC = pi / (nu*xi^p)'''
    from scipy.optimize import fsolve

    def ecart(p, dic):
        nu = 1 / dic['A']
        omega = dic['w0'] * dic['zw'] * nu / (dic['a0'] * dic['za'] * p)
        gamma = O.matmul(dic['Gamma'], p) / p
        xi = O.matmul(dic['Xi'], p) / p

        return 1 - gamma - omega - nu * xi * (dic['alpha'] + dic['n'] + dic['delta'])

    p = fsolve(ecart, np.array([1.] * len(dic['Nprod'])), args=dic)
    return p


def Leontievinverse(params, Eigenvalues=False):
    '''Give the equivalent of the Leontiev Matrix with intermediate consumption and capital weight'''
    LeontievInverse = np.linalg.inv(np.eye(params['Nsect']) - params['Gamma'] - params['delta'] / params['A'] * params['Xi'])
    Eigenvalues, Eigenvectors = np.linalg.eig(LeontievInverse)
    return LeontievInverse, Eigenvalues, Eigenvectors


# ##################### LOCAL SPECIAL PLOTS ################
def PiRepartition(hub, tini=False, tend=False):
    '''Plot the relative profit repartition for each sector'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT['repartition'](hub,
                                  ['pi', 'omega', 'Mxi', 'Mgamma', 'rd', 'reloverinvest', 'reldotv'],
                                  sign=[1, 1, 1, 1, 1, 1, -1],
                                  sector=sector,
                                  title=f'Expected relative budget $\pi$ for sector {sector}',
                                  tini=tini,
                                  tend=tend)


def PhysicalFluxes(hub, tini=False, tend=False):
    '''Plot the physical fluxes for each sector'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT['repartition'](hub,
                                  ['dotV', 'Minter', 'Minvest', 'C'],
                                  ref='Y',
                                  stock='V',
                                  sector=sector,
                                  title=f'Physical Fluxes for sector {sector}',
                                  tini=tini,
                                  tend=tend)


def MonetaryFluxes(hub, tini=False, tend=False):
    '''Plot monetary fluxes for each sectore'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT['repartition'](hub,
                                  ['MtransactY', 'MtransactI', 'wL', 'pC', 'rD'],
                                  sign=[1, 1, 1, -1, 1],
                                  ref='dotD',
                                  sector=sector,
                                  title=f'Monetary Fluxes for sector {sector}',
                                  removetranspose=True,
                                  tini=tini,
                                  tend=tend)


_SUPPLEMENTS = {
    # Generating Set_dfields
    'generateNgoodwin': generategoodwin,
    'Kfor0dotV': Kfor0dotV,
    'pForROC': pForROC,

    # Exploring Leontiev Inverse
    'LeontievInverse': Leontievinverse,

    # Plots
    'PiRepartition': PiRepartition,
    'PhysicalFluxes': PhysicalFluxes,
    'MonetaryFluxes': MonetaryFluxes,
}


preset_TRI = {
    'Tsim': 50,
    'dt': 0.1,
    'Nprod': ['Consumption', 'Intermediate', 'Capital'],
    'nx': 1,

    'alpha': 0.02,
    'n': 0.025,
    'phinull': 0.1,

    'gammai': 0,
    'r': 0.03,
    'a': 3,
    'N': 1,
    'Dh': 0,
    'w': 0.8,

    #'sigma': [1, 5, 5],
    'K': [2.1, 0.4, 0.4],
    'D': [0, 0, 0],
    #'u': [.95, .95, .95],
    'p': [1, 1, 1],
    #'V': [1, 1, 1],
    'zw': 1,
    'k0': 1.,
    'kappaC': [1, 0, 0],
    'mu0': 1.2,
    'delta': 0.05,
    'deltah': 0.05,
    'eta': 0.3,
    'chi': 1,
    'b': .5,
    'A': 1 / 3,

    # MATRICES
    'Gamma': [[0.0, 0.1, 0],
              [0, 0.1, 0],
              [0.0, 0.1, 0]],
    'Xi': [[0.0, 0, 1],
           [0.0, 0, 1],
           [0.0, 0, 1]],
    'rho': np.eye(3),
}

preset_basis = {
    # Numerical values
    'Tsim': 100, 'Tini': 0, 'dt': 0.1,
    'Nprod': [''],  # ['Consumption','Capital'],
    'nx': [''], 'nr': [''],

    # Monosectoral initial
    'N': 1, 'w0': 0.75, 'a0': 3,
    'Dh': 0,
    # Monosectoral parameters
    'alpha': 0.02,
    'n': 0.025,
    'gammai': 0,
    'r': 0.03,
    'philinConst': -0.292, 'philinSlope': 0.469,

    # Multisectoral Initial condition
    'p': [1,],  # 1],
    'K': [2., ],  # 0.5],
    'D': [0,],  # 0],
    'V': [1000],  # ,  1000],

    'b': .5,
    'A': 1 / 3,
    'CESexp': 10,

    # 'sigma':[1,5],

    # 'u':[.95,.7],

    'zw': [1],  # ,1],
    'za': [1],  # ,1],
    'k0': 1.,

    'kappaC': [1],  # ,0],

    'mu0': [1.5],  # ,1.2],
    'delta': 0.05,
    'deltah': 0.05,
    'eta': 0.1,
    'chi': 0,  # [1],#1],


    # MATRICES
    'Gamma': .05,  # [[0.05 ,0],
    # [0    ,0]],
    # 'Xi': [['Consumption','Capital','Consumption','Capital'],
    #       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
    'Xi': 1,  # [[0.01,1],
    # [0.1,1]],
    # 'rho': np.eye(2),
}

preset_basis2 = preset_basis.copy()
preset_basis2['K'] = [2]  # .3,0.5]

_PRESETS = {
    'Goodwin': {
        'fields': {'K': 5,
                   'N': 1},  # _SUPPLEMENTS['generateNgoodwin'](1),
        'com': ('Basic Goodwin dynamics on a monosectorial '),
        'plots': {'XY': [{'x': 'omega',
                         'y': 'employment',
                          'color': 'time'}]},
    },
    '2Goodwin': {
        'fields': _SUPPLEMENTS['generateNgoodwin'](2),
        'com': (''),
        'plots': {},
    },
    '5Goodwin': {
        'fields': _SUPPLEMENTS['generateNgoodwin'](5),
        'com': (''),
        'plots': {},
    },
    'SimpleBi': {
        'fields': preset_basis2,
        'com': '',
        'plots': {}
    },
    'SimpleTri': {
        'fields': preset_TRI,
        'com': '',
        'plots': {}
    }
}
