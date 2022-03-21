# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:35:02 2022

@author: Paul Valcke
"""

# IN CLASS_CHECKS, LOAD_MODELS

elif os.path.isfile(model) and model.endswith('.py'):

    raise Exception('Absolute path for models disactivated for the moment')
    '''
        # get from arbitrary model file
        model_file = str(model)

        # trying to derive model name from file name
        model = os.path.split(model_file)[-1]
        if model.startswith('_model_') and model.count('_') == 2:
            model = model[model.index('_model_') + len('_model_'):-3]
        else:
            msg = (
                "model file has non-standard name:\n"
                f"\t- model file: {model_file}\n"
                "  => setting model name to 'custom'"
            )
            warnings.warn(msg)
            model = 'custom'


        spec = importlib.util.spec_from_file_location(k0, model_file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)

        # checking attributes
        lattr = [att for att in _LMODEL_ATTR if not hasattr(foo, att)]
        if len(lattr) > 0:
            lstr = [f'\t- {att}' for att in lattr]
            msg = (
                "The provided model file should have at least attributes:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

        # loading attributes
        dmodel = {
            'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
            'presets': {k0: v0 for k0, v0 in foo._PRESETS.items()},
            'description': foo.__doc__,
            'file': model_file,
            'name': model,
        }
        '''


#########

# #############################################################################
# #############################################################################
#               DEPRECATED for Back-up
# #############################################################################


# DEPRECATED
def _suggest_funct_order_DEPRECATED(
    dparam=None,
    func_order=None,
    lfunc=None,
    method=None,
):
    """ Propose a logical order for computing the functions

    Strategy:
        1) Determine if a natural order exists (i.e. no cyclical dependency)
        2) if no => identify functions that, if updated from the previous time
        step, allow to compute the maximum number of other functions without
        having to rely on the previous time step for them

        Auxiliary functions are not considered
    """

    # -------------
    # check inputs
    if method is None:
        method = 'other'

    included = ['statevar']
    lfunc_state = [
        kk for kk in lfunc if dparam[kk]['eqtype'] in included
    ]

    # ---------------------------
    # func_order is user-provided
    if func_order is not None:
        if len(set(func_order)) != len(lfunc_state):
            msg = (
                "Provided order of functions is incomplete / too large!\n"
                + f"\t- functions: {lfunc_state}\n"
                + f"\t- provided order: {func_order}"
            )
            raise Exception(msg)
        return func_order

    # ---------------------------
    # func_order is determined automatically

    if method == 'brute force':
        # try orders until one works
        # Dummy y just for calls, start with nans (see if they propagate)
        y = {
            k0: np.nan for k0, v0 in dparam.items()
            if v0.get('eqtype') == 'intermediary'
        }
        # The list of variable still to find
        var_still_in_list = [kk for kk in lfunc_state]

        # Initialize and loop
        func_order = []
        for ii in range(len(lfunc_state)):
            for jj in range(len(var_still_in_list)):

                # add to a temporary list
                templist = func_order + [var_still_in_list[jj]]

                # try and if work => break and go to the next i
                try:
                    for k0 in templist:
                        # get dict of input args for func k0, from y
                        kwdargs = {
                            k1: y[k1]
                            for k1 in dparam[k0]['args']['intermediary']
                        }

                        # if lambda => substitute by lamb
                        if 'lambda' in dparam[k0]['args']['intermediary']:
                            kwdargs['lamb'] = kwdargs['lambda']
                            del kwdargs['lambda']

                        # try calling k0
                        y[k0] = dparam[k0]['func'](**kwdargs)

                        # raise Exception if any nan
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

        """
        2 possible issues with brute force:
            - a non-expected error can happen => division by zero
            - final list may be incomplete (division by 0 => always error)
        """

    elif method == 'other':

        # count the number of args in each category, for each function
        nbargs = np.array([
            (
                len(dparam[k0]['args']['param']),
                len(dparam[k0]['args']['statevar']),
                # len(dparam[k0]['args']['ode']),           # not considered
            )
            for k0 in lfunc_state
        ])

        if np.all(np.sum(nbargs[:, 1:], axis=1) > 0):
            msg = "No sorting order of functions can be identified!"
            raise Exception(msg)

        # first: functions that only depend on parameters (and self if ode)
        isort = (np.sum(nbargs[:, 1:], axis=1) == 0).nonzero()[0]
        isort = isort[np.argsort(nbargs[isort, 0])]
        func_order = [lfunc_state[ii] for ii in isort]

        # ---------------------------
        # try to identify a natural sorting order
        # i.e.: functions that only depend on the previously sorted functions
        while isort.size < len(lfunc_state):

            # list of conditions (True, False) for each function
            lc = [
                (
                    ii not in isort,                       # not sorted yet
                    np.sum(nbargs[ii, 1:]) <= isort.size,  # not too many args
                    all([                                  # only sorted args
                        ss in func_order
                        for ss in (
                            dparam[lfunc_state[ii]]['args']['statevar']
                            # + dparam[lfunc[ii]]['args']['ode']
                        )
                    ])
                )
                for ii in range(len(lfunc_state))
            ]

            # indices of functions matching all conditions
            indi = [ii for ii in range(len(lfunc_state)) if all(lc[ii])]

            # If none => no easy solution
            if len(indi) == 0:
                msg = "No natural sorting order of functions "
                raise Exception(msg)

            # Concantenate with already sorted indices
            isort = np.concatenate((isort, indi))
            func_order += [lfunc_state[ii] for ii in indi]

    # safety checks
    if len(set(lfunc_state)) != len(func_order):
        msg = (
            "Suggested func_order does not seem to include all functions!\n"
            + f"\t- suggested: {func_order}\n"
            + f"\t- available: {lfunc_state}\n"
        )
        raise Exception(msg)

    # print suggested order
    msg = (
        'Suggested order for statevar functions (func_order):\n'
        f'{func_order}'
    )
    print(msg)

    return func_order
