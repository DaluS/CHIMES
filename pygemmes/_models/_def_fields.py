# -*- coding: utf-8 -*-

"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

----

This file contains :
    _DFIELDS the big dictionnary with basic information on
        * Variables
        * Parameters
        * Numerical parameters

    _DALLOWED_FIELDS : Contains all the restrictions on each field for each
    element in _DFIELD
    _DEFAULTFIELDS : The value that will be added if none are

    __DOTHECHECK Flag to check or not the dictionnary
    __FILLDEFAULTVALUES Flag to fill the defaultfields
"""


import warnings


import numpy as np


__DOTHECHECK = True
__FILLDEFAULTVALUES = True


# #############################################################################
# #############################################################################
#                   FIELDS OF FIELDS AND EXPECTED VALUES
# #############################################################################
# dict of default value in fields


__DEFAULTFIELDS = {
    'value': {
        'default': None,
        'type': (int, float, np.int_, np.float_, np.ndarray, list),
        'allowed': None,
    },
    'definition': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'com': {
        'default': 'No comment',
        'type': str,
        'allowed': None,
    },
    'dimension': {
        'default': 'undefined',
        'type': str,
        'allowed': None,
    },
    'units': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'Units',  #
            'y',      # Time
            '$',      # Money
            'C',      # Concentration
            'Humans',  # Population
            '',
        ],
    },
    'type': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'intensive',
            'extensive',
            'dimensionless',
        ],
    },
    'symbol': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'group': {
        'default': '',
        'type': str,
        'allowed': None,
        # 'Numerical',
        # 'Population',
        # 'Prices', 'Capital', 'Philips', 'Gemmes',
        # 'Keen', 'Dividends', 'Economy', 'Production',
        # 'Coupling',
        # 'RelaxBuffer',
        # 'Climate', 'Damage',
    },
}


# --------------------
# Make sure the default is allowed
for k0, v0 in __DEFAULTFIELDS.items():
    if v0.get('allowed') is not None:
        __DEFAULTFIELDS[k0]['allowed'].append(v0['default'])


# #############################################################################
# #############################################################################
#                   Library (new formalism)
# #############################################################################


_LIBRARY = {
    'Temporary': {
        'Final': {'value': 0,
                  'definition': 'Final value',
                  },
        'Omega': {'value': 1,
                  'definition': 'Pulsation',
                  },
        'gamma': {'value': 1,
                  'definition': 'Dampening',
                  },
    },


    'Numerical': {
        'Tmax': {
            'value': 100,
            'units': 'y',
            'definition': 'Total simulated time',
        },
        'dt': {
            'value': 0.01,
            'units': 'y',
            'definition': 'time between two steps',
        },
        'nt': {
            'func': lambda Tmax=0, dt=1: int(Tmax / dt),
            'units': '',
            'definition': 'Number of timestep',
            'com': 'Constant dt',
            'eqtype': 'param',
        },
        'nx': {
            'value': 1,
            'units': 'y',
            'definition': 'NUMBER OF PARRALLEL SYSTEMS',
        },
        'time': {
            'initial': 0.,
            'func': lambda dt=0: 1.,
            'definition': 'Time vector',
            'com': 'dt/dt=1, time as ODE',
            'units': 'y',
            'eqtype': 'ode',
        },
    },


    'Household': {
        # VARIABLES
        'N': {
            'value': 1.,
            'definition': 'Population',
            'units': 'Humans',
        },
        'L': {
            'value': None,
            'definition': 'Workers',
            'units': 'Humans',
        },
        'a': {
            'value': 1,
            'units': 'Units.Humans^{-1}.y^{-1}',
            'definition': 'Productivity',
        },
        'w': {
            'value': 0.85,
            'definition': 'Wage value',
            'units': '$.Humans^{-1}.y^{-1}'
        },

        # INTERMEDIARY TYPICAL VARIABLES
        'lambda': {
            'value': .97,
            'definition': 'employement rate',
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
        'beta': {
            'value': 0.025,
            'definition': 'Rate of population growth',
            'units': 'y^{-1}',
        },
        'alpha': {
            'value': 0.02,
            'definition': 'Rate of productivity increase',
            'units': 'y^{-1}',
        },
    },

    'Recipies': {
        'gamma': {
            'value': 0.1,
            'definition': 'Input-output production recipy',
            'units': '',
        },
        'Xi': {
            'value': 0.1,
            'definition': 'Input-output capital recipy',
            'units': '',
        },
        'rho': {
            'value': 0.1,
            'definition': 'Capital consumption recipy',
            'units': 'y^{-1}',
        },
    },

    'Production': {
        # VARIABLES
        'K': {
            'value': 2.7,
            'units': 'Units',
            'definition': 'Capital',
        },
        'Y': {
            'value': None,
            'definition': 'GDP in output quantity',
            'units': 'Units.y^{-1}',
        },
        'GDP': {
            'value': None,
            'definition': 'GDP in output quantity',
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
            'units': 'Units',
        },


        # INTERMEDIARY VARIABLES
        'g': {
            'value': None,
            'definition': 'Relative growth of GDP',
            'units': 'y^{-1}',
        },
        'pi': {
            'value': None,
            'definition': 'relative profit',
            'units': '',
            'symbol': r'$\pi$',
        },
        'Pi': {
            'value': None,
            'definition': 'Absolute profit',
            'units': '$.y^{-1}',
            'symbol': r'$\Pi$',
        },
        'c': {
            'value': None,
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
        'nu': {
            'value': 3,
            'definition': 'Kapital to output ratio',
            'units': '',
            'symbol': r'$\nu$',
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
            'value': None,
            'definition': 'Wage inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$\phi$',
        },
        'phinull': {
            'value': 0.04,
            'definition': 'Unemployment rate with no salary increase',
            'units': '',
        },
        'phi0': {
            'func': lambda phinull=0: phinull / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'param',
        },
        'phi1': {
            'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
            'definition': 'Parameter1 for diverving squared',
            'com': '',
            'units': '',
            'eqtype': 'param',
        },
        'zphi': {
            'value': 0.1,
            'definition': 'nonlinearity on profit in negociation',
            'com': '',
            'units': ''
        }

    },

    'Investment': {
        'I': {
            'value': None,
            'definition': 'Investment in money',
            'units': '$.y^{-1}',
        },
        'Ir': {
            'value': None,
            'definition': 'Number of real unit from investment',
            'units': 'Units.y^{-1}',
        },
        'kappa': {
            'value': None,
            'definition': 'Part of GDP in investment',
            'units': '',
            'symbol': r'$\kappa$',
        },
        'k0': {
            'value': -0.0065,
            'definition': 'Percent of GDP invested when profit is zero',
            'units': '',
        },
        'k1': {
            'value': np.exp(-5),
            'definition': 'Investment slope',
            'units': '',
        },
        'k2': {
            'value': 20,
            'definition': 'Investment power in kappa',
            'units': '',
        },
        'zsolv': {
            'value': 0.1,
            'definition': 'nonlinearity on solvability in investment',
            'com': '',
            'units': ''
        }
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
            'units': '',
        },
        'solvability': {
            'definition': 'capital compared to debt',
            'units': ''
        },
    },

    'Prices': {
        # VARIABLES
        'inflation': {
            'value': None,
            'definition': 'inflation rate',
            'units': 'y^{-1}',
        },
        'p': {
            'value': 1,
            'definition': 'price of goods',
            'units': '$.Units^{-1}'
        },

        # PARAMETERS
        'mu': {
            'value': 2,
            'definition': 'Markup on prices',
            'units': '',
        },
        'eta': {
            'value': 1,
            'definition': 'timerate of price adjustment',
            'units': 'y^{-1}',
        },
        'chi': {
            'value': 1,
            'definition': 'inflation rate on inventory',
            'units': 'y^{-1}', }

    },

    'Consumption': {
        # VARIABLES
        'C': {'value': None,
              'definition': 'Purchased good flow',
              'units': 'Units.y^{-1}',
              'symbol': r'$C$',
              },
        'H': {'value': 0,
              'definition': 'Household possessions',
              'units': 'Units',
              'symbol': r'$H$', },
        'Hid': {'value': None,
                'definition': 'Household optimal possessions',
                'units': 'Units',
                'symbol': r'$H^{id}$', },

        # PARAMETERS
        'deltah': {'value': 0.1,
                   'definition': 'possessions deterioration rate',
                   'units': 'y^{-1}',
                   'symbol': r'$\delta^h$', },
        'fC': {'value': 1,
               'definition': 'Typical rate for consumption optimisation',
               'units': 'y^{-1}',
               'symbol': r'$f$', },
        'Omega0': {'value': 1,
                   'definition': 'Purchasing power of inflexion',
                   'units': 'Units.Humans^{-1}.y^{-1}',
                   'units': None},
        'x': {'value': 1,
              'definition': 'Inflexion effectiveness',
              'Units': None},
        'h': {'value': 1,
              'definition': 'saturated p per person',
              'units': None},
    },
}


# ------------------------------------
# Derive new _DFIELDS from _LIBRARY

__LKLIB = [dict.fromkeys(v0.keys(), k0) for k0, v0 in _LIBRARY.items()]
for ii, dd in enumerate(__LKLIB[1:]):
    __LKLIB[0].update(dd)

_DFIELDS = {
    k0: dict(_LIBRARY[v0][k0]) for k0, v0 in __LKLIB[0].items()
}

for k0, v0 in __LKLIB[0].items():
    _DFIELDS[k0]['group'] = v0


# #############################################################################
# #############################################################################
#               Conformity checks (for safety, to detect typos...)
# #############################################################################


def _complete_DFIELDS(
    dfields=_DFIELDS,
    default_fields=__DEFAULTFIELDS,
    complete=__FILLDEFAULTVALUES,
    check=__DOTHECHECK,
):
    """ Complete dfields from default"""

    # --------------
    # run loop

    dfail = {}
    for k0, v0 in dfields.items():
        for k1, v1 in default_fields.items():

            # ---------
            # complete
            if complete and v0.get(k1) is None:
                # set symbol to key if not defined
                if k1 == 'symbol':
                    dfields[k0][k1] = k0
                else:
                    dfields[k0][k1] = default_fields[k1]['default']

            # ---------
            # check
            if check and v0.get(k1) is not None:

                # check type
                if not isinstance(v0[k1], default_fields[k1]['type']):
                    dfail[k0] = (
                        f"wrong type for {k1} "
                        f"({default_fields[k1]['type']} vs {type(v0[k1])})"
                    )

                # check allowed values
                elif default_fields[k1].get('allowed') is not None:

                    # treat units spearately
                    if k1 == 'units':
                        unit = v0[k1].split('.') if '.' in v0[k1] else [v0[k1]]

                        c0 = True
                        lok = default_fields[k1]['allowed']
                        for uu in unit:

                            # simple case
                            if '^{' not in uu:
                                if uu not in lok:
                                    c0 = False
                                    break
                                else:
                                    continue

                            # case with '^{'
                            if not uu.endswith('}'):
                                c0 = False
                                break

                            # check u0 is ok and u1 is a number
                            u0, u1 = uu.split('^{')
                            u1 = u1[:-1].split('.')
                            c0 = (
                                u0 in lok
                                and all([
                                    u11.strip('-').isdigit() for u11 in u1
                                ])
                            )
                            if not c0:
                                break

                    else:
                        c0 = v0[k1] in default_fields[k1]['allowed']

                    if not c0:
                        dfail[k0] = (
                            f"Non-allowed value for {k1} "
                            f"({default_fields[k1]['allowed']} vs {v0[k1]})"
                        )

    # --------------
    # Raise exception if relevant
    if len(dfail) > 0:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
        msg = (
            "The followinbg entries in _DFIELDS are not valid:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)


_complete_DFIELDS()
