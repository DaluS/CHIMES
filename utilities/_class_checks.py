# -*- coding: utf-8 -*-


# Built-in
import os
import inspect


# common
import numpy as np


# library specific
import models


_PATH_HERE = os.path.dirname(__file__)
_PATH_MODELS = os.path.join(os.path.dirname(_PATH_HERE), 'models')


# #############################################################################
# #############################################################################
#                       dparam checks
# #############################################################################


_LTYPES = [int, float, np.int_, np.float_]


def _check_dparam(dparam=None):

    # check type
    if not isinstance(dparam, dict):
        msg = (
            "dparam must be a dict!\n"
            f"You provided: {type(dparam)}"
        )
        raise Exception(msg)

    # check keys
    lk0 = [
        k0 for k0 in dparam.keys() if k0 not in models._DFIELDS.keys()
    ]
    if len(lk0) > 0:
        msg = (
            "dparam must have keys identified in models._DFIELDS!\n"
            f"You provided: {lk0}"
        )
        raise Exception(msg)

    # check values
    dk0 = {
        k0: v0 for k0, v0 in dparam.items()
        if not (
            (
                v0 is None
                or type(v0) in _LTYPES
                or type(v0) in [list, np.ndarray]
                or hasattr(v0, '__call__')
            )
            or (
                isinstance(v0, dict)
                and all([
                    ss in models._DFIELDS[k0].keys()
                    for ss in v0.keys()
                ])
                and 'value' in v0.keys()
                and (
                    v0['value'] is None
                    or type(v0['value']) in _LTYPES
                    or type(v0['value']) in [list, np.ndarray]
                    or hasattr(v0['value'], '__call__')
                )
            )
        )
    }
    if len(dk0) > 0:
        msg = (
            "Arg dparam be of the form:\n"
            + "{key0: {'value': v0}, key1: ...}\n\n"
            + "Where value can be:\n"
            + "\t- scalar: int or float\n"
            + "\t- array: for benchmarks\n"
            + "\t- function: will be associated to a variable\n\n"
            + "You provided:\n{}".format(dk0)
        )
        raise Exception(msg)

    # Fill in default fields if any missing
    for k0, v0 in dparam.items():
        for ss in models._DFIELDS[k0].keys():
            if dparam[k0].get(ss) is None:
                dparam[k0][ss] = models._DFIELDS[k0][ss]

    # add numerical parameters if not included
    lknum = [
        k0 for k0, v0 in models._DFIELDS.items()
        if v0['group'] == 'Numerical'
    ]
    for k0 in lknum:
        if k0 not in dparam.keys():
            dparam[k0] = models._DFIELDS[k0]

    return dparam


def check_dparam(dparam=None):

    # if str => load from file
    if isinstance(dparam, str):
        # In this case, dparam is the name of a model
        # Get list of available models in models/, as a dict
        df = {
            ff[len('_model_'):ff.index('.py')]: os.path.join(_PATH_MODELS, ff)
            for ff in os.listdir(_PATH_MODELS)
            if ff.startswith('_model_') and ff.endswith('.py')
        }
        # raise Exception if requested model does not exist 
        if dparam not in df.keys():
            lstr = [f'\t\t- {kk}' for kk in df.keys()]
            msg = (
                "The requested pre-defined model does not exist yet!\n"
                f"\t- requested: {dparam}\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)
        model = dparam
        dparam = getattr(models, dparam)._DPARAM
    else:
        model = 'custom'

    # check conformity
    dparam = _check_dparam(dparam)
    return dparam, model


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

    # Identify functions
    dparam, lf = _check_func(dparam)
    return dparam, lf


# #############################################################################
# #############################################################################
#                       dfunc checks
# #############################################################################


def _check_func(dparam=None):

    # extract functions 
    lf = [k0 for k0, v0 in dparam.items() if hasattr(v0['value'], '__call__')]
    lfi = list(lf)

    # extract dependencies
    for k0 in lf:
        v0 = dparam[k0]
        kargs = set(inspect.getfullargspec(v0['value']).args)

        # check if any parameter is unknown
        lkout = [kk for kk in kargs if kk not in dparam.keys()]
        if len(lkout) > 0:
            lstr = [f'\t- {kk}' for kk in lkout]
            msg = (
                f"Functions '{k0}' seesm to depend on unknown parameters:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

        # Check is there is a circular dependency
        if k0 in kargs:
            msg = (
                f"Function '{k0}' seems to depend on itself!"
            )
            raise Exception(msg)

        # test the function


        # Identify function depending on static parameters and update
        if not any([kk in lf for kk in kargs]):
            dparam[k0]['value'] = dparam[k0]['value'](
                **{kk: dparam[kk]['value'] for kk in kargs}
            )
            lfi.remove(k0)
            continue

        # bruteforce determination of input args
        dparam[k0]['args'] = list(kargs.difference(lfi))
        dparam[k0]['args_func'] = list(kargs.intersection(lfi))

    # Determine order of functions
    ind_order = np.argsort([len(dparam[k0]['args_func']) for k0 in lfi])
    import pdb; pdb.set_trace() # DB
    func_order = None

    return dparam, func_order


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


