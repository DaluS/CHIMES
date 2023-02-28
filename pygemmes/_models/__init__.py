
# Check December 2022

import os
import importlib

from ._def_fields import _DFIELDS, _complete_DFIELDS
from ._def_functions import Funcs
from ._def_Operators import Operators
from .._utilities import _utils
import inspect

from .._config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS,_MODEL_NAME_CONVENTION,_MODELS_SHOWDETAILS,_MODEL_FOLDER_HIDDEN

from copy import deepcopy
import pandas as pd

# ####################################################
# ####################################################
#       Automatically load all available models
# ####################################################
def _get_DMODEL(model=False,from_user=_FROM_USER):
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
        raise Exception(f'You have at least two models with the same name !')

    if model is not False:
        _df = {k:v for k,v in _df.items() if v == model}

    # CREATE A DICTIONNARY CONTAINING EVERYTHING THEY HAVE
    _DMODEL = {}
    for k0, v0 in _df.items():
        #try :
        pfe = os.path.join(path_models, k0 + '.py')
        spec = importlib.util.spec_from_file_location(k0, pfe)
        foo = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(foo)
        _DMODEL[v0] = {
            'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
            'file': foo.__file__,
            'description': foo.__doc__,
            #'presets': {k0: dict(v0) for k0, v0 in foo._PRESETS.items()},
            'name': v0,
            'address': k0,
        }
        ### ADD Presets 
        try : _DMODEL[v0]['presets']={k0: dict(v0) for k0, v0 in foo._PRESETS.items()}
        except BaseException: _DMODEL[v0]['presets']={}
        ### ADD Supplements
        try :  _DMODEL[v0]['supplements']=foo._SUPPLEMENTS
        except BaseException: _DMODEL[v0]['supplements']={}
    
        ### ADD Long Description 
        try : _DMODEL[v0]['longDescription']= foo._DESCRIPTION
        except BaseException: _DMODEL[v0]['longDescription']= foo.__doc__
        #except BaseException as Err:
        #    print(f'''Model {v0} could not be loaded from folder {k0} ! \n you might have a commma "," at the end of one of your dictionnaries. Error message :\n {Err}\n''')
    return path_models, _DMODEL


# ####################################################
# ####################################################
# Generic function to get the list of available models
# ####################################################

def get_available_model_documentation(model):
    '''
    Gives a more detailed description of the model you are asking for  
    '''
    df = get_available_models(FULL=True) 
    mess = '## Model: '+df.loc[model].loc['name']
    mess+='\n'
    #mess+= df.loc[model].loc['description']    
    mess+=df.loc[model].loc['description']
    mess+='\n'
    mess+=df.loc[model].loc['address']
    mess+='\n'
    if df.loc[model].loc['description'] != df.loc[model].loc['longDescription']:
        mess+=df.loc[model].loc['longDescription']
    mess+='\n'
    mess+='# Presets'
    mess+='\n'
    mess+=str(pd.DataFrame(pd.DataFrame(df.loc[model].loc['presets']).transpose()['com']))
    mess+='\n'
    mess+='# Supplements'
    mess+='\n'
    for k,v in df.loc[model].loc['supplements'].items():
        mess+='    '+str(k)+'\n   '+str(v.__doc__)+' \n\n '
    #mess+= str(df.loc[model].loc['supplements'])
    return mess


def get_available_models(
    model=None,
    details=_MODELS_SHOWDETAILS,
    verb=None,
    from_user=_FROM_USER,
    Return=False, 
    FULL=False
):
    # Check 2022
    '''
    Return all available models with their respective instructions as a dataframe
    if model is None, gives all the model
    if model is not None, gives details of the model
    if details, gives model description
    if FULL, gives all it can

    if Return is dict, gives a dictionnary
    if Return is list, gives the list of model 
    if Return is False, gives dataframe
    '''
    # Load the "models dictionnary"
    path_models, _DMODEL = _get_DMODEL(from_user=from_user)

    # Tranform input into machine-friendly
    if model is None:
        model = sorted(_DMODEL.keys())
    if isinstance(model, str):
        model = [model]
        details=True

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

    ## Choosing what infos is in
    dic={v0['name']: {'Folder': v0['address'][len(_PATH_MODELS)+1:-len(_MODEL_NAME_CONVENTION)-len(v0['name'])-1],
                      'Preset': v0['presets'],}for k0, v0 in dmod.items()}
    if details: 
        dic={v0['name']: {'Folder': v0['address'][len(_PATH_MODELS)+1:-len(_MODEL_NAME_CONVENTION)-len(v0['name'])-1],
                      'Preset': v0['presets'],
                      'Short Documentation': v0['description']}for k0, v0 in dmod.items()}       
    if FULL:
        dic = _DMODEL
    modeldf=pd.DataFrame(dic)

    # format
    if Return is list: 
        return model
    if Return is dict:
        return dic
    else:
        return modeldf.transpose()


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
           deepcopy({k0: dict(v0) for k0, v0 in foo._PRESETS.items()}),\
           deepcopy({k0: dict(v0) for k0, v0 in foo._SUPPLEMENTS.items()})


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



def filldimensions(_LOGICS,Dimensions,DIM=False):
    '''Add sizes to fields (for multisectorality), and can complete a default category.

    * Dimensions : dictionnary with 'scalar','vector,'matrix' and the list of corresponding fields
    * fieldtype

    Dimensions = { 
        'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W',
                'alpha', 'a0', 'Nprod', 'Phillips', 'rDh', 'gammai',
                'n', 'ibasket', 'Dh'],
        'matrix': [ 'Gamma','Xi','Mgamma','Mxi','Minter',
                    'Minvest','MtransactY','MtransactI']
        #'vector': will be deduced by filldimensions 
    }
    DIM= {'scalar':['__ONE__'],
        'vector':['Nprod'],
        'matrix':['Nprod','Nprod']  }

    _LOGICS=filldimensions(Dimensions,'vector',_LOGICS,DIM)
    '''
    
    if not DIM :
        DIM= {'scalar':['__ONE__'],
      'vector':['Nprod'],
      'matrix':['Nprod','Nprod']  }
    
    ### COMPLETING THE MISSING DIMENSION
    if len(list(Dimensions.keys()))<3:
        t1,t2 = list(Dimensions.keys())[0],list(Dimensions.keys())[1]
        t3 = [f for f in ['scalar','vector','matrix'] if f not in Dimensions.keys()][0]
        Allfields = []
        for k0 in _LOGICS.keys(): Allfields.extend([k for k in _LOGICS[k0]])
        Dimensions[t3] = list( set(Allfields)     -
                               set(Dimensions[t1])-
                               set(Dimensions[t2]) )

    
    ### COMPLETING _LOGICS WITH VARIABLES EXISTING INSIDE
    Added = []
    for cat, liste in Dimensions.items():
        for cat2, dicte in _LOGICS.items():
            for var, prop in dicte.items():
                if var in liste:
                    prop['size']=DIM[cat]
                    Added.append(var)
    ### COMPLETING PARAMETERS NOT DEFINED BEFORE IN _LOGICS
    Ds = []
    for V in Dimensions.values():Ds.extend(V)

    for var in list(set(Ds)-set(Added)):
        for cat, liste in Dimensions.items():
            if var in liste :
                #print(var)
                _LOGICS['parameter'][var]={'size':DIM[cat]}

    return _LOGICS

"""
def filldimensions(Dimensions,fieldtype,_LOGICS,DIM):
    '''Add sizes to fields (for multisectorality), and can complete a default category.

    Dimensions = { 
        'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W',
                'alpha', 'a0', 'Nprod', 'Phillips', 'rDh', 'gammai',
                'n', 'ibasket', 'Dh'],
        'matrix': [ 'Gamma','Xi','Mgamma','Mxi','Minter',
                    'Minvest','MtransactY','MtransactI']
        #'vector': will be deduced by filldimensions 
    }
    DIM= {'scalar':['__ONE__'],
        'vector':['Nprod'],
        'matrix':['Nprod','Nprod']  }

    _LOGICS=filldimensions(Dimensions,'vector',_LOGICS,DIM)'''
    
    if fieldtype=='scalar': t1,t2 = ['vector','matrix']
    if fieldtype=='vector': t1,t2 = ['scalar','matrix']
    if fieldtype=='matrix': t1,t2 = ['vector','scalar']

    ### COMPLETING THE MISSING DIMENSION
    Allfields = []
    for k0 in _LOGICS.keys(): Allfields.extend([k for k in _LOGICS[k0]])
    Dimensions[fieldtype] = list( set(Allfields)-
                                  set(Dimensions[t1])-
                                  set(Dimensions[t2]) )

    ### COMPLETING _LOGICS WITH VARIABLES EXISTING INSIDE
    Added = []
    for cat, liste in Dimensions.items():
        for cat2, dicte in _LOGICS.items():
            for var, prop in dicte.items():
                #print(cat,cat2,var)
                if var in liste:
                    prop['size']=DIM[cat]
                    Added.append(var)

    ### COMPLETING PARAMETERS NOT DEFINED BEFORE IN _LOGICS
    Ds = []
    for V in Dimensions.values():Ds.extend(V)
    for var in list(set(Ds)-set(Added)):
        for cat, liste in Dimensions.items():
            if var in liste:
                _LOGICS['parameter'][var]={'size':DIM[cat]}

    return _LOGICS
"""
pass