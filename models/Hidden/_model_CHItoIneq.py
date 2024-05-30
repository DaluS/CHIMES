"""Three output-green-brown capital dynamics"""

from chimes.libraries import Funcs, importmodel, merge_model
from chimes.libraries import Operators as O
import numpy as np
_DESCRIPTION = """
Three types of capital:
* output goods for consumption and investment
* green energy to feed output capital
* brown energy to feed output capital, with different technical coefficients

* **Article :**
* **Author  :**
* **Coder   :**
"""


_LOGICS = {
    'differential': {
        'Ky': {
            'func': lambda Ky, Iy, deltay: Iy - deltay * Ky,
            'units': 'Units',
            'initial': 1.9},
        'Kg': {
            'func': lambda Kg, deltag, Ig: Ig - deltag * Kg,
            'units': 'Units',
            'initial': 0.1},
        'Kb': {
            'func': lambda Kb, deltab, Ib: Ib - deltab * Kb,
            'units': 'Units',
            'initial': .6},

        'V': {'func': lambda Y, C, I: Y - C - I},

        # Debts
        'D': {'func': lambda r, D, w, L, Delta, Pi, C, p: r * D + w * L + Delta * Pi - C * p,
              'initial': 0},
        'Dc': {'func': lambda r, D, Delta, Pi, Cc, p: -r * D - Delta * Pi + Cc,
               'initial': 0,
               'units': '$'},

        # 3-sector productivity
        'ay': {
            'func': lambda ay, alphay: ay * alphay,
            'units': 'Humans.Units^{-1}',
            'initial': 3},
        'ag': {
            'func': lambda ag, alphag: ag * alphag,
            'units': 'Humans.Units^{-1}',
            'initial': 3},
        'ab': {
            'func': lambda ab, alphab: ab * alphab,
            'units': 'Humans.Units^{-1}',
            'initial': 3},

        # 2-sector Population
        'Nw': {
            'func': lambda Nw, nw: Nw * nw,
            'units': 'Humans',
            'initial': .5},
        'Nc': {
            'func': lambda Nc, nc: Nc * nc,
            'units': 'Humans',
            'initial': .5},

        # Wage-price
        'p': {'func': lambda p, inflation: p * inflation},
        'w': {'func': lambda w, phillips: w * phillips,
              'initial': 0.75},

        # investment allocation
        'epsilony': {'func': lambda sigmay, epsilony, uE: sigmay * epsilony * (1 - epsilony) * (1 - uE),
                     'initial': .5,
                     'units': ''}
    },

    'statevar': {

        # Monosectoral
        'K': {'func': lambda Ky, Kb, Kg: Ky + Kb + Kg},
        'N': {'func': lambda Nc, Nw: Nc + Nw,
              'com': 'Sum of both population'},
        'L': {'func': lambda Ky, ay, Kb, ab, Kg, ag: Ky / ay + Kb / ab + Kg / ag},
        # 'L': {'func': lambda Ky,ay: Ky/ay},
        'a': {'func': lambda K, L: K / L},
        'nu': {'func': lambda K, Y: K / Y},
        'prod': {'func': lambda Y, L: Y / L,
                 'units': 'Units.Humans^{-1}.y^{-1}'},

        # Bonus: Endogenous green technology
        'Ag': lambda Kg: .9 * (Kg / 0.1)**(0.2),

        # Energy
        'E': {'func': lambda Ab, Ag, Kb, Kg: Ab * Kb + Ag * Kg},
        'uE': {'func': lambda Ky, E: Ky / E,
               'units': ''},
        'Emission': {'func': lambda Kb, sigmab: Kb * sigmab,
                     },

        # Investment
        'I': {'func': lambda Y, C: Y - C,
              'units': 'Units.y^{-1}'},
        'Iy': {
            'func': lambda I, epsilony: I * epsilony,
            'units': '$.y^{-1}', },
        'Ig': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * epsilong,
            'units': '$.y^{-1}', },
        'Ib': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * (1 - epsilong),
            'units': '$.y^{-1}', },

        # Nominal consumption
        'Cc': {
            'func': lambda r, D, Delta, Pi, kappaC: kappaC * (r * D + Delta * Pi),
            'units': '$.y^{-1}', },
        'Cw': {
            'func': lambda w, L, : w * L,
            'units': '$.y^{-1}', },
        'Cn': {
            'func': lambda Cc, Cw: Cc + Cw,
            'units': '$.y^{-1}', },
        'C': {'func': lambda Cn, p: Cn / p},

        # local returns on capital
        'rocb': {'func': lambda Ab, w, p, ab, deltab: Ab - w / (p * ab) - deltab},
        'rocg': {'func': lambda Ag, w, p, ag, deltag: 2},
        # Ag-w/(p*ag)-deltag },
        'droc': lambda rocb, rocg: rocg / rocb,

        # Allocation
        # 'epsilony': {
        #    'func': lambda :.5,
        #    #epsilony,
        #    'units':''},
        'epsilong': {
            'func': lambda rocg, rocb, zi, zg: .5 * (1 + np.tanh(zi * (rocg - rocb - zg))),
            'units': ''},

        # PHYSICAL FLOW
        'Pi': {'func': lambda p, Y, w, L, deltab, Kb, deltag, Kg, deltay, Ky, r, D: p * Y - w * L - p * (deltab * Kb + deltag * Kg + deltay * Ky) - r * D},
        'Y': {'func': lambda Ay, Ky, uE, CESexp: Ay * Ky},  # *(1+(1/uE)**(-CESexp))**(-1/CESexp)},

        # Classics
        'employment': {'func': lambda L, N: L / N},
        'phillips': {'func': lambda Phi0, Phi1, flambda: Phi0 + 10 * Phi1 * flambda},
        'flambda': {'func': lambda employment: .1 / (1 - employment)**2},

        'omega': {'func': lambda w, L, p, Y: w * L / (p * Y)},
        'd': {'func': lambda D, p, Y: D / (p * Y)},
        'pi': {'func': lambda Pi, p, Y: Pi / (p * Y)},
        'g': {'func': lambda Iy, deltay, Ky: Iy / Ky - deltay},
        'ROC': {'func': lambda Pi, K, p: Pi / (p * K)},
        'inflation': {'func': lambda ROC0, ROC, finflation: finflation * np.log(ROC0 / ROC)}
        # 'Solvability': {'func': lambda D,K,Xi,p: 1- D/(K*Xi*p)},
        # 'c': {'func': lambda p,omega,Gamma,nu,delta,Xi: p*(omega+Gamma+nu*delta*Xi)},
        # 'mu': {'func': lambda p,c: p/c},
        # 'GDPn': {'func': lambda p,Y,Gamma: p*Y*(1-Gamma)},
        # 'GDP': {'func': lambda Y,Gamma: Y*(1-Gamma)},
        # 'omegaeq': {'func': lambda Gamma,nu,delta,Xi,alpha,n,Delta: 1-Gamma-nu*Xi*delta-nu*Xi*(alpha+n)/(1-Delta),
        #          'symbol':r'$\omega_{eq}$'},
    },

    'parameter': {

        'inflation': 0.01,

        'alphab': 0.025,
        'alphag': 0.085,
        'alphay': 0.025,

        'deltay': 0.05,
        'deltab': 0.05,
        'deltag': 0.05,

        'sigmab': 1,

        'sigmay': 1.5,

        'Ab': 2,
        # 'Ag' : .9,
        'Ay': 1 / 2,

        'Delta': 0.2,

        'finflation': 0.05,
        'ROC0': 0.1,

        'nc': {'value': 0.01},
        'nw': {'value': 0.01},
        'r': {'value': 0.03},
        'delta': {'value': 0.05},
        'Phi0': {'value': -0.1010101},
        'Phi1': {'value': 0.0010101},
        'phialpha': {'value': 0.5},
        'phii': {'value': 0.5},
        # 'inflation' : {'value': 0.03},
        'A': {'value': 0.33},
        'kappaC': {'value': 1},
        # 'kappaI'    : {'value': 1},

        'zi': 2,
        'zg': 0,

    },
    'size': {},
}

_LOGICS_CLIMATE, _PRESETS0, _SUPPLEMENTS = importmodel('Climate_3Layers')
_LOGICS = merge_model(_LOGICS_CLIMATE, _LOGICS, verb=False)
