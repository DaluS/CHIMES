# -*- coding: utf-8 -*-


# Built-in
import os
import inspect
import itertools as itt


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
_LEQTYPES = ['ode', 'intermediary', 'auxiliary']
_LEXTRAKEYS = ['kargs', 'args']


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
    dfail = {}
    for k0, v0 in dparam.items():
        if v0 is None or type(v0) in _LTYPES + [list, np.ndarray]:
            dparam[k0] = {'value': v0}
        elif hasattr(v0, '__call__'):
            dfail[k0] = "Function must be in a dict {'value': func, 'eqtype':}"
            continue
        elif isinstance(v0, dict):
            lk = [
                kk for kk in v0.keys()
                if kk != 'eqtype'
                and kk not in _LEXTRAKEYS + list(models._DFIELDS[k0].keys())
            ]
            if len(lk) > 0:
                dfail[k0] = f"Invalid keys: {lk}"
                continue
            if 'value' not in v0.keys():
                dfail[k0] = "dict must have key 'value'"
                continue
            if v0['value'] is None or type(v0) in _LTYPES + [list, np.ndarray]:
                pass
            elif hasattr(v0['value'], '__call__'):
                if 'eqtype' not in v0.keys():
                    dfail[k0] = "For a function, key 'eqtype' must be provided"
                    continue
                if v0['eqtype'] not in _LEQTYPES:
                    dfail[k0] = (
                        f"Invalid eqtype ({v0['eqtype']}), "
                        f"allowed: {_LEQTYPES}"
                    )
                    continue

    if len(dfail) > 0:
        lstr = [f'\t- {kk}: {vv}' for kk, vv in dfail.items()]
        msg = (
            "Arg dparam must be of the form:\n"
            "{key0: {'value': v0}, key1: ...}\n\n"
            "Where value can be:\n"
            "\t- scalar: int or float\n"
            "\t- array: for benchmarks\n"
            "\t- function: will be associated to a variable\n\n"
            "The following non-conformities have been found:\n"
            + "\n".join(lstr)
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
        model = {dparam: df[dparam]}
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


def _check_func(dparam=None, func_order=None):

    # -------------------------------------
    # extract parameters that are functions 
    lf = [k0 for k0, v0 in dparam.items() if hasattr(v0['value'], '__call__')]
    lfi = list(lf)

    # ---------------------------------------
    # extract input args and check conformity
    dfail = {}
    for k0 in lf:
        v0 = dparam[k0]
        kargs = inspect.getfullargspec(v0['value']).args

        # Replace lamb by lambda
        if 'lamb' in kargs:
            kargs[kargs.index('lamb')] = 'lambda'

        # check if any parameter is unknown
        lkok = ['self'] + list(dparam.keys())
        lkout = [kk for kk in kargs if kk not in lkok]
        if len(lkout) > 0:
            dfail[k0] = f"depend on unknown parameters: {lkout}"
            continue

        # check ode
        if 'self' in kargs and v0['eqtype'] != 'ode':
            dfail[k0] = f"self in args => eqtype = 'ode' ({v0['eqtype']})!"
            continue

        # Check is there is a circular dependency
        if k0 in kargs:
            dfail[k0] = "depends on itself (circular dependency)!"
            continue

        # check the function is working
        try:
            out = v0['value']()
        except Exception as err:
            dfail[k0] = f"Function doesn't work with default values ({err})"
            continue

        # Identify function depending on static parameters and update
        # Replace by computed value and remove from list of functions
        if not any([kk in lf for kk in kargs]) and 'self' not in kargs:
            din = {kk: dparam[kk]['value'] for kk in kargs if kk != 'lambda'}
            if 'lambda' in kargs:
                din['lamb'] = dparam['lambda']['value']
            dparam[k0]['value'] = dparam[k0]['value'](**din)
            lfi.remove(k0)
            del dparam[k0]['eqtype']
            continue

        # store keyword args
        dparam[k0]['kargs'] = kargs

    # raise exception if any non-conformity
    if len(dfail) > 0:
        lstr = [f'\t- {kk}: {vv}' for kk, vv in dfail.items()]
        msg = (
            "The following functions seem to have inconsistencies:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # check lfi is still consistent
    c0 = (
        all([
            hasattr(dparam[k0]['value'], '__call__')
            and dparam[k0].get('eqtype') is not None
            for k0 in lfi
        ])
        and [
            not (hasattr(dparam[k0]['value'], '__call__'))
            and dparam[k0].get('eqtype') is None
            for k0 in set(dparam.keys()).difference(lfi)
        ]
    )
    if not c0:
        msg = "Inconsistency in lfi identified!"
        raise Exception(msg)

    # --------------------------------
    # classify input args per category
    for k0 in lfi:
        kargs = [kk for kk in dparam[k0]['kargs'] if kk != 'self']
        argsf = set(kargs).intersection(lfi)
        dparam[k0]['args'] = {
            'param': list(set(kargs).difference(lfi)),
            'ode': [
                kk for kk in argsf
                if dparam[kk]['eqtype'] == 'ode'
            ],
            'auxiliary': [
                kk for kk in argsf
                if dparam[kk]['eqtype'] == 'auxiliary'
            ],
            'intermediary': [
                kk for kk in argsf
                if dparam[kk]['eqtype'] == 'intermediary'
            ],
        }

    # -------------------------------
    # Make sure no auxiliary function is needed for the computation
    dfail = {}
    for k0 in lfi:
        if dparam[k0]['eqtype'] == 'auxiliary':
            lk1 = [
                k1 for k1 in lfi
                if dparam[k1]['eqtype'] != 'auxiliary'
                and k0 in dparam[k1]['args']['auxiliary']
            ]
            if len(lk1) > 0:
                dfail[k0] = lk1

    # raise Exception if any
    if len(dfail) > 0:
        lstr = [f"\t- {kk}: {vv}" for kk, vv in dfail.items()]
        msg = (
            "The following auxiliary functions are necessary for computation\n"
            + "\n".join(lstr)
            + "\n=> Consider setting them to 'intermediary'"
        )
        raise Exception(msg)

    # -------------------------------
    # Store the source for later use (doc, saving...)
    for k0 in lfi:
        dparam[k0]['source'] = inspect.getsource(dparam[k0]['value'])

    # -------------------------------------------
    # Create variables for all varying quantities
    for k0 in lfi:
        pass

    # ----------------------------
    # Determine order of functions
    func_order = _suggest_funct_order(
        dparam=dparam, func_order=func_order, lfunc=lfi,
    )

    return dparam, func_order


# #############################################################################
# #############################################################################
#               dfunc: suggest an order for functions computation
# #############################################################################


def _suggest_funct_order(dparam=None, func_order=None, lfunc=None):
    """ Propose a logical order for computing the functions

    Strategy:
        1) Determine if a natural order exists (i.e. no cyclical dependency)
        2) if no => identify functions that, if updated from the previous time
        step, allow to compute the maximum number of other functions without
        having to rely on the previous time step for them

        Auxiliary functions are not considered
    """

    included = ['ode', 'intermediary']
    lfunc = [
        kk for kk in lfunc if dparam[kk]['eqtype'] in included
    ]

    # ---------------------------
    # func_order is user-provided
    if func_order is not None:
        if len(set(func_order)) != len(lfunc):
            msg = (
                "Provided order of functions is incomplete / too large!\n"
                + f"\t- functions: {lfunc}\n"
                + f"\t- provided order: {func_order}"
            )
            raise Exception(msg)
        return func_order

    # ---------------------------
    # count the number of args in each category, for each function
    nbargs = np.array([
        (
            len(dparam[k0]['args']['param']),
            len(dparam[k0]['args']['intermediary']),
            # len(dparam[k0]['args']['auxiliary']),
            len(dparam[k0]['args']['ode']),
        )
        for k0 in lfunc
    ])
    if np.all(np.sum(nbargs[:, 1:], axis=1) > 0):
        msg = "No sorting order of functions can be identified!"
        raise Exception(msg)

    # first: functions that only depend on parameters and self
    indsort = (np.sum(nbargs[:, 1:], axis=1) == 0).nonzero()[0]
    indsort = indsort[np.argsort(nbargs[indsort, 0])]
    lfsort = [lfunc[ii] for ii in indsort]

    # ---------------------------
    # try to identify a natural sorting order
    # i.e.: functions that only depend on the previously sorted functions
    try:
        while indsort.size < len(lfunc):
            lc = [
                (
                    ii not in indsort,
                    np.sum(nbargs[ii, 1:]) <= indsort.size,
                    all([
                        ss in lfsort for ss in (
                            dparam[lfunc[ii]]['args']['intermediary']
                            # + dparam[lfunc[ii]]['args']['auxiliary']
                            + dparam[lfunc[ii]]['args']['ode']
                        )
                    ])
                )
                for ii in range(len(lfunc))
            ]
            indi = [ii for ii in range(len(lfunc)) if all(lc[ii])]
            if len(indi) == 0:
                msg = "No natural sorting order of functions "
                raise Exception(msg)
            indsort = np.concatenate((indsort, indi))
            lfsort += [lfunc[ii] for ii in indi]

    except Exception as err:
        # No natural order => at least one function has to be calculated from
        # the previous time step
        # For each remaining function count how many other functions can be
        # calculated from it without having to get the previous time step
        # for this we investigate up to 2 layers of dependencies

        # we work with dict of remaining function (not sorted yet)
        dfremain = {}
        # first layer
        lfremain = set(lfunc).difference(lfsort)
        for k0 in lfremain:
            lk1 = [
                k1 for k1 in lfremain
                if k1 != k0
                and set([k0]) == set(
                    dparam[k1]['args']['intermediary']
                    # + dparam[k1]['args']['auxiliary']
                    + dparam[k1]['args']['ode']
                ).difference(lfsort)
            ]
            if len(lk1) > 0:
                dfremain[k0] = lk1

        if len(dfremain) == 0:
            msg = "No function identified that would allow computing others"
            raise Exception(msg)

        dfremaini = dict(dfremain)
        while not any([len(vv) == len(lfremain) for vv in dfremaini.values()]):
            # second layer
            dfremainj = {}
            for k0 in dfremaini.keys():
                lk1 = [
                    k1 for k1 in dfremaini.keys()
                    if k1 not in [k0] + dfremaini[k0]
                    and all([
                        ss in [k0] + dfremaini[k0]
                        for ss in set(
                            dparam[k1]['args']['intermediary']
                            # + dparam[k1]['args']['auxiliary']
                            + dparam[k1]['args']['ode']
                        ).difference(lfsort)
                    ])
                ]
                if k0 == 'I':
                    import pdb; pdb.set_trace()      # DB
                if len(lk1) > 0:
                    dfremainj[k0] = list(dict.fromkeys(np.concatenate(
                        (dfremaini[k0], lk1)
                    )))
            import pdb; pdb.set_trace()      # DB
            dfremaini = dict(dfremainj)
            # TBF
            import pdb; pdb.set_trace()      # DB

    finally:
        assert indsort.size == len(lfunc)
        assert len(set(lfsort)) == len(lfsort)
        func_order = lfsort

    return func_order



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


