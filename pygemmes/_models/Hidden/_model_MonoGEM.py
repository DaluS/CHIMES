# -*- coding: utf-8 -*-
"""
Canonical Monosectorial Gemmes model, with no climate.

This model is mostly taken from : https://www.overleaf.com/read/wrxcvrkwpgfm


"""
import numpy as np
from pygemmes._models import Funcs


_LOGICS_MONOGEM = {
    # FIELDS DEFINED BY ODE
    'ode': {

        'a': Funcs.Productivity.verdoorn,
        'N': Funcs.Population.exp,
        'w': Funcs.Phillips.salaryfromPhillipsProfits,
        'K': Funcs.Kappa.kfromIr,
        'p': Funcs.Inflation.pricefrominflation,

        # Stock-flow consistency
        'Dh': {
            'func': lambda itself=0, w=0, L=0, r=0, p=0, C=0: -w*L + r*itself + C*p,
            'com': 'Stock-flow on household, no share/bank profits'},
        'D': {
            'func': lambda r=0, itself=0, w=0, L=0, G=0, p=0: r*itself + w*L - G*p,
            'com': 'Stock-flow on household, no share/bank profits'},
        'V': {
            'func': lambda dotV=0:  dotV,
            'com': 'inventory logic moved in dotV'},
        'H': {
            'func': lambda C=0, deltah=0, itself=0, rho=0: C - deltah*itself - rho*itself,
            'com': 'Household capital accumulation'},

        # Sector properties
        'u': {
            'func': lambda itself=0, sigma=0, pi=0, dotV=0, V=1, c=1, p=0: (1-itself)*(1-p/c)*sigma*dotV/V,
            'com': 'Rate of utilisation adjustment'},


    },


    # FIELDS DEFINED BY OTHER VARIABLES
    'statevar': {
        # Stock-Flux related
        'Pi': {
            'func': lambda p=0,Y=0, w=0,L=0,C=0,Gamma=0,r=0,D=0 : p*Y*(1-Gamma)-w*L+p*C-r*D,
            'com': 'Explicit flux Mono'},
        'dotV': {
            'func': lambda Y=0, gamma=0, G=0, Xi=0, Ir=0: Y-gamma*Y-G-Xi*Ir,
            'com': "Stock-flow Inventory evolution"},
        'c': {
            'func': lambda w=0, a=1, gamma=0, p=0:  w/a + gamma*p,
            'com': 'unitary cost of creation'},

        # Production function and its employement
        'Y': Funcs.ProductionWorkers.Leontiev_Optimised.Y,
        'L': Funcs.ProductionWorkers.Leontiev_Optimised.L,

        # Parametric curve
        'phillips': Funcs.Phillips.div,
        'kappa': Funcs.Kappa.exp,

        # HOUSEHOLD INTERMEDIARY CHARACTERISTICS
        'pi': Funcs.Definitions.pi,
        'lambda': Funcs.Definitions.lamb,
        'omega': Funcs.Definitions.omega,
        'GDP': Funcs.Definitions.GDPmonosec,
        'd': Funcs.Definitions.d,

        # CONSUMPTION RELATED PROPERTIES
        'C': {
            'func': lambda Hid=0, H=0, fC=1, rho=0: (Hid-H)*fC + rho*H,
            'com': 'consumption to rectify possession+its consumption'},
        'Hid': {
            'func': lambda N=0, h=0, x=0, w=0, p=1, Omega0=0: N*h*(1+np.exp(-x*(w/p) - Omega0))**-1,
            'com': 'Ideal Possession from logistic on salary'},
        'Omega': {
            'func': lambda w=0, p=1, lamb=0, L=1, r=0, D=0: lamb*(w/p + r*D/(p*L)),
            'com': 'Purchasing power'},

        # Behavioral functions
        'inflation': {
            'func': lambda eta=0, mu=0, c=0, p=1, chi=0, dotV=0, V=1: eta*(mu*c/p - 1) + chi * (dotV/V),
            'com': 'inflation by markup and demand'},

        # Investment handling
        'I': {
            'func': lambda p=0, Y=0, kappa=0, u=0: p*Y*kappa/(1-u),
            'com': 'employement rate'},
        'Ir': {
            'func': lambda I=0, Xi=1, p=1: I/(Xi*p),
            'com': 'From monetary to real unit'},


    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
