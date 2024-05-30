
"""Inequality-Carbon-Energy-Dynamics"""

import numpy as np
from chimes.libraries import importmodel      # Import another model _LOGICS, _PRESETS
from chimes.libraries import merge_model       # Merge two model logics into each others

from chimes.plots.sankey import Sankey
_DESCRIPTION = """
## Parameters added 

* sigmay :
* pc :
* deltaC : 
* zi : market sensibility
* zg : market preference
* Ag : Green efficiency 
* CESexp : Energy - (Labor-Capital) non-substitution
* Eeff : Energy efficiency 

## What is this model ?


## Why is it interesting ?




## what is the purpose of your model


## Expected behavior


"""
_TODO = ['Completing the model', 'that should be done']
_ARTICLE = "https://www.overleaf.com/read/fxppgztffzph#6fa1cb"
_DATE = "2023/12/07 model file creation"
_CODER = "Paul Valcke"
_KEYWORDS = ['module', 'capital', 'investment', 'decarbonation']
_UNITS = []  # Optional: Adding accepted units for fields
# ###########################################################


_LOGICS_3CAP, _PRESETS_3CAP, _SUPP_3CAP = importmodel('3Capital')


_LOGICS_MINICHI = dict(
    differential=dict(
        D=lambda r, D, w, L, Delta, Pi, C, p: r * D + w * L + Delta * Pi - C * p,
        p=lambda p, inflation: p * inflation,
        N=lambda N, n: N * n,
        w=lambda w, phillips: w * phillips,
    ),
    statevar=dict(
        C=lambda Ww, Wc, kappaC, p: (Ww+kappaC*Wc)/p,
        Ww=lambda w, L: w*L,
        Wc=lambda r, D, Delta, Pi: r * D + Delta * Pi,

        employment=lambda L, N: L / N,
        phillips=lambda Phi0, Phi1, flambda: Phi0 + Phi1 * flambda,
        flambda=lambda employment, pi, zpi: ((np.maximum(pi, 0.01)/0.1)**zpi) / (1 - employment)**2,

        omega=lambda w, L, p, Y: w * L / (p * Y),
        d=lambda D, p, Y: D / (p * Y),

        Pi=lambda p, Y, w, L, r, D, delta, K: p*Y-w*L-r*D-delta*p*K,
        pi=lambda Pi, p, Y: Pi/(p*Y),
        # ROC': {'func': lambda Pi, K,  p: Pi / (p * K)},
        # Solvability': {'func': lambda D, K, p: 1 - D / (K * p)},
        # c {'func': lambda p, omega, Gamma, nu, delta: p * (omega + Gamma + nu * delta )},
        # mu {'func': lambda p, c: p / c},


    ),
    parameter=dict(
        kappaC=0.5,
        Delta=0.1,
        Phi0=-0.1010101,
        Phi1=0.0010101,
        inflation=0.05,
        zpi=1,
        # pc=1,
    ),
)

_LOGICS_INEQ = {
    'differential': {
        'Hc': dict(func=lambda Hc, deltaHc, Cc: Cc - deltaHc*Hc,
                   initial=0.1),
        'Hw': dict(func=lambda Hw, deltaHw, Cw: Cw - deltaHw*Hw,
                   initial=0.1),
        # 'Nc': {'func': lambda Nc, nc: Nc*nc,
        # 'Nw': lambda Nw, nw: Nw*nw,
    },
    'statevar': dict(
        Cc=lambda Wc, p, kappaC: kappaC*Wc/p,
        Cw=lambda Ww, p: Ww/p,
    ),
    'parameter': dict(
        # nw=0.02,
        # nc=0.02,
        deltaHc=0.5,
        deltaHw=0.5,
    ),
}

_LOGICS_ENDO = {
    'differential': {
        'pc': dict(func=lambda pc, inflation, omega: pc*(inflation),
                   initial=0.1),
        # 'ag': {
        #    'func': lambda ag, alphag: ag * alphag,
        #    'com': 'Basic exogenous technological change',
        #    'units': 'Humans.Units^{-1}',
        #    'symbol': r'$a_g$',
        #    'initial': 3},

        # investment allocation
        # 'epsilony': {'func': lambda sigmay, epsilony, uE: sigmay * epsilony * (1 - epsilony) * (1 - uE),
        #             'initial': .65,
        #             'definition': 'share of investment into energy capital',
        #             'com': "lazy way to ensure that enough energy is available. Unstable mechanism in a CHI",
        #             'symbol': r'$\epsilon_y$',
        #             'units': ''},
        # Integral carbon
        # 'Carb': {'func': lambda Emission: Emission/20,
        #         'initial': 0},
    },
    'statevar': {
        # 'Y': {'func': lambda Ay, Ky, uE, CESexp: Ay * Ky},  # *(1+(1/uE)**(-CESexp))**(-1/CESexp)},


        # Bonus: Endogenous green technology
        'Ag': {'func': lambda Ag0, Kg: Ag0 * (Kg / 0.1)**(0.1),
               'definition': 'Efficiency of green capital',
               'symbol': r'$A_g$',
               'units': 'y^{-1}',
               'com': 'Increasing output on capital'},

        # Bonus: Brown capital destruction
        # 'deltaC': {'func': lambda time: 0.001*time,
        #           'definition': 'Voluntary destruction of brown capital',
        #           'com':        'Ad-hoc shape',
        #           'units':      'y^{-1}',
        #           'symbol':     r'$\delta^{carb}_b$'},


        # 'Eeff': {'func': lambda time: 1*np.exp(0.01*time),
        #         'units': '',
        #         'definition': 'Energy consumption efficiency',
        #         'symbol': r'$E_{eff}$',
        #         'com': 'Exponential 1%'},

    },
    'parameter': {
        'Ag0': 1,
    }
}


def get_sankeys(hub):
    """Display the Physical and nominal Sankey for the run of the hub"""
    R = hub.get_dvalues(params=True)

    # Physical Sankey
    title = 'Physical goods Flows in ICED model'
    Units = ""
    Scale = R['Y']/R['Y'][0]
    nodes = {k: i for i, k in enumerate([
        'Production',
        'Consumption',
        'Workers Possessions',
        'Investor Possessions',
        'Investment',
        'Output Capital',
        'Energy Investment',
        'Green Capital',
        'Brown Capital',
        'Destruction flow'])}
    Links0 = [
        ['Consumption',  R['C'], nodes['Production'], nodes['Consumption'], 11],
        ['Worker Consumption',  R['Ww']/R['p'], nodes['Consumption'], nodes['Workers Possessions'], 7],
        ['Capitalists Consumption', R['kappaC']*R['Wc']/R['p'], nodes['Consumption'], nodes['Investor Possessions'], 2],
        ['Investment', R['I'], nodes['Production'], nodes['Investment'], 19],
        ['Output Investment', R['Iy'], nodes['Investment'], nodes['Output Capital'], 1],
        ['Energy Investment', R['Ig']+R['Ib'], nodes['Investment'], nodes['Energy Investment'], 5],
        ['Green Investment', R['Ig'], nodes['Energy Investment'], nodes['Green Capital'], 3],
        ['Brown Investment', R['Ib'], nodes['Energy Investment'], nodes['Brown Capital'], 15],
        ['Output capital depreciation', R['Ky']*R['deltay'], nodes['Output Capital'], nodes['Destruction flow'], 4],
        ['Brown capital depreciation', R['Kb']*R['deltab'], nodes['Brown Capital'], nodes['Destruction flow'], 4],
        ['Green capital depreciation', R['Kg']*R['deltag'], nodes['Green Capital'], nodes['Destruction flow'], 4],
        ['Capitalist possessions dissipation', R['Hc']*R['deltaHc'], nodes['Investor Possessions'], nodes['Destruction flow'], 4],
        ['Workers possessions dissipation', R['Hw']*R['deltaHw'], nodes['Workers Possessions'], nodes['Destruction flow'], 4],
    ]

    # Nominal Sankey
    Mtitle = 'Monetary Flows in ICED model'
    Mnodes = {
        'Production Sales': 0,
        'Profits': 1,
        'Investors': 2,
        'Workers': 3,
    }
    Mnodes = {k: i for i, k in enumerate([
        'Production Sales',
        'Profits',
        'Investors',
        'Workers'])}
    MLinks0 = [
        ['Wages', R['Ww'], Mnodes['Production Sales'], Mnodes['Workers'], 0],
        ['Dividends', R['Delta']*R['Pi'], Mnodes['Profits'], Mnodes['Investors'], 3],
        ['Interests', R['r']*R['D'], Mnodes['Production Sales'], Mnodes['Investors'], 3],
        ['ConsWork', R['Ww'], Mnodes['Workers'], Mnodes['Production Sales'], 1],
        ['ConsCap', R['kappaC']*R['Wc'], Mnodes['Investors'], Mnodes['Production Sales'], 1],
        ['Profits', R['Pi'], Mnodes['Production Sales'], Mnodes['Profits'], 2],
        ['Debt-based Investment', (1-R['kappaC'])*R['Wc'], Mnodes['Investors'], Mnodes['Production Sales'], 8],
        ['Reinvested Profits', R['Pi']*(1-R['Delta']), Mnodes['Profits'], Mnodes['Production Sales'], 4],
    ]
    MUnits = "$"
    MScale = R['Y']*R['p']/(R['Y'][0]*R['p'][0])

    OutM = Sankey(nodes=Mnodes, Links0=MLinks0, time=R['time'], Units=MUnits, title=Mtitle, Scale=False, returnFig=True)
    OutP = Sankey(nodes=nodes, Links0=Links0, time=R['time'], Units=Units, title=title, Scale=False, returnFig=True)
    return OutM, OutP


_SUPPLEMENTS = {'Sankey': get_sankeys}

_LOGICS = merge_model(_LOGICS_3CAP, _LOGICS_MINICHI, verb=False)
_LOGICS = merge_model(_LOGICS, _LOGICS_INEQ, verb=False)
_LOGICS = merge_model(_LOGICS, _LOGICS_ENDO, verb=False)

_PRESETS = {
    'default': {
        'com': 'Changes nothing, just plot holders',
        'fields': {},
        'plots': {
            'nyaxis': [
                dict(y=[['ab', 'ag'], ['Ag'], ['Emission']],
                     title='Extensive technological properties'),
                dict(y=[['epsilony', 'epsilong'], ['Eeff'], ['Color']],
                     title='Repartition'),
                dict(y=[['nu'], ['delta', 'g'], ['a'], ['pi', 'omega'], ['employment']],
                     title='Monosectoral equivalent'),
                dict(y=[['rocb', 'rocg'], ['pi', 'omega']],
                     title='Market dynamics'),
                dict(y=[['Ky', 'Kb', 'Kg'], ['C', 'Y', 'Iy', 'Ib', 'Ig']],
                     log=['log', 'linear'],
                     title='Capital'),
                dict(y=[['Ky', 'Kb', 'Kg'], ['ay', 'ab', 'ag', 'a'], ['L'],],
                     log=['log', 'log', 'log'],
                     title='Labor-Capital'),
                dict(y=[['employment'], ['omega'], ['epsilony', 'epsilong'], ['d']]),
                dict(y=[['p', 'pc']], title='prices', log=True)
            ],

        },
    },
}
