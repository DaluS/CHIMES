# -*- coding: utf-8 -*-


import numpy as np


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
                "len(col) should be in np.array(ar, dtype='U').shape:\n"
                + "\t- len(col) = {}\n".format(len(col))
                + "\t- ar.shape = {}".format(ar.shape)
            )
            raise Exception(msg)
        if len(col) != ar.shape[1]:
            ar = ar.T
            nn = np.char.str_len(ar).max(axis=0)
        nn = np.fmax(nn, [len(cc) for cc in col])

    # Apply to array
    fjust = np.char.ljust if just == 'l' else np.char.rjust
    out = np.array([sep.join(v) for v in fjust(ar,nn)])

    # Apply to col
    if col is not None:
        arcol = np.array([col, [line*n for n in nn]], dtype='U')
        arcol = np.array([sep.join(v) for v in fjust(arcol, nn)])
        out = np.append(arcol,out)

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
            for ar, col in zip(*[lar,lcol])
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


# #############################################################################
# #############################################################################
#                      
# #############################################################################





