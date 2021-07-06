# -*- coding: utf-8 -*-


import _def_parameters
import _def_variables


# #############################################################################
# #############################################################################
#                       dparam checks
# #############################################################################


def _check_dparam(dparam=None):

    c0 = (
        isinstance(dparam, dict)
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
            for kk, vv in dparam.items()
        ])
        and all([isinstance(vv)])
    )
    if not c0:
        msg = (
            "Arg dparam is not conform!\n"
            + "{key0: {\n"
            + "    'value': v0, 'units': 's', 'com': 'bla', 'group': 'time'\n"
            + "},\n"
            + " key1: {\n"
            + "    'value': v1, 'units': 's', 'com': 'bla', 'group': 'time'\n"
            + "},}\n"
            + "You provided:\n{}".format(dparam)
        )
        raise Exception(msg)

    for k0, v0 in dparam.items():
        if v0.get('com') is None:
            dparam[k0]['com'] = ''
        if v0.get('units') is None:
            dparam[k0]['units'] = 'unknown'
    return dparam


def check_dparam(dparam=None):
    pramset = None
    if isinstance(dparam, str):
        # In this case, dparam is the name of a parameters preset
        paramset = dparam
        dparam = _def_parameters.get_params(paramset=dparam)
    else:
        dparam = _check_dparam(dparam)
    return dparam, paramset


def update_dparam(dparam=None):

    # Update numerical group
    c0 = all([ss in dparam.keys() for ss in ['dt', 'Nt', 'Tmax']])
    if c0 is True:
        dparam['Tstore']['value'] = dparam['dt']['value']
        dparam['Nt']['value'] = int(
            dparam['Tmax']['value'] / dparam['dt']['value']
        )
        dparam['Ns']['value'] = int(
            dparam['Tmax']['value'] / dparam['Tstore']['value']
        ) + 1


# #############################################################################
# #############################################################################
#                       dvar checks
# #############################################################################


def _check_dvar(dvar=None):

    c0 = (
        isinstance(dvar, dict)
        and all([
            isinstance(kk, str)
            and isinstance(vv, dict)
            and all([
                isinstance(vv, str)
                and vv in ['value', 'com', 'units']
                for ss in vv.keys()
            ])
            and all([ss in vv.keys() for ss in ['value']])
            and isinstance(vv['group'], str)
            for kk, vv in dvar.items()
        ])
        and all([isinstance(vv)])
    )
    if not c0:
        msg = (
            "Arg dvar is not conform!\n"
            + "{key0: {'value': v0, 'units': 's', 'com': 'bla'},\n"
            + " key1: {'value': v1, 'units': 's', 'com': 'bla'},\n"
            + "You provided:\n{}".format(dvar)
        )
        raise Exception(msg)

    for k0, v0 in dvar.items():
        if v0.get('com') is None:
            dvar[k0]['com'] = ''
        if v0.get('units') is None:
            dvar[k0]['units'] = 'unknown'
    return dvar


def check_dvar(dvar=None):
    varset = None
    if isinstance(dvar, str):
        # In this case, dparam is the name of a parameters preset
        varset = dvar
        dvar = _def_variables.get_variables(varset=dvar)
    else:
        dvar = _check_dvar(dvar)
    return dvar, varset


# #############################################################################
# #############################################################################
#                       dfunc checks
# #############################################################################


def _check_dfunc(dfunc=None):

    c0 = (
        isinstance(dfunc, dict)
        and all([
            isinstance(kk, str)
            and isinstance(vv, dict)
            and all([
                isinstance(vv, str)
                and vv in ['value', 'com', 'units']
                for ss in vv.keys()
            ])
            and all([ss in vv.keys() for ss in ['value']])
            and isinstance(vv['group'], str)
            for kk, vv in dfunc.items()
        ])
        and all([isinstance(vv)])
    )
    if not c0:
        msg = (
            "Arg dfunc is not conform!\n"
            + "{key0: {'value': v0, 'units': 's', 'com': 'bla'},\n"
            + " key1: {'value': v1, 'units': 's', 'com': 'bla'},\n"
            + "You provided:\n{}".format(dfunc)
        )
        raise Exception(msg)

    for k0, v0 in dfunc.items():
        if v0.get('com') is None:
            dfunc[k0]['com'] = ''
        if v0.get('units') is None:
            dfunc[k0]['units'] = 'unknown'
    return dvar


def check_dfunc(dvar=None):
    funcset = None
    if isinstance(dfunc, str):
        # In this case, dfunc is the name of a functions preset
        funcset = dfunc
        dfunc = _def_variables.get_variables(funcset=dfunc)
    else:
        dfunc = _check_dvar(dfunc)
    return dfunc, funcset
