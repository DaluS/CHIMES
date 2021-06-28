# -*- coding: utf-8 -*-


import _def_parameters


# #############################################################################
# #############################################################################
#                       dinput checks
# #############################################################################


def _check_dinput(dinput=None):

    c0 = (
        isinstance(dinput, dict)
        and all([
            isinstance(kk, str)
            and isinstance(vv, dict)
            and all([
                isinstance(vv, str)
                and vv in ['value', 'com', 'units', 'group']
                for ss in vv.keys()
            ])
            and all([ss in vv.keys() for ss in ['value', 'group']])
            and isinstance(vv['group'], str)
            for kk, vv in dinput.items()
        ])
        and all([isinstance(vv)])
    )
    if not c0:
        msg = (
            "Arg dinput is not conform!\n"
            + "{key0: {\n"
            + "    'value': v0, 'units': 's', 'com': 'bla', 'group': 'time'\n"
            + "},\n"
            + " key1: {\n"
            + "    'value': v1, 'units': 's', 'com': 'bla', 'group': 'time'\n"
            + "},}\n"
            + "You provided:\n{}".format(dinput)
        )
        raise Exception(msg)

    for k0, v0 in dinput.items():
        if v0.get('com') is None:
            dinput[k0]['com'] = ''
        if v0.get('units') is None:
            dinput[k0]['units'] = 'unknown'
    return dinput


def check_dinput(dinput=None):
    if isinstance(dinput, str):
        # In this case, dinput is the name of a parameters preset
        dinput = _def_parameters.get_params(paramset=dinput)
    else:
        _check_dinput(dinput)
    return dinput


def update_dinput(dinput=None):

    # Update numerical group
    c0 = all([ss in dinput.keys() for ss in ['dt', 'Nt', 'Tmax']])
    if c0 is True:
        dinput['Tstore']['value'] = dinput['dt']['value']
        dinput['Nt']['value'] = int(
            dinput['Tmax']['value']/dinput['dt']['value']
        )
        dinput['Ns']['value'] = int(
            dinput['Tmax']['value']/dinput['Tstore']['value']
        ) + 1

