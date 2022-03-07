# -*- coding: utf-8 -*-


# Built-in
import os
import types
import functools
import inspect
import itertools as itt
import copy
import warnings
import time
import importlib

# common
import numpy as np


# library specific
from .. import _models


_PATH_HERE = os.path.dirname(__file__)
_PATH_USER_HOME = os.path.expanduser('~')
_PATH_PRIVATE_MODELS = os.path.join(_PATH_USER_HOME, '.pygemmes', '_models')


_LMODEL_ATTR = ['_LOGICS', 'presets']
_DMODEL_KEYS = {
    'logics': dict,
    'presets': dict,
    'file': str,
    'description': str,
    'name': str,
}
_LTYPES = [int, float, np.int_, np.float_]
_LTYPES_ARRAY = [list, tuple, np.ndarray]
_LEQTYPES = ['ode', 'pde', 'statevar', 'param', 'undeclared']


_LEXTRAKEYS = [
    'func', 'kargs', 'args', 'initial', 'grid', 'multi_ind',
    'source_kargs', 'source_exp', 'source_name', 'isneeded',
    'cycles', 'cycles_bykey'
]


_GRID = False


# ##############################
# ##############################
#        Exception
# ##############################


class ShapeError(Exception):

    def __init__(self, lkeys=None, dparam=None, value=None, key=None):
        if key is None:
            lstr = [
                f"\t- {k0}: {dparam[k0]['value'].shape}"
                for k0 in lkeys
            ]
        else:
            lstr = [
                f"\t- {k0}: {value.shape}"
                if k0 == key
                else f"\t- {k0}: {dparam[k0]['value'].shape}"
                for k0 in lkeys
            ]

        self.message = (
            "With grid = False, all parameters shape must be equal:\n"
            + "\n".join(lstr)
        )
        super().__init__(self.message)


# ##############################
# ##############################
#        copy func
# ##############################


def copy_func(func):
    """
    Based on:
        http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)
        https://stackoverflow.com/questions/13503079 (unutbu)
    """
    func2 = types.FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )
    func2 = functools.update_wrapper(func2, func)
    func2.__kwdefaults__ = func.__kwdefaults__
    return func2


# #############################################################################
# #############################################################################
#                       Load library
# #############################################################################


def load_model(model=None, dmulti=None, verb=None, from_user=None):
    """ Load a model from a model file

    model can be:
        - a model name:
            - from_user = False => loaded from the library
            - from_user = True => loaded the user's personal .pygemmes folder
        - the absolute path to an abitrary model file

    """

    # -------------
    # check inputs

    dmodels = _models._get_DMODEL(from_user=from_user)[1]

    if model in dmodels.keys():
        # Get from known models
        model_file = dmodels[model]['file']
        dmodel = dict(dmodels[model])

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

    else:
        msg = (
            "Arg model must be either:\n"
            "\t- the absolute path to valid .py file\n"
            f"\t- the name of an existing model (see get_available_models())\n"
            f"You provided:\n{model}"
        )
        raise Exception(msg)

    # -------------
    # check conformity of dmodel (has 'file', 'name', 'logics', ...)
    _check_dmodel_preset(dmodel)
    dmodel['preset'] = None

    # --------------
    # check conformity of logics (has 'ode', 'pde', 'statevar'...)
    _check_logics(dmodel, verb=verb)

    # convert logics (new formalism) to dparam
    dparam = get_dparam_from_logics(dmodel)
    del dmodel['logics']

    # --------------------
    # re-check dparam + Identify functions order + get dargs
    dparam, dmulti, dfunc_order, dargs = check_dparam(
        dparam=dparam, dmulti=dmulti, verb=verb,
    )

    return dmodel, dparam, dmulti, dfunc_order, dargs


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
        #raise Exception(msg)


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


def _check_logics(dmodel=None, verb=None):
    """ Check conformity of the 'logics' sub-dict

    In particulart, checks:
        - ode
        - pde
        - statevar

    If necessary, add initial values
    Checks all keys are known to _models._DFIELDS
    """

    if verb is None:
        verb = True

    if verb is True:
        msg = (
            "#" * 20
            + f"\nLoading model {dmodel['name']} from {dmodel['file']}"
        )
        print(msg)

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
        k0: [k1 for k1 in v0.keys() if k1 not in _models._DFIELDS]
        for k0, v0 in dmodel['logics'].items()
        if any([k1 for k1 in v0.keys() if k1 not in _models._DFIELDS])
    }
    if len(dkout) > 0:

        if verb is True:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dkout.items()]
            msg = (
                "\nThe following keys are unknown to _LIBRARY, "
                "adding from model:\n"
                + "\n".join(lstr)
            )
            print(msg)

        # adding to local _models._DFIELDS
        for k0, v0 in dkout.items():
            for k1 in v0:
                _models._DFIELDS[k1] = dict(dmodel['logics'][k0][k1])
                # _models._DFIELDS[k1]['eqtype'] = k0
                # _models._DFIELDS[k1]['args'] = {key:[] for key in _LEQTYPES }
                # _models._DFIELDS[k1]['kargs']= []

        # Make sure all fields are set
        _models._complete_DFIELDS(
            dfields=_models._DFIELDS,
            complete=True,
            check=True,
        )

    # -----------------------
    # check ode

    if 'ode' in dmodel['logics'].keys():

        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['ode'])

        # if initial not defined, get from _LIBRARY
        for k1, v1 in dmodel['logics']['ode'].items():
            if v1.get('initial') is None:
                dmodel['logics']['ode'][k1]['initial'] \
                    = _models._DFIELDS[k1]['value']

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
        if lk[0][k0] not in ['param']:
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

    <Missing fields are filled in from defaults values in _models._DFIELDS

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
    # check keys are known to _models._DFIELDS

    lk0 = [
        k0 for k0 in dparam.keys() if k0 not in _models._DFIELDS.keys()
    ]
    if len(lk0) > 0:
        msg = (
            "dparam must have keys identified in _models._DFIELDS!\n"
            f"You provided: {lk0}"
        )
        raise Exception(msg)

    # ---------------------------------------
    # add numerical parameters if not included

    lknum = [
        k0 for k0, v0 in _models._DFIELDS.items()
        if v0['group'] == 'Numerical'
    ]
    for k0 in lknum:
        if k0 not in dparam.keys():
            dparam[k0] = _models._DFIELDS[k0]

    # --------------------------
    # Add time vector if missing

    if 'time' not in dparam.keys():
        dparam['time'] = dict(_models._DFIELDS['time'])

    # ------------
    # check values

    dfail = {}
    for k0, v0 in dparam.items():

        # if value directly provided => put into dict
        if v0 is None or type(v0) in _LTYPES + _LTYPES_ARRAY + [str, bool]:
            dparam[k0] = {'value': v0}

        # if function directly provided => put inot dict
        if hasattr(v0, '__call__'):
            dfail[k0] = "Function must be in a dict {'func': func, 'eqtype':}"
            continue

        # if dict => investigate
        if isinstance(dparam[k0], dict):

            # set missing field to default
            for ss in _models._DFIELDS[k0].keys():
                if dparam[k0].get(ss) is None:
                    dparam[k0][ss] = _models._DFIELDS[k0][ss]

            # identify invalid keys
            lk = [
                kk for kk in dparam[k0].keys()
                if kk != 'eqtype'
                and kk not in _LEXTRAKEYS + list(_models._DFIELDS[k0].keys())
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
                and type(dparam[k0]['value']) in _LTYPES + _LTYPES_ARRAY + [
                    str, bool,
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

            # set grid
            c0 = (
                dparam[k0].get('eqtype') is None
                and isinstance(dparam[k0]['value'], tuple(_LTYPES_ARRAY))
            )
            if c0 and dparam[k0].get('grid') is None:
                dparam[k0]['grid'] = _GRID
            c0 = (
                dparam[k0].get('eqtype') == 'ode'
                and isinstance(dparam[k0]['initial'], tuple(_LTYPES_ARRAY))
            )
            if c0 and dparam[k0].get('grid') is None:
                dparam[k0]['grid'] = _GRID

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

    return copy.deepcopy(dparam)


def _set_key_value(dparam=None, key=None, value=None, grid=None):
    if key not in dparam.keys():
        msg = (
            "key {} is not identified!\n".format(key)
            + "See get_dparam() method"
        )
        raise Exception(msg)

    tochange = 'initial' if dparam[key].get('eqtype', None) == 'ode' else 'value'

    if hasattr(value, '__iter__'):
        dparam[key][tochange] = np.atleast_1d(value).ravel()
    else:
        dparam[key][tochange] = float(value)

    if hasattr(value, '__iter__'):
        if grid is None:
            grid = _GRID
        dparam[key]['grid'] = bool(grid)


def _get_multiple_systems(dparam, dmulti=None):
    """

    A mix of grid=False and grid=True is possible only if all grid=False are
    together
    """

    if dmulti is None:
        dmulti = {
            'multi': False,
            'shape_keys': [],
            'shape': [],
            'keys': [],
            'hasFalse': None,
            'dparfunc': None,
        }

    # -----------
    # add possible new values

    lk0_param = [
        k0 for k0, v0 in dparam.items()
        if v0.get('eqtype') is None
        and isinstance(v0['value'], tuple(_LTYPES_ARRAY))
    ]
    lk0_ode = [
        k0 for k0, v0 in dparam.items()
        if v0.get('eqtype') == 'ode'
        and isinstance(v0['initial'], tuple(_LTYPES_ARRAY))
    ]
    lk0 = lk0_param + lk0_ode

    if len(lk0) == 0:
        shape = (1,)
        shape_keys = []
        lkeys = []
        hasFalse = False

    else:
        # -----------
        # check for pre-existing shape (possibly remove non-relevant keys)

        # rebuild shape and shape_keys only keeping relevant cases
        if dmulti['shape'] == (1,):
            shape = []
            shape_keys = []
            lkeys = []
            hasFalse = False

        else:
            shape = []
            shape_keys = []
            for ii, ss in enumerate(dmulti['shape']):
                lk = []
                for k0 in dmulti['shape_keys'][ii]:

                    kval = (
                        'value' if dparam[k0].get('eqtype') is None
                        else 'initial'
                    )

                    if dparam[k0].get('grid') is None:
                        # grid = None => remove from multi
                        continue

                    lk.append(k0)

                if len(lk) > 0:
                    shape.append(ss)
                    shape_keys.append(lk)

            # concatenation
            lkeys = list(itt.chain.from_iterable(shape_keys))
            hasFalse = any([dparam[k0]['grid'] is False for k0 in lkeys])

        # -----------
        # add new

        for k0 in lk0:

            # get relevant key for the value, flatten and get size
            kval = 'value' if dparam[k0].get('eqtype') is None else 'initial'
            dparam[k0][kval] = np.atleast_1d(dparam[k0][kval]).ravel()
            size = dparam[k0][kval].size

            if k0 not in lkeys:
                if dparam[k0]['grid'] is True:
                    shape.append(size)
                    shape_keys.append([k0])
                    lkeys.append(k0)
                elif dparam[k0]['grid'] is False:
                    if hasFalse:
                        if size != shape[0]:
                            msg = f"Inconsistent shape for dparam['{k0}']"
                            raise Exception(msg)
                        else:
                            shape_keys[0].append(k0)
                            lkeys.insert(0, k0)
                    else:
                        shape.insert(0, size)
                        shape_keys.insert(0, [k0])
                        lkeys.insert(0, k0)
                        hasFalse = True
                else:
                    msg = f"Inconsistent shape for dparam['{k0}']"
                    raise Exception(msg)

        # -----------
        # double-check all

        if hasFalse is not any([dparam[k0]['grid'] is False for k0 in lk0]):
            msg = "Inconsistent hasFalse"
            raise Exception(msg)

        for k0 in lk0:

            kval = 'value' if dparam[k0].get('eqtype') is None else 'initial'

            if dparam[k0]['grid'] is False:
                indi = 0
            else:
                indi = [ii for ii, lk in enumerate(shape_keys) if k0 in lk]
                if len(indi) != 1:
                    msg = f"Inconsistent index for dparam['{k0}']"
                    raise Exception(msg)
                indi = indi[0]

            # double-check the size vs the common shape
            if dparam[k0][kval].size != shape[indi]:
                msg = f"Inconsistent size for dparam['{k0}']"
                raise Exception(msg)
            if dparam[k0]['grid'] is True and shape_keys[indi] != [k0]:
                msg = ""
                raise Exception(msg)
            elif dparam[k0]['grid'] is False and k0 not in shape_keys[indi]:
                msg = ""
                raise Exception(msg)

            dparam[k0]['multi_ind'] = indi

        # -----------
        # broadcast
        # e.g.: shapek0 = (1, 1, sizek0, 1)

        shape0 = [1 for ii in shape]
        for k0 in lk0:
            kval = 'value' if dparam[k0].get('eqtype') is None else 'initial'
            shape0[dparam[k0]['multi_ind']] = dparam[k0][kval].size
            dparam[k0][kval] = dparam[k0][kval].reshape(shape0)
            shape0[dparam[k0]['multi_ind']] = 1

    # update nx
    dparam['nx']['value'] = int(np.prod(shape))

    return {
        'multi': shape != (1,),
        'shape_keys': tuple(shape_keys),
        'shape': tuple(shape),
        'keys': lkeys,
        'hasFalse': hasFalse,
    }


def _get_multiple_systems_functions(dparam=None, dmulti=None):

    # Get list of function parameters with multiple values
    lpf = [
        k0 for k0 in dparam.keys()
        if dparam[k0].get('eqtype') == 'param'
        and hasattr(dparam[k0]['value'], '__iter__')
    ]

    dmulti['dparfunc'] = {k0: [] for k0 in dmulti['keys']}

    if dmulti['multi']:

        # A unique dimension for variation
        if dmulti['hasFalse'] and len(dmulti['shape']) == 1:
            for k0 in lpf:
                lpar = [
                    k1 for k1 in dmulti['keys']
                    if k1 in dparam[k0]['kargs']
                ]

                if len(lpar) == 0:
                    msg = f'Inconsistency with npar for {k0}'
                    raise Exception(msg)

                for k1 in lpar:
                    dmulti['dparfunc'][k1].append(k0)

        # Mix between a non-grid and grids
        elif dmulti['hasFalse'] and len(dmulti['shape']) > 1:
            for k0 in lpf:
                lpar = [
                    k1 for ii, k1 in enumerate(dmulti['keys'])
                    if k1 in dparam[k0]['kargs']
                    and dparam[k0]['value'].shape[dparam[k1]['multi_ind']] > 1
                ]

                if len(lpar) > 1:
                    msg = (
                        f"Not handled yet for {k0}:\n"
                        "Parameters functions depending on several parameters"
                        " with multiple values\n"
                        f"\t- lpar: {lpar}"
                    )
                    raise Exception(msg)

                elif len(lpar) == 0:
                    msg = f'Inconsistency with npar for {k0}'
                    raise Exception(msg)

                dmulti['dparfunc'][lpar[0]].append(k0)

        # multiple dimensions for variation (grid only)
        elif not dmulti['hasFalse']:
            for k0 in lpf:
                lpar = [
                    k1 for ii, k1 in enumerate(dmulti['keys'])
                    if k1 in dparam[k0]['kargs']
                    and dparam[k0]['value'].shape[dparam[k1]['multi_ind']] > 1
                ]

                if len(lpar) > 1:
                    msg = (
                        f"Not handled yet for {k0}:\n"
                        "Parameters functions depending on several parameters"
                        " with multiple values\n"
                        f"\t- lpar: {lpar}"
                    )
                    raise Exception(msg)

                elif len(lpar) == 0:
                    msg = f'Inconsistency with npar for {k0}'
                    raise Exception(msg)

                dmulti['dparfunc'][lpar[0]].append(k0)


# #############################################################################
# #############################################################################
#                       dargs by reference
# #############################################################################


def get_dargs_by_reference(dparam, dfunc_order=None):

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

    return dargs


# #############################################################################
# #############################################################################
#                       dparam checks - high-level
# #############################################################################


def check_dparam(dparam=None, dmulti=None, verb=None):
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
    _extract_parameters(dparam, verb=verb)
    dparam = _check_dparam(dparam)

    # -------------------
    # Identify multiple systems
    dmulti = _get_multiple_systems(dparam, dmulti=dmulti)

    # ----------------
    # Identify functions
    dparam, dfunc_order = _check_func(dparam, dmulti=dmulti, verb=verb)

    # -------------------
    # Identify params that are not multi but functions of multi
    _get_multiple_systems_functions(dparam=dparam, dmulti=dmulti)

    # ----------------
    # Make sure to copy to avoid passing by reference
    dparam = {
        k0: dict(v0) for k0, v0 in dparam.items()
    }

    # ---------------
    # dargs (to be used in solver, faster to define it here)
    dargs = get_dargs_by_reference(dparam, dfunc_order=dfunc_order)

    return dparam, dmulti, dfunc_order, dargs


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
            kargs = inspect.getfullargspec(_models._DFIELDS[key]['func']).args

        # check if any parameter is unknown
        for kk in kargs:
            key = 'lambda' if kk == 'lamb' else kk
            if key not in lkok:
                if _models._DFIELDS[key].get('func') is None:
                    if key not in lpar_add:
                        lpar_add.append(key)
                elif key not in lfunc_add:
                    lfunc_add.append(key)

    return lpar_add, lfunc_add


def _extract_parameters(dparam, verb=None):
    """ Extract fixed-value parameters

    If relevant, the list of fixed-value parameters is extracted from
        the func kwdargs
    """

    if verb is None:
        verb = True

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
            if key not in _models._DFIELDS.keys():
                dfail[k0] = "Unknown parameter"
                continue
            dparam[key] = dict(_models._DFIELDS[key])

        # -------------------
        # Raise Exception if any
        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following unknown parameters have been identified:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    # -------------
    # print
    if verb is True:
        msg = (
            "\nThe following fields are identified as parameters :\n"
            f"\t- param (fixed): {lpar_new}\n"
            f"\t- param (func.): {lfunc_new}"
        )
        print(msg)


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
            # print(k0, inspect.getsource(dparam[k0]['func']).replace(
            #    '    ', '').split('] =')[-1].split('com')[0])
            sour = inspect.getsource(dparam[k0]['func']).replace(
                '    ', '').split('\n')[0]
            c0 = (
                sour.count(':') >= 1
                and (
                    sour.replace(' ', '').count("'func':lambda") == 1
                    # and sour.count(':') == 2 # Comment for remote lambda expression
                    # and 'lambda' in sour.split(':')[1] #Comment for remote lambda
                    # and sour.count('\n') == 1
                    # Comment because comment at end of the line or no ',' when in a remote file
                    # and sour.endswith(',\n')
                )
                or (
                    sour.replace(' ', '').count("'func':lambda") == 0
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

            # Extract kargs and exp (for lambda only)
            if sour.replace(' ', '').count("'func':lambda") == 1:
                # clean-up source
                sour = sour.strip().replace(',\n', '').replace('\n', '')
                sour = sour[sour.index('lambda') + len('lambda'):]
                # separate keyword args from expression
                kargs, exp = sour.split(':')[:2]

                # store exp for lambda only
                dparam[k0]['source_exp'] = exp.strip()
            else:
                kargs = sour[sour.index('(') + 1:sour.index(')')]
                dparam[k0]['source_name'] = dparam[k0]['func'].__name__

            kargs = [kk.strip() for kk in kargs.strip().split(',')]
            if not all(['=' in kk for kk in kargs]):
                msg = (
                    'Only keyword args can be used for lambda functions!\n'
                    f'Provided:\n{sour}'
                )
                raise Exception(msg)

            # store keyword args and cleaned-up expression separately
            kargs = ', '.join(kargs)
            dparam[k0]['source_kargs'] = kargs


def _check_func(dparam=None, dmulti=None, verb=None):
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
    tltypes = tuple(_LTYPES + _LTYPES_ARRAY)

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
        c0 = (
            v0['eqtype'] == 'ode'
            and not isinstance(v0.get('initial'), tltypes)
        )
        if c0:
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
    dfunc_order = _suggest_funct_order(dparam=dparam, verb=verb)

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

    # ------------------
    # copy func to avoid passing by reference
    for k0 in lfunc:
        dparam[k0]['func'] = copy_func(dparam[k0]['func'])

    # --------------------------------
    # set default values of parameters to their real values
    # this way we don't have to feed the parameters value inside the loop
    _update_func_default_kwdargs(lfunc=lfunc, dparam=dparam, dmulti=dmulti)

    # -------------------------------------------
    # Create variables for all varying quantities
    shape = tuple(np.r_[dparam['nt']['value'], dmulti['shape']])
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

    try:
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

    except Exception as err:
        if eqtype == 'ode':
            # function order not necessary => pick any order
            lfsort = [
                kk for kk, vv in dparam.items()
                if vv.get('eqtype') == eqtype
            ]
        else:
            # For 'statevar' and 'param' a function order is necessary => raise
            raise err

    return lfsort


def _suggest_funct_order(
    dparam=None,
    verb=None,
):
    """ Propose a logical order for computing the functions

    Strategy:
        1) Determine if a natural order exists (i.e. no cyclical dependency)
        2) if no => identify functions that, if updated from the previous time
        step, allow to compute the maximum number of other functions without
        having to rely on the previous time step for them

        Auxiliary functions are not considered
    """

    # -----------
    # check inputs

    if verb is None:
        verb = True

    # -------------
    # we want a function order for statevar and param
    dfunc_order = {
        k0: _suggest_funct_order_by_group(eqtype=k0, dparam=dparam)
        for k0 in ['param', 'statevar', 'ode']
    }

    # -----------
    # print

    if verb is True:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfunc_order.items()]
        msg = (
            "\nThe following order has been determined for functions:\n"
            + "\n".join(lstr)
        )
        print(msg)

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


def _update_func_default_kwdargs(lfunc=None, dparam=None, dmulti=None):
    """ Here we update the default valuee of all functions """

    for k0 in lfunc:

        # skip trivial
        if len(dparam[k0]['args']) == 0:
            continue

        # get defaults
        defaults = list(dparam[k0]['func'].__defaults__)
        kargs = dparam[k0]['source_kargs'].split(', ')
        # print(k0, dparam[k0]['source_kargs'])
        # update using fixed param (eqtype = None)
        for k1 in dparam[k0]['args'][None]:
            key = 'lamb' if k1 == 'lambda' else k1

            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key == vv.split('=')[0]]

            if len(ind) != 1:
                msg = f"Inconsistency in (fixed) kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])

        # update using param
        for k1 in dparam[k0]['args']['param']:
            key = 'lamb' if k1 == 'lambda' else k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key in vv]
            if len(ind) != 1:
                msg = f"Inconsistency in (func) kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])

        # update
        dparam[k0]['func'].__defaults__ = tuple(defaults)
        # dparam[k0]['source_kargs'] = ', '.join(kargs)


# #############################################################################
# #############################################################################
#                   update from preset
# #############################################################################


def update_from_preset(
    dparam=None,
    dmodel=None,
    dmulti=None,
    preset=None,
    dpresets=None,
    verb=None,
):
    """ Update the dparam dict from values taken from preset """

    tltypes = tuple(_LTYPES + _LTYPES_ARRAY)

    # ---------------
    # check inputs

    if preset is None:
        dmodel['preset'] = None
        return

    if dpresets is None:
        dpresets = dmodel['presets']

    if preset not in dpresets.keys():
        lstr = [
            f"\t- {k0}: {v0['com']}" for k0, v0 in dpresets.items()
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
        k0 for k0, v0 in dpresets[preset]['fields'].items()
        if not (
            k0 in dparam.keys()
            and (isinstance(v0, dict) or isinstance(v0, tltypes))
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

    lkok = ['value', 'initial', 'grid']
    for k0, v0 in dpresets[preset]['fields'].items():
        if dparam[k0].get('eqtype') not in [None, 'ode']:
            msg = f"Non-supported eqtype for {preset}['fields']['{k0}']"
            raise Exception(msg)

        kval = 'value' if dparam[k0].get('eqtype') is None else 'initial'
        if isinstance(v0, tltypes):
            dparam[k0][kval] = v0

        else:
            lkout = [kk for kk in v0.keys() if kk not in lkok]
            if len(lkout) > 0:
                lstr = [f'\t- {k0}' for k0 in lkout]
                msg = (
                    f"The following keys from {preset} are not supported:\n"
                    + "\n".join(lstr)
                )
                raise Exception(msg)

            if v0.get('value') is not None:
                dparam[k0][kval] = v0['value']
            if v0.get('initial') is not None:
                dparam[k0][kval] = v0['initial']
            if v0.get('grid') is not None:
                dparam[k0]['grid'] = v0['grid']

    # ----------------------
    # re-check dparam

    dparam, dmulti, dfunc_order, dargs = check_dparam(
        dparam=dparam, dmulti=dmulti, verb=verb,
    )

    # ------------
    # update preset
    dmodel['preset'] = preset

    return dparam, dmulti, dfunc_order, dargs


# #############################################################################
# #############################################################################
#                       run checks
# #############################################################################


def _run_verb_check(
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
    return {
        'verb': verb, 'end': end,
        'flush': flush, 'timewait': timewait,
    }


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


# #############################################################################
# #############################################################################
#                       check idx
# #############################################################################

def _check_idx(idx=None, nt=None, dmulti=None):
    """ Check idx is conform to dmulti['shape']

    Return None or a time slice

    """

    c0 = (
        idx is None
        or (
            (
                dmulti is None
                or len(dmulti['shape']) == 1
            )
            and isinstance(idx, int)
        )
        or (
            hasattr(idx, '__iter__')
            and len(idx) == len(dmulti['shape'])
            and all([
                isinstance(ii, int)
                and 0 <= vv < dmulti['shape'][ii]
                for ii, vv in enumerate(idx)
            ])
        )
    )
    if not c0:
        msg = (
            "Arg idx must be either:\n"
            "\t- None\n"
            f"\t- iterable of int indices for shape {dmulti['shape']}\n"
            f"Provided: {idx}"
        )
        raise Exception(msg)

    if isinstance(idx, int):
        idx = [idx]

    if idx is not None:
        idx = tuple([slice(0, nt)] + list(idx))
    return idx
