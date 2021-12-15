# -*- coding: utf-8 -*-


import os
import importlib


from ._def_fields import _DFIELDS, _LIBRARY, _complete_DFIELDS


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
        'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
        'func_order': foo._FUNC_ORDER,
        'file': foo.__file__,
        'description': foo.__doc__,
        'presets': {k0: dict(v0) for k0, v0 in foo._PRESETS.items()},
        'name': v0,
    }


# ####################################################
# ####################################################
# Generic function to get the list of available models
# ####################################################


def get_available_models(
    model=None,
    details=None,
    returnas=None,
    verb=None,
):

    # -----------------
    # check inputs

    if model is None:
        model = sorted(_DMODEL.keys())
    if isinstance(model, str):
        model = [model]
    if returnas is None:
        returnas = False
    if verb is None:
        verb = returnas is False
    if details is None:
        details = returnas is False

    # -----------------
    # get available models

    dmod = {
        k0: {
            'file': str(_DMODEL[k0]['file']),
            'name': str(_DMODEL[k0]['name']),
            'description': str(_DMODEL[k0]['description']),
            'presets': list(_DMODEL[k0]['presets']),
        }
        for k0, v0 in _DMODEL.items()
        if k0 in model
    }

    # -----------------
    # print

    if verb is True or returnas is str:

        if details is True:
            # detailed message
            msg = "\n".join([
                "\n#################################################\n"
                f"################### DESCRIPTION OF {v0['name']}\n"
                + v0['description']
                + "\n\n"
                + f"presets:\n"
                + "\n".join([
                    f" '{k1}' :"
                    # f"\t- {k1.ljust(max(*[len(vv) for vv in v0['presets']]))}:"
                    f" {v1['com']}"
                    for k1, v1 in _DMODEL[k0]['presets'].items()
                ])
                + f"\nnb. of functions:\n"
                + "\n".join([
                    f"\t- {k1}: {len(v1)}"
                    for k1, v1 in _DMODEL[k0]['logics'].items()
                ])
                + f"\nfile: {v0['file']}\n"
                for k0, v0 in dmod.items()
            ])

        else:
            # compact message
            lstr = [
                f"\t- {v0['name']}: {v0['presets']}"
                for k0, v0 in dmod.items()
            ]
            msg = (
                "The following predefined models are currently available:\n"
                + "\n".join(lstr)
            )

        if verb is True:
            print(msg)

    # -----------------
    # return

    if returnas is list:
        return model
    elif returnas is dict:
        return dmod
    elif returnas is str:
        return msg
