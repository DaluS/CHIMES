# -*- coding: utf-8 -*-



# #############################################################################
# #############################################################################
#                       Predefined sets of variables
# #############################################################################


_DVAR = {
    'GK': {
        'a': {
            'value': None,
            'com': '',
            'units': '',
        },
        'N': {
            'value': None,
            'com': '',
            'units': '',
        },
        'K': {
            'value': None,
            'com': '',
            'units': '',
        },
        'W': {
            'value': None,
            'com': '',
            'units': '',
        },
        'D': {
            'value': None,
            'com': '',
            'units': '',
        },
    },
    'GK_Reduced': {
        'omega': {
            'value': None,
            'com': '',
            'units': '',
        },
        'lambda': {
            'value': None,
            'com': '',
            'units': '',
        },
        'd': {
            'value': None,
            'com': '',
            'units': '',
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
