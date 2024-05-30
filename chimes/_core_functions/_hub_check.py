# typical
# import copy
# import os
import inspect
import time

# library specific
from .. import libraries
from .._config import config
# from .._config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS

_DMODEL_KEYS = {
    'logics': dict,
    'presets': dict,
    'file': str,
    'description': str,
    'name': str,
}


# #################### RUN CHECK ########################
def _run_verb_check(
    verb=None,
):
    # ------
    # verb
    if verb in [True, int]:
        verb = 0.1
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
        end = '\r'              # delta of real time between print
        flush = True
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
# ###################### MODEL FILE ############################################
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

    # _DMODEL_KEYS = config.get_current('_DMODEL_KEYS')
    _LEQTYPES = config.get_current('_LEQTYPES')
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
            "dmodel must be a dict with keys:\n" + "\n".join(lstr)
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
            k0 in _LEQTYPES and isinstance(v0, dict)
        )
    ]
    if len(lkout) > 0:
        lstr = [f'\t- {kk}' for kk in lkout]
        raise Exception(
            "The following keys in _LOGIC are not supported:\n" + "\n".join(lstr) + '\n, valid list is'.join(_LEQTYPES)
        )

    # check ode ############
    if 'ode' in dmodel['logics'].keys():
        # list non-conform keys (must have a 'func' function)
        _check_are_functions(indict=dmodel['logics']['ode'])

        # if initial not defined, get from _LIBRARY
        for k1, v1 in dmodel['logics']['ode'].items():
            if v1.get('initial') is None:
                dmodel['logics']['ode'][k1]['initial'] \
                    = libraries._DFIELDS[k1]['value']

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
            isinstance(v1, dict) and hasattr(v1.get('func'), '__call__')
        )
    ]
    if len(lkout) > 0:
        lstr = [f'\t- {kk}' for kk in lkout]
        msg = (
            "The following ode have non-conform 'func':\n" + "\n".join(lstr)
        )
        raise Exception(msg)
