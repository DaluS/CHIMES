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
            'units': 'Output per person',
        },
        'N': {
            'value': None,
            'com': 'Population',
            'units': 'pop',
        },
        'K': {
            'value': None,
            'com': 'Capital',
            'units': 'Capital',
        },
        'W': {
            'value': None,
            'com': 'Salary',
            'units': 'dollars',
        },
        'D': {
            'value': None,
            'com': 'Absolute private debt',
            'units': 'dollars',
        },
    },
    'GK_Reduced': {
        'omega': {
            'value': None,
            'com': 'wage share',
            'units': '',
        },
        'lambda': {
            'value': None,
            'com': 'employement rate',
            'units': '',
        },
        'd': {
            'value': None,
            'com': 'relative private debt',
            'units': '',
        },
    },
        
    'COPING': {
        ### CO2 AND TEMPERATURE STATE
        'CO2at': {
            'value': 851,
            'com': 'atmosphere carbon concentration',
            'units': '10^{12} C',
        },
        'CO2up': {
            'value': 460,
            'com': 'Upper layer carbon concentration',
            'units': '10^{12} C',
        },
        'CO2lo': {
            'value': 1740,
            'com': 'deep ocean carbon concentration',
            'units': '10^{12} C',
        },
        'T': {
            'value': .85,
            'com': 'Atmosphere temperature',
            'units': '',
        },
        'T0': {
            'value': .0068,
            'com': 'Deep ocean temperature',
            'units': '',
        },
        ### EMISSIONS AND FORCING 
        'E_ind': {
            'value': 35.85,
            'com'  : 'Industrial CO2 emission per year',
            'units': '10^{12} C t^{-1}',
        },
        'E_land': {
            'value': 2.6,
            'com'  : 'Land CO2 emission per year',
            'units': '10^{12} C t^{-1}',
        'F_exo': {
            'value': 0.5,
            'com'  : 'Exogeneous radiative forcing',
            'units': 'W m^{-2}',
        },
                
        ### TYPICAL ECONOMY VALUES
        'd': {
            'value': 1.53,
            'com': 'relative private debt',
            'units': '',
        },    
        'lambda': {
            'value': .675,
            'com': 'employement rate',
            'units': '',
        },
        'Y': {
            'value': 59.74,
            'com': 'GDP',
            'units': '10^{12} dollars',
        },
        'N': {
            'value': 4.83,
            'com': 'Population',
            'units': '10^{9} pop',
        },
        'omega': {
            'value': .578,
            'com': 'Wage share of the economy',
            'units': '',
        },
        'p': {
            'value': 1,
            'com': 'Price level',
            'units': 'dollars',
        },        
        
        ### COUPLING ECONOMY-CLIMATE
        'p_bs': {
            'value': 574.22,
            'com': 'Price backstop technology',
            'units': 'dollars',
        },   
        'g_sigma': {
            'value': -0.0152,
            'com': 'Growth rate of the emission intensity of the economy',
            'units': 't^{-1}',
        },   
    }
}

        ### CLIMATE VARIABLES FOR MINIMODEL

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
