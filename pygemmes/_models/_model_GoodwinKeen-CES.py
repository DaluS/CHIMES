# -*- coding: utf-8 -*-
import numpy as np
"""
DESCRIPTION :
    * 2 sector model ( Household and Firms ) with loans.
    * The structure is the same as in a Goodwin-Keen typical models
    * Productiob function has been substituted from an optimised Leontiev to a CES (Constant Elasticity of substitution)
    * In consequence the optimisation problem makes the quantity of workers a function of wage share

This is the reduced version : the dynamical variables are lambda,omega,d

TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


class Phillips:
    """
    The Phillips function is linking the relative wage share increase rate to the
    employement.
    The phenomena behind is a class struggle
    """

    def expo(lamb=0,
             phiexp0=0,
             phiexp1=0,
             phiexp2=0,
             ):
        '''
        From article :
        '''
        return phiexp0 + phiexp1 * np.exp(phiexp2 * lamb)

    def div(lamb=0,
            phi0=0,
            phi1=0,
            phi2=0,
            ):
        '''
        From article :
        '''
        return -phi0 + phi1 / (1 - lamb)**2

    def lin(lamb=0,
            philinConst=0,
            philinSlope=0,
            ):
        '''
        From article :
        '''
        return philinConst + philinSlope * lamb,


class kappa:
    """
    The kappa function is linking the relative profit to the share of GDP a firm
    will invest in new productive capital

    It is taking into account both the willingness of bankers to gives loans, and
    the will of the firm to ask for such loan
    """

    def lin(pi=0,
            kappalinConst=0,
            kappalinSlope=0):
        '''
        From article :
        '''
        return kappalinConst + kappalinConst * pi

    def exp(pi=0,
            k0=0,
            k1=0,
            k2=0,):
        '''
        From article :
        '''
        return k0 + k1 * np.exp(k2 * pi)


class productionYL:
    """
    Production functions are the output to input factors.

    """
    leontiev = lambda b=0.5,a=0,L=0,K=0,nu=1: 2*np.minimun((b*K/nu,(1-b)*a*L))
    leontiev_optimised = lambda K=0,nu=1: K/nu
    leontiev_labor_optimal = lambda b=0.5,a=0,L=0,K=0,nu=1: K*b/((1-b)*(a*nu))

    CES = lambda A=1, b=0.5, K=1, L=1, a=1, eta=1: A*(b*K**(-eta) + (1 - b)*(L * a)**(-eta))**(-1./eta)
    CES_nu_optimal = lambda omega=0.1, b=1, A=1, eta=1: ((1 - omega) / b)**(-1./eta) / A
    CES_labord_optimal = lambda eta=0 : 0

class productivity:
    """
    Productivity is the "human power" in production function, the ponderation of each unit
    """
    prod_exogenous = lambda itself=0, alpha=0 : itself*alpha
    prod_Verdoorn = lambda itself=0, g=0, alpha=0, beta=0: itself * alpha + g * beta

class shareholding:
    """
    Shareholding is the share of GDP going from the firm to the shareowner
    """
    def sharehold_lin(divlinSlope=0, divlinconst=0, pi=0):
        """
        From article :
        """
        return (divlinSlope*pi+divlinconst)

# -------------------------
# intermediate utility func


def _domega_on_omega(eta=1, phillips=1, alpha=0.1):
    return (eta / (1 + eta)) * (phillips - alpha)


def _term2(eta=1, phillips=1, alpha=0.1, omega=0.1):
    omegadotomega = _domega_on_omega(eta=eta, phillips=phillips, alpha=alpha)
    return omegadotomega / (eta * (1 - omega))


# ---
# ode
def func_ode_lambda(
    itself=1,
    kappa=1,
    nu=1,
    A=1,
    omega=0.1,
    b=1,
    eta=1,
    delta=1,
    alpha=0.1,
    n=1,
    phillips=1,
):
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return itself * (kappa/nu - delta - alpha - n - term2)


def func_ode_d(
    itself=1,
    nu=1,
    r=1,
    kappa=1,
    A=1,
    omega=0.1,
    b=1,
    eta=1,
    delta=1,
    phillips=1,
    alpha=0.1,
):
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return itself * (r - kappa/nu + delta + term2) + kappa - (1 - omega)


# ---------------
# state variables


def func_g(kappa=1, nu=1, A=1, b=1, eta=1, phillips=1, alpha=0.1, omega=0.1, delta=1):
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return kappa/nu - delta - term2


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'omega': {
            'func': lambda itself=1, eta=1, phillips=1, alpha=0.1 : itself * (eta / (1 + eta)) * (phillips - alpha),
            'com' : 'Explicit reduced dynamics'
        },
        'lambda': {
            'func': func_ode_lambda,
            'com' : "explicit reduced dynamics"
        },
        'd': {
            'func': func_ode_d,
            'com' : "explicit reduced dynamics"
        },

        # Not needed for computation
        'N': {
            'func': lambda itself=0, n=1: itself * n,
            'com' : 'exogenous pop for extensive behaviour',
        },
        'K': {
            'func': lambda g=0, itself=0: itself * g,
            'com' : 'auxilliary from growth'
        },
        'a': {
            'func': lambda alpha=0, itself=0: itself * alpha,
            'com' : 'auxilliary'
            }
    },

    # Intermediary relevant functions
    'statevar': {

        # Needed for computation
        'phillips': {
            'func': Phillips.expo,.
            'com': 'Exponential curve',
        },
        'kappa': {
            'func': kappa.exp,
            'com': 'Exponential curve',
        },
        'pi': {
            'func': lambda omega=1, r=1, d=1: 1 - omega - r*d,
            'com': 'as defined',
        },

        # Not needed for computation
        'Y': {
            'func': productionYL.CES,
            'com': "Auxilliary CES"
        },
        'L': {
            'func': lambda lamb=0, N=0: lamb*N,
            'com': 'Auxilliary forn lambda'
        },
        'g': {
            'func': func_g,
            'com': 'explicit exoression',
        },
        'nu': {
            'func': lambda omega=0.1, b=1, A=1, eta=1: ((1 - omega) / b)**(-1./eta) / A,
            'com': 'Explicit expression from optimal',
        },
    },
    'param': {
        ### PARAMETERS IN THE CES FUNCTION
        'A': {
            'value' : 1/3.,
            'definition': 'Efficiency in CES prod',
        },
        'b': {
            'value' : 0.5,
            'definition': 'part of capital in prod intensity',
        },

        ### PARAMTERS IN THE EXPONENTIAL PHILLIPS
        'phiexp0': {
            'value' : -0.01,
            'definition': 'Constant in expo phillips',
        },
        'phiexp1':{
            'value' : 0.5,
            'definition': 'slope in expo phillips',
        },
        'phiexp2':{
            'value' : 50,
            'definition': 'exponent in expo phillips',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'article_fig01-05': {
        'fields': {
            'dt': 0.1,
            'Tmax': 200,
            'eta': [500, 100],
            'phiexp0': -0.01,
            'phiexp1': 2.35e-23,
            'phiexp2': 50,
            'k0': 0.05,
            'k1': 0.05,
            'k2': 1.75,
            'n': 0.01,   # 'n' in _def_fields
            'delta': 0.01,
            'r': 0.04,
            'A': 1./3.,
            'b': 0.135,
            # initial ode values
            'lambda': 0.96,
            'omega': 0.65,
            'd': 2.94,
        },
        'com': '',
        'plots': [],
    },
}
