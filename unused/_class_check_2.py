# typical
import copy
import os
import inspect

# library specific
from .. import _models
from .._config import _LMODEL_ATTR, _DMODEL_KEYS, _LTYPES, _LTYPES_ARRAY, _LEQTYPES, _LEXTRAKEYS
from .._config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS


##################### RUN CHECK ########################
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


# %%###########################################################################
####################### MODEL FILE ############################################
def dmodel(dmodel=None,
           verb=None):
    """ 
    1) all keys from dmodel are valid    
    2) preset are well written
    3)  Check conformity of the 'logics' sub-dict
        In particulart, checks:
        - ode
        - statevar

    """
    # 1) CHECK THAT ALL KEYS FROM _DMODEL ARE INSIDE
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

    # 2) CHECK THAT PRESETS ARE WELL WRITTEN
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
        print(f"WARNING :The following presets are non-valid:\n {lkout}")

    lkout = [
        k0 for k0, v0 in dmodel['logics'].items()
        if not (
            k0 in _LEQTYPES
            and isinstance(v0, dict)
        )
    ]
    if len(lkout) > 0:
        lstr = [f'\t- {kk}' for kk in lkout]
        raise Exception(
            "The following keys in _LOGIC are not supported:\n"
            + "\n".join(lstr) + '\n, valid list is'.join(_LEQTYPES)
        )

    # check ode ############
    if 'ode' in dmodel['logics'].keys():
        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['ode'])

        # if initial not defined, get from _LIBRARY
        for k1, v1 in dmodel['logics']['ode'].items():
            if v1.get('initial') is None:
                dmodel['logics']['ode'][k1]['initial'] \
                    = _models._DFIELDS[k1]['value']

    # check statevar #######
    if 'statevar' in dmodel['logics'].keys():

        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['statevar'])


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


def dparam_pre(dparam):
    dfail = {}
    for k0, v0 in dparam.items():

        # if function directly provided => put inot dict
        if hasattr(v0, '__call__'):
            dfail[k0] = "Function must be in a dict {'func': func, 'eqtype':}"
            continue

        # if dict => investigate
        if isinstance(dparam[k0], dict):
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


def dparam(dparam=None):
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
        raise Exception((
            "dparam must be a dict!\n"
            f"You provided: {type(dparam)}"
        ))

    # ------------
    # check values
    dfail = {}
    for k0, v0 in dparam.items():

        # if function directly provided => put inot dict
        if hasattr(v0, '__call__'):
            dfail[k0] = "Function must be in a dict {'func': func, 'eqtype':}"
            continue

        # if dict => investigate
        if isinstance(dparam[k0], dict):
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


def functions(dparam=None, verb=None):
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

    # extract parameters that are functions
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]

    # extract input args and check conformity
    dfail = {}
    for k0 in lfunc:
        v0 = dparam[k0]
        kargs = inspect.getfullargspec(v0['func']).args

        # Replace lamb by lambda
        if 'lamb' in kargs:
            kargs[kargs.index('lamb')] = 'employment'

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
    # time_dependence(dparam=dparam)

    # -------------------------------
    # Store the source for later use (doc, saving...)
    check_source(lfunc=lfunc, dparam=dparam)

    return dparam


def check_source(lfunc=None, dparam=None):
    """ Extract the source code of functions

    Useful for:
        - extracting default values of keyword args and changing them
        - displaying the function in get_summary() (for one-liners only)

    """

    for k0 in lfunc:
        if dparam[k0].get('source_kargs') is None:
            assert dparam[k0].get('source_exp') is None

            # extract source and check if lambda
            sour = inspect.getsource(dparam[k0]['func']).replace(
                '    ', '').split('\n')[0]
            c0 = (
                sour.count(':') >= 1
                and (
                    sour.replace(' ', '').count("'func':lambda") == 1
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
                    "Should be either a lambda (one-liner) or a 'def():'"
                )
                raise Exception(msg)


def time_dependence(dparam=None):
    """ Safety check on time dependence

    Here we:
        - identify functions that depend on time
        - make sure that time-dependent functions are 'ode' or 'statevar'
        - make sure that time-independent functions are 'param'

    """
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
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
