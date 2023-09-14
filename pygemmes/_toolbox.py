

from ._core import Hub
from ._models import get_available_models  
from ._models import _DFIELDS
from ._utilities import _utils
from . import _plots as plots

import os
import inspect
import pandas as pd
import dill

import matplotlib.pyplot as plt
import numpy as np

from ._config import _FIELDS_EXPLOREMODEL
from ._config import _SAVE_FOLDER
from ._core import Hub
from ._utilities._distribution_generator import *

# FULLY CHECKED SEPTEMBER 2023
# #############################################################################

__all__ = [
    'get_available_fields',
    'get_available_plots',
    'generate_dic_distribution',
    'get_available_saves',
    'load'
]

def get_available_saves(path='local',
                        returnas=True):
    '''
    Check all .chm files in a a folder.
    if path is 'local', the default folder of CHIMES is used
    
    returnas can be list, dic, of True (in that case it's a dataframe)
    if openfile, there is more information than just the names (model, description)
    '''
    if path=='local':
        _PATH_SAVE = os.path.join(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
            _SAVE_FOLDER)
        content = os.listdir(_PATH_SAVE)
    else: 
        content = os.listdir(path)
    
    files = [f for f in content if f[-4:]=='.chm']
    
    if returnas is list:
        return files 
    if returnas in [dict,True]:
        dic= {}
        for f in files:
            with open(os.path.join(_PATH_SAVE,f),'rb') as r:
                file = dill.load(r)
                dic[f]= {'model': file['hub'].dmodel['name'],
                         'description': file['description']}
    if returnas is dict:
        return dic 
    else: 
        return pd.DataFrame(dic).transpose()
        
    print(content)
        
def load(name:str,
         localsave=True,
         verb=True):
    '''
Load a .chm file to create a hub. You can create those files, by creating a hub 
`Hub=chm.Hub(modelname)
 Hub.save(name)`
 
 name if the path to the file. It can be relative, it can be with or without .chm
 verb is a boolean, to get a loaded message or not when load
    '''
    _PATH_SAVE = os.path.join(
                os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
                _SAVE_FOLDER)

    # NAME MANAGEMENT 
    if (name[-4:]!='.chm' and '.' not in name):
        name=name+'.chm'
    if name[-4:]=='.chm':
        pass
    elif '.' in name:
        raise Exception(f"extension not understood :{name.split('.')[1]}, expected .chm or nothing")
     
    # RELATIVE PATH 
    if localsave:
        address = os.path.join(_PATH_SAVE,name)
    else:
        address = name
     
    # LOADING FILE  
    if verb:
        print('loading:', address)   
    with open(address,'rb') as f:
        file = dill.load(f)
        hub = file['hub']
        description=file['description']
        
    # CHECKING INTEGRITY
    fakehub= Hub('__TEMPLATE__',verb=False)
    #if type(hub)!= type(fakehub):
    #    print('File is not a model Hub!',f'type {type(hub)}, expected {type(Hub)}')
    if verb:
        print('file Loaded!')
        print('Description:',description)
    
    return hub

def get_available_plots():
    '''Print all the plots routines with their docstring and dependencies through a dataframe
    '''
    # Check 01 2023

    all_functions = inspect.getmembers(plots, inspect.isfunction)

    dic={i[0]: {'documentation': i[1].__doc__,
                'signature': inspect.signature(i[1])}  for i in all_functions}
    plotdf=pd.DataFrame(dic)
    return plotdf.transpose().style.set_properties(**{'text-align': 'left'})

def get_available_fields(exploreModels=_FIELDS_EXPLOREMODEL):
    '''
    Shows their units, default value and informations from the library.
    Will load the library of fields, then if exploreModels all fields defined inside model.
    Return as a dataframe (typically use pandasgui show to check it out)
    
    * exploreModels (True,False) to explore or not all available models
    '''
    # Check 2023/08/11

    # INITIALIZE
    dparam_sub = _DFIELDS
    for key, val in dparam_sub.items():
        dparam_sub[key]['inmodel'] = []
    models = get_available_models(Return=list,verb=False)

    if exploreModels:
        fieldsnotinDfields = []
        if exploreModels:
            for model in models:
                try:
                    hub = Hub(model, verb=False)
                    params = hub.get_dparam(returnas=dict)
                    for key in params.keys():
                        if key in dparam_sub:
                            if 'inmodel' not in dparam_sub[key].keys():
                                dparam_sub[key]['inmodel'] = []
                            dparam_sub[key]['inmodel'].append(model)
                        else:
                            fieldsnotinDfields.append([key.ljust(20), model])
                except BaseException as E:
                    print(f'ISSUE WITH MODEL : {model} \n {E}')


    print(f'{len(dparam_sub)} fields in the library \n')

    dic = {k0:{
            'definition':v0['definition'], 
            'group':v0['group'],
            'value':v0['value'], 
            'units':v0['units'], 
            'In model': str(v0['inmodel'])}
              for k0, v0 in dparam_sub.items() if v0['group'] != 'Numerical'}
    modeldf=pd.DataFrame(dic)
    return modeldf.transpose()#.style.set_properties(**{'text-align': 'left'})


