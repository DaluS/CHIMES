'''Economic Core for multisectoral models'''
from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
from chimes.libraries import Operators as O                              #
import numpy as np
_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY

* **Article :** https://www.overleaf.com/read/thbdnhbtrbfx
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
* **Date    :** 14/09/23

## Description

E-CHIMES is an economic model with multiple productive sectors in dependency.
The model is fully stock-flow consistent on both the monetary and physical plan.

It is a platform for endogenisation, both on the physical and monetary plan.

It integrates :
* Nprod productive sector, by activity
* Material flow analysis integrated inside
* Loans dynamics for investment and cross-sector expanses
* Inventory fluctuations
* Inflation
* Adaptive use of capital

## TODO
* Shareholding reintegration

"""
##########################################################################
#
##########################################################################


def dotD(MtransactI, MtransactY, wL, rD, pC, Shareholding):
    return rD \
        + wL \
        - pC \
        + Shareholding \
        + O.ssum2(MtransactI - O.transpose(MtransactI)) \
        + O.ssum2(MtransactY - O.transpose(MtransactY))


def dotV(Y, Gamma, Ir, C, Xi):
    return Y \
        - C \
        - O.matmul(O.transpose(Gamma), Y) \
        - O.matmul(O.transpose(Xi), Ir)


_LOGICS = {
    'size': {'Nprod': {'list': ['MONO']}},
    ###################################################################
    'differential': {
        # MONETARY STOCK-FLOW CONSISTENCY
        'D': {'func': lambda dotD: dotD},
        'Dh': {'func': lambda W, p, C, Shareholding: -W + O.sprod(p, C) - O.ssum(Shareholding)},

        # PHYSICAL STOCK-FLOW CONSISTENCY
        'V': {'func': lambda dotV: dotV},
        'K': {'func': lambda Ir, delta, K: Ir - delta * K},
        # 'H'             :{'func': lambda H,rho,deltah,C: C- deltah*H - O.matmul(rho,H)},

        # PRICES AND WAGES
        'p': {'func': lambda p, inflation: p * inflation},
        'w0': {'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket)},

        # BEHAVIOR
        # 'u0'            :{'func': lambda u0, sigma, V, dotV: -sigma * (1 - u0) * (dotV / V),},
        #                  'com': 'On dotV/V',},
        # 'u0'            :{'func': lambda u0, sigma, Y, dotV: -sigma * (1 - u0) * (dotV / Y),},
        'u0': {'func': lambda u0, sigma, v: sigma * (1 - u0) * (1 - v), },
        # 'func': lambda u: 0,

        # EXOGENOUS SCALING
        'a0': {'func': lambda a0, alpha: a0 * alpha,
               'definition': 'Capital unit per worker'},
        'N': {'func': lambda N, n: N * n},
    },
    'statevar': {
        # BY-SECTOR PRODUCTIVITY AND WAGE
        'w': {'func': lambda w0, z: w0 * z, },
        'a': {'func': lambda a0, apond: a0 * apond},

        # PROFITS AND COSTS
        'xi': {'func': lambda delta, nu, Mxi: (delta * nu) * O.ssum2(Mxi)},
        'omega': {'func': lambda L, Y, w, p: w * L / (p * Y)},
        'gamma': {'func': lambda Mgamma: O.ssum2(Mgamma)},
        'rd': {'func': lambda r, D, p, Y: r * D / (p * Y)},
        'pi': {'func': lambda omega, gamma, xi, rd: 1 - omega - gamma - xi - rd, },

        'ROC': {'func': lambda pi, nu, Xi, p: pi / (nu * O.matmul(Xi, p) / p)},
        'c': {'func': lambda omega, gamma, xi, p: p * (omega + gamma + xi)},
        'mu': {'func': lambda p, c: p / c,
               'units': ''},

        # USE AND ACCESSIBILITY
        'u': {'func': lambda u0: u0,
              'com': 'just u0'},

        # COST COMPONENTS
        'Mgamma': {'func': lambda Gamma, p: Gamma * O.transpose(p) / p},
        'Mxi': {'func': lambda Xi, p, nu, delta: nu * delta * Xi * O.transpose(p) / p},

        # Inflations
        # 'inflation'     :{'func': lambda inflationMarkup,inflationdotVv,inflationdotVY,inflationdotVV: inflationMarkup+inflationdotVY+inflationdotVv+inflationdotVV,},
        # 'inflationMarkup':{'func': lambda eta, mu0, mu: eta* np.log(mu0/mu),},#eta * (mu0/mu -1 )},#
        # 'inflationdotVv' :{'func': lambda chiv,v: chiv *(v-1),
        #            'com': 'V0/V'},
        # 'inflationdotVY' :{'func': lambda chiY, dotV, Y: - chiY *( dotV / Y),
        #                  'com': 'dotV/Y'},
        # 'inflationdotVV' :{'func': lambda chiV, dotV, V: - chiV *( dotV / V),
        #                  'com': 'dotV/V'},

        'basket': {'func': lambda p, C: p * C / O.sprod(p, C)},
        'ibasket': {'func': lambda inflation, basket: O.sprod(inflation, basket)},
        'L': {'func': lambda u, K, a: u * K / a},

        # PHYSICAL FLUXES
        'dotV': {'func': dotV},
        'Y': {'func': lambda u, nu, K: u * K / nu, },
        'Ir': {'func': lambda I, Xi, p: I / O.matmul(Xi, p), },
        'C': {'func': lambda W, Cpond, p: Cpond * W / p, },
        'v': {'func': lambda epsilonV, Y, V: epsilonV * Y / V,
              'symbol': '$\dot{v} $'},
        'Kdelta': {'func': lambda K, delta: delta * K, },
        'GammaY': {'func': lambda Gamma, Y: O.matmul(O.transpose(Gamma), Y),
                   'definition': 'flux to intermediate consumption',
                   'units': 'Units.y^{-1}',
                   'symbol': '$(\Gamma^T Y)$'},
        'TakenforIr': {'func': lambda Xi, Ir: O.matmul(O.transpose(Xi), Ir),
                       'units': 'Units.y^{-1}',
                       'symbol': '$(\Xi^T I^r)$'},

        # Matrix approach
        'Minter': {'func': lambda Y, Gamma: O.transpose(Gamma * Y)},
        'Minvest': {'func': lambda Ir, Xi: O.transpose(Xi * Ir)},
        'MtransactY': {'func': lambda p, Y, Gamma: Y * Gamma * O.transpose(p)},
        'MtransactI': {'func': lambda I, Xi, p: I * Xi * O.transpose(p) / (O.matmul(Xi, p))},

        # MONETARY FLUXES
        'wL': {'func': lambda w, L: w * L},
        'Shareholding': {'func': lambda Delta, p, Y, pi: Delta * p * Y * pi},
        'pC': {'func': lambda p, C: p * C},
        'Idelta': {'func': lambda xi, p, Y: p * Y * xi},
        'Ilever': {'func': lambda p, Y, kappa: p * Y * kappa},
        'I': {'func': lambda Idelta, Ilever: Idelta + Ilever},
        'rD': {'func': lambda r, D: r * D},
        'dotD': {'func': dotD},

        # LABOR-SIDE THEORY
        'W': {'func': lambda w, L, r, Dh, Shareholding: O.sprod(w, L) - r * Dh + O.ssum(Shareholding)},
        'rDh': {'func': lambda r, Dh: r * Dh, },
        'employmentAGG': {'func': lambda employment: O.ssum(employment), },
        'Phillips': {'func': lambda Phi0, Phi1, employmentAGG: Phi0 + Phi1 / (1 - employmentAGG)**2,
                     'com': 'DIVERGING'},

        'kappa': {'func': lambda pi, k0, k1: k0 + k1 * pi,
                  'com': 'AFFINE KAPPA FUNCTION'},
        'omegaAGG': {'func': lambda w, L, p, Y : O.sprod(w, L)/O.sprod(p, Y)},

        # PROFITS AND INVESTMENTS
        'g': {'func': lambda Ir, K, delta: Ir / K - delta},
        'employment': {'func': lambda L, N: L / N},
        'reldotv': {'func': lambda dotV, Y, p, c: (c - p) * dotV / (p * Y)},  # 'com': 'calculated as inventorycost on production',
        'reloverinvest': {'func': lambda kappa, pi: pi - kappa},  # 'com': 'difference between kappa and pi',
    },
    'parameter': {
        'apond': {'value': 1,
                  'definition': 'sector-ponderation of production'},
        'CESexp': {'value': 1000},
        'b': {'value': 0.5},
        'epsilonV': {'value': 0.1},
        'chiv': {'value': 0},
        'chiV': {'value': 0},
        'chiY': {'value': 0},
        'inflation': {'value': 0},
        'Phi0': {'value': -0.1010101},
        'Phi1': {'value': 0.0010101},
    },
}

##########################################################################
Dimensions = {
    'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W','omegaAGG',
               'alpha', 'Nprod', 'Phillips', 'rDh', 'gammai',
               'n', 'ibasket', 'Dh', 'flambda', 'Phi0', 'Phi1'],
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
    Given the value of parameters (Gamma,Xi,Cpond,delta,nu,p,a,w),
    Find the vector of capital that ensure dotV=0 at the first iteration, only for a GOODWIN.
    You can then multiply it in order to have the right GDP or employment
    '''
    from scipy.optimize import fsolve

    def dotV(K, params):
        Gamma = np.array(params['Gamma'])
        Xi = np.array(params['Xi'])
        Cpond = np.array(params['Cpond'])
        delta = np.array(params['delta']) + 0 * K
        A = np.array(params['A']) + 0 * K
        p = np.array(params['p']) + 0 * K
        a = np.array(params['a']) + 0 * K
        w = np.array(params['w']) + 0 * K

        # Deriving equations
        Y = K * A
        L = K / a
        Inter = np.matmul(np.transpose(Gamma), Y)
        C = Cpond * sum(w * L) / p
        Pi = p * Y
        Pi -= w * L
        Pi -= Y * np.matmul(Gamma, p)
        Pi -= delta * K * np.matmul(Xi, p)
        Ir = Pi / (np.matmul(Xi, p)) + K * delta

        # Returning dotV
        return Y - Inter - C - np.matmul(np.transpose(Xi), Ir)
    K = fsolve(dotV, np.array([1.] * len(params['Nprod'])), args=params)
    return K


def generategoodwin(Nsect, gamma=0.1, xi=1):
    '''Generate a dfields to generate N Goodwin in parrallel, at equilibrium'''
    GOODWIN_PRESET = {
        # Numerical values
        'Tsim': 100., 'Tini': 0., 'dt': 0.1,
        'Nprod': [''],

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

        'Cpond': 1.,
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
    GOODWIN_N['Cpond'] = 1 / Nsect

    # useful statevar for calculation that will not be loaded in set_fields
    GOODWIN_N['a'] = GOODWIN_N['a0'] * GOODWIN_N['apond']
    GOODWIN_N['w'] = GOODWIN_N['w0'] * GOODWIN_N['z']

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
        omega = dic['w0'] * dic['z'] * nu / (dic['a0'] * dic['apond'] * p)
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
def PiRepartition(hub, tini=False, tend=False, returnFig=True):
    '''Plot the relative profit repartition for each sector'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT.repartition(hub,
                               ['pi', 'omega', 'Mxi', 'Mgamma', 'rd', 'reloverinvest', 'reldotv'],
                               sign=[1, 1, 1, 1, 1, 1, -1],
                               sector=sector,
                               title=f'Expected relative budget $\pi$ for sector {sector}',
                               tini=tini,
                               tend=tend,
                               returnFig=returnFig)


def PhysicalFluxes(hub, tini=False, tend=False, returnFig=True):
    '''Plot the physical fluxes for each sector'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT.repartition(hub,
                               ['dotV', 'Minter', 'Minvest', 'C'],
                               ref='Y',
                               stock='V',
                               sector=sector,
                               title=f'Physical Fluxes for sector {sector}',
                               tini=tini,
                               tend=tend,
                               returnFig=returnFig)


def MonetaryFluxes(hub, tini=False, tend=False, returnFig=True):
    '''Plot monetary fluxes for each sectore'''
    for sector in hub.dfields['Nprod']['list']:
        hub._DPLOT.repartition(hub,
                               ['MtransactY', 'MtransactI', 'wL', 'pC', 'rD'],
                               sign=[1, 1, 1, -1, 1],
                               ref='dotD',
                               sector=sector,
                               title=f'Monetary Fluxes for sector {sector}',
                               removetranspose=True,
                               tini=tini,
                               tend=tend,
                               returnFig=returnFig)


def Generate_LinksNodes_CHIMES(hub, Matrices, Vectors, Scalars, idt0=0, idt1=-1, coloroffset=0):
    from chimes.plots.tools._plot_tools import value

    R = hub.get_dfields()
    Nodes = []
    Links0 = []
    color = coloroffset
    for m in Matrices:
        for i, sect1 in enumerate(R[R[m]['size'][0]]['list']):
            V = value(R, m, idt0, idt1, ms1=i, ms2=True)
            for j, sect2 in enumerate(R[R[m]['size'][1]]['list']):
                Links0.append([m, V[:, j], sect1, sect2, color])
                if sect2 not in Nodes:
                    Nodes.append(sect2)
            if sect1 not in Nodes:
                Nodes.append(sect1)
        color += 1

    for v in Vectors:
        V = value(R, v[0], idt0, idt1, ms1=True, ms2=0)
        if v[-1]:
            V *= -1
        for i, sect in enumerate(R[R[v[0]]['size'][0]]['list']):
            Links0.append([v[1], V[:, i], sect, v[2], color])
            if sect not in Nodes:
                Nodes.append(sect)
            if v[2] not in Nodes:
                Nodes.append(v[2])
        color += 1

    for s in Scalars:
        V = value(R, s[0], idt0, idt1)
        if s[-1]:
            V *= -1
        Links0.append([s[3], V, s[1], s[2], color])
        if s[1] not in Nodes:
            Nodes.append(s[1])
        if s[2] not in Nodes:
            Nodes.append(s[2])
        color += 1

    Nodes = {k: i for i, k in enumerate(Nodes)}

    Links0 = [[L[0], L[1], Nodes[L[2]], Nodes[L[3]], L[4]] for L in Links0]
    return Nodes, Links0


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
    'Generate_LinksNodes_CHIMES': Generate_LinksNodes_CHIMES,
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

    'sigma': [1, 5, 5],
    'K': [2.1, 0.4, 0.4],
    'D': [0, 0, 0],
    'u': [.95, .95, .95],
    'p': [1, 1, 1],
    'V': [1, 1, 1],
    'z': 1,
    'k0': 1.,
    'Cpond': [1, 0, 0],
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

    'z': [1],  # ,1],
    'apond': [1],  # ,1],
    'k0': 1.,

    'Cpond': [1],  # ,0],

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
