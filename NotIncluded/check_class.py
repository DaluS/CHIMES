# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:35:02 2022

@author: Paul Valcke
"""

# IN CLASS_CHECKS, LOAD_MODELS

elif os.path.isfile(model) and model.endswith('.py'):

    raise Exception('Absolute path for models disactivated for the moment')
    '''
        # get from arbitrary model file
        model_file = str(model)

        # trying to derive model name from file name
        model = os.path.split(model_file)[-1]
        if model.startswith('_model_') and model.count('_') == 2:
            model = model[model.index('_model_') + len('_model_'):-3]
        else:
            msg = (
                "model file has non-standard name:\n"
                f"\t- model file: {model_file}\n"
                "  => setting model name to 'custom'"
            )
            warnings.warn(msg)
            model = 'custom'


        spec = importlib.util.spec_from_file_location(k0, model_file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)

        # checking attributes
        lattr = [att for att in _LMODEL_ATTR if not hasattr(foo, att)]
        if len(lattr) > 0:
            lstr = [f'\t- {att}' for att in lattr]
            msg = (
                "The provided model file should have at least attributes:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

        # loading attributes
        dmodel = {
            'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
            'presets': {k0: v0 for k0, v0 in foo._PRESETS.items()},
            'description': foo.__doc__,
            'file': model_file,
            'name': model,
        }
        '''
