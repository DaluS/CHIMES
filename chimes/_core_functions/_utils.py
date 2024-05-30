
# Standard
import copy
import inspect
import numpy as np

# Library-specific
from . import _utils

from .._config import config
from itertools import chain
_LTYPES = [int, float, np.int_, np.float_]


# #############################################################################
# #############################################################################
#           Generic function to get / print a subset of a dict
#              used by get_dfields(), get_dvar(), get_dfunc()
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
            "Arg returnas must be in:\n" + "\n".join(lstr)
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
#           str representation
# #############################################################################


def paramfunc2str(
    dfields=None,
    key=None,
    large=False,
    dmisc=None,
    idx=None,
):
    _LEQTYPES = config.get_current('_LEQTYPES')
    eqtype = dfields[key].get('eqtype')
    if eqtype is None:
        if key not in dmisc['dmulti']['scalar']:
            msg = str(dfields[key]['value'].shape)
        else:
            if not hasattr(dfields[key]['value'], '__iter__'):
                msg = '{:4.2g}'.format(dfields[key]['value'])
            elif idx is None:
                msg = ', '.join([
                    f'{aa:4.2g}' for aa in dfields[key]['value'].ravel()
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
                msg = '{:4.2g}'.format(dfields[key]['value'][ind])

    elif eqtype in _LEQTYPES:
        if dfields[key].get('source_exp') is None:
            kargs = ', '.join([
                kk.split('=')[0]
                for kk in dfields[key]['source_kargs'].split(', ')
            ])
            msg = f"f({kargs})"
        else:
            msg = dfields[key]['source_exp']
    return msg


def param_minmax2str(
    dfields=None,
    key=None,
    large=None,
    dmisc=None,
    which=None,
):

    c0 = (
        large and dfields[key].get('eqtype') in [None, 'param']
        and (
            key in dmisc['dmulti']['keys'] or hasattr(dfields[key]['value'], '__iter__')
        )
    )
    if c0:
        if which == 'min':
            msg = "{:4.2g}".format(np.nanmin(dfields[key]['value']))
        else:
            msg = "{:4.2g}".format(np.nanmax(dfields[key]['value']))
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

    dfields_sub = hub.get_dfields(
        returnas=dict,
        eqtype=[None, 'param'],
        group='Numerical',
    )

    # ------------------
    # get column headers

    col1 = ['Numerical param.',
            'value',
            'units',
            'definition']

    # ------------------
    # get values

    ar1 = [
        [
            k0,
            v0['value'],
            v0['units'],
            v0['definition'],
        ]
        for k0, v0 in dfields_sub.items()
    ]
    ar1.append(['run', str(hub.dflags['run']), '', ''])

    # add solver if has run
    if hub.dflags['run'][0] is True:
        ar1.append(['solver', hub.dmisc['solver'], '', ''])

    return col1, ar1


def _get_summary_parameters(hub, idx=0, Region=0, filtersector=()):

    # ----------------
    # preliminary criterion
    # ----------------
    # get sub-dict of interest

    dfields_sub = hub.get_dfields(
        returnas=dict,
        eqtype=[None, 'parameter'],
        group=('Numerical',),
    )

    # ------------------
    # get column headers
    col2 = [
        'Model param.', 'sector', 'value',
        'units', 'group', 'definition',
    ]

    # ------------------
    # get values
    ar2 = [[
        [
            k0,
            ksector,
            f"{v0.get('value')[idx,Region,idsectr,0]:.3f}",
            str(v0['units']),
            v0['group'],
            v0['definition'],
        ]
        for idsectr, ksector in enumerate(hub.dfields[v0['size'][0]].get('list', ['.'])) if ksector not in filtersector]
        for k0, v0 in dfields_sub.items() if v0['size'][1] == '__ONE__'
    ]

    return col2, list(chain.from_iterable(ar2))
    # else:
    #    return col2, ar2


def _print_matrix(hub,
                  idx=None,
                  Region=None):

    for m in [m for m in hub.dfields.keys() if hub.dfields[m]['size'][1] != '__ONE__']:
        # IF IT IS A PARAMETER
        ax1 = hub.dfields[hub.dfields[m]['size'][0]]['list']
        ax2 = hub.dfields[hub.dfields[m]['size'][1]]['list']

        if m in hub.dmisc['dfunc_order']['parameters']:
            val = hub.dfields[m]['value'][idx, Region, ...]
        else:
            val = hub.dfields[m]['value'][0, idx, Region, ...]

        col1 = ['', '|'] + [str(x) for x in ax2]
        ar1 = []
        print(f"name : {m},\nunits : {hub.dfields[m]['units']},\ntype : {hub.dfields[m].get('eqtype','parameter')}")
        # print(ax1,ax2)
        # print(np.shape(val))
        for ii, x in enumerate(ax1):
            liste = [x, '|'] + [f"{val[ii,jj]:.2E}" if (abs(val[ii, jj]) < 0.01 and val[ii, jj] != 0) else f"{val[ii,jj]:.2f}" for jj in range(len(ax2))]
            ar1.append(liste)

        _utils._get_summary(
            lar=[ar1],
            lcol=[col1],
            verb=True,
            returnas=False, )
        print(' ')


def _get_summary_functions_vector(hub, idx=0, Region=0, eqtype=['ode', 'statevar'], filtersector=()):

    # get sub-dict of interest
    dfields_sub = hub.get_dfields(
        returnas=dict,
        eqtype=eqtype,
    )

    col3 = [
        str('vector '.join(eqtype)),
        'sector',
        'source',
        'initial',
        'latest' if hub.dflags['run'][0] else '',
        'units',
        'definition',
        'comment',
        'Auxilliary'
    ]

    # get content
    ar3 = [[[
        k0,
        ksector,
        paramfunc2str(dfields=dfields_sub, key=k0, dmisc=hub.dmisc,),  # if idsectr==0 else '.',
        f"{v0.get('value')[0,idx,Region,idsectr,0]:.3f}",  # f"{v0.get('value')[tuple(np.r_[0, idx[1:],0,0])]:.3f}",
        f"{v0.get('value')[hub.dflags['run'][0],idx,Region,idsectr,0]:.3f}" if hub.dflags['run'][0] else '',  # ",#f"{v0.get('value')[tuple(np.r_[-1, idx[1:],0,0])]:.3f}",
        v0['units'],  # if idsectr==0 else '.',
        v0['definition'],  # if idsectr==0 else '.',
        v0['com'],  # if idsectr==0 else '.',
        not (v0['isneeded']),  # if idsectr==0 else '.'
    ]
        for idsectr, ksector in enumerate(hub.dfields[v0['size'][0]].get('list', ['.',])) if ksector not in filtersector]
        for k0, v0 in dfields_sub.items() if v0['size'][1] == '__ONE__'
    ]

    if len(ar3):
        return col3, list(chain.from_iterable(ar3))
    else:
        return col3, ar3

# #############################################################################
# #############################################################################
#                       Pretty printing
# #############################################################################


def _getcharray(ar, col=None, sep='  ', line='-', just='l', msg=True):

    c0 = ar is None or len(ar) == 0
    if c0:
        return ''
    ar = np.array(ar, dtype='U')

    if ar.ndim == 1:
        ar = ar.reshape((1, ar.size))

    # Get just len
    nn = np.char.str_len(ar).max(axis=0)
    if col is not None:
        if len(col) not in ar.shape:
            msg = (
                "len(col) should be in np.array(ar, dtype='U').shape:\n" + f"\t- len(col) = {len(col)}\n" + f"\t- ar.shape = {ar.shape}"
            )
            raise Exception(msg)
        if len(col) != ar.shape[1]:
            ar = ar.T
            nn = np.char.str_len(ar).max(axis=0)
        nn = np.fmax(nn, [len(cc) for cc in col])

    # Apply to array
    fjust = np.char.ljust if just == 'l' else np.char.rjust
    out = np.array([sep.join(v) for v in fjust(ar, nn)])

    # Apply to col
    if col is not None:
        arcol = np.array([col, [line * n for n in nn]], dtype='U')
        arcol = np.array([sep.join(v) for v in fjust(arcol, nn)])
        out = np.append(arcol, out)

    if msg:
        out = '\n'.join(out)
    return out


def _get_summary(
    lar=None,       # list of data arrays
    lcol=None,      # list of column headers
    sep='  ',
    line='-',
    just='l',
    table_sep=None,
    verb=True,
    returnas=False,
):
    """ Summary description of the object content as a np.array of str """
    if verb is None:
        verb = True
    if returnas is None:
        returnas = False
    if table_sep is None:
        table_sep = '\n\n'

    # Out
    if verb or returnas in [True, str]:
        lmsg = [
            _getcharray(ar, col, sep=sep, line=line, just=just)
            for ar, col in zip(*[lar, lcol])
        ]
        if verb:
            msg = table_sep.join(lmsg)
            print(msg)

    if returnas is not False:
        if returnas is True:
            out = lar, lmsg
        elif returnas is list:
            out = lar
        elif returnas is str:
            out = table_sep.join(lmsg)
        else:
            lok = [False, True, str, 'array']
            msg = "Valid return_ values are: {}".format(lok)
            raise Exception(msg)
        return out
