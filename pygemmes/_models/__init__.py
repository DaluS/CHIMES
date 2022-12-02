# -*- coding: utf-8 -*-
# Check 9/27/22

import os
import importlib

from ._def_fields import _DFIELDS, _complete_DFIELDS
from ._def_functions import Funcs
from .._utilities import _utils

import inspect

from .._config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS,_MODEL_NAME_CONVENTION,_MODELS_SHOWDETAILS,_MODEL_FOLDER_HIDDEN

from copy import deepcopy

# ####################################################
# ####################################################
#       Automatically load all available models
# ####################################################
def _get_DMODEL(from_user=_FROM_USER):
    # check 09/27/2022 OK


    # FIND THE PATH TO MODELS
    if from_user is True and _PATH_PRIVATE_MODELS is not None:
        path_models = _PATH_PRIVATE_MODELS
    else:
        path_models = _PATH_MODELS


    _df= {}
    _dfr = {}
    ERROR=[]
    for root, dir, files in os.walk(path_models):
        if (_MODEL_FOLDER_HIDDEN not in root and root.split("\\")[-1][0]!='_') :
            for ff in files :
                if ff.startswith(_MODEL_NAME_CONVENTION) and ff.endswith('.py'):

                    # IF THERE IS ALREADY A MODEL WITH THE SAME NAME
                    if ff[len(_MODEL_NAME_CONVENTION):ff.index('.py')] in _dfr.keys():
                        ERROR.append([_dfr[ff[len(_MODEL_NAME_CONVENTION):ff.index('.py')]],
                                      os.path.join(root,ff[:-3])])

                    _df[os.path.join(root,ff[:-3])]= ff[len(_MODEL_NAME_CONVENTION):ff.index('.py')]
                    _dfr[ ff[len(_MODEL_NAME_CONVENTION):ff.index('.py')]]=os.path.join(root,ff[:-3])
    if ERROR:
        for f in ERROR : print(f)
        raise Exception(f'You have at leas two models with the same name !')



    # CREATE A DICTIONNARY CONTAINING EVERYTHING THEY HAVE
    _DMODEL = {}
    for k0, v0 in _df.items():
        try :
            pfe = os.path.join(path_models, k0 + '.py')
            spec = importlib.util.spec_from_file_location(k0, pfe)
            foo = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(foo)
            _DMODEL[v0] = {
                'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
                'file': foo.__file__,
                'description': foo.__doc__,
                'presets': {k0: dict(v0) for k0, v0 in foo._PRESETS.items()},
                'name': v0,
                'address': k0,
            }
        except BaseException as Err:
            print(f'Model {v0} could not be loaded from folder {k0} ! \n you might have a commma "," at the end of one of your dictionnaries. Error message :\n {Err}\n')



    return path_models, _DMODEL


# ####################################################
# ####################################################
# Generic function to get the list of available models
# ####################################################

def get_available_models(
    model=None,
    details=_MODELS_SHOWDETAILS,
    returnas=None,
    verb=None,
    from_user=_FROM_USER,
):
    '''
    Check all models available in pygemmes, and gives back the information that are asked.
    With no arguments, it prints everything it can

    Parameters
    ----------
    model : Name of the models you are intereted in
    details : Boolean
    returnas : dict, none, list depending of what you need
    verb : print or not !
    from_user : TYPE, optional
    '''
    # Check 9/27/22
    # -----------------
    # check inputs

    # Load the "models dictionnary"
    path_models, _DMODEL = _get_DMODEL(from_user=from_user)

    # Tranform input into machine-friendly
    if model is None:
        model = sorted(_DMODEL.keys())
    if isinstance(model, str):
        model = [model]
    if returnas is None:
        returnas = False
    if verb is None:
        verb = returnas is False

    # Filter the dictionnary
    dmod = {
        k0: {
            'file': str(_DMODEL[k0]['file']),
            'name': str(_DMODEL[k0]['name']),
            'description': str(_DMODEL[k0]['description']),
            'presets': list(_DMODEL[k0]['presets']),
            'address': _DMODEL[k0]['address']
        }
        for k0, v0 in _DMODEL.items()
        if k0 in model
    }

    if details is None:
        details = len(dmod) == 1

    # THE BIG PRINT
    if verb is True or returnas is str:

        if details is True:
            # detailed message
            msg = "\n".join([
                "\n\n"
                f"{11*'#'}{'#'*len(v0['name'])}{11*'#'}\n"
                f"{10*'#'} {v0['name']} {10*'#'}\n"
                + v0['description']
                + "\n\n"
                + f"####Variables ####:\n"
                + f"#differential variables ({len(_DMODEL[k0]['logics']['differential'])}):\n"
                + "\n".join([
                    f"\t-  {k1} :{(10-len(k1))*' '}{_DFIELDS.get(k1,{}).get('definition','')}"
                    for k1 in _DMODEL[k0]['logics']['differential']])
                + '\n'

                + f"# State Variables ({len(_DMODEL[k0]['logics']['statevar'])}):\n"
                + "\n".join([
                    f"\t-  {k1} :{(10-len(k1))*' '}{_DFIELDS.get(k1,{}).get('definition','')}"
                    for k1 in _DMODEL[k0]['logics']['statevar']])
                + '\n\n'
                + f"#### ADDED Parameters #### ({len(_DMODEL[k0]['logics'].get('parameter',{}))}):\n"
                + "\n".join([
                    f"\t-  {k1} :{(10 - len(k1)) * ' '}{_DFIELDS.get(k1, {}).get('definition', 'unread')}"
                    for k1 in _DMODEL[k0]['logics'].get('parameter',{})])
                + '\n'
                + "\n####"
                + f"presets:\n"
                + "\n".join([
                    f" '{k1}' :"
                    f" {v1['com']}"
                    for k1, v1 in _DMODEL[k0]['presets'].items()
                ])


                + f"\n\nfile: {v0['file']}\n"
                for k0, v0 in dmod.items()
            ])

        else:
            # compact message
            nmax = max([len(v0['name']) for v0 in dmod.values()])
            n2max = max([len(v0['address'][len(_PATH_MODELS)+1:-len(_MODEL_NAME_CONVENTION)-len(v0['name'])-1]) for v0 in dmod.values()])+1
            lstr = [
                f" {v0['address'][len(_PATH_MODELS)+1:-len(_MODEL_NAME_CONVENTION)-len(v0['name'])-1].ljust(n2max)+'| '+v0['name'].ljust(nmax)} | {v0['presets']}"
                for k0, v0 in dmod.items()
            ]
            msg = (
                f"The following models are available from '{path_models}'\n"
                + "\n"+' FOLDER'.ljust(n2max+1)+"| MODEL NAME".ljust(nmax+3)+'| Presets\n'
                + '#'*len("\n"+' FOLDER'.ljust(n2max+1)+"| MODEL NAME".ljust(nmax+3)+'| Presets\n')+'\n'
                + "\n".join(lstr)
            )

        if verb is True:
            print(msg)



    # return
    if returnas is list:
        return model
    elif returnas is dict:
        return dmod
    elif returnas is str:
        return msg


def _printsubgroupe(sub, it):
    # Check 9/27/22
    print(f"{3*it*' '}---- {it*'Sub'}group : {sub[0]} {60*'-'}")
    print(str(sub[1].__doc__.replace('\n        ', '')))

    subsubgroup = [f for f in inspect.getmembers(
        sub[1]) if ('_' in f[0] and '__' not in f[0])]
    for sub2 in subsubgroup:
        _printsubgroupe(sub2, it+1)

    subfunc = [f for f in inspect.getmembers(sub[1]) if '_' not in f[0]]
    col = ['name', 'com', 'function']

    ar2 = [[v[0], v[1]['com'], inspect.getsource(v[1]['func']).split(':')[2].replace('\n', '')
            ] for v in subfunc]

    _utils._get_summary(
        lar=[ar2],
        lcol=[col],
        verb=True,
        returnas=False,
    )

    print('\n')


def get_available_functions():
    '''
    Print the content of the `def_function` file
    '''
    # Check 9/27/22
    Subgroups = [f for f in inspect.getmembers(Funcs) if '_' not in f[0]]

    print(f'found {len(Subgroups)} groups of functions :')
    for sub in Subgroups:
        print(f"-----------------{57*'-'}{len(sub[0])*'-'}")
        it = 0
        _printsubgroupe(sub, it)



def importmodel(name : str,
                from_user=False):
    # FIND THE PATH TO MODELS
    if from_user is True and _PATH_PRIVATE_MODELS is not None:
        path_models = _PATH_PRIVATE_MODELS
    else:
        path_models = _PATH_MODELS

    ### FIND THE ADRESSES
    for root, dir, files in os.walk(path_models):
        if (_MODEL_FOLDER_HIDDEN not in root and root.split("\\")[-1][0]!='_') :
            for ff in files :
                if ff.startswith(_MODEL_NAME_CONVENTION) and ff.endswith('.py'):
                    if ff[len(_MODEL_NAME_CONVENTION):ff.index('.py')]==name:
                        address = os.path.join(root,ff[:-3])
                        break


    pfe = os.path.join(path_models, address + '.py')
    spec = importlib.util.spec_from_file_location(address, pfe)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    return deepcopy({k0: dict(v0) for k0, v0 in foo._LOGICS.items()}),\
           deepcopy({k0: dict(v0) for k0, v0 in foo._PRESETS.items()})



def mergemodel(Recipient,dictoadd,override=True,verb=False):
    '''
    If you mix two models or want to add new auxlliary logics,
    you can merge your two dictionnaries.

    override : true will replace previous fields with new one if conflict such as :
        * another definition with the same type of logic (ODE, statevar)
        * change of logic type (transform a statevar to an ODE)

    Recipient is _LOGICS that you want to fill
    dicttoadd contains the new elements you want
    '''
    #verb=False
    ### Category of the variable in a dict
    keyvars = { k:v.keys() for k,v in Recipient.items() }
    typ= {}
    for k,v in keyvars.items():
        for vv in v :
            typ[vv]=k
    ### Merging dictionnaries
    for category, dic in dictoadd.items(): ### LOOP ON [SECTOR SIZE,ODE,STATEVAR,PARAMETERS]
        for k, v in dic.items(): ### LOOP ON THE FIELDS
            if k in typ.keys(): ### IF FIELD ALREADY EXIST
                if override:
                    if (Recipient[category][k] !=v and verb):
                        print(f'Override {category} variable {k}.\n Previous :{Recipient[category][k]} \n by       :{v}')
                    Recipient[category][k] = v
                if typ[k]!=category :
                    if verb : print(f'Category change for logic of {k} : from {typ[k]} to {category}')
                    del Recipient[typ[k]][k]
                #elif verb : print(f'Keeping old definition {category} variable {k}. Previous :{Recipient[category][k]} \n {v}')
            else: ### IF FIELD DOES NOT
                Recipient[category][k] = v
    return Recipient
