# -*- coding: utf-8 -*-


# Standard
import copy
import inspect


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


def _get_dict_subset(
    indict=None,
    condition=None,
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

    if condition is None:
        condition = 'all'
    if condition not in ['all', 'any']:
        msg = f"Arg condition must be 'all' or 'any'!\nProvided: {condition}"
        raise Exception(msg)
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
            k0: v0 if isinstance(v0, (list, tuple)) else [v0]
            for k0, v0 in kwdargs.items()
            if k0 in lcrit
        }

        # select param keys matching all critera
        arok = np.zeros((len(dcrit), len(indict)), dtype=bool)
        lk0 = np.array(list(indict.keys()))
        for ii, (k1, v1) in enumerate(dcrit.items()):
            if k1 == 'key':
                arok[ii, :] = [k0 in v1 for k0 in lk0]
            else:
                arok[ii, :] = [indict[k0].get(k1) in v1 for k0 in lk0]
            if isinstance(v1, tuple):
                arok[ii, :] = ~arok[ii, :]

        # Apply condition
        if condition == 'all':
            ind = np.all(arok, axis=0)
        elif condition == 'any':
            ind = np.any(arok, axis=0)
        lk = lk0[ind].tolist()

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
                    if indict[k0].get('eqtype') not in [None, 'param']:
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
        return copy.deepcopy({k0: dict(indict[k0]) for k0 in lk})
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


def _dict_equal(dict1, dict2, dd=None, atol=None, rtol=None):

    if atol is None:
        atol = 1.e-05
    if rtol is None:
        rtol = 1.e-05

    # initialize failures dict
    dfail = {}

    # check they have identical keys
    c0 = dict1.keys() == dict2.keys()
    if not c0:
        lk1 = set(dict1.keys()).difference(dict2.keys())
        lk2 = set(dict2.keys()).difference(dict1.keys())
        dfail[dd] = f"non-common keys: {lk1.union(lk2)}"
        return dfail

    # check the content of each key
    for k0, v0 in dict1.items():
        key = f"{dd}['{k0}']"
        msg = None

        # check type
        if not isinstance(v0, type(dict2[k0])):
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
            elif not np.allclose(np.isnan(v0), np.isnan(dict2[k0])):
                msg = (
                    "non-matching NaNs "
                    f"({np.isnan(v0).sum()} vs {np.isnan(dict2[k0]).sum()})"
                )
            elif not np.allclose(
                v0, dict2[k0],
                atol=atol, rtol=rtol,
                equal_nan=True,
            ):
                ind_ok = ~np.isnan(v0)
                diff = np.abs(v0 - dict2[k0])[ind_ok]
                thresh = atol + rtol*np.abs(dict2[k0][ind_ok])
                ind = diff > thresh
                msg = (
                    f"different values ({ind.sum()}/{ind_ok.sum()}):"
                    f"    mean {np.mean(diff[ind])} vs {np.mean(thresh[ind])}"
                    f"      max {np.max(diff[ind])} vs {np.max(thresh[ind])}"
                )
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
            args = inspect.getfullargspec(v0)
            dargs = {k0: args.defaults[ii] for ii, k0 in enumerate(args.args)}
            # dargs = {}
            v0_val = v0(**dargs)
            c0 = (
                (
                    isinstance(v0_val, np.ndarray)
                    and np.allclose(v0_val, dict2[k0]())
                )
                or (
                    type(v0_val) in _LTYPES
                    and v0_val == dict2[k0](**dargs)
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


def _equal(obj1, obj2, atol=None, rtol=None, verb=None, return_dfail=None):
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
            msg = f"Object have different types ({type(obj1)} vs {type(obj2)})!"
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
            atol=atol,
            rtol=rtol,
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


# #############################################################################
# #############################################################################
#           str representation
# #############################################################################


def paramfunc2str(
    dparam=None,
    key=None,
    large=None,
    dmisc=None,
    idx=None,
):

    eqtype = dparam[key].get('eqtype')
    if eqtype is None:
        if large and key in dmisc['dmulti']['keys']:
            msg = str(dparam[key]['value'].shape)
        else:
            if not hasattr(dparam[key]['value'], '__iter__'):
                msg = '{:4.2g}'.format(dparam[key]['value'])
            elif idx is None:
                msg = ', '.join([
                    f'{aa:4.2g}' for aa in dparam[key]['value'].ravel()
                ])
            else:
                if len(dmisc['dmulti']['shape']) > 1:
                    ind = list(idx[1:])
                    if key in dmisc['dmulti']['keys']:
                        kref = key
                    else:
                        lk = [
                            kk for kk, vv in dmisc['dmulti']['dparfunc']
                            if key in vv
                        ]
                        if len(lk) != 1:
                            msg = "Inconsistency in dmisc['dmulti']['dparfunc']"
                            raise Exception(msg)
                        kref = lk[0]
                    indi = dmisc['dmulti']['keys'].index(kref)
                    ind = tuple([
                        jj if ii == indi else 0
                        for ii, jj in enumerate(idx[1:])
                    ])
                else:
                    ind = idx[1]
                msg = '{:4.2g}'.format(dparam[key]['value'][ind])

    elif eqtype in ['param', 'ode', 'statevar']:
        if dparam[key].get('source_exp') is None:
            kargs = ', '.join([
                kk.split('=')[0]
                for kk in dparam[key]['source_kargs'].split(', ')
            ])
            msg = f"f({kargs})"
        else:
            msg = dparam[key]['source_exp']

    return msg


def param_minmax2str(
    dparam=None,
    key=None,
    large=None,
    dmisc=None,
    which=None,
):

    c0 = (
        large
        and dparam[key].get('eqtype') in [None, 'param']
        and (
            key in dmisc['dmulti']['keys']
            or hasattr(dparam[key]['value'], '__iter__')
        )
    )
    if c0:
        if which == 'min':
            msg = "{:4.2g}".format(np.nanmin(dparam[key]['value']))
        else:
            msg = "{:4.2g}".format(np.nanmax(dparam[key]['value']))
    else:
        msg = ''
    return msg


# #############################################################################
# #############################################################################
#           get_summary parts
# #############################################################################


def _get_summary_numerical(hub):

    # ----------------
    # get sub-dict of interest

    dparam_sub = hub.get_dparam(
        returnas=dict,
        eqtype=[None, 'param'],
        group='Numerical',
    )

    # ------------------
    # get column headers

    col1 = ['Numerical param.', 'value', 'units', 'definition', 'comment']

    # ------------------
    # get values

    ar1 = [
        [
            k0,
            paramfunc2str(dparam=dparam_sub, key=k0),
            v0['units'],
            v0['definition'],
            v0['com'],
        ]
        for k0, v0 in dparam_sub.items()
    ]
    ar1.append(['run', str(hub.dmisc['run']), '', '', ''])

    # add solver if has run
    if hub.dmisc['run'] is True:
        ar1.append(['solver', hub.dmisc['solver'], '', '', ''])

    return col1, ar1


def _get_summary_parameters(hub, idx=None):

    # ----------------
    # preliminary criterion

    large = (
        idx is None
        and hub.dmisc['dmulti'] is not None
        and np.any(np.array(hub.dmisc['dmulti']['shape']) > 3)
    )

    # ----------------
    # get sub-dict of interest

    dparam_sub = hub.get_dparam(
        returnas=dict,
        eqtype=[None, 'param'],
        group=('Numerical',),
    )

    # ------------------
    # get column headers

    if large:
        col2 = [
            'Model param.', 'value', 'min', 'max',
            'units', 'group', 'definition',
        ]
    else:
        col2 = [
            'Model param.', 'value',
            'units', 'group', 'definition',
        ]

    # ------------------
    # get values

    if large:
        # if many systems => don't show all, just shape, min, max

        ar2 = [
            [
                k0,
                paramfunc2str(
                    dparam=dparam_sub,
                    key=k0,
                    large=large,
                    dmisc=hub.dmisc,
                ),
                param_minmax2str(
                    dparam=dparam_sub,
                    key=k0,
                    large=large,
                    dmisc=hub.dmisc,
                    which='min',
                ),
                param_minmax2str(
                    dparam=dparam_sub,
                    key=k0,
                    large=large,
                    dmisc=hub.dmisc,
                    which='max',
                ),
                str(v0['units']),
                v0['group'],
                v0['definition'],
            ]
            for k0, v0 in dparam_sub.items()
        ]

    else:
        ar2 = [
            [
                k0,
                paramfunc2str(
                    dparam=dparam_sub,
                    key=k0,
                    large=large,
                    dmisc=hub.dmisc,
                    idx=idx,
                ),
                str(v0['units']),
                v0['group'],
                v0['definition'],
            ]
            for k0, v0 in dparam_sub.items()
        ]

    return col2, ar2


def _get_summary_functions(hub, idx=None, eqtype=['ode', 'statevar'],isneeded=None):

    # ----------------
    # preliminary criterion

    if hub.dmisc['dmulti'] is None:
        shape = (1,)
    else:
        shape = hub.dmisc['dmulti']['shape']
    large = (
        idx is None
        and (
            np.any(np.array(shape) > 3)
            or len(shape) > 1
        )
    )

    # ----------------
    # get sub-dict of interest

    if isneeded is not None:
        dparam_sub = hub.get_dparam(
            returnas=dict,
            eqtype=eqtype,
            isneeded=isneeded
        )
    else :
        dparam_sub = hub.get_dparam(
            returnas=dict,
            eqtype=eqtype,
            isneeded=isneeded
        )

    # ------------------
    # get column headers
    if isneeded is False :
        eqtype[0] ='auxilliary '+ eqtype[0]

    if large:
        col3 = [
            str(''.join(eqtype)), 'source',
            'shape',
            'units',
            'definition', 'comment',
        ]
    else:
        if hub.dmisc['run']:
            col3 = [
                str(''.join(eqtype)), 'source',
                'initial', 'final',
                'units',
                'definition', 'comment',
            ]
        else:
            col3 = [
                str(''.join(eqtype)), 'source',
                'initial',
                'units',
                'definition', 'comment',
            ]

    # ------------------
    # get values

    if large:
        ar3 = [
            [
                k0,
                paramfunc2str(
                    dparam=dparam_sub,
                    key=k0,
                    large=large,
                    dmisc=hub.dmisc,
                ),
                f"{v0.get('value').shape}",
                v0['units'],
                v0['definition'],
                v0['com'],
            ]
            for k0, v0 in dparam_sub.items()
        ]

    elif idx is None:
        if hub.dmisc['run']:
            ar3 = [
                [
                    k0,
                    paramfunc2str(
                        dparam=dparam_sub,
                        key=k0,
                        large=large,
                        dmisc=hub.dmisc,
                    ),
                    f"{v0.get('value')[0, ...]}",
                    f"{v0.get('value')[-1, ...]}",
                    v0['units'],
                    v0['definition'],
                    v0['com'],
                ]
                for k0, v0 in dparam_sub.items()
            ]
        else:
            ar3 = [
                [
                    k0,
                    paramfunc2str(
                        dparam=dparam_sub,
                        key=k0,
                        large=large,
                        dmisc=hub.dmisc,
                    ),
                    f"{v0.get('value')[0, ...]}",
                    v0['units'],
                    v0['definition'],
                    v0['com'],
                ]
                for k0, v0 in dparam_sub.items()
            ]

    else:
        if hub.dmisc['run']:
            ar3 = [
                [
                    k0,
                    paramfunc2str(
                        dparam=dparam_sub,
                        key=k0,
                        large=large,
                        dmisc=hub.dmisc,
                    ),
                    f"{v0.get('value')[tuple(np.r_[0, idx[1:]])]}",
                    f"{v0.get('value')[tuple(np.r_[-1, idx[1:]])]}",
                    v0['units'],
                    v0['definition'],
                    v0['com'],
                ]
                for k0, v0 in dparam_sub.items()
            ]

        else:
            ar3 = [
                [
                    k0,
                    paramfunc2str(
                        dparam=dparam_sub,
                        key=k0,
                        large=large,
                        dmisc=hub.dmisc,
                    ),
                    f"{v0.get('value')[tuple(np.r_[0, idx[1:]])]}",
                    v0['units'],
                    v0['definition'],
                    v0['com'],
                ]
                for k0, v0 in dparam_sub.items()
            ]

    return col3, ar3
