'''
Regroup all get functions in one file. 
Those are the functions that are used to get information about the library in general. They do not modify it
'''

from IPython.display import Markdown  # display, HTML,
from IPython.display import display
import ipywidgets as widgets
import inspect
import pandas as pd
import cloudpickle
import os

from ._core import Hub
from ._plot_class import Plots
from .libraries import _get_DMODEL, Funcs, Operators
from ._core_functions import _utils
from ._toolbox import _printsubgroupe

from .libraries import _DFIELDS
from ._config import config


def get_available_config() -> pd.DataFrame:
    """
    Retrieves the current configuration data.

    config is a module that influence the behavior of the library in general, beyond each model.
    It is displaed as a dataframe, with the following columns:
    * name : name of the parameter
    * type : type of the parameter
    * default : when the user does not specify a value, this is the default value
    * current : the value stored beyond the default value, that you can change with `chm.config.set(key,value)`

    The configuration data includes various settings and parameters that control the behavior of the application. 
    These settings can be modified using the `chm.config.set()` function.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-01
    """
    return config.get('all')


def get_available_saves(path='local',
                        returnas=True):
    """
    Retrieves all chimes saved runs (.chm) files in a specified folder. display them as a list, dictionary or dataframe.
    the function uses the default folder of CHIMES. you can change it with path.

    Parameters
    ----------
    path : str, optional
        The path to the folder to check for .chm files. If 'local', the function uses the default folder of CHIMES. 
        Default is 'local'.
    returnas : type or bool, optional
        The format to return the files in. If list, the function returns a list of file names. If dict or True, the function 
        returns a dictionary where each key is a file name and each value is a dictionary containing the model and description 
        of the file. If any other value, the function returns a DataFrame representation of the dictionary. Default is True.

    Returns
    -------
    list or dic or pandas.DataFrame
        The .chm files in the specified folder, in the specified format.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-01
    """

    _SAVE_FOLDER = config.get_current('_SAVE_FOLDER')
    if path == 'local':
        path = os.path.join(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
            _SAVE_FOLDER)

    content = os.listdir(path)

    files = [f for f in content if f.endswith('.chm')]

    if returnas is list:
        return files
    elif returnas in [dict, True]:
        dic = {}
        for f in files:
            try:
                with open(os.path.join(path, f), 'rb') as r:
                    file = cloudpickle.load(r)
                    dic[f] = {'model': file['hub'].dmodel['name'],
                              'description': file['description']}
            except Exception:
                print(f'Savefile {f} could not be opened !')
        return dic if returnas is dict else pd.DataFrame(dic).transpose()


def get_available_plots() -> pd.DataFrame:
    """
    Retrieves all plot routines along with their docstrings and dependencies. 
    They can be used to visualize the results of a model run.

    This function inspects the 'plots' module and retrieves all functions defined in it. For each function, it retrieves 
    the function's docstring and signature. It then formats this information into a pandas DataFrame and returns it.

    Returns
    -------
    pandas.DataFrame
        A DataFrame where each row represents a function in the 'plots' module and each column represents a property of 
        that function. The 'documentation' column contains the function's docstring, and the 'signature' column contains 
        the function's signature.

    Author
    ------
    Paul Valcke

    Date
    ----
    2023
    """
    print('use chm.get_plot_documentation(plotname) for full docstring')
    return Plots.documentation


def get_plot_documentation(plotname: str) -> None:
    '''
    Gives the Markdown description located in the plot file
    '''
    if plotname not in Plots.documentation.index:
        raise Exception(f'Plot {plotname} not found in the library! \n Available plots are {list(Plots.documentation.index)}')

    help(getattr(Plots, plotname))
    # return (getattr(Plots, plotname).__doc__)


def get_available_fields(exploreModels=config.get_current('_FIELDS_EXPLOREMODEL')) -> pd.DataFrame:
    """
    Retrieves all fields in CHIMES along with their units, default values, and additional information.
    Fields are quantities that can be used in models.

    This function loads the library of fields and, if exploreModels is True, all fields defined inside each available model. 
    It returns a DataFrame with the units, default value, and information from the library for each field. If a field is 
    defined in a model, the model's name is added to the 'inmodel' list for that field.

    Parameters
    ----------
    exploreModels : bool, optional
        Whether to explore all available models. If True, the function will explore all models and add any fields defined 
        in a model to the 'inmodel' list for that field. Default is _FIELDS_EXPLOREMODEL.

    Returns
    -------
    modeldf : pandas.DataFrame
        A DataFrame where each row represents a field and each column represents a property of the field. The 'In model' 
        column contains a list of models in which the field is defined.

    Author
    ------
    Paul Valcke

    Date
    ----
    2023
    """

    # Initialize
    dfields_sub = _DFIELDS.copy()
    for key, val in dfields_sub.items():
        dfields_sub[key]['inmodel'] = []
    models = get_available_models(Return=list)

    if exploreModels:
        fieldsnotinDfields = []
        for model in models:
            try:
                hub = Hub(model, verb=False)
                params = hub.get_dfields(returnas=dict)
                for key in params.keys():
                    if key in dfields_sub:
                        dfields_sub[key]['inmodel'].append(model)
                    else:
                        fieldsnotinDfields.append([key.ljust(20), model])
            except Exception as E:
                print(f'ISSUE WITH MODEL : {model} \n {E}')

    print(f'{len(dfields_sub)} fields in the library \n')

    dic = {k0: {
        'definition': v0['definition'],
        'group': v0['group'],
        'value': v0['value'],
        'units': v0['units'],
        'In model': str(v0['inmodel'])}
        for k0, v0 in dfields_sub.items() if v0['group'] != 'Numerical'}
    modeldf = pd.DataFrame(dic)
    return modeldf.transpose()


def get_available_models(
        Return=True,
        FULL=False,
        hide_underscore=True) -> pd.DataFrame:
    """
    Retrieves all available models along with their properties.

    This function loads the dictionary of models and retrieves the properties of each model. It can return the models as a 
    list, dictionary, or DataFrame. If FULL is True, the function returns all properties of the models. If hide_underscore 
    is True, the function excludes models with names like _model__NAME.py.

    Parameters
    ----------
    Return : bool or type, optional
        The format to return the models in. If list, the function returns a list of model names. If dict, the function 
        returns a dictionary of models and their properties. If any other value, the function returns a DataFrame 
        representation of the dictionary. Default is True.
    FULL : bool, optional
        Whether to return all properties of the models. If True, the function returns all properties. Default is False.
    hide_underscore : bool, optional
        Whether to exclude models with names like _model__NAME.py. If True, the function excludes these models. 
        Default is True.

    Returns
    -------
    models : list or dict or pandas.DataFrame
        The models and their properties, in the specified format.

    Author
    ------
    Paul Valcke

    Date
    ----
    2023
    """

    model_name_convention = config.get_current('_MODEL_NAME_CONVENTION')
    _LOCAL_MODEL = config.get_current('_LOCAL_MODEL')
    # Load the "models dictionnary"
    _DMODEL = _get_DMODEL()

    # Tranform input into machine-friendly
    model = sorted(_DMODEL.keys())
    if Return is list:
        return model

    # Filter the dictionnary
    dmod = {
        k0: {
            'file': str(_DMODEL[k0]['file']),
            'name': str(_DMODEL[k0]['name']),
            'description': str(_DMODEL[k0]['description']),
            'presets': list(_DMODEL[k0]['presets']),
            'address': _DMODEL[k0]['address'],
            'Keywords': _DMODEL[k0]['Keywords'],
        }
        for k0, v0 in _DMODEL.items()
        if k0 in model
    }

    # Address management, local and nonlocal
    for k, v in dmod.items():
        if v['address'].startswith(config.get_current('_PATH_MODELS')):
            v['local'] = False
            v['Folder'] = v['address'][len(config.get_current('_PATH_MODELS')) + 1:-len(model_name_convention) - len(v['name']) - 1]
        else:
            v['local'] = True
            v['Folder'] = v['address'][len(_LOCAL_MODEL) + 1:-len(model_name_convention) - len(v['name']) - 1]

    dic = {v0['name']: {'Folder': v0['Folder'],
                        'Short Documentation': v0['description'],
                        'Keywords': v0['Keywords'],
                        'Preset': v0['presets'],
                        'Local file': v0['local'], } for k0, v0 in dmod.items()
           }
    if FULL:
        dic = _DMODEL
    if hide_underscore:
        dic = {k: v for k, v in dic.items() if '__' not in k}
    modeldf = pd.DataFrame(dic)

    # format
    if Return is dict:
        return dic
    else:
        return modeldf.transpose()


def get_available_functions():
    '''
    Print the content of the `def_function` file 

    Note
    ----
    This is an old function, that should be restructured to be more readable.

    Author
    ------
    Paul Valcke

    Date
    ----
    2022
    '''
    # Check 9/27/22
    data = []
    # Iterate over the Funcs class attributes
    for category_name, category_class in Funcs.__dict__.items():
        if isinstance(category_class, type):
            # Iterate over the nested dictionaries inside the class
            for key, value in category_class.__dict__.items():
                if isinstance(value, dict):
                    data.append({'key': key, 'category': category_name, 'func': value.get('func', ''), 'comment': value.get('com', '')})
    dt = {}
    for d in data:
        dt[d['key']] = {'category': d['category'], 'func': inspect.getsource(d['func']).split(':')[2].replace('\n', ''), 'comment': d['comment']}
    df = pd.DataFrame(dt)
    return df.transpose()


def get_available_operators() -> pd.DataFrame:
    """
    Retrieves all non-trivial operators from the Operators module.

    This function inspects the Operators module and retrieves all functions defined in it that do not have a name starting 
    with '__'. For each function, it retrieves the function's docstring and the expression it returns. It then formats this 
    information into a pandas DataFrame and returns it.

    Author
    ------
    Paul Valcke

    Date
    ----
    2023
    """
    dict = {F[0]: {'documentation': F[1].__doc__, 'function': inspect.getsource(F[1]).split('return')[1][:-1]} for F in inspect.getmembers(Operators) if '__' not in F[0]}
    return pd.DataFrame(dict).transpose()


def get_model_documentation(model: str) -> None:
    '''
    Gives the Markdown description located in the model file
    '''

    df = get_available_models(FULL=True)
    try:
        mess = '## Model: ' + df.loc[model].loc['name']
    except BaseException as E:
        modellist = "".join(['* ' + str(f) + "\n" for f in list(get_available_models(Return=list))])
        msg = f"""Your model {model} cannot be found!
Available models are {modellist}."""
        print(msg)
        raise Exception(msg)

    hub0 = Hub(model, verb=False)
    f = widgets.Output()
    with f:
        txt = f'''
* **Creation** : {str(df.loc[model].loc['date'])}
* **Coder**    : {str(df.loc[model].loc['Coder'])}
* **Article**  : {str(df.loc[model].loc['article'])}
* **Keywords** : {str(df.loc[model].loc['Keywords'])}'''
        display(Markdown('## Model: ' + df.loc[model].loc['name']))
        display(Markdown(txt))

        display(Markdown(df.loc[model].loc['longDescription']))

        display(Markdown('### Presets'))
        display(hub0.get_presets())

        display(Markdown('### Supplements'))
        d0 = {}
        for k, v in hub0.supplements.items():
            try:
                d0[k] = {'documentation': v.__doc__,
                         'signature': inspect.signature(v)}
            except BaseException:
                try:
                    d0[k] = {'documentation': v.__doc__,
                             'signature': f'type: {help(v)}'}
                except BaseException:
                    d0[k] = {'documentation': type(v),
                             'signature': 'no signature'}
        display(pd.DataFrame(d0).transpose().style.set_properties(**{'text-align': 'left'}))

        display(Markdown('### Todo'))
        lis = df.loc[model].loc['Todo']
        l2 = ''
        for l in lis:
            l2 += '* ' + l + '\n'
        display(Markdown(l2))

        display(Markdown('### Equations'))
        d = hub0.get_new_summary()
        keys_to_exclude = ['Tsim', 'Tini', 'dt', 'nx', 'nr', 'Nprod', '__ONE__', 'time', 'nt']
        df = pd.DataFrame(d['Field Basic Properties'])[['eqtype', 'definition', 'source_exp', 'com']]
        display(df[~df.index.isin(keys_to_exclude)].style.set_properties(**{'text-align': 'left'}))

    return f
