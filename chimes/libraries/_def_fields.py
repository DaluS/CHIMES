

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
import numpy as np
from .._config import config

from .fields_library import ADDITIONAL_FIELDS

# #############################################################################
# #############################################################################
#                   Library (new formalism)
# #############################################################################

############################################################
# DANGER ZONE DO NOT MODIFY IF YOU ARE NOT SURE ############
_LIBRARY = {
    'Numerical': {
        # TIME GESTION ##############################################
        'Tsim': {
            'value': 100,
            'units': 'y',
            'definition': 'Total simulated time',
        },
        'Tini': {
            'value': 0,
            'definition': 'Initial time for simulations',
            'units': 'y',
        },
        'dt': {
            'value': 0.1,
            'units': 'y',
            'definition': 'solver timestep',
        },

        # You should not modify this here, use preset or setdfields ##
        'nx': {
            'value': 1,
            'list': [''],
            'units': '',
            'definition': 'Number of system in parrallel',
            'eqtype': 'size',
        },
        'nr': {
            'value': 1,
            'list': [''],
            'units': '',
            'definition': 'Number of regions interconnected',
            'eqtype': 'size',
        },
        'Nprod': {
            'value': 1,
            'units': '',
            'list': ['MONO'],
            'definition': 'Name of productive sectors',
            'eqtype': 'size',
        },

        '__ONE__': {
            'value': 1,
            'units': '',
            'definition': 'value by default for monosectorial field',
            'list': ['']
        },
        'time': {
            'initial': 0.,
            'func': lambda dt=0: 1.,
            'definition': 'Time vector',
            'com': 'dt/dt=1, time as ODE',
            'units': 'y',
            'eqtype': 'differential',
        },
        'nt': {
            'func': lambda Tsim=0, dt=1: int(Tsim / dt),
            'units': '',
            'definition': 'Number of timestep',
            'com': 'Constant dt',
            'eqtype': 'parameter',
        },


    },
}
# END OF DANGER ZONE #######################################
############################################################

for k, v in ADDITIONAL_FIELDS.items():
    _LIBRARY[k] = v


# #############################################################################
# #############################################################################
#                   FIELDS OF FIELDS AND EXPECTED VALUES
# #############################################################################

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
        'default': '',
        'type': str,
        'allowed': None,
    },
    'units': {
        'default': 'undefined',
        'type': str,
        'allowed': [
            'Units',
            'y',       # Time
            '$',       # Money
            'C',       # Carbon Concentration
            'Tc',      # Temperature (Celsius)
            'Humans',  # Population
            'W',       # Energy
            'L',       # Length
            '',        # Dimensionless
        ],
    },
    'minmax': {
        'default': [0, 1],
        'type': list,
        'allowed': None
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
    },
    'multisect': {
        'default': '',
        'type': str,
        'allowed': None,
    },
    'size': {
        'default': ['__ONE__', '__ONE__'],
        'type': list,
        'allowed': None
    }
}


def _complete_DFIELDS(
    dfields=_DFIELDS,
    default_fields=__DEFAULTFIELDS,
    complete=True,
    check=True,
):
    """ Complete dfields from default"""

    # --------------------
    # Make sure the default is allowed
    for k0, v0 in default_fields.items():
        if v0.get('allowed') is not None:
            default_fields[k0]['allowed'].append(v0['default'])

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
                    dfields[k0][k1] = str('$' + k0 + '$') if '$' not in k0 else k0
                else:
                    dfields[k0][k1] = default_fields[k1]['default']
    """
            # ---------
            # check
            if check and v0.get(k1) is not None:
                # check type
                if not type(v0[k1]) in default_fields[k1]['type']:
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
                                u0 in lok and all([
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
            "The following entries in _DFIELDS are not valid:\n" + "\n".join(set(lstr))
        )
        raise Exception(msg)
    """
    return dfields


_DFIELDS = _complete_DFIELDS(_DFIELDS)
for k, v in _DFIELDS.items():
    size = v.get('size', [])
    if len(size) == 1:
        v['size'] = [size[0], __DEFAULTFIELDS['size']['default'][1]]
    else:
        v['size'] = __DEFAULTFIELDS['size']['default']
