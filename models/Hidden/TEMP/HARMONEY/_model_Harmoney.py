"""An integrated biophysical and economic modeling framework for long-term
sustainability analysis: the HARMONEY model"""

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O
_DESCRIPTION = """

# NOT FUNCTIONAL (YET)
This paper derives a long-term dynamic growth model that endogenously links biophysical and economic
variables in a stock-flow consistent manner. The two industrial sector HARMONEY (Human And Resources with
MONEY) model enables exploration of interdependencies among resource extraction rate and depletion; the
accumulation of population, capital, and debt; and the distribution of money flows within the economy. Using a
post-Keynesian economic framework, we find that wage share declines after the model reaches a constant per
capita resource extraction rate, with the level of investment and markup on costs determining the rate of decline.
This pattern is consistent with data for the United States.
Thus, the model framework enables realistic investigation of trade-offs between economic distribution,
size, and resources consumption between sectors as well
as between labor and capital. These trade-offs are core to the debates regarding environmental and socioeconomic sustainability.
This model serves as a platform upon which to add features to explore long-term
sustainability questions such as a transition to low-carbon energy.

* **Name :** HARMONEY
* **Article :** https://doi.org/10.1016/j.ecolecon.2019.106464
* **Author  :** Carey King
* **Coder   :** Paul Valcke

* **Supplements description :**

**TODO:**
 Population : population dynamics is not workers dynamics
 Debt dynamics : Written with profit-investment
 Should go deeper into y,g,wh dynamics
 Convergence for inertial variables
 How can inventory move with residual consumption ?!
"""
# ################ IMPORTS ##################################################


def relax(Xt, X, tau):
    '''Subfunction for relaxation dynamics
* X is the relaxed variable,
* Xt is the targed signal
* tau is the relaxation time

To be used in chimes for differential variables:
    $\dot{X}=(Xt-X)/tau$'''
    return (Xt - X) / tau


# ################# ALL THE NEW FIELDS LOGICS ###############################
_LOGICS = {
    'differential': {
        # Traditional wage-pop
        'w': {
            'func': lambda w, phillips: w * phillips,
            'units': '$.Humans^{-1}.y^{-1}',
            'definition': 'Wage per person',
            'com': 'Traditional Phillips dynamics'},
        'N': {
            'func': lambda N, betaN, alphaN, Ce, Pe: N * (betaN - alphaN * Ce / Pe),
            'units': 'Humans',
            'definition': 'Population',
            'com': 'Population dynamics endogenous coefficient'},

        # Capital and debt
        'Ke': {
            'func': lambda Ie, Pg, delta, Ke: Ie / Pg - delta * Ke,
            'units': 'Units',
            'definition': 'Capital for resources extraction',
            'com': 'Capital equation'},
        'Kg': {
            'func': lambda Ig, Pg, delta, Kg: Ig / Pg - delta * Kg,
            'units': 'Units',
            'definition': 'Capital for goods production',
            'com': 'Capital equation'},
        'De': {
            'func': lambda Ie, Pg, delta, Kg, Pie: Ie - Pg * delta * Kg - Pie,
            'units': '$',
            'definition': 'Debts of extraction sectors',
            'com': 'written as profit-investment, not very SFC'},
        'Dg': {
            'func': lambda Ig, Pg, delta, Kg, Pig: Ig - Pg * delta * Kg - Pig,
            'units': '$',
            'definition': 'Debts of  goods sectors',
            'com': 'written as profit-investment, not very SFC'},

        # Relaxation dynamics
        'CUelag': {'func': lambda tauCUe, CUelag, CUe: relax(CUe, CUelag, tauCUe), 'initial': 0},
        'CUglag': {'func': lambda tauCUg, CUglag, CUg: relax(CUg, CUglag, tauCUg), 'initial': 0},

        'ICelag': {'func': lambda tauICe, ICelag, ICe: relax(ICe, ICelag, tauICe), 'initial': 0},
        'ICglag': {'func': lambda tauICg, ICglag, ICg: relax(ICg, ICglag, tauICg), 'initial': 0},

        'Pelag': {'func': lambda tauPe, Pelag, Pe: relax(Pe, Pelag, tauPe), 'initial': 0},
        'Pglag': {'func': lambda tauPg, Pglag, Pg: relax(Pg, Pglag, tauPg), 'initial': 0},

        'Velag': {'func': lambda tauVe, Velag, Ve: relax(Ve, Velag, tauVe), 'initial': 0},
        'Vglag': {'func': lambda tauVg, Vglag, Vg: relax(Vg, Vglag, tauVg), 'initial': 0},

        'Yelag': {'func': lambda tauYe, Yelag, Ye: relax(Ye, Yelag, tauYe), 'initial': 0},
        'Yglag': {'func': lambda tauYg, Yglag, Yg: relax(Yg, Yglag, tauYg), 'initial': 0},

        'Pielag': {'func': lambda tauPie, Pielag, Pie: relax(Pie, Pielag, tauPie), 'initial': 0},
        'Piglag': {'func': lambda tauPig, Piglag, Pig: relax(Pig, Piglag, tauPig), 'initial': 0},

        # HANDY-related variables
        'y': {
            'func': lambda y, gamma, lambday, deltay, Ke, CUe: y * (gamma * (lambday - y) - deltay * Ke * CUe),
            'units': 'Units',
            'definition': 'Resources in the environment',
            'com': 'Pers. not studied'},
        'g': {
            'func': lambda ICe, ICelag, Ce, Pe, aeg, Xg, aee, Xe: (ICe - ICelag) * (Ce / Pe + aeg * Xg + aee * Xe),
            'units': 'Units',
            'definition': 'Physical inventory of goods',
            'com': 'Pers. not studied'},
        'wh': {
            'func': lambda ICg, ICglag, Cg, Ig, Ie, Pg, age, Xe, agg, Xg: (ICg - ICglag) * ((Cg + Ig + Ie) / Pg + age * Xe + agg * Xg),
            'units': 'Units',
            'definition': 'Physical inventory of resources, wealth (per (Motesharrei et al., 2014))',
            'com': 'Pers. not studied'},

    },
    'statevar': {
        # Technical requirements matrix
        'aee': {
            'func': lambda etae, deltay, y: etae / (deltay * y),
            'units': '',
            'definition': 'Resources input required per unit of gross nature extraction'},

        'aeg': {
            'func': lambda etag, yXg, nug: (etag + yXg) * nug,
            'units': '',
            'definition': 'Goods input required per unit of gross resource extraction'},
        # 'agg' CONSTANT
        # 'age' CONSTANT

        # Production
        'nue': {
            'func': lambda deltay, y: 1 / (deltay * y),
            'units': 'y',
            'definition': 'Capital to output ratio for extraction output'},
        # nug exogenous
        'Xe': {
            'func': lambda Ke, CUe, nue: Ke * CUe / nue,
            'units': 'Units.y^{-1}',
            'definition': 'Gross output of extraction sector (= resources extraction)',
            'com': 'Optimized Leontiev'},
        'Xg': {
            'func': lambda Kg, CUg, nug: CUg * Kg / nug,
            'units': 'Units.y^{-1}',
            'definition': 'Gross output of goods sector (= goods production)',
            'com': 'Optimized Leontiev'},


        # Labor
        'Le': {
            'func': lambda Ke, CUe, nue, ae: Ke * CUe / (nue, ae),
            'units': 'Humans',
            'definition': 'Labor for resources extraction',
            'com': 'Leontiev use with basic productivity'},
        'Lg': {
            'func': lambda Kg, CUg, nug, ag: Kg * CUg / (nug, ag),
            'units': 'Humans',
            'definition': 'Labor for goods production',
            'com': 'Leontiev use with basic productivity'},
        'lambdaN': {
            'func': lambda Le, Lg, N: (Le + Lg) / N,
            'units': '',
            'definition': 'Participation (employment) rate',
            'com': 'Definition'},
        'phillips': {
            'func': lambda lambdaN, lambdaNo, phi0, phis, phimin: phimin + (phi0 - phimin) * np.exp(phis * (lambdaN - lambdaNo) / (phi0 - phimin)),
            'units': 'y^{-1}',
            'definition': 'wage negociation dynamics',
            'com': 'non-linear exponential phillips'
        },

        # Costs
        'ce': {
            'func': lambda Pe, aee, Pg, age, w, Le, rl, De, delta, Ke, Xe: Pe * aee + Pg * age + (w * Le + rl * De + Pg * delta * Ke) / Xe,
            'units': '$.Unit^{-1}',
            'definition': 'Unit cost of production of extraction sector '},
        'cg': {
            'func': lambda Pg, agg, Pe, aeg, w, Lg, rl, Dg, delta, Kg, Xg: Pg * agg + Pe * aeg + (w * Lg + rl * Dg + Pg * delta * Kg) / Xg,
            'units': '$.Unit^{-1}',
            'definition': 'Unit cost of production of goods sector'},

        # Price
        'Pe': {
            'func': lambda: 0,
            'units': '',
            'definition': 'price of extraction material'},
        'Pg': {
            'func': lambda: 0,
            'units': '',
            'definition': 'price of goods'},

        # Productivity
        'ae': {
            'func': lambda: 1,
            'units': 'Units.Humans^{-1}.y^{-1}',
            'definition': 'Labor productivity of resource extraction sector'},

        'ag': {
            'func': lambda: 1,
            'units': 'Units.Humans^{-1}.y^{-1}',
            'definition': 'Labor productivity of goods sector goods'},

        # Investment
        'I': {
            'func': lambda Ie, Ig: Ie + Ig,
            'units': '$.y^{-1}',
            'definition': 'Total private investment',
            'com': 'definition'},
        'Ie': {
            'func': lambda kappa0, kappa1, Pg, delta, Ke, Pie: np.maximum(0, kappa0 * Pg * delta * Ke + kappa1 * Pie),
            'units': '$.y^{-1}',
            'definition': 'Investment by extraction sector',
            'com': 'kappa linear capped dynamics'},
        'Ig': {
            'func': lambda kappa0, kappa1, Pg, delta, Ke, Pie: np.maximum(0, kappa0 * Pg * delta * Ke + kappa1 * Pie),
            'units': '$.y^{-1}',
            'definition': 'Investment by goods sector',
            'com': 'kappa linear capped dynamics'},
        'Ige': {
            'func': lambda Ie, Pg: Ie / Pg,
            'units': 'Units.y^{-1}',
            'definition': 'Real Investment by extraction sector (by firms)',
            'com': 'definition'},
        'Igg': {
            'func': lambda: 0,
            'units': 'Units.y^{-1}',
            'definition': 'Real Investment by goods sector (by firms)'},

        # Inventory
        'INVe': {
            'func': lambda ce, g: ce * g,
            'units': '$',
            'definition': 'Value of inventory of extraction sector',
            'com': 'inventory nominal value'},
        'INVg': {
            'func': lambda cg, wh: cg * wh,
            'units': '$',
            'definition': 'Value of inventory of goods sector',
            'com': 'inventory nominal value'},
        # Consumption
        'Ce': {
            'func': lambda Ye, DeltaINVe: Ye - DeltaINVe,
            'units': '$.y^{-1}',
            'definition': 'Consumption of extraction sector output by households',
            'com': 'Fully accomodating'},
        'Cg': {
            'func': lambda Yg, Pg, Igg, Ige, DeltaINVg: Yg - Pg * (Igg + Ige) - DeltaINVg,
            'units': '$.y^{-1}',
            'definition': 'Consumption of goods sector output by households',
            'com': 'Fully accomodating'},


        # Markup, profits
        'mue': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Cost markup for extraction sector'},
        'mug': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Cost markup for goods sector'},

        'Pie': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Net profit of extraction sector'},
        'Pig': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Net profit of goods sector'},
        'pie': {
            'func': lambda Pie, Xe, Pe: Pie / (Xe * Pe),
            'units': '',
            'definition': 'Profit share of extraction sector',
            'com': 'definition'},
        'pig': {
            'func': lambda Pig, Xg, Pg: Pig / (Xg * Pg),
            'units': '',
            'definition': 'Profit share of goods sector',
            'com': 'definition'},
        'pire': {
            'func': lambda: 0,
            'units': 'y^{-1}',
            'definition': 'Profit rate of extraction sector'},
        'pirg': {
            'func': lambda: 0,
            'units': 'y^{-1}',
            'definition': 'Profit rate of goods sector'},


        # Capacity Use, inventories...
        'CUe': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Capacity utilization of extraction capital'},
        'CUg': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Capacity utilization of goods capital'},
        'ICe': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Inventory coverage of extraction capital'},
        'ICg': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Inventory coverage of goods capital'},
        'DeltaINVe': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Change in value of inventory of extraction sector'},
        'DeltaINVg': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Change in value of inventory of goods sector'},

    },
    'parameter': {
        # Population dynamics
        'alpham': {'definition': 'Minimum death rate of population (Equation S.9) ',
                   'value': 0.01},
        'alphaN': {'definition': 'Maximum death rate of population (Equation S.9) ',
                   'value': 0.07},
        'betaN': {'definition': 'Birth rate of population ',
                  'value': 0.03},

        # Ressource
        'yXg': {'definition': 'Resource input required per unit of goods sector output ',
                'value': 0.1},
        'lambday': {'definition': 'Maximum size natural resources stock (renewable scenarios) ',
                    'value': 100},
        'deltay': {'definition': 'Resources extraction factor (constant markup renewable scenarios) ',
                   'value': 0.012},
        'gamma': {'definition': 'Regeneration rate of resources (renewable scenarios) ',
                  'value': 0.01},

        # Production
        'age': {'definition': 'Goods input required per unit of gross resources extraction ',
                'value': 0.2},
        'agg': {'definition': 'Goods input required per unit of gross goods production ',
                'value': 0.1},
        'nug': {'definition': 'Capital to output ratio for goods sector ',
                'value': 1.5},

        'etae': {'definition': 'Resources input to operate extraction capital ',
                 'value': 0.16},
        'etag': {'definition': 'Resources input to operate goods capital ',
                 'value': 0.16},

        'delta': {'definition': 'Depreciation rate of capital ',
                  'value': 0.03},

        # Investment
        'kappa0e': {
            'func': lambda: 1,
            'units': '',
            'definition': 'Investment function parameter'},
        'kappa1e': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Investment function parameter'},
        'kappa0g': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Investment function parameter'},
        'kappa1g': {
            'func': lambda: 1,
            'units': '',
            'definition': 'Investment function parameter'},

        # Inventory
        'ICrefg': {'definition': 'Reference (target) inventory coverage for goods sector ',
                   'value': 1},
        'ICrefe': {'definition': 'Reference (target) inventory coverage for extraction sector ',
                   'value': 1},

        # Consumption parameters (?!)
        's': {'definition': 'threshold household consumption of resources per person (Equation S.9) ',
              'units': 'Units.Humans^{-1}.y^{-1}',
              'value': 0.08},
        'rhoe': {'definition': 'Minimum household consumption of extraction sector output ',
                 'units': 'Units.Humans^{-1}.y^{-1}',
                 'value': 0.01},
        'rhog': {'definition': 'Minimum household consumption of goods sector output ',
                 'units': 'Units.Humans^{-1}.y^{-1}',
                 'value': 0},

        # Interest rates
        'rL': {'definition': 'Interest rate(L: on loans) ',
               'value': 0.05},
        'rM': {'definition': 'Interest rate(M: for household deposits) ',
               'value': 0.0},

        # Relaxation times
        'tauCUe': {'definition': 'Time delay for extraction capacity utilization differential (lag) equation ',
                   'value': 0.3},
        'tauCUg': {'definition': 'Time delay for goods capacity utilization differential (lag) equation ',
                   'value': 0.3},
        'tauICe': {'definition': 'Time delay for extraction inventory coverage differential (lag) equation ',
                   'value': 0.3},
        'tauICg': {'definition': 'Time delay for goods inventory coverage differential (lag) equation ',
                   'value': 0.3},
        'tauPe': {'definition': 'Time delay for extraction price differential (lag) equation ',
                  'value': 0.3},
        'tauPg': {'definition': 'Time delay for goods price differential (lag) equation ',
                  'value': 0.3},
        'tauVe': {'definition': 'Time delay for extraction value added differential (lag) equation ',
                  'value': 0.3},
        'tauVg': {'definition': 'Time delay for goods net value added differential (lag) equation ',
                  'value': 0.3},
        'tauYe': {'definition': 'Time delay for extraction net output differential (lag) equation ',
                  'value': 0.3},
        'tauYg': {'definition': 'Time delay for goods net output differential (lag) equation',
                  'value': 0.3},
        'tauPie': {'definition': 'Time delay for extraction profit differential (lag) equation ',
                   'value': 0.3},
        'tauPig': {'definition': 'Time delay for goods profit differential (lag) equation ',
                   'value': 0.3},

        # Phillips Curve
        'phimin': {'definition': 'Wage function parameter',
                   'value': -0.05},
        'phi0': {'definition': 'Wage function parameter',
                 'value': 0},
        'phis': {'definition': 'Wage function parameter',
                 'value': 0.2},
        'lambdaNo': {'definition': 'wage function parameter (Equation S.1), equilibrium participation rate ',
                     'value': 0.6},
    },
}

_LOGICS_RESSOURCEANALYSIS = {
    'statevar': {
        # RESSOURCE-RELATED ANALYSIS VARIABLES
        'NEPR': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Net external power ratio'},
        'NPReco': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Net power ratio'},
        'GEPR': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Gross external power ratio'},
    }
}
_LOGICS_ADDSTOCKFLOW = {
    'statevar': {
        # Wage share
        'omega': {
            'func': lambda: 0,
            'units': '',
            'definition': 'Wage share (of value added)'},

        # Total debt and capital
        'Pib': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Bank dividends'},
        'D': {
            'func': lambda De, Dg: De + Dg,
            'units': '$',
            'definition': 'Total private debt (of firms)',
            'com': 'definition'},
        'K': {
            'func': lambda Pg, Kg, Ke: Pg * (Ke + Kg),
            'units': '$',
            'definition': 'Total capital',
            'com': 'In nominal quantities'},
        'L': {
            'func': lambda Le, Lg: Le + Lg,
            'units': 'Humans',
            'definition': 'Total labor'},

        # STOCK-FLOW BLABLA VARIABLES
        'M': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Total deposits (of money) in banks'},
        'Mh': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Household deposits (of money)'},
        'Sb': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Saving of banks money'},
        'Sh': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Saving of households money'},
        'V': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Total value added of the economy money'},
        'Ve': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Value added of extraction sector'},
        'Vg': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Value added of goods sector'},
        'Xb': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Net worth of banks'},
        'Xh': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Net worth of households'},
        'Xef': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Net worth of extraction firms'},
        'Xgf': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Net worth of goods firms'},
        'Xtot': {
            'func': lambda: 0,
            'units': '$',
            'definition': 'Net worth of the entire economy'},
        'Y': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Total net economic output of the economy'},
        'Ye': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Net economic output of extraction sectors'},
        'Yg': {
            'func': lambda: 0,
            'units': '$.y^{-1}',
            'definition': 'Net economic output of goods sectors'},
        'We': {
            'func': lambda w, Le: w * Le,
            'units': '$.y^{-1}',
            'definition': 'Wages for labor in extraction sector '},
        'Wg': {
            'func': lambda w, Lg: w * Lg,
            'units': '$.y^{-1}',
            'definition': 'Wages for labor in goods sector '},
    }
}

_LOGICS_FAMINE = {
    'differential': {
        'N': {
            'func': lambda N, betaN, alphaN, alpham, Ce, Pe: N * (betaN - (alpham + np.maximum(0, (1 - Ce / Pe) * (alphaN - alpham) / s * N))),
            'units': 'Humans',
            'definition': 'Population',
            'com': 'Population dynamics endogenous coefficient'},
    }
}

# ################# MODELS YOU WANT TO MERGE THE NEW LOGICS INTO ############
# _LOGICS_GOODWIN,_PRESETS0= importmodel('Goodwin')

# _LOGICS = merge_model(_LOGICS, _LOGICS_ADDSTOCKFLOW, verb=False)


# ################# ADDING DIMENSIONS TO VARIABLES IF NOT DONE BEFORE #######
'''Comment the line in 'Dimensions' you want to be filled by default.
The system does not handle automatically multiple types of matrix/vector dimensions. do it manually'''
Dimensions = {
    # 'scalar': [],
    'matrix': [],
    'vector': [],       #
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nprod'],
       'matrix': ['Nprod', 'Nprod']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)

# ################## SUPPLEMENTS IF NEEDED ###################################
_SUPPLEMENTS = {}

# ################## DEFIMING PRESETS WITH THEIR SUPPLEMENTS #################

plotdics = {'Var': [{'key': '',
                     'mode': False,  # sensitivity, cycles
                     'log': False,
                     'idx': 0,
                     'Region': 0,
                     'tini': False,
                     'tend': False,
                     'title': ''},
                    ],
            'XY': [{'x': '',
                    'y': '',
                    'color': '',
                    'scaled': False,
                    'idx': 0,
                    'Region': 0,
                    'tini': False,
                    'tend': False,
                    'title': '',
                    },
                   ],
            'XYZ': [{'x': '',
                     'y': '',
                     'z': '',
                     'color': 'time',
                     'idx': 0,
                     'Region': 0,
                     'tini': False,
                     'tend': False,
                     'title': ''},
                    ],
            'byunits': [{'filters_key': (),
                         'filters_units': (),
                         'filters_sector': (),
                         'separate_variables': {},
                         'lw': 1,
                         'idx': 0,
                         'Region': 0,
                         'tini': False,
                         'tend': False,
                         'title': ''}
                        ],
            'nyaxis': [{'y': [[], []],
                        'x': 'time',
                        'idx': 0,
                        'Region': 0,
                        'log': False,  # []
                        'title': '',
                        }
                       ],
            }

_PRESETS = {
    'Renewable-Low  Invest (a)': {
        'fields': {'kappa0': 1,
                   'kappa1': 1.3,
                   'mu1': 0.07,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Renewable-Low  Invest (b)': {
        'fields': {'kappa0': 1.3,
                   'kappa1': 1.,
                   'mu1': 0.07,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Renewable-Low  Invest (c)': {
        'fields': {'kappa0': 1.015,
                   'kappa1': 1.015,
                   'mu1': 0.07,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Renewable-High Invest (a)': {
        'fields': {'kappa0': 1.0,
                   'kappa1': 1.5,
                   'mu1': 0.07,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Renewable-High Invest (b)': {
        'fields': {'kappa0': 1.5,
                   'kappa1': 1.0,
                   'mu1': 0.07,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Renewable-High Invest (c)': {
        'fields': {'kappa0': 1.015,
                   'kappa1': 1.015,
                   'mu1': 0.11,
                   'mu2': 0.012,
                   'lambday': 100,
                   'gamma': 1},
        'com': '',
        'plots': plotdics},
    'Fossil': {
        'fields': {'kappa0': 1.,
                   'kappa1': 1.55,
                   'mu1': 0.07,
                   'mu2': 0.0012,
                   'lambday': 1000,
                   'gamma': 0},
        'com': '',
        'plots': plotdics}
}
