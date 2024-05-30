# The library is where all default fields values and definitions are located
import numpy as np

ADDITIONAL_FIELDS = {
    'ICED': {

        'prod': {'value': 1,
                 'definition': 'productivity per worker',
                 'units': 'Units.Humans^{-1}.y^{-1}',
                 'symbol': r'$\mathcal{A}$'},

        'flambda': {'value': 1,
                    'definition': 'non-linear function of employment in wage',
                    'units': '',
                    'symbol': r'$f(\lambda)$'},
        'Ww': {'value': 1,
               'definition': 'workers total disposable income',
               'units': '$.y^{-1}',
               'symbol': r'$W_w$'},
        'Wc': {'value': 1,
               'definition': 'capitalists total disposable income',
               'units': '$.y^{-1}',
               'symbol': r'$W_c$'},
        'Ky': {
            'func': lambda Ky, Iy, deltay: Iy - deltay * Ky,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'symbol': r'$K_y$',
            'initial': 1.6},
        'Kg': {
            'func': lambda Kg, deltag, Ig: Ig - deltag * Kg,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'symbol': r'$K_g$',
            'initial': 0.1},
        'Kb': {
            'func': lambda Kb, deltab, Ib: Ib - deltab * Kb,
            'units': 'Units',
            'com': 'Basic investment-depreciation',
            'symbol': r'$K_b$',
            'initial': .75},
        'ay': {
            'func': lambda ay, alphay: ay * alphay,
            'units': 'Humans.Units^{-1}',
            'com': 'Basic exogenous technological change',
            'symbol': r'$a_y$',
            'initial': 3},
        'ag': {
            'func': lambda ag, alphag: ag * alphag,
            'com': 'Basic exogenous technological change',
            'units': 'Humans.Units^{-1}',
            'symbol': r'$a_g$',
            'initial': 3},
        'ab': {
            'func': lambda ab, alphab: ab * alphab,
            'com': 'Basic exogenous technological change',
            'units': 'Humans.Units^{-1}',
            'symbol': r'$a_b$',
            'initial': 3},
        'epsilony': {
            'func': lambda sigmay, epsilony, uE: sigmay * epsilony * (1 - epsilony) * (1 - uE),
            'initial': .65,
            'definition': 'share of investment into energy capital',
            'com': "lazy way to ensure that enough energy is available. Unstable mechanism in a CHI",
            'symbol': r'$\epsilon_y$',
            'units': ''},
        'Iy': {
            'func': lambda I, epsilony: I * epsilony,
            'units': r'$.y^{-1}', },
        'Ig': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * epsilong,
            'units': r'$.y^{-1}', },
        'Ib': {
            'func': lambda I, epsilony, epsilong: I * (1 - epsilony) * (1 - epsilong),
            'units': r'$.y^{-1}', },
        'uE': {'func': lambda Ky, E, Eeff: Ky / (Eeff*E),
               'units': '',
               'definition': 'use of energy capital',
               'symbol': r'$u_E$'},
        'E': {'func': lambda Ab, Ag, Kb, Kg: Ab * Kb + Ag * Kg,
              'definition': 'Energy flux',
              'units': r'Units.y^{-1}'},
        'Color': {'func': lambda Ag, Kg, E: Ag*Kg/E,
                  'units': '',
                  'definition': '1 energy is fully green, 0 fully brown'},
        'rocb': {'func': lambda Ab, omega, ay, ab, deltab, pc, p, pollb: Ab - omega * ay / ab - deltab - pc/p*pollb*Ab,
                 'definition': 'Return of capital for brown technology',
                 'com':        'no carbon tax',
                 'symbol':     r'$\mathcal{R}^{oc}_B$',
                 'units':      'y^{-1}'},
        'rocg': {'func': lambda Ag, omega, ay, ag, deltag, Ab, pollb, p, pc, Kb, Kg: Ag - omega * ay / ag - deltag+(Kb/Kg) * pc/p*pollb*Ab,
                 'definition': 'Return of capital for green technology',
                 'com':        'no carbon tax',
                 'symbol':     r'$\mathcal{R}^{oc}_G$',
                 'units':      'y^{-1}'},
        'epsilong': {
            'func': lambda rocg, rocb, zi, zg: .5 * (1 + np.tanh(zi * (rocg - rocb - 1 + zg))),
            'units': '',
            'symbol': r'$\epsilon_g$',
            'definition': 'share of energy investment in green',
            'com': 'market allocation through ROC'},
        'pc': {'value': 0,
               'definition': 'carbon price',
               'units': r'$.C^{-1}',
               'symbol': r'$p_{carbon}$'},
        'pollb': {'value': 1,
                  'definition': 'Carbon intensity of producing 1 unit of energy through Kb',
                  'units': r'C.Units^{-1}',
                  'symbol': r''
                  },
        'Eeff': {'value': 1,
                 'units': '',
                 'definition': 'Energy consumption efficiency',
                 'symbol': r'$E_{eff}$'},
        'deltaC': {'value': 0,
                   'definition': 'Voluntary destruction of brown capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$\delta^{carb}_b$'},
        'alphab': {'value': 0,
                   'definition': 'Automatisation rate for brown capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$\alpha_b$'},
        'alphag': {'value': 0,
                   'definition': 'Automatisation rate for grown capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$\alpha_g$'},
        'alphay': {'value': 0,
                   'definition': 'Automatisation rate for output capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$\alpha_y$'},
        'deltay': {'value': 0,
                   'definition': 'depreciation rate of useful capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$$'},
        'deltab0': {'value': 0,
                    'definition': 'exogenous depreciation rate of brown capital',
                    'units':      'y^{-1}',
                    'symbol':     r'$$'},
        'deltab': {'value': 0,
                   'definition': 'effective depreciation rate of useful capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$$'},
        'deltag': {'value': 0,
                   'definition': 'depreciation rate of green capital',
                   'units':      'y^{-1}',
                   'symbol':     r'$$'},
        'Ab': {'value': 0,
               'definition': 'production efficiency for browm technology',
               'units':      '',
               'symbol':     r'$$'},
        'Ay': {'value': 0,
               'definition': 'production efficiency general level',
               'units':      'y^{-1}',
               'symbol':     r'$$'},
        'Ag0': {'value': 0,
                'definition': 'Base level of production efficiency for green technology',
                'units':      '',
                'symbol':     r'$$'},
        'Ag': {'value': 0,
               'definition': 'Effective production efficiency for green technology',
               'units':      '',
               'symbol':     r'$$'},
        'sigmay': {'value': 0,
                   'definition': 'rate of allocation change for energy',
                   'units':      'y^{-1}',
                   'symbol':     r'$$'},
        'zi': {'value': 0,
               'definition': 'Market profit sensibility in arbitrage',
               'units':      '',
               'symbol':     r'$$'},
        'zg': {'value': 0,
               'definition': 'Market green willingness',
               'units':      '',
               'symbol':     r'$$'},
        'kappaC': {'value': 0,
                   'definition': 'Share of income spent in consumption',
                   'units':      '',
                   'symbol':     r'$\kappa_c$'},
        'Phi0': {'value': 0,
                 'definition': 'Wage negociation base level (no employment)',
                 'units':      'y^{-1}',
                 'symbol':     r'$\Phi_0$'},
        'Phi1': {'value': 0,
                 'definition': 'Linear sensibility to employment in wage negociation',
                 'units':      'y^{-1}',
                 'symbol':     r'$\Phi_1$'},
        'zpi': {'value': 0,
                'definition': 'profit sensibility in wage negotiation',
                'units':      '',
                'symbol':     r'$z_{pi}$'},
    },

    'ECHIMES': {
        'w0': {
            'definition': 'wage indicator',
            'units': '$.Humans^{-1}.y^{-1}',
            'size': ['__ONE__'],
            'symbol': r'$w^0$',
            'value': 0.6,
        },
        'u0': {
            'definition': 'voluntary use of productive capital',
            'units': '',
            'size': ['Nprod'],
            'value': 1,
        },
        'a0': {
            'value': 3,
            'com': 'Productivity indicator',
            'units': 'Units.Humans^{-1}.y^{-1}',
            # 'value': 1,
        },

        # MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod'],
            'units': '',
            'definition': 'intermediate consumption coefficients'
        },
        'Xi': {
            'value': 1,
            'size': ['Nprod', 'Nprod'],
            'units': '',
            'definition': 'capital recipe creation',
        },
        'Mgamma': {
            'value': 0,
            'definition': 'weight of intermediate consumption from j',
            'units': '',
            'com': 'Matrix version',
            'size': ['Nprod', 'Nprod'],

        },
        'Mxi': {
            'value': 0,
            'definition': 'weight of capital destruction from j',
            'units': '',
            'com': 'Matrix version',
            'size': ['Nprod', 'Nprod'],
        },
        'Minter': {
            'value': 0,
            'definition': 'Money from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^Y$'
        },
        'Minvest': {
            'value': 0,
            'definition': 'Money from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^I$'
        },
        'MtransactY': {
            'value': 0,
            'definition': 'Money from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^Y$'

        },
        'MtransactI': {
            'value': 0,
            'definition': 'Money from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$\mathcal{T}^I$'

        },
        'basket': {
            'value': 1,
            'com': 'cannot be non-auxilliary',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
            'units': '',

        },
        'Phillips': {
            'value': 0,
            'definition': 'non-inflationary wage growth rate',
            'units': 'y^{-1}',
            'symbol': r'$\Phi(\lambda)$',
        },
        'ibasket': {
            'value': 0,
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
            'units': 'y^{-1}',
            'symbol': r'$i_{Basket}$',

        },
        'C': {
            'value': 0,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod', '__ONE__'],
        },
        'dotV': {
            'value': 0,
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$\dot{V}$'
        },
        'Kdelta': {
            'value': 0,
            'func': lambda K, delta: delta * K,
            'definition': 'physical degraded of capital',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$(\delta K)$'
        },
        'gamma': {
            'value': 0,
            'definition': 'share of intermediary consumption',
            'units': '',
            'symbol': r'$\gamma$',
            'size': ['Nprod'],
        },
        'reldotv': {
            'value': 0,
            'definition': 'relative budget weight of inventory change',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\dot{v}$',
        },
        'reloverinvest': {
            'value': 0,
            'units': '',
            'symbol': r'$(\kappa-\pi)$',
            'size': ['Nprod'],
            'definition': 'relative overinstment of the budget',
        },
        'xi': {
            'value': 0,
            'definition': 'relative capex weight',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\xi$',
        },
        'wL': {
            'value': 0,
            'com': 'wage bill per sector',
            'definition': 'wage bill per sector',
            'units': '$.y^{-1}',
            'size': ['Nprod'],

        },
        'pC': {
            'value': 0,
            'com': 'explicit monetary flux',
            'definition': 'monetary consumption',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },

        'rD': {
            'value': 0,
            'com': 'explicit monetary flux',
            'definition': 'debt interests',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'dotD': {
            'value': 0,
            'com': 'explicit monetary flux',
            'definition': 'debt variation',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'W': {
            'value': 0,
            'definition': 'Total income of household',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'
        },
        'Shareholding': {
            'value': 0,
            'definition': 'flow of profits to households',
            'units': '$.y^{-1}',
        },
        'Delta': {
            'value': 0,
            'definition': 'proportion of profits as shareholding',
            'units': '',
            'symbol': r'$\Delta^{\pi}$'
        },

        'rDh': {
            'value': 0,
            'definition': 'bank interests for household',
            'units': '$.y^{-1}',
        },

        'rd': {
            'value': 0,
            'com': 'explicit form',
            'definition': 'relative weight debt',
            'size': ['Nprod'],
            'units': ''
        },
        'ROC': {
            'value': 0.1,
            'definition': 'return on capital',
            'com': 'raw definition',
            'size': ['Nprod'],
            'units': 'y^{-1}',
        },
        'z': {
            'value': 1,
            'definition': 'local wage ponderation',
            'size': ['Nprod']
        },
        'b': {'value': 0.5,
              'definition': 'capital intensity of production',
              'size': ['Nprod']
              },
        'nu0': {
            'value': 3,
            'definition': 'Sector-dependant capital to output ratio',
            'symbol': r'$\nu^{(0)}',
            'units': 'y',
        },
        'Cpond': {
            'value': 1,
            'definition': 'part of salary into consumption of the product',
            'size': ['Nprod']
        },
        'mu0': {
            'value': 1,
            'definition': 'target markup for productive sector',
            'size': ['Nprod']
        },

        'employmentAGG': {
            'value': 0.9,
            'definition': 'Agregated employment',
            'units': '',
            'symbol': r'$\Lambda$'
        },
    },



    'Household': {
        # VARIABLES
        'N': {
            'value': 1.,
            'definition': 'Population of people able to work',
            'units': 'Humans',
        },
        'L': {
            'value': 1,
            'definition': 'Workers',
            'units': 'Humans',
        },
        'a': {
            'value': 1.00,
            'units': 'Units.Humans^{-1}.y^{-1}',
            'definition': 'Productivity',
        },
        'w': {
            'value': 0.85,
            'definition': 'Wage value',
            'units': '$.Humans^{-1}.y^{-1}'
        },
        'employment': {
            'value': .97,
            'definition': 'employment rate',
            'units': '',
            'symbol': r'$\lambda$',
        },
        'omega': {
            'value': .85,
            'definition': 'wage share',
            'units': '',
            'symbol': r'$\omega$',
        },


        # PARAMETERS
        'n': {
            'value': 0.025,
            'definition': 'Rate of population growth',
            'units': 'y^{-1}',
        },
        'alpha': {
            'value': 0.02,
            'definition': 'Rate of productivity increase',
            'units': 'y^{-1}',
            'symbol': r'$\alpha$',
        },
        'beta': {
            'value': 0,
            'definition': 'productivity increase dependency to g',
            'units': '',
            'symbol': r'$\beta$',
        },
        'Nmax': {
            'value': 12,
            'definition': 'Saturating population',
            'units': 'Humans',
        },
    },

    'Production': {
        'A': {
            'value': 1 / 3.,
            'definition': 'Efficiency in CES prod',
            'units': 'y^{-1}',
        },
        'nu': {
            'value': 3,
            'definition': 'Capital to output ratio',
            'units': 'y',
            'symbol': r'$\nu$',
        },
        'b': {
            'value': 0.5,
            'definition': 'part of capital in prod intensity',
            'units': '',
        },

        # CES PROPERTIES
        'CESexp': {
            'value': 100,
            'definition': 'exponent in CES function',
            'units': '',
        },
        'cesLcarac': {
            'value': 1,
            'definition': 'Typical Labor from capital',
            'com': 'Extracted from YCES',
            'units': 'Humans',
            'eqtype': 'param',
        },
        'cesYcarac': {
            'value': 1,
            'definition': 'Typical Y from capital',
            'com': 'Extracted from YCES',
            'units': 'Units.y^{-1}',
            'eqtype': 'param',
        },
        'omegacarac': {
            'value': 1,
            'definition': 'Typical omega without substituability',
            'com': 'Extracted from YCES',
            'units': '',
            'eqtype': 'param',
        },
        'l': {
            'value': 1,
            'definition': 'ratio btwn effective workers and typical worker',
            'com': 'deduced from Pi optimisation',
            'units': '',
            'eqtype': 'param',
        },
        #############

        # VARIABLES
        'K': {
            'value': 2.3,
            'units': 'Units',
            'definition': 'Capital in real units',
        },
        'Y': {
            'value': 1,
            'definition': 'GDP in real units',
            'units': 'Units.y^{-1}',
        },
        'Y0': {
            'value': 1,
            'definition': 'Yearly Production without climate damage and abatment',
            'units': 'Units.y^{-1}',
        },
        'GDP': {
            'value': 1,
            'definition': 'nominal GDP ',
            'units': '$.y^{-1}',
        },
        'V': {
            'value': 1,
            'definition': 'Inventory of Goods',
            'units': 'Units',
        },
        'u': {
            'value': .85,
            'definition': 'Use intensity of capital',
            'units': '',
        },


        # INTERMEDIARY VARIABLES
        'g': {
            'value': 0.03,
            'definition': 'Relative growth of GDP',
            'units': 'y^{-1}',
        },
        'pi': {
            'value': 0.1,
            'definition': 'relative profit',
            'units': '',
            'symbol': r'$\pi$',
        },
        'Pi': {
            'value': 0,
            'definition': 'Absolute profit',
            'units': '$.y^{-1}',
            'symbol': r'$\Pi$',
        },
        'c': {
            'value': 0,
            'definition': 'production price',
            'units': '$.Units^{-1}'
        },

        # PARAMETERS
        'delta': {
            'value': 0.005,
            'definition': 'Rate of capital depletion',
            'units': 'y^{-1}',
            'symbol': r'$\delta$',
        },
        'gammai': {
            'value': 1,
            'definition': 'inflation awareness',
            'units': '',
            'symbol': r'$\Gamma$',
        },
        'sigma': {
            'value': 1,
            'definition': 'rate of use adjustment',
            'units': 'y^{-1}',
            'symbol': r'$\sigma$',
        },
    },


    'Salary Negociation': {
        'phillips': {
            'value': 0,
            'definition': 'Wage inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$\phi$',
        },

        # Diverging Philips
        'phinull': {
            'value': 0.1,
            'definition': 'Unemployment rate with no salary increase',
            'units': '',
        },
        'phi0': {
            'func': lambda phinull=0: phinull / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'parameter',
        },
        'phi1': {
            'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'parameter',
        },

        # Linear Phillips (from Coping article)
        'philinConst': {
            'value': -0.292,
            'definition': 'wage rate when full unemployement',
            'units': 'y^{-1}',
            'symbol': r'$\Phi_0$',
        },
        'philinSlope': {
            'value': 0.469,
            'definition': 'wage rate dependance to unemployement',
            'units': 'y^{-1}',
            'symbol': r'$\Phi_1$',
        },

        # Exponential Philips (from CES article)
        'phiexp0': {
            'value': -0.01,
            'definition': 'Constant in expo phillips',
            'units': 'y^{-1}',
        },
        'phiexp1': {
            'value': 2.35 * 10**(-23),
            'definition': 'slope in expo phillips',
            'units': 'y^{-1}',
        },
        'phiexp2': {
            'value': 50,
            'definition': 'exponent in expo phillips',
            'units': '',
        },
    },

    'Speculation': {
        'Speculation': {
            'value': 0,
            'definition': 'flux of money going from firm to finance',
            'units': '$.y^{-1}'
        },
        'SpecExpo1': {
            'value': -0 * 0.25,
            'definition': 'Speculation constant (expo)',
            'units': '$.y^{-1}',
        },
        'SpecExpo2': {
            'value': 0 * 0.25,
            'definition': 'Speculation expo slope (expo)',
            'units': '$.y^{-1}',
        },
        'SpecExpo3': {
            'value': 0 * 0.36,
            'definition': 'Speculation attenuation in exp (expo)',
            'units': '',
        },
        'SpecExpo4': {
            'value': 0 * 12,
            'definition': 'Speculation sensitivity to growth',
            'units': 'y',
        },
    },

    'Shareholding': {
        'Sh': {
            'value': 0,
            'definition': 'Shareholding dividends',
            'units': '$.y^{-1}',
        },
        # Dividend fit from copingwithcollapse
        'divlinSlope': {
            'value': 0.473,
            'definition': 'Shareholding dependency to profits (affine)',
            'units': '$.y^{-1}',
        },
        'divlinconst': {
            'value': 0.138,
            'definition': 'Shareholding dividends when no profits (affine)',
            'units': '$.y^{-1}',
        },
        'divlinMin': {
            'value': 0,
            'definition': 'Shareholding minimum part',
            'units': '$.y^{-1}',
        },
        'divlinMax': {
            'value': 3,
            'definition': 'Shareholding maximum part',
            'units': '$.y^{-1}',
        },
    },


    'Investment': {
        'I': {
            'value': 0,
            'definition': 'Investment in nominal value',
            'units': '$.y^{-1}',
        },
        'Ir': {
            'value': 0,
            'definition': 'Number of real unit from investment',
            'units': 'Units.y^{-1}',
        },
        'kappa': {
            'value': 0,
            'definition': 'Part of GDP in investment',
            'units': '',
            'symbol': r'$\kappa$',
        },
        'k0': {
            'value': -0.0065,
            'definition': 'GDP share investedat zeroprofit (expo)',
            'units': '',
            'symbol': r'$k_0$',
        },
        'k1': {
            'value': np.exp(-5),
            'definition': 'Investment slope (expo)',
            'units': '',
            'symbol': r'$k_1$',
        },
        'k2': {
            'value': 20,
            'definition': 'Investment power in kappa (expo)',
            'units': '',
            'symbol': r'$k_2$',
        },
        'kappalinSlope': {
            'value': 0.575,
            'definition': 'Investment slope kappa (affine)',
            'units': '',
        },
        'kappalinConst': {
            'value': 0.0318,
            'definition': 'Investment no profit (affine)',
            'units': '',
        },
        'kappalinMin': {
            'value': 0,
            'definition': 'Minimum value of kappa (affine)',
            'units': '',
        },
        'kappalinMax': {
            'value': 0.3,
            'definition': 'Maximum value of kappa (affine)',
            'units': '',
        },
    },


    'Debt': {
        'r': {
            'value': .03,
            'definition': 'Interest on debt',
            'units': 'y^{-1}',
        },
        'D': {
            'value': 0.1,
            'definition': 'Debt of private sector',
            'units': '$',
        },
        'Dh': {
            'value': 0.1,
            'definition': 'Debt of household',
            'units': '$',
        },
        'd': {
            # 'func': lambda GDP=0, D=0: D/GDP,
            'value': 0.1,
            'definition': 'relative debt',
            'units': 'y',
        },
        'solvability': {
            'definition': 'capital compared to debt',
            'units': ''
        },
    },


    'Prices': {
        # VARIABLES
        'inflation': {
            'value': 0,
            'definition': 'inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$i$',
        },
        'inflationMarkup': {
            'value': 0,
            'definition': 'cost-pushed inflation',
            'units': 'y^{-1}',
            'symbol': '$i^{\mu}$'
        },
        'inflationdotV': {
            'value': 0,
            'definition': 'inventory-pushed inflation',
            'units': 'y^{-1}',
            'symbol': '$i^{\dot{V}}$'
        },
        'p': {
            'value': 1,
            'definition': 'price of goods',
            'units': '$.Units^{-1}'
        },

        # PARAMETERS
        'mu': {
            'value': 1.3,
            'definition': 'Markup on prices',
            'units': '',
            'symbol': r'$\mu$',
        },
        'eta': {
            'value': 0.5,
            'definition': 'timerate of price adjustment',
            'units': 'y^{-1}',
            'symbol': r'$\eta$',
        },
        'chi': {
            'value': 1,
            'definition': 'inflation rate on inventory',
            'units': 'y^{-1}',
            'symbol': r'$\chi$',
        },
    },


    'Consumption': {
        # VARIABLES
        'H': {'value': 1,
              'definition': 'Household possessions',
              'units': 'Units',
              'symbol': r'$H$', },
        'Hid': {'value': 1,
                'definition': 'Household optimal possessions',
                'units': 'Units',
                'symbol': r'$H^{id}$', },

        # PARAMETERS
        'deltah': {'value': 0.1,
                   'definition': 'possessions deterioration rate',
                   'units': 'y^{-1}',
                   'symbol': r'$\delta^h$', },
        'Omega0': {'value': 1,
                   'definition': 'Purchasing power of inflexion',
                   'units': 'Units.Humans^{-1}.y^{-1}',
                   },
    },


    'Coping-Damages': {
        'deltad': {
            'value': 0.005,
            'definition': 'Rate of capital depletion with CC',
            'units': 'y^{-1}',
        },
        'Dy': {
            'value': 0,
            'definition': 'Damage on production',
            'units': '',
        },
        'DK': {
            'value': 0,
            'definition': "Intermediary damage on capital",
            'units': '',
        },
        'Damage': {
            'value': 0,
            'definition': 'Damage function',
            'units': '',
        },
        'pi1': {
            'value': 0,
            'definition': 'Linear damage parameter',
            'units': 'Tc^{-1}',
        },
        'pi2': {
            'value': 0.00236,
            'definition': 'quadratic damage parameter',
            'units': 'Tc^{-2}',
        },
        'pi3': {
            'value': 0.00000507,
            'definition': 'Weitzman damage parameter',
            'units': None,
        },
        'zeta3': {
            'value': 6.754,
            'definition': 'Weitzmann dmg temp exponent',
            'units': '',
        },
        'fk': {
            'value': 1 / 3,
            'definition': 'Fraction of damage allocated to capital',
            'units': '',
        },
    },


    'Emissions': {
        'Eind': {
            'value': 38.85,
            'definition': 'Emission from the society',
            'units': 'C.y^{-1}',
        },
        'Eland': {
            'value': 2.6,
            'definition': 'Natural Emission',
            'units': 'C.y^{-1}',
        },
        'deltaEland': {
            'value': 0,
            'definition': 'timerate of natural emission reduction',
            'units': 'y^{-1}',
        },
        'sigmaEm': {
            'value': 0,
            'definition': 'current emission intensity of the economy',
            'units': 'C.Units^{-1}.y^{-1}',
        },
        'gsigmaEm': {
            'value': -0.0152,
            'definition': 'Growth rate economic emission intensity',
            'units': 'y^{-1}',
        },
        'deltagsigmaEm': {
            'value': -0.001,
            'definition': 'growth rate of the emission growth rate',
            'units': 'y^{-1}',
        }
    },


    'Coping-Technologies': {
        'pbackstop': {
            'value': 547,
            'definition': 'Magic backstop technology price',
            'units': '',
        },
        'pcarbon': {
            'value': 100,
            'definition': 'aggregated real price of carbon',
            'units': '',
        },
        'pcarbon_pot': {
            'value': 100,
            'definition': 'aggregated potential price of carbon',
            'units': '',
        },
        'carbontax': {
            'value': 100,
            'definition': 'aggregated carbon tax paid by private sector',
            'units': '',
        },
        'apc': {
            'value': 0,
            'definition': 'parameter apc for ex. carbon price',
            'units': '',
        },
        'bpc': {
            'value': 0,
            'definition': 'parameter bpc for ex. carbon price',
            'units': '',
        },
        'deltapbackstop': {
            'value': -0.005,
            'definition': 'growth rate of backstop price',
            'units': '',
        },
        'conv10to15': {
            'value': 1.160723971 / 1000,
            'definition': 'conversion factor',
            'units': '',
        },
        'emissionreductionrate': {
            'value': 0.03,
            'definition': 'Emission reduction rate',
            'units': 'y^{-1}',
        },
        'Abattement': {
            'value': 0,
            'definition': 'Redirection of production',
            'units': '',
        },
        'convexitycost': {
            'value': 2.6,
            'definition': 'Convexity of cost function for reduction',
            'units': '',
        },
    },


    '3Layer-Climate': {
        'Emission0': {
            'value': 38.85,
            'definition': 'CO2 Emission per year (Gt) at t=0',
            'units': 'C.y^{-1}',
        },
        'Emission': {
            'value': 38,
            'definition': 'CO2 Emission per year (Gt)',
            'units': 'C.y^{-1}',
        },
        'deltaEmission': {
            'value': 0.01,
            'definition': 'Diminution rate of carbon emission',
            'units': 'y^{-1}',
        },
        'F2CO2': {
            'value': 3.681,
            'definition': 'Forcing when doubling CO2',
            'units': None,
        },
        'CO2AT': {
            'value': 851,
            'definition': 'CO2 in atmosphere',
            'units': 'C',
        },
        'CO2UP': {
            'value': 460,
            'definition': 'CO2 in upper ocean',
            'units': 'C',
        },
        'CO2LO': {
            'value': 1740,
            'definition': 'CO2 in lower ocean',
            'units': 'C',
        },
        'CUP': {
            'value': 460,
            'definition': 'Historical CO2 in upper ocean',
            'units': 'C',
        },
        'CAT': {
            'value': 588,
            'definition': 'Historical CO2 in atmosphere',
            'units': 'C',
        },
        'CLO': {
            'value': 1720,
            'definition': 'Historical CO2 in lower ocean',
            'units': 'C',
        },
        'phi12': {
            'value': 0.024,
            'definition': 'Transfer rate atmosphere-ocean',
            'units': 'y^{-1}',
        },
        'phi23': {
            'value': 0.001,
            'definition': 'Transfer rate upper-lower ocean',
            'units': 'y^{-1}',
        },
        'Capacity': {
            'value': 1 / 0.098,
            'definition': 'Heat capacity atmosphere+upper ocean',
            'units': None,
        },
        'Capacity0': {
            'value': 3.52,
            'definition': 'Heat capacity lower ocean',
            'units': None,
        },
        'rhoAtmo': {
            'value': 3.681 / 3.1,
            'definition': 'radiative feedback parameter',
            'units': None,
        },
        'gammaAtmo': {
            'value': 0.0176,
            'definition': 'Heat exchange between layers',
            'units': None,
        },
        'T': {
            'value': 1,
            'definition': 'temperature anomaly of atmosphere',
            'units': 'Tc',
        },
        'T0': {
            'value': 1,
            'definition': 'temperature anomaly of ocean',
            'units': 'Tc',
        },
        'F': {
            'value': 3.6,
            'definition': 'Radiative Forcing',
            'units': '',
        },
    },
}
