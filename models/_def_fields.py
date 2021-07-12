# -*- coding: utf-8 -*-

"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

"""


import warnings


import numpy as np


# #############################################################################
# #############################################################################
#                   Dict of default fields 
# #############################################################################


_DFIELDS = {
    # --------------
    # Numerical
    'Tmax': {
        'value': 100,
        'com': 'Duration of simulation',
        'dimension': 'time',
        'units': 'y',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'nx': {
        'value': 1,
        'com': 'Number of similar systems evolving in parrallel',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'dt': {
        'value': 0.01,
        'com': 'Time step (fixed timestep method)',
        'dimension': 'time',
        'units': 'y',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'Tstore': {
        'value': None,  # Dynamically allocated
        'com': 'Time between storages (if StorageMode=full, it goes to dt)',
        'dimension': 'time',
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'nt': {
        'value': None,  # Dynamically allocated
        'com': 'Number of temporal iteration',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'ns': {
        'value': None,  # Dynamically allocated
        'com': 'Number of elements stored',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    # 'verb': {
        # 'value': True,
        # 'com': 'flag indicating whether to print intermediate info',
        # 'dimension': None,
        # 'units': None,
        # 'type': None,
        # 'symbol': None,
        # 'group': 'Numerical'
    # },
    'storage': {
        'value': 'full',
        'com': 'flag indicating which time steps to store',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical'
    },
    'save': {
        'value': True,
        'com': 'flag indicating whether to save output data',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical'
    },

    # --------------
    # Time vector
    'time': {
        'func': lambda dt=0: dt,
        'com': 'Time vector',
        'dimension': 'time',
        'units': 'y',
        'type': 'extensive',
        'symbol': r'$t$',
        'group': 'Time',
        'eqtype': 'ode',
        'initial': 0,
    },

    # --------------
    # Population evolution
    'beta': {
        'value': 0.025,
        'com': 'Rate of population growth',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$beta$',
        'group': 'Population',
    },
    'alpha': {
        'value': 0.02,
        'com': 'Rate of productivity increase',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$alpha$',
        'group': 'Population',
    },

    # --------------
    # Capital properties
    'delta': {
        'value': 0.005,
        'com': 'Rate of capital depletion',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta$',
        'group': 'Capital',
    },

    # --------------
    # Production
    'nu': {
        'value': 3,
        'com': 'Kapital to output ratio',   # !! IN CES its 1/A !!',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'\nu',
        'group': 'Production',
    },
    'eta': {
        'value': 1000,
        'com': '1/(1+substituability)',     # CES parameter
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },
    'b': {
        'value': .5,
        'com': 'capital part of the production',    # CES parameter
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },
    'z': {
        'value': 1,
        'com': 'Markup on salary estimation by employer',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Production',
    },

    # --------------
    # INTEREST / Price
    'r': {
        'value': .03,
        'com': 'Interest at the bank',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'etaP': {
        'value': .192,
        'com': 'Typical rate for inflation',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'muP': {
        'value': 1.3,
        'com': 'Mark-up of price',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },
    'gammaP': {
        'value': 1,
        'com': 'Money-illusion',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },

    # --------------
    # PHILIPS CURVE (employement-salary increase)
    'phinull': {
        'value': 0.04,
        'com': 'Unemployment rate that stops salary increase (no inflation)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },
    'phi0': {
        'value': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': '',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },
    'phi1': {
        'value': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': '',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },

    # --------------
    # KEEN INVESTMENT FUNCTION (profit-investment function)
    'k0': {
        'value': -0.0065,
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_0$',
        'group': 'Keen',
    },
    'k1': {
        'value': np.exp(-5),
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_1$',
        'group': 'Keen',
    },
    'k2': {
        'value': 20,
        'com': '',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_2$',
        'group': 'Keen',
    },

    # --------------
    # LINEAR DIVIDENT PROFITS
    'div0': {
        'value': 0.138,
        'com': 'Part of GDP as dividends when pi=0',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$div_0$',
        'group': 'Dividends',
    },
    'div1': {
        'value': 0.473,
        'com': 'Slope',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$div_1$',
        'group': 'Dividends',
    },

    # --------------
    # Coupling Effets (EDP)
    'g1': {
        'value': .0,
        'com': 'GLOBAL EFFECTS OF LAMBDA (Mean field)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$g_1$',
        'group': 'Coupling',
    },
    'g2': {
        'value': .00,
        'com': 'WITH NEIGHBORS EFFECTS OF LAMBDA (field)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$g_2$',
        'group': 'Coupling',
    },
    'muI': {
        'value': 0.,
        'com': '',
        'dimension': None,
        'units': "NOTDONEYET",
        'type': 'intensive',
        'symbol': r'$_mu_I$',
        'group': 'Coupling',
    },
    'muN': {
        'value': 0.,
        'com': '',
        'dimension': None,
        'units': "NOTDONEYET",
        'type': 'intensive',
        'symbol': r'$\mu_N$',
        'group': 'Coupling',
    },

    # --------------
    # RELAXATION-BUFFER DYNAMICS
    'tauR': {
        'value': 2.0,
        'com': 'Typical time for recruitement',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_R$',
        'group': 'RelaxBuffer',
    },
    'tauF': {
        'value': 0.1,
        'com': 'Typical time for firing',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_F$',
        'group': 'RelaxBuffer',
    },
    'tauL': {
        'value': 2.,
        'com': 'Typical time for employement information',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$tau_L$',
        'group': 'RelaxBuffer',
    },
    'tauK': {
        'value': 2.,
        'com': 'Typical time on new capital integration',
        'dimension': 'time',
        'units': 'y',
        'type': 'intensive',
        'symbol': r'$\tau_K$',
        'group': 'RelaxBuffer',
    },

    # --------------
    # GEMMES PARAMETERS
    'theta': {
        'value': 2.6,
        'com': 'Convexity on abattement cost function',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\theta$',
        'group': 'Gemmes',
    },
    'dsigma': {
        'value': -0.001,
        'com': 'Variation rate of the growth of emission intensity',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{\sigma}$',
        'group': 'Gemmes',
    },
    'dPBS': {
        'value': -0.005,
        'com': 'Growth rate of back-stop technology price',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{PBS}$',
        'group': 'Gemmes',
    },
    'dEland': {
        'value': -0.022,
        'com': 'Growth rate of land use change in CO2 emission',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta_{Eland}$',
        'group': 'Gemmes',
    },

    # --------------
    # Damage function (on GDP)
    # D = 1 - (1 + p['pi1']*T + p['pi2']*T**2 + p['pi3']*T**p['zeta'] )**(-1)
    'pi1': {
        'value': 0.,
        'com': 'Linear temperature impact',
        'dimension': 'Temperature rate',
        'units': 'C^{-1}',
        'type': 'intensive',
        'symbol': r'$\pi_1$',
        'group': 'Damage',
    },
    'pi2': {
        'value': .00236,
        'com': 'Quadratic temperature impact',
        'dimension': None,
        'units': 'C^{-2}',
        'type': 'intensive',
        'symbol': r'$\pi_2$',
        'group': 'Damage',
    },
    'pi3': {
        'value': .00000507,
        'com': 'Weitzmann Damage temperature impact',
        'dimension': None,
        'units': 'C^{-zeta}',
        'type': 'intensive',
        'symbol': r'$\pi_3$',
        'group': 'Damage',
    },
    'zeta': {
        'value': 6.754,
        'com': 'Weitzmann impact',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\zeta$',
        'group': 'Damage',
    },
    'fk': {
        'value': 1. / 3.,
        'com': 'Fraction of environmental damage',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$f_K$',
        'group': 'Damage',
    },

    # allocated to the stock of capital

    # --------------
    # Climate model
    'Phi12': {
        'value': .024,
        'com': 'Transfer of carbon from atmosphere to biosphere',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_{1\rightarrow2}$',
        'group': 'Climate',
    },
    'Phi23': {
        'value': .001,
        'com': 'Transfer from biosphere to stock',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_{2\rightarrow3}$',
        'group': 'Climate',
    },
    'C': {
        'value': 1 / .098,
        'com': 'Heat capacity of fast-paced climate',
        'dimension': None,
        'units': "SI",
        'type': 'intensive',
        'symbol': r'$C$',
        'group': 'Climate',
    },
    'C0': {
        'value': 3.52,
        'com': 'Heat capacity of inertial component of climate',
        'dimension': None,
        'units': "SI",
        'type': 'intensive',
        'symbol': r'$C_0$',
        'group': 'Climate',
    },
    'gammaHEAT': {
        'value': 0.0176,
        'com': 'Heat exchange coefficient between layer',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\gamma_{heat}$',
        'group': 'Climate',
    },
    'Tsens': {
        'value': 3.1,
        'com': 'Climate sensitivity (deltaT/log2CO2)',
        'dimension': 'Temperature',
        'units': 'C',
        'type': 'intensive',
        'symbol': r'$T_{sens}$',
        'group': 'Climate',
    },

    'FexoMax': {
        'value': 0.7,
        'com': 'Maximal exougenous radiative forcing',
        'dimension': None,
        'units': 'W M^{-2}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Climate',
    },
    'F2CO2': {
        'value': 3.681,
        'com': 'doubling CO2 impact on forced radiations',
        'dimension': None,
        'units': 'W/m2',
        'type': 'intensive',
        'symbol': r'$F^2_{CO2}$',
        'group': 'Climate',
    },

    'PopSat': {
        'value': 12,
        'com': 'Maximal population (billions)',
        'dimension': 'Humans',
        'units': 'Humans',
        'type': 'intensive',
        'symbol': r'$N_{sat}$',
        'group': 'Population',
    },

    # --------------
    # Variables
    'a': {
        'value': None,
        'com': 'productivity per worker',
        'dimension': 'Productivity',
        'units': 'Output Humans^{-1}',
        'type': 'intensive',
        'symbol': r'$a$',
        'group': 'Economy',
    },
    'N': {
        'value': 4.83,
        'com': 'Population',
        'dimension': 'Humans',
        'units': '10^{9} Humans',
        'type': 'extensive',
        'symbol': r'$N$',
        'group': 'Population',
    },
    'K': {
        'value': None,
        'com': 'Capital',
        'dimension': 'Money',
        'units': 'Technological Unit',
        'type': 'extensive',
        'symbol': r'$K$',
        'group': 'Economy',
    },
    'W': {
        'value': None,
        'com': 'Salary',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$W$',
        'group': 'Economy',
    },
    'D': {
        'value': None,
        'com': 'Absolute private debt',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$D$',
        'group': 'Economy',
    },
    'omega': {
        'value': .578,
        'com': 'Wage share of the economy',
        'dimension': '',
        'units': '',
        'type': 'intensive',
        'symbol': r'$\omega$',
        'group': 'Economy',
    },
    'lambda': {
        'value': .675,
        'com': 'employment rate',
        'dimension': '',
        'units': '',
        'type': 'intensive',
        'symbol': r'$\lambda$',
        'group': 'Economy',
    },
    # TYPICAL ECONOMY VALUES
    'd': {
        'value': 1.53,
        'com': 'relative private debt',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$d$',
        'group': 'Economy',
    },
    # CO2 AND TEMPERATURE STATE
    'CO2at': {
        'value': 851,
        'com': 'atmosphere carbon concentration',
        'dimension': 'Gas concentration',
        'units': 'GtC',
        'type': 'intensive',
        'symbol': r'$CO2_{at}$',
        'group': 'Climate',
    },
    'CO2up': {
        'value': 460,
        'com': 'Upper layer carbon concentration',
        'dimension': 'Gas concentration',
        'units': 'GtC',
        'type': 'intensive',
        'symbol': r'$CO2_{up}$',
        'group': 'Climate',
    },
    'CO2lo': {
        'value': 1740,
        'com': 'deep ocean carbon concentration',
        'dimension': 'Gas concentration',
        'units': 'GtC',
        'type': 'intensive',
        'symbol': r'$CO2_{deep}$',
        'group': 'Climate',
    },
    'T': {
        'value': .85,
        'com': 'Atmosphere temperature',
        'dimension': 'Temperature',
        'units': 'C',
        'type': 'intensive',
        'symbol': r'$T$',
        'group': 'Climate',
    },
    'T0': {
        'value': .0068,
        'com': 'Deep ocean temperature',
        'dimension': 'Temperature',
        'units': 'C',
        'type': 'intensive',
        'symbol': r'$T_0$',
        'group': 'Climate',
    },
    # EMISSIONS AND FORCING 
    'E_ind': {
        'value': 35.85,
        'com'  : 'Industrial CO2 emission per year',
        'dimension': 'Gas flux',
        'units': 'GtC Y^{-1}',
        'type': 'extensive',
        'symbol': r'$E_{ind}$',
        'group': 'Climate',
    },
    'E_land': {
        'value': 2.6,
        'com'  : 'Land CO2 emission per year',
        'dimension': 'Gas flux',
        'units': 'GtC Y^{-1}',
        'type': 'extensive',
        'symbol': r'$E_{land}$',
        'group': 'Climate',
    },
    'F_exo': {
        'value': 0.5,
        'com'  : 'Exogeneous radiative forcing',
        'dimension': 'Power flux',
        'units': 'W m^{-2}',
        'type': 'extensive',
        'symbol': r'$F_{exo}$',
        'group': 'Climate',
    },
    # PUT Yn for Nominal output
    'Yn': {
        'value': 59.74,
        'com': 'GDP',
        'dimension': 'Money',
        'units': '10^{12} Dollars',
        'type': 'extensive',
        'symbol': r'$Y_n$',
        'group': 'Economy',
    },
    'p': {
        'value': 1,
        'com': 'indicative Price level',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'intensive',
        'symbol': r'$p$',
        'group': 'Economy',
    },
    # COUPLING ECONOMY-CLIMATE
    'p_bs': {
        'value': 574.22,
        'com': 'Price backstop technology',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'intensive',
        'symbol': r'$p_{bs}$',
        'group': 'Economy',
    },
    'g_sigma': {
        'value': -0.0152,
        'com': 'Growth rate of the emission intensity of the economy',
        'dimension': 'time rate',
        'units': 'Y^{-1}',
        'type': 'intensive',
        'symbol': r'$g_{\sigma}$',
        'group': 'Economy',
    },
    # From functions
    'pi': {
        'value': None,
        'com': 'relative profit?',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$\pi$',
        'group': 'Economy',
    },
    'Pi': {
        'value': None,
        'com': 'Absolute profit?',
        'dimension': 'Money?',
        'units': '',
        'type': '',
        'symbol': r'$\Pi$',
        'group': 'Economy',
    },
    'g': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$g$',
        'group': '?',
    },
    'philips': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$\phi$',
        'group': 'Economy',
    },
    'worker': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': '',
        'group': 'Economy',
    },
    'GDP': {            # Possible conflict with 'Yn'?
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$GDP$',
        'group': 'Economy',
    },
    'invest': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': '',
        'group': 'Economy',
    },
    'kappa': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$\kappa$',
        'group': 'Economy',
    },
    # Missing
    'Y': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$Y$',
        'group': 'Missing',
    },
    'L': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$L$',
        'group': 'Missing',
    },
    'i': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$i$',
        'group': 'Missing',
    },
    'I': {
        'value': None,
        'com': '',
        'dimension': '',
        'units': '',
        'type': '',
        'symbol': r'$I$',
        'group': 'Missing',
    },
}


# #############################################################################
# #############################################################################
#               Conformity checks (for saefty, to detect typos...) 
# #############################################################################


# dict of allowed fields (None => no restriction)
_DALLOWED_FIELDS = {
    'value': None,
    'com': None,
    'dimension': [
        'time', 'time rate',
        'Temperature', 'Temperature rate',
        'Gas concentration', 'Gas flux',
        'Power flux',
        'Humans',
        'Money'
    ],
    'units': [
        'y', 'y^{-1}',
        'Dollars',
        'C', 'C^{-1}', 'C^{-2}', 'C^{-zeta}',
        'Humans',
        'W/m2',
    ],
    'type': ['intensive', 'extensive', 'dimensionless'],
    'symbol': None,
    'group': [
        'Numerical',
        'Population',
        'Prices', 'Capital', 'Philips', 'Gemmes',
        'Keen', 'Dividends', 'Economy', 'Production',
        'Coupling',
        'RelaxBuffer',
        'Climate', 'Damage',
    ],
}


# List non-conform keys in dict, for detailed error printing
dk0 = {
    k0: [
        v0[ss] for ss in _DALLOWED_FIELDS.keys()
        if _DALLOWED_FIELDS[ss] is not None and not (
            v0[ss] is None
            or v0[ss] == ''
            or v0[ss] in _DALLOWED_FIELDS[ss]
        )
    ]
    for k0, v0 in _DFIELDS.items()
    if not (
        isinstance(v0, dict)
        and sorted(_DALLOWED_FIELDS) == sorted(v0.keys())
        and all([
            v0[ss] is None
            or v0[ss] == ''
            or v0[ss] in _DALLOWED_FIELDS[ss]
            for ss in _DALLOWED_FIELDS.keys()
            if _DALLOWED_FIELDS[ss] is not None
        ])
    )
}


# Raise warning if any non-conformity
# Include details per key
if len(dk0) > 0:
    lstr = [f'\t- {k0}: {v0}' for k0, v0 in dk0.items()]
    msg = (
        "The following keys of _DFIELDS are non-conform:\n"
        + "\n".join(lstr)
    )
    warnings.warn(msg)
