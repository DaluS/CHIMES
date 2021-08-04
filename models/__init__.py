# -*- coding: utf-8 -*-


import os
import importlib
import numpy as np

from ._def_fields import _DFIELDS


_PATH_HERE = os.path.dirname(__file__)


# ####################################################
# ####################################################
#       Automatically load all available models
# ####################################################

_df = {
    ff[:-3]: ff[len('_model_'):ff.index('.py')]
    for ff in os.listdir(_PATH_HERE)
    if ff.startswith('_model_') and ff.endswith('.py')
}


_DMODEL = {}
for k0, v0 in _df.items():
    pfe = os.path.join(_PATH_HERE, k0 + '.py')
    spec = importlib.util.spec_from_file_location(k0, pfe)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    _DMODEL[v0] = {
        'dparam': foo._LOGICS,
        'func_order': foo._FUNC_ORDER,
        'file': foo.__file__,
        'description': foo._DESCRIPTION,
        'presets': foo._PRESETS,
    }

# ####################################################
# ####################################################
# Generic function to get the list of available models
# ####################################################


def get_available_models(returnas=None, verb=None):
    if returnas is None:
        returnas = False
    if verb is None:
        verb = returnas is False

    lmod = sorted(_DMODEL.keys())
    if verb is True or returnas is str:
        lstr = [f'\t- {k0}' for k0 in lmod]
        print(60*'#')
        msg = (
            "The following predefined models are currently available:\n"
            + "\n".join(lstr)
        )
        if verb is True:
            print(msg)
    if returnas is list:
        return lmod
    elif returnas is str:
        return msg


def describe_ALL_available_models():
    # print(60*'#')
    # print('DESCRIPTION OF EACH MODEL :')
    for k0, v0 in _DMODEL.items():
        describe_available_model(k0)
    print(60*'#')


def describe_available_model(model):
    k0 = model
    v0 = _DMODEL[k0]

    print('### DESCRIPTION OF', k0, (40-len(k0))*'#')
    print('# Location    :', v0['file'])
    print('# Description :\n', v0['description'])
    print('# VARIABLES   :')
    for key1, val1 in v0['dparam'].items():
        print('Section :', key1)
        for key, val in v0['dparam'][key1].items():
            if type(val) is dict:
                print('    ', key+(10-len(key))*' ',
                      val.get('com', 'comment not given'))
    print('# PRESETS     :')
    for v1 in v0['presets']:
        print('    ', v1+(15-len(v1))*' ', v0['presets'][v1]['com'])
    print(2*'\n')


def PrintDFIELDS(inpt=None):
    k0 = "THE DEFAULT LIBRARY"
    print('### DESCRIPTION OF', k0, (40-len(k0))*'#')
    if inpt is None:
        inpt = _DFIELDS
    Grouplist = list(set([v0['group'] for v0 in inpt.values()]))

    for group in Grouplist:
        print('')
        print('### group :', group, (15-len(group))*'#')
        col0 = ['key',
                'definition',
                'value',
                'type',
                'units',
                ]
        ar0 = [
            tuple([
                k0,
                v0['definition'],
                printavalue(v0),
                v0['type'],
                v0['units'],
            ])
            for k0, v0 in inpt.items() if v0['group'] == group]
        _get_summary(
            lar=[ar0],
            lcol=[col0],
            verb=True,
            returnas=False,
        )
    print(2*'\n', 60*'#', 2*'\n')


def printavalue(v0):
    if v0['eqtype'] == 'parameter':
        return v0['value']
    if v0['eqtype'] == 'ode':
        return 'ode :'+str(v0['initial'])
    if v0['eqtype'] == 'statevar':
        return 'State variable'
    else:
        return ' '


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
                + f"\t- len(col) = {len(col)}\n"
                + f"\t- ar.shape = {ar.shape}"
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
