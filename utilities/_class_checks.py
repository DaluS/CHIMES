# -*- coding: utf-8 -*-


# Built-in
import os
import inspect
import itertools as itt
import warnings


# common
import numpy as np


# library specific
import models


_PATH_HERE = os.path.dirname(__file__)
_PATH_MODELS = os.path.join(os.path.dirname(_PATH_HERE), 'models')


# #############################################################################
# #############################################################################
#                       dparam checks - low-level basis
# #############################################################################


_LTYPES = [int, float, np.int_, np.float_]
_LEQTYPES = ['ode', 'intermediary', 'auxiliary']
_LEXTRAKEYS = ['func', 'kargs', 'args', 'initial', 'source']


def _check_dparam(dparam=None):
    """ Check basic properties of dparam

    It must be a dict
    with only str as keys
    with only some fields allowed for each key
    with values that can be scalars or functions

    <Missing fields are filled in from defaults values in models._DFIELDS

    """

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
            if ('value' not in v0.keys() and 'func' not in v0.keys()):
                dfail[k0] = "dict must have key 'value' or 'func'"
                continue
            if v0.get('func') is not None and hasattr(v0['func'], '__call__'):
                if 'eqtype' not in v0.keys():
                    dfail[k0] = "For a function, key 'eqtype' must be provided"
                    continue
                if v0['eqtype'] not in _LEQTYPES:
                    dfail[k0] = (
                        f"Invalid eqtype ({v0['eqtype']}), "
                        f"allowed: {_LEQTYPES}"
                    )
                    continue
            elif (
                v0['value'] is None
                or type(v0) in _LTYPES + [list, np.ndarray]
            ):
                pass

    if len(dfail) > 0:
        lstr = [f'\t- {kk}: {vv}' for kk, vv in dfail.items()]
        msg = (
            "Arg dparam must be of the form:\n"
            "{key0: {'value': v0}, key1: {'func': lambda ...: ...}, ...}\n\n"
            "Where value can be:\n"
            "\t- scalar: int or float\n"
            "\t- array: for benchmarks\n"
            "And where func is and callable "
            "(and will be associated to a variable in 'value')\n\n"
            "The following non-conformities have been found:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # Add time vector if missing
    if 'time' not in dparam.keys():
        dparam['time'] = models._DFIELDS['time']

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


# #############################################################################
# #############################################################################
#                       dparam checks - high-level
# #############################################################################


def check_dparam(dparam=None, func_order=None, method=None):
    """ Check user-provided dparam

    dparam can be:
        - a dict of parameters / functions
        - a str: the name of a predefined model (loaded from file)

    After loading (if necessary):
        - the dict basic conformity is checked
        - All functions are checked, as well as the func_order

    """

    # if str => load from file
    if isinstance(dparam, str):
        # In this case, dparam is the name of a model
        # Get list of available models in models/, as a dict
        if dparam not in models._DMODEL.keys():
            msg = (
                f"Requested pre-defined model ('{dparam}') not available!\n"
                + models.get_available_models(returnas=str, verb=False)
            )
            raise Exception(msg)
        model = {dparam: models._DMODEL[dparam]['file']}
        if func_order is None:
            func_order = models._DMODEL[dparam]['func_order']
        dparam = models._DMODEL[dparam]['dparam']
    else:
        model = 'custom'

    # check conformity
    dparam = _check_dparam(dparam)

    # Update numerical group
    c0 = all([ss in dparam.keys() for ss in ['dt', 'nt', 'Tmax']])
    if c0 is True:
        dparam['Tstore']['value'] = dparam['dt']['value']
        dparam['nt']['value'] = int(
            dparam['Tmax']['value'] / dparam['dt']['value']
        )

    # Identify functions
    dparam, func_order = _check_func(
        dparam,
        func_order=func_order,
        method=method,
    )

    return dparam, model, func_order


# #############################################################################
# #############################################################################
#                       functions checks - low-level basis
# #############################################################################


def _check_func(dparam=None, func_order=None, method=None):
    """ Check basic conformity of functions

    They must:
        - have only known input arguments
        - no circular dependency
        - the right type (e.g.: itself in args => ode)
        - must work with default value (to detect typos)
        - no auxiliary function should be used for computation

    Functions that depend only on fixed parameters are replaced by the computed
    parameter value

    For real functions, the dict is then completed with:
        - a sub-dict of their input arguments, claissified by types
        - the source
        - a np.ndarray is created for each, to hold its time-dependent variable

    If not user-provided, an order can be suggested for function execution

    """

    # -------------------------------------
    # extract parameters that are functions 
    lf = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
    lfi = list(lf)

    # ---------------------------------------
    # extract input args and check conformity
    dfail = {}
    for k0 in lf:
        v0 = dparam[k0]
        kargs = inspect.getfullargspec(v0['func']).args

        # Replace lamb by lambda
        if 'lamb' in kargs:
            kargs[kargs.index('lamb')] = 'lambda'

        # check if any parameter is unknown
        lkok = ['itself'] + list(dparam.keys())
        lkout = [kk for kk in kargs if kk not in lkok]
        if len(lkout) > 0:
            dfail[k0] = f"depend on unknown parameters: {lkout}"
            continue

        # check ode
        if 'itself' in kargs and v0['eqtype'] != 'ode':
            dfail[k0] = f"itself in args => eqtype = 'ode' ({v0['eqtype']})!"
            continue

        # if ode => inital value necessary
        if v0['eqtype'] == 'ode' and type(v0.get('initial')) not in _LTYPES:
            dfail[k0] = "ode equation needs a 'initial' value"
            continue

        # Check is there is a circular dependency
        if k0 in kargs:
            dfail[k0] = "circular dependency!"
            continue

        # check the function is working
        try:
            out = v0['func']()
            assert not np.any(np.isnan(out))
        except Exception as err:
            dfail[k0] = f"Function doesn't work with default values ({err})"
            continue

        # Identify function depending on static parameters and update
        # Replace by computed value and remove from list of functions
        c0 = (
            not any([kk in lf for kk in kargs])
            and dparam[k0]['eqtype'] != 'ode'
        )
        if c0:
            din = {kk: dparam[kk]['value'] for kk in kargs if kk != 'lambda'}
            if 'lambda' in kargs:
                din['lamb'] = dparam['lambda']['value']
            dparam[k0]['value'] = dparam[k0]['func'](**din)
            lfi.remove(k0)
            del dparam[k0]['eqtype']
            del dparam[k0]['func']
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
            hasattr(dparam[k0]['func'], '__call__')
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
        kargs = [kk for kk in dparam[k0]['kargs'] if kk != 'itself']
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

    # --------------------------------
    # set default values of parameters to their real values
    # this way we don't have to feed the parameters value inside the loop
    for k0 in lfi:
        if len(dparam[k0]['args']) > 0:
            defaults = list(dparam[k0]['func'].__defaults__)
            for k1 in dparam[k0]['args']['param']:
                defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            dparam[k0]['func'].__defaults__ = tuple(defaults)

    # -------------------------------
    # Store the source for later use (doc, saving...)
    for k0 in lfi:
        dparam[k0]['source'] = inspect.getsource(dparam[k0]['func'])

    # -------------------------------------------
    # Create variables for all varying quantities
    shape = (dparam['nt']['value'], dparam['nx']['value'])
    for k0 in lfi:
        dparam[k0]['value'] = np.full(shape, np.nan)

    # ----------------------------
    # Determine order of functions
    func_order = _suggest_funct_order(
        dparam=dparam, func_order=func_order, lfunc=lfi, method=method,
    )

    return dparam, func_order


# #############################################################################
# #############################################################################
#               dfunc: suggest an order for functions computation
# #############################################################################


def _suggest_funct_order(
    dparam=None, func_order=None,
    lfunc=None, method=None,
):
    """ Propose a logical order for computing the functions

    Strategy:
        1) Determine if a natural order exists (i.e. no cyclical dependency)
        2) if no => identify functions that, if updated from the previous time
        step, allow to compute the maximum number of other functions without
        having to rely on the previous time step for them

        Auxiliary functions are not considered
    """

    # check inputs
    if method is None:
        method = 'other'

    included = ['ode', 'intermediary']
    lfunc = [
        kk for kk in lfunc if dparam[kk]['eqtype'] in included
    ]

    # ---------------------------
    # func_order is user-provided
    if func_order is not None:
        lfunc_inter = [
            kk for kk in lfunc if dparam[kk]['eqtype'] == 'intermediary'
        ]
        if len(set(func_order)) != len(lfunc_inter):
            msg = (
                "Provided order of functions is incomplete / too large!\n"
                + f"\t- functions: {lfunc}\n"
                + f"\t- provided order: {func_order}"
            )
            raise Exception(msg)
        return func_order

    # ---------------------------
    # func_order is determined automatically

    if method == 'brute force':
        # try orders until one works
        lfunc_inter = [
            k0 for k0 in lfunc if dparam[k0]['eqtype'] == 'intermediary'
        ]
        # Dummy y just for calls, start with nans (see if they propagate)
        y = {
            k0: np.nan for k0, v0 in dparam.items()
            if v0.get('eqtype') == 'intermediary'
        }
        # The list of variable still to find
        var_still_in_list = [k for k in lfunc_inter]

        # Initialize and loop
        func_order = []
        for ii in range(len(lfunc_inter)):
            for jj in range(len(var_still_in_list)):
                # add to a temporary list
                templist = func_order + [var_still_in_list[jj]]
                # try and if work => break and go to the next i
                try :
                    for k0 in templist:
                        kwdargs = {
                            k1: y[k1]
                            for k1 in dparam[k0]['args']['intermediary']
                        }
                        # if lambda => substitute by lamb
                        if 'lambda' in dparam[k0]['args']['intermediary']:
                            kwdargs['lamb'] = kwdargs['lambda']
                            del kwdargs['lambda']
                        y[k0] = dparam[k0]['func'](**kwdargs)
                        if np.any(np.isnan(y[k0])):
                            raise ValueError('wrong order')
                    func_order = templist.copy()
                    _ = var_still_in_list.pop(jj)
                    break
                except ValueError:
                    # didn't work => reinitialise y to avoid keeping error
                    y = {
                        k0: np.nan for k0, v0 in dparam.items()
                        if v0.get('eqtype') == 'intermediary'
                    }
                except Exception as err:
                    # didn't work => reinitialise y to avoid keeping error
                    y = {
                        k0: np.nan for k0, v0 in dparam.items()
                        if v0.get('eqtype') == 'intermediary'
                    }
                    warnings.warn(str(err))


    elif method == 'other':
        # count the number of args in each category, for each function
        nbargs = np.array([
            (
                len(dparam[k0]['args']['param']),
                len(dparam[k0]['args']['intermediary']),
                # len(dparam[k0]['args']['auxiliary']),  # not considered
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
                            ss in lfsort
                            for ss in (
                                dparam[lfunc[ii]]['args']['intermediary']
                                # + dparam[lfunc[ii]]['args']['auxiliary']
                                # + dparam[lfunc[ii]]['args']['ode']
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

            # print suggested order
            msg = (
                'Suggested order for intermediary functions (func_order):\n'
                f'{lfsort}'
            )
            print(msg)

        except Exception as err:
            # No natural order => at least one function has to be calculated from
            # the previous time step
            # For each remaining function count how many other functions can be
            # calculated from it without having to get the previous time step
            # for this we investigate up to 2 layers of dependencies

            # we work with dict of remaining function (not sorted yet)
            dfremain = {}
            # first layer
            lfremain = set([
                kk for kk in lfunc if dparam[kk]['eqtype'] == 'intermediary'
            ]).difference(lfsort)
            for k0 in lfremain:
                lk1 = [
                    k1 for k1 in lfremain
                    if k1 != k0
                    and set([k0]) == set(
                        dparam[k1]['args']['intermediary']
                        # + dparam[k1]['args']['auxiliary']
                        # + dparam[k1]['args']['ode']
                    ).difference(lfsort)
                ]
                if len(lk1) > 0:
                    dfremain[k0] = lk1

            if len(dfremain) == 0:
                msg = "No function identified that would allow computing others"
                raise Exception(msg)

            ii = 0
            keepon, found = True, False
            dfremaini = dict(dfremain)
            while keepon is True:
                dfremainj = {}
                for k0 in dfremaini.keys():
                    lk1 = [
                        k1 for k1 in lfremain
                        if k1 not in [k0] + dfremaini[k0]
                        and all([
                            ss in [k0] + dfremaini[k0]
                            for ss in set(
                                dparam[k1]['args']['intermediary']
                                # + dparam[k1]['args']['auxiliary']
                                # + dparam[k1]['args']['ode']
                            ).difference(lfsort)
                        ])
                    ]
                    if len(lk1) > 0:
                        dfremainj[k0] = list(dict.fromkeys(np.concatenate(
                            (dfremaini[k0], lk1)
                        )))

                # check finish conditions
                llen = [len(vv) for vv in dfremainj.values()]
                if len(llen) == 0:
                    keepon = False
                elif np.max(llen) == len(lfremain) - 1:
                    keepon = False
                    dfremaini = {
                        k0: v0 for k0, v0 in dfremainj.items()
                        if len(v0) == len(lfremain) - 1
                    }
                    found = True
                else:
                    dfremaini = dict(dfremainj)
                    ii += 1

            # found or not
            if found is False:
                lstr = [
                    '\t- {}'
                    for k0 in set(lfremain).difference(dfremainj)
                ]
                msg = (
                    "No order could be identified with a unique (n-1)!\n"
                    "functions remaining after all tries:\n"

                )
                raise Exception(msg)

            # print suggested orders
            lstr = [
                f'\t- {k0} {v0} (chosen)' if ii == 0 else f'\t- {k0} {v0}'
                for ii, (k0, v0) in enumerate(dfremaini.items())
            ]
            msg = (
                "The following possible orders have been identified:"
                " assuming the first term is taken from the time n-1\n"
                + "\n".join(lstr)
            )
            print(msg)

        # set func_order
        assert indsort.size == len(lfunc)
        assert len(set(lfsort)) == len(lfsort)
        func_order = lfsort

    # only keep intermediary functions
    func_order = [
        kk for kk in func_order if dparam[kk]['eqtype'] == 'intermediary'
    ]

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
            + f"You provided:\n{dvar}"
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
