# -*- coding: utf-8 -*-


import os
import importlib


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
        'dparam': foo._DPARAM,
        'func_order': foo._FUNC_ORDER,
        'file': foo.__file__,
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
