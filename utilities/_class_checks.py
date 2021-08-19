# -*- coding: utf-8 -*-


# Built-in
import os
import inspect
import itertools as itt
import warnings
import time

# common
import numpy as np


# library specific
import models


_PATH_HERE = os.path.dirname(__file__)
_PATH_MODELS = os.path.join(os.path.dirname(_PATH_HERE), 'models')


_LMODEL_ATTR = ['_LOGICS', 'presets']
_DMODEL_KEYS = {
    'logics': dict,
    'presets': dict,
    'file': str,
    'description': str,
    'name': str,
}
_LTYPES = [int, float, np.int_, np.float_]
_LEQTYPES = ['ode', 'pde', 'statevar', 'param', 'undeclared']

_LEXTRAKEYS = [
    'func', 'kargs', 'args', 'initial',
    'source_kargs', 'source_exp', 'source_name', 'isneeded',
]


# #############################################################################
# #############################################################################
#                       Load library
# #############################################################################


def load_model(model=None, method=None):
    """ Load a model from a model file

    model can be:
        - a model name, taken from directory {}
        - the absolute path to an abitrary model file

    """.format(_PATH_MODELS)

    # -------------
    # check inputs

    if model in models._DMODEL.keys():
        # Get from known models
        model_file = models._DMODEL[model]['file']
        dmodel = dict(models._DMODEL[model])

    elif os.path.isfile(model) and model.endswith('.py'):
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

        # load model file
        spec = importlib.util.spec_from_file_location(k0, model_file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)

        # checking attributes
        lattr = [att for att in _MODEL_ATTR if not hasattr(foo, att)]
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

    else:
        msg = (
            "Arg model must be either:\n"
            "\t- the absolute path to valid .py file\n"
            f"\t- the valid name of an existing model in {_PATH_MODELS}\n"
            f"You provided:\n{model}"
        )
        raise Exception(msg)

    # -------------
    # check conformity of dmodel (has 'file', 'name', 'logics', ...)
    _check_dmodel_preset(dmodel)
    dmodel['preset'] = None

    # --------------
    # check conformity of logics (has 'ode', 'pde', 'statevar'...)
    _check_logics(dmodel)

    # convert logics (new formalism) to dparam
    dparam = get_dparam_from_logics(dmodel)
    del dmodel['logics']

    # --------------------
    # re-check dparam + Identify functions order + get dargs
    dparam, dfunc_order, dargs = check_dparam(dparam=dparam)

    return dmodel, dparam, dfunc_order, dargs


# #############################################################################
# #############################################################################
#                       check dmodel
# #############################################################################


def _check_dmodel_preset(dmodel=None):
    """ Check dmodel is a dict with proper keys """

    # ----------
    # check dmodel
    if not isinstance(dmodel, dict):
        msg = f"Arg dmodel must be a dict\nProvided: {type(dmodel)}"
        raise Exception(msg)

    dkout = {
        k0: type(dmodel.get(k0))
        for k0, v0 in _DMODEL_KEYS.items()
        if not isinstance(dmodel.get(k0), v0)
    }
    if len(dkout) > 0:
        lstr = [
            f'\t- {k0}: {_DMODEL_KEYS[k0]} vs {v0}'
            for k0, v0 in dkout.items()
        ]
        msg = (
            "dmodel must be a dict with keys:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # ----------
    # check presets

    lkout = [
        k0 for k0, v0 in dmodel['presets'].items()
        if not (
            isinstance(v0, dict)
            and all([ss in ['fields', 'com', 'plots'] for ss in v0.keys()])
            and isinstance(v0['com'], str)
            and isinstance(v0['fields'], dict)
        )
    ]

    if len(lkout) > 0:
        lstr = ["\t- {k0}" for k0 in lkout]
        msg = (
            "The following presets are non-valid:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)


# #############################################################################
# #############################################################################
#                       check logics
# #############################################################################


def _check_are_functions(indict=None):
    """ Check that all values have a 'func' key that contain a callable

    Raise Exc eption with list of non-conform keys if any

    """

    # list non-conform keys (must have a 'logics' function)
    lkout = [
        k1 for k1, v1 in indict.items()
        if not (
            isinstance(v1, dict)
            and hasattr(v1.get('func'), '__call__')
        )
    ]
    if len(lkout) > 0:
        lstr = [f'\t- {kk}' for kk in lkout]
        msg = (
            "The following ode have non-conform 'func':\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)


def _check_logics(dmodel=None):
    """ Check conformity of the 'logics' sub-dict

    In particulart, checks:
        - ode
        - pde
        - statevar

    If necessary, add initial values
    Checks all keys are known to models._DFIELDS
    """

    # ---------------
    # list non-conform keys

    lkout = [
        k0 for k0, v0 in dmodel['logics'].items()
        if not (
            k0 in _LEQTYPES
            and isinstance(v0, dict)
        )
    ]
    if len(lkout) > 0:
        lstr = [f'\t- {kk}' for kk in lkout]
        msg = (
            "The following keys in _LOGIC are not supported:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # --------------------
    # List all keys in all dict that are not known to _DFIELDS

    dkout = {
        k0: [k1 for k1 in v0.keys() if k1 not in models._DFIELDS]
        for k0, v0 in dmodel['logics'].items()
        if any([k1 for k1 in v0.keys() if k1 not in models._DFIELDS])
    }
    if len(dkout) > 0:
        lstr = [
            '\n'.join([f"\t- {k0}['{k1}']" for k1 in v0])
            for k0, v0 in dkout.items()
        ]
        msg = (
            "The following keys are not known to _LIBRARY / _DFIELDS:\n"
            f"From model: {dmodel['name']} ({dmodel['file']})\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # -----------------------
    # check ode

    if 'ode' in dmodel['logics'].keys():

        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['ode'])

        # if initial not defined, get from _LIBRARY
        for k1, v1 in dmodel['logics']['ode'].items():
            if v1.get('initial') is None:
                dmodel['logics']['ode'][k1]['initial'] \
                        = models._DFIELDS[k1]['value']

    # -----------------------
    # check pde

    # -----------------------
    # check statevar
    if 'statevar' in dmodel['logics'].keys():

        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['statevar'])


# #############################################################################
# #############################################################################
#                       convert logic to dparam
# #############################################################################


def get_dparam_from_logics(dmodel=None):
    """ Convert logic (from dmodel) to dparam (used in instance)

    """

    lk = [dict.fromkeys(v0.keys(), k0) for k0, v0 in dmodel['logics'].items()]
    for ii, dd in enumerate(lk[1:]):
        lk[0].update(dd)

    dparam = {
        k0: dict(dmodel['logics'][v0][k0]) for k0, v0 in lk[0].items()
    }

    # ---------------
    # Add eqtype
    for k0 in dparam.keys():
        dparam[k0]['eqtype'] = lk[0][k0]

    return dparam


# #############################################################################
# #############################################################################
#                       dparam checks - low-level basis
# #############################################################################


def _check_dparam(dparam=None):
    """ Check basic properties of dparam

    It must be a dict
    with only str as keys
    with only some fields allowed for each key
    with values that can be scalars or functions

    <Missing fields are filled in from defaults values in models._DFIELDS

    """

    # -----------------
    # check type is dict

    if not isinstance(dparam, dict):
        msg = (
            "dparam must be a dict!\n"
            f"You provided: {type(dparam)}"
        )
        raise Exception(msg)

    # ---------------
    # check keys are known to models._DFIELDS

    lk0 = [
        k0 for k0 in dparam.keys() if k0 not in models._DFIELDS.keys()
    ]
    if len(lk0) > 0:
        msg = (
            "dparam must have keys identified in models._DFIELDS!\n"
            f"You provided: {lk0}"
        )
        raise Exception(msg)

    # ---------------------------------------
    # add numerical parameters if not included

    lknum = [
        k0 for k0, v0 in models._DFIELDS.items()
        if v0['group'] == 'Numerical'
    ]
    for k0 in lknum:
        if k0 not in dparam.keys():
            dparam[k0] = models._DFIELDS[k0]

    # --------------------------
    # Add time vector if missing

    if 'time' not in dparam.keys():
        dparam['time'] = dict(models._DFIELDS['time'])

    # ------------
    # check values

    dfail = {}
    for k0, v0 in dparam.items():

        # if value directly provided => put into dict
        if v0 is None or type(v0) in _LTYPES + [list, np.ndarray, str, bool]:
            dparam[k0] = {'value': v0}

        # if function directly provided => put inot dict
        if hasattr(v0, '__call__'):
            dfail[k0] = "Function must be in a dict {'func': func, 'eqtype':}"
            continue

        # if dict => investigate
        if isinstance(dparam[k0], dict):

            # set missing field to default
            for ss in models._DFIELDS[k0].keys():
                if dparam[k0].get(ss) is None:
                    dparam[k0][ss] = models._DFIELDS[k0][ss]

            # identify invalid keys
            lk = [
                kk for kk in dparam[k0].keys()
                if kk != 'eqtype'
                and kk not in _LEXTRAKEYS + list(models._DFIELDS[k0].keys())
            ]
            if len(lk) > 0:
                dfail[k0] = f"Invalid keys: {lk}"
                continue

            # check at least value xor func is present
            c0 = (
                'value' not in dparam[k0].keys()
                and 'func' not in v0.keys()
            )
            if c0:
                dfail[k0] = "dict must have key 'value' or 'func' (or both)"
                continue

            # check function or value
            c0 = (
                dparam[k0].get('func') is not None
                and hasattr(dparam[k0]['func'], '__call__')
            )
            c1 = (
                not c0
                and type(dparam[k0]['value']) in _LTYPES + [
                    list, np.ndarray, str, bool,
                ]
            )

            if c0:
                # func
                if 'eqtype' not in dparam[k0].keys():
                    dparam[k0]['eqtype'] = 'param'
                    # dfail[k0] = "For a func, 'eqtype' must be provided"
                    # continue
                if dparam[k0]['eqtype'] not in _LEQTYPES:
                    dfail[k0] = (
                        f"Invalid eqtype ({v0['eqtype']}), "
                        f"allowed: {_LEQTYPES}"
                    )
                    continue

            elif not c1:
                # fixed valkue
                dfail[k0] = f"Invalid value type ({type(v0['value'])})"

    # ----------------
    # Raise Exception if any failure
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

    return dparam


# #############################################################################
# #############################################################################
#                       dparam checks - high-level
# #############################################################################


def check_dparam(dparam=None):
    """ Check user-provided dparam

    dparam can be:
        - a dict of parameters / functions
        - a str: the name of a predefined model (loaded from file)

    After loading (if necessary):
        - the dict basic conformity is checked
        - All functions are checked, as well as the func_order

    """

    # --------------------
    # check conformity
    dparam = _check_dparam(dparam)

    # -------------------
    # if any unidentified parameter => load them and re-check conformity
    _extract_parameters(dparam)
    dparam = _check_dparam(dparam)

    # ----------------
    # Identify functions
    dparam, dfunc_order = _check_func(dparam)

    # ----------------
    # Make sure to copy to avoid passing by reference
    dparam = {
        k0: dict(v0) for k0, v0 in dparam.items()
    }

    # ---------------
    # dargs (to be used in solver, faster to define it here)

    lode = [
        k0 for k0, v0 in dparam.items()
        if v0.get('eqtype') == 'ode'
    ]
    lstate = dfunc_order

    dargs = {
        k0: {
            k1: dparam[k1]['value']
            for k1 in (
                dparam[k0]['args']['ode']
                + dparam[k0]['args']['statevar']
            )
            if k1 != 'lambda'
        }
        for k0 in dfunc_order['statevar'] + dfunc_order['ode']
    }

    # Handle the lambda exception here to avoid test at every time step
    # if lambda exists and is a function
    c0 = (
        'lambda' in dparam.keys()
        and dparam['lambda'].get('func') is not None
    )
    # then handle the exception
    for k0, v0 in dargs.items():
        if c0 and 'lambda' in dparam[k0]['kargs']:
            dargs[k0]['lamb'] = dparam['lambda']['value']

    return dparam, dfunc_order, dargs


# #############################################################################
# #############################################################################
#                       functions checks - low-level basis
# #############################################################################


def _extract_par_from_func(lfunc=None, lpar=None, dparam=None):

    lpar_add, lfunc_add = [], []
    lkok = ['itself'] + lpar + lfunc
    for k0 in lfunc:
        key = 'lambda' if k0 == 'lamb' else k0

        if k0 in dparam.keys():
            kargs = inspect.getfullargspec(dparam[key]['func']).args
        else:
            kargs = inspect.getfullargspec(models._DFIELDS[key]['func']).args

        # check if any parameter is unknown
        for kk in kargs:
            key = 'lambda' if kk == 'lamb' else kk
            if key not in lkok:
                if models._DFIELDS[key].get('func') is None:
                    if key not in lpar_add:
                        lpar_add.append(key)
                elif key not in lfunc_add:
                    lfunc_add.append(key)

    return lpar_add, lfunc_add


def _extract_parameters(dparam):
    """ Extract fixed-value parameters

    If relevant, the list of fixed-value parameters is extracted from
        the func kwdargs
    """

    lpar = [k0 for k0, v0 in dparam.items() if v0.get('func') is None]
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
    lpar_new = []
    lfunc_new = []

    # ---------------------------------------
    # extract input args and check conformity
    keepon = True
    while keepon:
        lp, lf = _extract_par_from_func(
            lfunc=lfunc + lfunc_new,
            lpar=lpar + lpar_new,
            dparam=dparam,
        )
        if len(lp) > 0:
            lpar_new += lp
        if len(lf) > 0:
            lfunc_new += lf
        else:
            keepon = False

    # ----------------------------------------
    # check parameters
    if len(lpar_new + lfunc_new) > 0:
        dfail = {}
        for k0 in lpar_new + lfunc_new:
            key = 'lambda' if k0 == 'lamb' else k0
            if key not in models._DFIELDS.keys():
                dfail[k0] = "Unknown parameter"
                continue
            dparam[key] = dict(models._DFIELDS[key])

        # -------------------
        # Raise Exception if any
        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following unknown parameters have been identified:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)


def _check_func_time_dependence(lfunc=None, dparam=None):
    """ Safety check on time dependence

    Here we:
        - identify functions that depend on time
        - make sure that time-dependent functions are 'ode' or 'statevar'
        - make sure that time-independent functions are 'param'

    """

    # ----------------
    #  Get list of func that depend on time

    # first functions that explicitly depend on time
    lft = [kk for kk in lfunc if 'time' in dparam[kk]['kargs']]

    # then ode
    for kk in lfunc:
        if kk not in lft and dparam[kk]['eqtype'] == 'ode':
            lft.append(kk)

    # Then function that depend on time-dependent functions
    keepon = True
    while keepon:
        lft_new = []
        for kk in lfunc:
            if kk not in lft and any([k1 in dparam[kk]['kargs'] for k1 in lft]):
                lft_new.append(kk)
        if len(lft_new) > 0:
            lft += lft_new
        else:
            keepon = False

    # ----------------
    # check consistency with declared eqtype
    dfail = {}
    for kk in lfunc:

        if kk in lft and dparam[kk]['eqtype'] not in ['ode', 'statevar']:
            dfail[kk] = f"Time dependent but eqtype='{dparam[kk]['eqtype']}'"
        elif kk not in lft and dparam[kk]['eqtype'] not in ['param']:
            dfail[kk] = f"Time independent but eqtype='{dparam[kk]['eqtype']}'"

    if len(dfail) > 0:
        lstr = [f"\t- {k0}: {v0}" for k0, v0 in dfail.items()]
        msg = (
            "The following inconsistencies have been found:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)


def _check_func_get_source(lfunc=None, dparam=None):
    """ Extract the source code of functions

    Useful for:
        - extracting default values of keyword args and changing them
        - displaying the function in get_summary() (for one-liners only)

    """

    for k0 in lfunc:
        if dparam[k0].get('source_kargs') is None:
            assert dparam[k0].get('source_exp') is None

            # extract source and check if lambda
            sour = inspect.getsource(dparam[k0]['func'])

            c0 = (
                sour.count(':') >= 1
                and (
                    sour.count('lambda') == 1
                    and sour.count(':') == 2
                    and 'lambda' in sour.split(':')[1]
                    and sour.count('\n') == 1
                    and sour.endswith(',\n')
                )
                or (
                    sour.count('lambda') == 0
                    and sour.count('def') == 1
                    and sour.startswith('def ')
                )
            )
            if not c0:
                msg = (
                    f"Non-valid function for {k0}: "
                    "Should be either 'lambda' (one-liner) or a 'def():'"
                )
                raise Exception(msg)

            # Extract kargs and exp(for lambda only)
            if sour.count('lambda') == 1:
                # clean-up source
                sour = sour.strip().replace(',\n', '').replace('\n', '')
                sour = sour[sour.index('lambda') + len('lambda'):]
                # separate keyword args from expression
                kargs, exp = sour.split(':')

                # store exp for lambda only
                dparam[k0]['source_exp'] = exp.strip()
            else:
                kargs = sour[sour.index('(') + 1:sour.index(')')]
                dparam[k0]['source_name'] = dparam[k0]['func'].__name__

            kargs = [kk.strip() for kk in kargs.strip().split(',')]
            if not all(['=' in kk for kk in kargs]):
                msg = (
                    'Only keyword args can be used for lambda functions!\n'
                    f'Provided:\n{source}'
                )
                raise Exception(msg)

            # store keyword args and cleaned-up expression separately
            kargs = ', '.join(kargs)
            dparam[k0]['source_kargs'] = kargs


def _check_func(dparam=None):
    """ Check basic conformity of functions

    They must:
        - have only known input arguments
        - no circular dependency
        - the right type (e.g.: itself in args => ode)
        - must work with default value (to detect typos)

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
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]

    # ---------------------------------------
    # extract input args and check conformity
    dfail = {}
    for k0 in lfunc:
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

    # ----------------------
    # check lfi is still consistent
    c0 = (
        all([
            hasattr(dparam[k0]['func'], '__call__')
            and dparam[k0].get('eqtype') is not None
            for k0 in lfunc
        ])
        and [
            not (hasattr(dparam[k0]['value'], '__call__'))
            and dparam[k0].get('eqtype') is None
            for k0 in dparam.keys() if k0 not in lfunc
        ]
    )
    if not c0:
        msg = "Inconsistency in lfunc identified!"
        raise Exception(msg)

    # ----------------------
    # check time dependence
    _check_func_time_dependence(lfunc=lfunc, dparam=dparam)

    # --------------------------------
    # classify input args per category
    for k0 in lfunc:
        kargs = [kk for kk in dparam[k0]['kargs'] if kk != 'itself']
        dparam[k0]['args'] = {
            None: [
                kk for kk in kargs
                if kk not in lfunc
            ],
            'param': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'param'
            ],
            'ode': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'ode'
            ],
            'statevar': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'statevar'
            ],
        }

    # -----------------------------
    # Identify non-necessary functions
    for k0 in lfunc:
        c0 = (
            dparam[k0]['eqtype'] == 'statevar'
            and not any([k0 in dparam[k1]['kargs'] for k1 in lfunc])
        )
        if c0:
            dparam[k0]['isneeded'] = False
        else:
            dparam[k0]['isneeded'] = True

    # -------------------------------
    # Store the source for later use (doc, saving...)
    _check_func_get_source(lfunc=lfunc, dparam=dparam)

    # ----------------------------
    # Determine order of functions
    dfunc_order = _suggest_funct_order(dparam=dparam)

    # --------------------------------
    # run all param func to set their values
    for k0 in dfunc_order['param']:
        dargs = {
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args'][None]
        }
        dargs.update({
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args']['param']
        })
        dparam[k0]['value'] = dparam[k0]['func'](**dargs)

    # --------------------------------
    # set default values of parameters to their real values
    # this way we don't have to feed the parameters value inside the loop
    _update_func_default_kwdargs(lfunc=lfunc, dparam=dparam)

    # -------------------------------------------
    # Create variables for all varying quantities
    shape = (dparam['nt']['value'], dparam['nx']['value'])
    for k0 in lfunc:
        if dparam[k0]['eqtype'] not in ['param']:
            dparam[k0]['value'] = np.full(shape, np.nan)

    return dparam, dfunc_order


# #############################################################################
# #############################################################################
#               dfunc: suggest an order for functions computation
# #############################################################################


def _suggest_funct_order_by_group(eqtype=None, dparam=None):
    """ Here we find a natural order for function of the same group

    """

    # Prepare list of relevant functsions
    lf = [kk for kk, vv in dparam.items() if vv.get('eqtype') == eqtype]

    lfsort = []
    keepon = True
    ntry = 0
    while keepon:

        # Identify func that can be sorted
        for kk in lf:
            if kk in lfsort:
                continue
            elif len(dparam[kk]['args'][eqtype]) == 0:
                lfsort.append(kk)
            elif all([k1 in lfsort for k1 in dparam[kk]['args'][eqtype]]):
                lfsort.append(kk)

        # evaluate termination condition
        ntry += 1
        if set(lf) == set(lfsort):
            keepon = False
        elif ntry == len(lf) - 1:
            msg = f"No sorting order of func could be found for {eqtype}"
            raise Exception(msg)

    return lfsort


def _suggest_funct_order(
    dparam=None,
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
    # we want a function order for statevar and param
    dfunc_order = {
        k0: _suggest_funct_order_by_group(eqtype=k0, dparam=dparam)
        for k0 in ['param', 'statevar', 'ode']
    }

    return dfunc_order


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


# #############################################################################
# #############################################################################
#               func: update default values of keyword args
# #############################################################################


def _update_func_default_kwdargs(lfunc=None, dparam=None):
    """ Here we update the default valuee of all functions """

    for k0 in lfunc:

        # skip trivial
        if len(dparam[k0]['args']) == 0:
            continue

        # get defaults
        defaults = list(dparam[k0]['func'].__defaults__)
        kargs = dparam[k0]['source_kargs'].split(', ')

        # update using fixed param (eqtype = None)
        for k1 in dparam[k0]['args'][None]:
            key = 'lamb' if k1 == 'lambda' else k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key in vv]
            if len(ind) != 1:
                msg = f"Inconsistency in kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])

        # update using param
        for k1 in dparam[k0]['args']['param']:
            key = 'lamb' if k1 == 'lambda' else k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key in vv]
            if len(ind) != 1:
                msg = f"Inconsistency in kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])

        # update
        dparam[k0]['func'].__defaults__ = tuple(defaults)
        dparam[k0]['source_kargs'] = ', '.join(kargs)


# #############################################################################
# #############################################################################
#                   update from preset
# #############################################################################


def update_from_preset(dparam=None, dmodel=None, preset=None):
    """ Update the dparam dict from values taken from preset """

    # ---------------
    # check inputs

    if preset is None:
        dmodel['preset'] = None
        return

    if preset not in dmodel['presets'].keys():
        lstr = [
            f"\t- {k0}: {v0['com']}" for k0, v0 in dmodel['presets'].items()
        ]
        msg = (
            f"Please choose among the available presets for model"
            " {dmodel['name']}:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # ----------------------
    # check fields in preset
    lkout = [
        k0 for k0, v0 in dmodel['presets'][preset]['fields'].items()
        if not (
            k0 in dparam.keys()
            and isinstance(v0, tuple(_LTYPES))
        )
    ]
    if len(lkout) > 0:
        lstr = [f"\t- {k0}" for k0 in lkout]
        msg = (
            "The following non-conform fields have been detected in preset "
            f"{preset} for model {dmodel['name']}:\n"
            + "\n".join(lstr)
            + "\nAll keys must correspond to existing fixed-value parameters!"
        )
        raise Exception(msg)

    # ----------------------
    # update from preset
    for k0, v0 in dmodel['presets'][preset]['fields'].items():
        if dparam[k0].get('func') is None:
            dparam[k0]['value'] = v0
        else:
            dparam[k0]['initial'] = v0

    # ------------
    # update preset
    dmodel['preset'] = preset


# #############################################################################
# #############################################################################
#                       run checks
# #############################################################################


def _run_check(
    compute_auxiliary=None,
    solver=None,
    verb=None,
):
    # ------
    # verb
    if verb is True:
        verb = 1
    if verb in [None, False]:
        verb = 0

    end, flush, timewait = None, None, None
    if (verb == 1 and type(verb) is int):
        end = '\r'
        flush = True
        timewait = False
    elif (verb == 2 and type(verb) is int):
        end = '\n'
        flush = False
        timewait = False
    elif type(verb) is float:   # if timewait is a float, then it is the
        end = '\n'              # delta of real time between print
        flush = False
        timewait = True         # we will check real time between iterations
    else:
        timewait = False

    # ------------
    # compute auxiliary
    if compute_auxiliary is None:
        compute_auxiliary = True

    # -------
    # solver

    dsolver = {
        'eRK4-homemade': {
            'com': 'explicit Runge_Kutta order 4 homemade',
        },
        'eRK2-scipy': {
            'scipy': 'RK23',
            'com': 'explicit Runge_Kutta order 2 from scipy',
        },
        'eRK4-scipy': {
            'scipy': 'RK45',
            'com': 'explicit Runge_Kutta order 4 from scipy',
        },
        'eRK8-scipy': {
            'scipy': 'DOP853',
            'com': 'explicit Runge_Kutta order 8 from scipy',
        },
    }
    if solver is None:
        solver = 'eRK4-homemade'
    if solver not in dsolver.keys():
        lstr = [f"\t- '{k0}': {v0['com']}" for k0, v0 in dsolver.items()]
        msg = (
            "Arg solver must be in:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    solver_scipy = None
    if 'scipy' in solver:
        solver_scipy = dsolver[solver]['scipy']

    return verb, end, flush, timewait, compute_auxiliary, solver, solver_scipy


def _print_or_wait(
    ii=None,
    nt=None,
    verb=None,
    timewait=None,
    end=None,
    flush=None,
    t0=0
):

    if not timewait:
        if ii == nt - 1:
            end = '\n'
        msg = (
            f'time step {ii+1} / {nt}'
        )
        print(msg, end=end, flush=flush)

    else:
        if time.time() - t0 > verb:
            msg = (
                f'time step {ii+1} / {nt}'
            )
            print(msg, end=end, flush=flush)
            t0 = time.time()
        elif (ii == nt - 1 or ii == 0):
            end = '\n'
            msg = (
                f'time step {ii+1} / {nt}'
            )
            print(msg, end=end, flush=flush)
    return t0
