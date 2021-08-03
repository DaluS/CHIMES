# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
from . import _utils


_LTYPES = [int, float, np.int_, np.float_]


# #############################################################################
# #############################################################################
#           Generic function to get / print a subset of a dict
#              used by get_dparam(), get_dvar(), get_dfunc()
# #############################################################################

def fromOldToNewModelFormalism(LOGICS):

    # Rewriting fuctions
    _DPARAM = {}
    for keys, funcs in LOGICS.get('ode', {}):
        _DPARAM['key'] = {
            'func': funcs['logic'],
            'com': funcs['com'],
            'eqtype': 'ode',
            'initial': funcs.get('initial', None)
        }
    for keys, funcs in LOGICS.get('statevar', {}):
        _DPARAM['key'] = {
            'func': funcs['logic'],
            'com': funcs['com'],
            'eqtype': 'statevar'
        }

    # Determination of parameters


def _get_dict_subset(
    indict=None,
    verb=None,
    returnas=None,
    lcrit=None,
    lprint=None,
    **kwdargs,
):
    """ Return a copy of the input parameters dict

    Return as:
        - dict: dict
        - 'DataGFrame': a pandas DataFrame
        - np.ndarray: a dict of np.ndarrays
        - False: return nothing (useful of verb=True)

    verb:
        - True: pretty-print the chosen parameters
        - False: print nothing
    """

    # ----------------------
    # check input

    if returnas is None:
        returnas = False
    if verb is None:
        verb = returnas is False

    dreturn_ok = {
        'False': False,
        'dict': dict,
        'np.ndarray': np.ndarray,
        'list': list,
        "'DataFrame'": 'DataFrame',
    }
    if returnas not in dreturn_ok.values():
        lstr = [f'\t- {ss}' for ss in dreturn_ok.keys()]
        msg = (
            "Arg returnas must be in:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # ----------------------
    # select relevant parameters

    if len(kwdargs) > 0:
        # isolate relevant criteria
        dcrit = {
            k0: v0 for k0, v0 in kwdargs.items()
            if k0 in lcrit
        }

        # select param keys matching all critera
        lk = [
            k0 for k0 in indict.keys()
            if all([
                indict[k0].get(k1) == dcrit[k1]
                for k1 in dcrit.keys()
            ])
        ]
    else:
        lk = list(indict.keys())

    # ----------------------
    # Optional print

    if verb is True or returnas in [np.ndarray, 'DataFrame']:
        col0 = lprint
        ar0 = [[k0] for k0 in lk]
        for ii, k0 in enumerate(lk):
            for ss in lprint[1:]:
                if ss == 'value':
                    if indict[k0].get('func') is not None:
                        ar0[ii].append(str(indict[k0]['value'].shape))
                    else:
                        ar0[ii].append(str(indict[k0]['value']))
                else:
                    ar0[ii].append(str(indict[k0].get(ss)))
            ar0[ii] = tuple(ar0[ii])

        if verb is True:
            _utils._get_summary(
                lar=[ar0],
                lcol=[col0],
                verb=True,
                returnas=False,
            )

    # ----------------------
    # return as dict or array

    if returnas is dict:
        # return a copy of the dict
        return {k0: dict(indict[k0]) for k0 in lk}
    elif returnas is list:
        # return only the keys
        return lk

    elif returnas in [np.ndarray, 'DataFrame']:
        out = {
            k0: np.array([ar0[jj][ii] for jj in range(len(ar0))])
            for ii, k0 in enumerate(col0)
        }
        if returnas == 'DataFrame':
            import pandas as pd
            return pd.DataFrame.from_dict(out)
        else:
            return out


# #############################################################################
# #############################################################################
#           Overload logical operations on Solver class
# #############################################################################


def _dict_equal(dict1, dict2, dd=None):

    # initialize failures dict
    dfail = {}

    # check they have identical keys
    c0 = sorted(dict1.keys()) == sorted(dict2.keys())
    if not c0:
        lk = set(dict1.keys()).difference(dict2.keys())
        lk = set(dict2.keys()).difference(dict1.keys())
        dfail[dd] = f"non-common keys: {lk}"
        return dfail

    # check the content of each key
    for k0, v0 in dict1.items():
        key = f"{dd}['{k0}']"
        msg = None

        # check type
        if type(v0) != type(dict2[k0]):
            msg = f"different type ({type(v0)} vs {type(dict2[k0])})"
            dfail[key] = msg
            continue

        # check easy cases (bool, str, floats...)
        c0 = (
            isinstance(v0, bool)
            or isinstance(v0, str)
            or type(v0) in _LTYPES
        )
        if c0:
            if v0 != dict2[k0]:
                msg = f"different values ({v0} vs {dict2[k0]})"
        elif isinstance(v0, np.ndarray):
            if v0.shape != dict2[k0].shape:
                msg = f"different shapes ({v0.shape} vs {dict2[k0].shape})"
            elif not np.allclose(v0, dict2[k0], equal_nan=True):
                msg = "different values"
        elif isinstance(v0, list) or isinstance(v0, tuple):
            if len(v0) != len(dict2[k0]):
                msg = f"different lengths ({len(v0)} vs {len(dict2[k0])})"
            elif v0 != dict2[k0]:
                msg = "different values"
        elif v0 is None:
            pass
        elif isinstance(v0, dict):
            dfail.update(_dict_equal(v0, dict2[k0], dd=f"{dd}['{k0}']"))
        elif k0 == 'func':
            c0 = (
                (
                    isinstance(v0(), np.ndarray)
                    and np.allclose(v0(), dict2[k0]())
                )
                or (
                    type(v0()) in _LTYPES
                    and v0() == dict2[k0]()
                )
            )
            if not c0:
                msg = "Different behaviour of func at default!"
        else:
            msg = "data type not handled yet!"
            raise NotImplementedError(msg)

        if msg is not None:
            dfail[key] = msg

    return dfail


def _equal(obj1, obj2, verb=None, return_dfail=None):
    """ Assess whether 2 instances are equal (i.e.: have the same attributes)
    """

    # ------------
    # check inputs
    if verb is None:
        verb = True
    if not isinstance(verb, bool):
        msg = f"Arg verb must be a bool!\nProvided: {verb}"
        raise Exception(msg)

    if return_dfail is None:
        return_dfail = False
    if not isinstance(return_dfail, bool):
        msg = f"Arg return_dfail must be a bool!\nProvided: {verb}"
        raise Exception(msg)

    # ------------
    # Basic check
    if type(obj1) != type(obj2):
        if verb is True:
            msg = "Object have different types ({type(obj1)} vs {type(obj2)})!"
            print(msg)
        return False

    # ------------
    # check equality

    dfail = {}
    for dd in ['dargs', 'dmisc', 'dparam']:
        dfail.update(_dict_equal(
            dict1=getattr(obj1, dd),
            dict2=getattr(obj2, dd),
            dd=dd,
        ))

    # ------------
    # print result and return

    if len(dfail) == 0:
        if return_dfail is True:
            return True, dfail
        else:
            return True
    else:
        if verb is True:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following differences have been found:\n"
                + "\n".join(lstr)
            )
            print(msg)
        if return_dfail is True:
            return False, dfail
        else:
            return False
