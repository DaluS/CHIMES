# -*- coding: utf-8 -*-
"""
Canonical Monosectorial Gemmes model, with no climate.

This model is mostly taken from : https://www.overleaf.com/read/wrxcvrkwpgfm


"""
import numpy as np

_FUNC_ORDER = None


_LOGICS = {
    # FIELDS DEFINED BY ODE
    'ode': {
        # Household properties
        'H': {'func': lambda C=0, deltah=0, itself=0, rho=0: C - deltah*itself - rho*itself,
              'com': 'Household capital accumulation'},
        'a': {'func': lambda itself=0, alpha=0: itself*alpha,
              'com': 'Exogenous productivity increase'},
        'N': {'func': lambda itself=0, beta=0: itself*beta,
              'com': 'Exogenous Population increase'},
        'Dh': {'func': lambda itself=0, w=0, L=0, r=0, p=0, C=0: -w*L + r*itself + C*p,
               'com': 'Stock-flow on household, no share/bank profits'},
        'w': {'func': lambda itself=0, phillips=0, gammai=0, i=0: (phillips+gammai*i)*itself,
              'com': 'Philips negociation'},

        # Sector properties
        'K': {'func': lambda Ir=0, delta=0, itself=0: Ir - delta*itself,
              'com': 'Productive capital accumulation'},
        'u': {'func': lambda itself=0, sigma=0, pi=0, dotV=0, V=1: (1-itself)*sigma*dotV/V,
              'com': 'Rate of utilisation adjustment'},
        'V': {'func': lambda dotV=0: dotV,
              'com': 'inventory logic moved in dotV'},
        'p': {'func': lambda itself=0, i=0: itself*i,
              'com': 'price from inflation'},
        'D': {'func': lambda r=0, itself=0, w=0, L=0, I=0, Y=0, p=0, gamma=0, C=0, Xi=0, Ir=0, : r*itself + w*L + I + Y*p*gamma-C*p - p*(Xi * Ir + gamma*Y),
              'com': 'Stock-flow on household, no share/bank profits'},
    },



    # FIELDS DEFINED BY OTHER VARIABLES
    'statevar': {

        # Production function related quantities
        'Y': {'func': lambda u=0, K=0, nu=1: u*K/nu,
              'com': 'Production Leontiev optimised with use'},
        'L': {'func': lambda Y=0, a=1: Y/a,
              'com': 'Amount of workers from leontiev'},
        'dotV': {'func': lambda Y=0, gamma=0, C=0, Xi=0, Ir=0: Y-gamma*Y-C-Xi*Ir,
                 'com': "Stock-flow Inventory evolution"},

        # HOUSEHOLD INTERMEDIARY CHARACTERISTICS
        'lambda': {'func': lambda L=0, N=1: L/N,
                   'com': 'employement rate'},
        'omega': {'func': lambda w=0, L=0, p=1, Y=1: w*L/(p*Y),
                  'com': 'wage share'},

        # CONSUMPTION RELATED PROPERTIES
        'C': {'func': lambda Hid=0, H=0, fC=1, rho=0: (Hid-H)*fC + rho*H,
              'com': 'consumption to rectify possession+its consumption'},
        'Hid': {'func': lambda N=0, h=0, x=0, w=0, p=1, Omega0=0: N*h*(1+np.exp(-x*(w/p) - Omega0))**-1,
                'com': 'Ideal Possession from logistic on salary'},
        'Omega': {'func': lambda w=0, p=1, lamb=0, L=1, r=0, D=0: lamb*(w/p + r*D/(p*L)),
                  'com': 'Purchasing power'},

        # INTERMEDIARY PRICE AND DIMENSIONLESS VARIABLES ###
        'pi': {'func': lambda c=0, p=1, r=0, d=0: 1 - c/p - r*d,
               'com': "relative profit with intermediary consumption"},
        'c': {'func': lambda w=0, a=1, gamma=0, p=0: w/a + gamma*p,
              'com': 'unitary cost of creation'},

        # Behavioral functions
        'i': {'func': lambda eta=0, mu=0, c=0, p=1, chi=0, dotV=0, V=1: eta*(mu*c/p - 1) + chi * (dotV/V),
              'com': 'inflation by markup and demand'},
        'kappa': {'func': lambda k0=0, k1=0, k2=0, pi=0: k0 + k1 * np.exp(k2 * pi),
                  'com': 'Relative GDP investment through relative profit', },
        'phillips': {'func': lambda phi0=0, phi1=0, lamb=0:  (-phi0 + phi1 / (1 - lamb)**2),
                     'com': 'Wage increase rate through employement and profit', },


        # Investment handling
        'I': {'func': lambda p=0, Y=0, kappa=0, u=0: p*Y*kappa/(1-u),
              'com': 'employement rate'},
        'Ir': {'func': lambda I=0, Xi=1, p=1: I/(Xi*p),
               'com': 'From monetary to real unit'},


    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
