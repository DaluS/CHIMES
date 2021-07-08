# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
import _utils


# #############################################################################
# #############################################################################
#           Generic function to get / print a subset of a dict
#              used by get_dparam(), get_dvar(), get_dfunc()
# #############################################################################


def _get_dict_subset(
    indict=None,
    verb=None,
    returnas=None,
    lcrit=None,
    lprint=None,
    keyname=None,
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
                indict[k0][k1] == dcrit[k1]
                for k1 in dcrit.keys()
            ])
        ]
    else:
        lk = list(indict.keys())

    # ----------------------
    # Optional print

    if verb is True:
        col0 = [keyname] + lprint
        ar0 = [
            tuple(
                [k0]
                + [
                    str(indict[k0]['value'].shape) if ss == 'shape'
                    else str(indict[k0][ss])
                    for ss in lprint
                ]
            )
            for k0 in lk
        ]
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

    elif returnas in [np.ndarray, 'DataFrame']:
        out = {'key': np.array(lk, dtype=str)}
        out.update({
            k1: np.array([indict[k0][k1] for k0 in lk])
            for k1 in indict[lk[0]].keys()
        })
        if returnas == 'DataFrame':
            import pandas as pd
            return pd.DataFrame.from_dict(out)
        else:
            return out
