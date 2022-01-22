# -*- coding: utf-8 -*-
"""
DESCRIPTION : This is a Goodwin model based on extensive variables.
Inflation not integrated to the process
TYPICAL BEHAVIOR : Convergence toward solow point ( good equilibrium) or debt crisis
LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""


import numpy as np


# ---------------------------
# user-defined function order (optional)


# -------------------------
# intermediate utility func


def _domega_on_omega(eta=1, phillips=1, alpha=0.1):
    return (eta / (1 + eta)) * (phillips - alpha)


def _term1(kappa=1, A=1, b=1, eta=1, omega=0.1):
    return kappa * A * ((1-omega) / b)**(1./eta)


def _term2(eta=1, phillips=1, alpha=0.1, omega=0.1):
    omegadotomega = _domega_on_omega(eta=eta, phillips=phillips, alpha=alpha)
    return omegadotomega / (eta * (1 - omega))


# ---
# ode
def func_ode_lambda(
    itself=1, kappa=1, A=1, omega=0.1, b=1, eta=1,
    delta=1, alpha=0.1, n=1, phillips=1,
):
    term1 = _term1(kappa=kappa, A=A, b=b, eta=eta, omega=omega)
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return itself * (term1 - delta - alpha - n - term2)

def func_ode_d(
    itself=1,
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
    term1 = _term1(kappa=kappa, A=A, b=b, eta=eta, omega=omega)
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return itself * (r - term1 + delta + term2) + kappa - (1 - omega)


# ---------------
# state variables


def func_g(kappa=1, A=1, b=1, eta=1, phillips=1, alpha=0.1, omega=0.1, delta=1):
    term1 = _term1(kappa=kappa, A=A, b=b, eta=eta, omega=omega)
    term2 = _term2(eta=eta, phillips=phillips, alpha=alpha, omega=omega)
    return term1 - delta - term2


def func_phillips_expo(phi0=0, phi1=0, phi2=0, lamb=0):
    return phi0 + phi1 * np.exp(phi2 * lamb)

def func_phillips_div(phi0=0, phi1=0, phi2=0, lamb=0):
    return -phi0 + phi1 / (1 - lamb)**2


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
        },
        'd': {
            'func': func_ode_d,
        },

        # Not needed for computation
        'N': {
            'func': lambda itself=0, n=1: itself * n,
            'com' : 'exogenous pop for extensive behaviour',
        },
        'K': {
            'func': lambda g=0, itself=0: itself * g,
        },
        'a': {
            'func': lambda alpha=0, itself=0: itself * alpha,
            }
    },

    # Intermediary relevant functions
    'statevar': {

        # Needed for computation
        'phillips': {
            'func': func_phillips_expo,
            'com': 'Exponential curve',
        },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, pi=0: k0 + k1 * np.exp(k2 * pi),
            'com': 'Exponential curve',
        },
        'pi': {
            'func': lambda omega=1, r=1, d=1: 1 - omega - r*d,
            'com': 'relative profit',
        },

        # Not needed for computation
        'Y': {
            'func': lambda A=1, b=0.5, K=1, L=1, a=1, eta=1: A*(b*K**(-eta) + (1 - b)*(L * a)**(-eta))**(-1./eta),
            #'func': lambda K=0,nu=1 : K/nu,
            'com': "CES production function"
        },
        'L': {
            'func': lambda lamb=0, N=0: lamb*N,
            'com': 'Calculated implictely from lambda'
        },
        'g': {
            'func': func_g,
            'com': 'relative growth rate',
        },
        'nu': {
            'func': lambda omega=0.1, b=1, A=1, eta=1: ((1 - omega) / b)**(-1./eta) / A,
            'com': 'Explicit expression',
        },
    },
    'param': {
        'A': { 'value' : 1/2.7,
               'definition': 'Efficiency in CES prod',
        },
        'b': { 'value' : 0.5,
               'definition': 'part of capital in prod intensity',
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
            'phi0': -0.01,
            'phi1': 2.35e-23,
            'phi2': 50,
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
