
"""
Canonical Monosectorial Gemmes model, with no climate.

This model is mostly taken from : https://www.overleaf.com/read/wrxcvrkwpgfm


"""
import numpy as np

_FUNC_ORDER = None


_LOGICS = {
    # FIELDS DEFINED BY ODE
    'differential': {
        # Household properties
        'H': {
            'func': lambda C, deltah, H, rho: C - deltah * H - np.matmul(rho, H),
            'com': 'Household capital accumulation'},
        'a': {
            'func': lambda a, alpha: a * alpha,
            'com': 'Exogenous productivity increase'},
        'N': {
            'func': lambda N, n: N * n,
            'com': 'Exogenous Population increase'},
        'Dh': {
            'func': lambda Dh, w, L, r, p, C: -w * L + r * Dh + C * p,
            'com': 'Stock-flow on household, no share/bank profits'},
        'w': {
            'func': lambda w, phillips, gammai, inflation: (phillips + gammai * inflation) * w,
            'com': 'Philips negociation'},

        # Sector properties
        'K': {
            'func': lambda Ir, delta, K: Ir - delta * K,
            'com': 'Productive capital accumulation'},
        'u': {
            'func': lambda u, sigma, pi, dotV, V: (1 - u) * sigma * dotV / V,
            'com': 'Rate of utilisation adjustment'},
        'V': {
            'func': lambda dotV: dotV,
            'com': 'inventory logic moved in dotV'},
        'p': {
            'func': lambda p, i: p * i,
            'com': 'price from inflation'},
        'D': {
            'func': lambda r, D, w, L, C, p: r * D + w * L - C * p,
            'com': 'Stock-flow on household, no share/bank profits'},
    },



    # FIELDS DEFINED BY OTHER VARIABLES
    'statevar': {

        # Production function related quantities
        'Y': {
            'func': lambda u, K, nu: u * K / nu,
            'com': 'Production Leontiev optimised with use'},
        'L': {
            'func': lambda Y, a: Y / a,
            'com': 'Amount of workers from leontiev'},
        'dotV': {
            'func': lambda Y, gamma, C, Xi, Ir: Y - gamma * Y - C - Xi * Ir,
            'com': "Stock-flow Inventory evolution"},
        # HOUSEHOLD INTERMEDIARY CHARACTERISTICS
        'employment': {
            'func': lambda L, N: L / N,
            'com': 'employement rate'},
        'omega': {
            'func': lambda w, L, p, Y: w * L / (p * Y),
            'com': 'wage share'},

        # CONSUMPTION RELATED PROPERTIES
        'C': {
            'func': lambda Hid, H, fC, rho: (Hid - H) * fC + np.matmul(rho, H),
            'com': 'consumption to rectify possession+its consumption'},
        'Hid': {

            'func': lambda N, h, x, w, p, Omega0: N * h * (1 + np.exp(-x * (w / p) - Omega0))**-1,
            'com': 'Ideal Possession from logistic on salary'},
        'Omega': {

            'func': lambda w, p, employment, L, r, D: employment * (w / p + r * D / (p * L)),
            'com': 'Purchasing power'},

        # INTERMEDIARY PRICE AND DIMENSIONLESS VARIABLES ###
        'pi': {
            'func': lambda c, p, r, d: 1 - c / p - r * d,
            'com': "relative profit with intermediary consumption"},
        'c': {
            'func': lambda w, a, gamma, p: w / a + gamma * p,
            'com': 'unitary cost of creation'},

        # Behavioral functions
        'i': {
            'func': lambda eta, mu, c, p, chi, dotV, V: eta * (mu * c / p - 1) + chi * (dotV / V),
            'com': 'inflation by markup and demand'},
        'kappa': {
            'func': lambda k0, k1, k2, pi: k0 + k1 * np.exp(k2 * pi),
            'com': 'Relative GDP investment through relative profit'},
        'phillips': {
            'func': lambda phi0, phi1, employment: (-phi0 + phi1 / (1 - employment)**2),
            'com': 'Wage increase rate through employement and profit'},


        # Investment handling
        'I': {
            'func': lambda p, Y, kappa, u: p * Y * kappa / (1 - u),
            'com': 'employement rate'},
        'Ir': {
            'func': lambda I, Xi, p: I / (Xi * p),
            'com': 'From monetary to real unit'},
    },
    'parameter': {},
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {}
