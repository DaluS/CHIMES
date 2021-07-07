# -*- coding: utf-8 -*-



# #############################################################################
# #############################################################################
#                       Predefined sets of variables
# #############################################################################


_DVAR = {
    'GK': {
        'a': {
            'value': None,
            'com': 'productivity per worker',
            'dimension': 'Productivity',
            'units': 'Output Humans^{-1}',
            'type': 'intensive',
            'symbol': r'$a$',
        },
        'N': {
            'value': None,
            'com': 'Population',
            'dimension': 'Humans',
            'units': 'Humans',
            'type': 'extensive',
            'symbol': r'$N$',
        },
        'K': {
            'value': None,
            'com': 'Capital',
            'dimension': 'Money',
            'units': 'Technological Unit',
            'type': 'extensive',
            'symbol': r'$K$',
        },
        'W': {
            'value': None,
            'com': 'Salary',
            'dimension': 'Money',
            'units': 'Dollars',
            'type': 'extensive',
            'symbol': r'$W$',
        },
        'D': {
            'value': None,
            'com': 'Absolute private debt',
            'dimension': 'Money',
            'units': 'Dollars',
            'type': 'extensive',
            'symbol': r'$D$',
        },
    },
    'GK_Reduced': {
        'omega': {
            'value': None,
            'com': 'wage share',
            'dimension': '',
            'units': '',
            'type': 'intensive',
            'symbol': r'$\omega$',
        },
        'lambda': {
            'value': None,
            'com': 'employment rate',
            'dimension': '',
            'units': '',
            'type': 'intensive',
            'symbol': r'$\lambda$',
        },
        'd': {
            'value': None,
            'com': 'relative private debt',
            'dimension': '',
            'units': '',
            'type': 'intensive',
            'symbol': r'$d$',
        },
    },
    'COPING': {
        # CO2 AND TEMPERATURE STATE
        'CO2at': {
            'value': 851,
            'com': 'atmosphere carbon concentration',
            'dimension': 'Gas concentration',
            'units': 'GtC',
            'type': 'intensive',
            'symbol': r'$CO2_{at}$',
        },
        'CO2up': {
            'value': 460,
            'com': 'Upper layer carbon concentration',
            'dimension': 'Gas concentration',
            'units': 'GtC',
            'type': 'intensive',
            'symbol': r'$CO2_{up}$',
        },
        'CO2lo': {
            'value': 1740,
            'com': 'deep ocean carbon concentration',
            'dimension': 'Gas concentration',
            'units': 'GtC',
            'type': 'intensive',
            'symbol': r'$CO2_{deep}$',
        },
        'T': {
            'value': .85,
            'com': 'Atmosphere temperature',
            'dimension': 'Temperature',
            'units': '+T (C)',
            'type': 'intensive',
            'symbol': r'$T$',
        },
        'T0': {
            'value': .0068,
            'com': 'Deep ocean temperature',
            'dimension': 'Temperature',
            'units': '+T (C)',
            'type': 'intensive',
            'symbol': r'$T_0$',
        },
        # EMISSIONS AND FORCING 
        'E_ind': {
            'value': 35.85,
            'com'  : 'Industrial CO2 emission per year',
            'dimension': 'Gas flux',
            'units': 'GtC Y^{-1}',
            'type': 'extensive',
            'symbol': r'$E_{ind}$',
        },
        'E_land': {
            'value': 2.6,
            'com'  : 'Land CO2 emission per year',
            'dimension': 'Gas flux',
            'units': 'GtC Y^{-1}',
            'type': 'extensive',
            'symbol': r'$E_{land}$',
        },
        'F_exo': {
            'value': 0.5,
            'com'  : 'Exogeneous radiative forcing',
            'dimension': 'Power flux',
            'units': 'W m^{-2}',
            'type': 'extensive',
            'symbol': r'$F_{exo}$',
        },
        # TYPICAL ECONOMY VALUES
        'd': {
            'value': 1.53,
            'com': 'relative private debt',
            'dimension': 'Money',
            'units': '',
            'type': 'intensive',
            'symbol': r'$d$',
        },
        'lambda': {
            'value': .675,
            'com': 'employment rate',
            'dimension': '',
            'units': '',
            'type': 'intensive',
            'symbol': r'$\lambda$',
        },
        # PUT Yn for Nominal output
        'Yn': {
            'value': 59.74,
            'com': 'GDP',
            'dimension': 'Money',
            'units': '10^{12} Dollars',
            'type': 'extensive',
            'symbol': r'$Y_n$',
        },
        'N': {
            'value': 4.83,
            'com': 'Population',
            'dimension': 'Humans',
            'units': '10^{9} Humans',
            'type': 'extensive',
            'symbol': r'$N$',
        },
        'omega': {
            'value': .578,
            'com': 'Wage share of the economy',
            'dimension': '',
            'units': '',
            'type': 'intensive',
            'symbol': r'$\omega$',
        },
        'p': {
            'value': 1,
            'com': 'indicative Price level',
            'dimension': 'Money',
            'units': 'Dollars',
            'type': 'intensive',
            'symbol': r'$p$',
        },
        # COUPLING ECONOMY-CLIMATE
        'p_bs': {
            'value': 574.22,
            'com': 'Price backstop technology',
            'dimension': 'Money',
            'units': 'Dollars',
            'type': 'intensive',
            'symbol': r'$p_{bs}$',
        },
        'g_sigma': {
            'value': -0.0152,
            'com': 'Growth rate of the emission intensity of the economy',
            'dimension': 'time rate',
            'units': 'Y^{-1}',
            'type': 'intensive',
            'symbol': r'$g_{\sigma}$',
        },
    },
}


# #############################################################################
# #############################################################################
#                       Getting the choosen set of variables
# #############################################################################


def get_variables(varset=None):
    """ Return a dict of variables """
    c0 = varset in _DVAR.keys()
    if c0 is not True:
        lstr = [
            "\t- '{}': {}".format(k0, sorted(v0.keys()))
            for k0, v0 in _DVAR.items()
        ]
        msg = (
            "Arg varset must be a valid key to an existing set of variables!\n"
            + "\n".join(lstr)
            + "\nYou provided: {}".format(varset)
        )
        raise Exception(msg)
    return _DVAR[varset]
