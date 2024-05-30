# IMPORTATIONS
import os
import importlib

from ._def_fields import _DFIELDS, _complete_DFIELDS
from .functions_library import Funcs
from .operators_library import Operators


# from .._config import _PATH_PRIVATE_MODELS, _PATH_MODELS  # _MODEL_NAME_CONVENTIONl, _MODEL_FOLDER_HIDDEN
# from .._config import _LOCAL_MODEL
from .._config import config
from copy import deepcopy


def _scan_modelfolders(model: str = False,
                       _LOCAL_MODEL: str = None) -> dict:
    '''Scan computer files to find unique model files'''

    model_name_convention = config.get_current('_MODEL_NAME_CONVENTION')
    _MODEL_FOLDER_HIDDEN = config.get_current('_MODEL_FOLDER_HIDDEN')
    _LOCAL_MODEL = config.get_current('_LOCAL_MODEL') if _LOCAL_MODEL is None else _LOCAL_MODEL
    # Scanning folder management
    Folders = [config.get_current('_PATH_MODELS')]
    if _LOCAL_MODEL:
        Folders += [_LOCAL_MODEL]

    # First scan : which files names and where
    _df = {}    # key : adress, value modelname
    _dfr = {}   # key : modelname, value address
    ERROR = []  # contains all errors in library structure
    for fold in Folders:
        for root, dir, files in os.walk(fold):
            if (_MODEL_FOLDER_HIDDEN not in root and root.split("\\")[-1][0] != '_'):
                for ff in [ff for ff in files if (ff.startswith(model_name_convention) and ff.endswith('.py'))]:
                    # IF THERE IS ALREADY A MODEL WITH THE SAME NAME
                    if ff[len(model_name_convention):ff.index('.py')] in _dfr.keys():
                        ERROR.append([_dfr[ff[len(model_name_convention):ff.index('.py')]],
                                      os.path.join(root, ff[:-3])])

                    _df[os.path.join(root, ff[:-3])] = ff[len(model_name_convention):ff.index('.py')]
                    _dfr[ff[len(model_name_convention):ff.index('.py')]] = os.path.join(root, ff[:-3])

    if ERROR:
        for f in ERROR:
            print(f'conflict between : {f[0]} and {f[1]}')
        raise Exception('You have at least two models with the same name !')

    # Special case: only considering one model
    if model not in [False, None]:
        if model not in _dfr.keys():
            text = 'Model files found:\n'
            for f in _df.keys():
                text += _df[f] + (30 - len(_df[f])) * ' ' + '   ' + f + '\n'
            text += f'\nModel:  {model} not found! Did you spelled it correctly ?\n Did you configured your local folder {_LOCAL_MODEL} correctly?'
            raise Exception(text)
        _df = {k: v for k, v in _df.items() if v == model}
    return _df


def _add_model_elements(foo, dic):
    '''Automatically add specified attributes from foo to dic.'''
    attributes = {
        'date': ['_DATE', ''],
        'article': ['_ARTICLE', ''],
        'Coder': ['_CODER', ''],
        'Keywords': ['_KEYWORDS', []],
        'presets': ['_PRESETS', {}],
        'supplements': ['_SUPPLEMENTS', {}],
        'longDescription': ['_DESCRIPTION', foo.__doc__],
        'Units': ['_UNITS', []],
        'Todo': ['_TODO', []],
    }

    for key, attr_name in attributes.items():
        try:
            dic[key] = getattr(foo, attr_name[0])
        except AttributeError:
            dic[key] = attr_name[1]

    return dic


def expandabbreviates(dic):
    # ADD func or value when a field is defined concisely
    for cat, dic1 in dic['logics'].items():
        for k, v in dic1.items():
            if type(v) is not dict:
                if cat == 'parameter':
                    dic['logics'][cat][k] = {'value': v}
                else:
                    dic['logics'][cat][k] = {'func': v}
    return dic


def _get_DMODEL(model: str = None,
                _LOCAL_MODEL: str = None):
    '''Core for model scanning'''

    _LOCAL_MODEL = config.get_current('_LOCAL_MODEL') if _LOCAL_MODEL is None else _LOCAL_MODEL
    # Get each model location
    _df = _scan_modelfolders(model, _LOCAL_MODEL)

    # CREATE A DICTIONNARY CONTAINING EVERYTHING THEY HAVE
    _DMODEL = {}
    for k0, v0 in _df.items():
        pfe = k0 + '.py'  # os.path.join(vo '.py')
        spec = importlib.util.spec_from_file_location(k0, pfe)
        foo = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(foo)
        _DMODEL[v0] = {
            'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
            'file': foo.__file__,
            'description': foo.__doc__,
            'name': v0,
            'address': k0,
        }

        _DMODEL[v0] = _add_model_elements(foo, _DMODEL[v0])
        _DMODEL[v0] = expandabbreviates(_DMODEL[v0])
        _DMODEL[v0] = _detect_sizes(_DMODEL[v0])
        _DMODEL[v0] = _change_categories_names(_DMODEL[v0])
        _DMODEL[v0] = detect_multiple_definitions(_DMODEL[v0])
        _DMODEL[v0] = replace_keys_fields(_DMODEL[v0])
    return _DMODEL


def replace_keys_fields(model):
    """
    For each variables in the model, improve key names if hastly written
    """

    dentrees = {
        'func': ['function', 'f', 'funcs'],
        'initial': ['init', 'ini'],
        'value': ['val'],
        'definition': ['def'],
        'com': ['comment'],
        'units': ['unit', 'Units', 'Unit'],
        'symbol': ['Symbol', 'symb', 'latex']
    }

    for k, v in model['logics'].items():
        for field, dics in v.items():
            for d in dics.keys():
                for inputs, possibilities in dentrees.items():
                    if d in possibilities:
                        print(f'You named your entry {d} for field {field} in category {k}. Please use "{inputs}" instead. Automatic correction, but update your model.')
                        model[k][field][inputs] = model[k][field][d]
                        model[k][field].pop[d]
    return model


def detect_multiple_definitions(model):
    """
    Detect and resolve multiple definitions in the model.

    This function detects if any attribute in the model is defined multiple times
    under different categories. If such duplicates are found, it keeps only one
    instance of each attribute and removes the rest.

    Args:
        model (dict): The model dictionary to process.

    Returns:
        dict: The processed model dictionary with resolved duplicates.

    Note:
        This function helps ensure the integrity of the model by removing duplicate
        definitions and keeping only one instance of each attribute. It prints
        warnings for each duplicate found, indicating the conflicting categories,
        and advises to edit the file directly for resolution.
    """
    vardic = {}
    toremove = []
    for k in model['logics'].keys():
        v = model['logics'][k]
        for key in v.keys():
            if key in vardic.keys():
                print(f'WARNING ON MODEL LOADING: field {key} is both a {vardic[key]} and a {k}. Keeping it as a {vardic[key]}\n You can edit the file directly.')
                toremove.append([k, key])
            else:
                vardic[key] = k
    for t in toremove:
        del model['logics'][t[0]][t[1]]
    return model


def _detect_sizes(model):
    """check if the sizes are consistent with the list of values. If not, correct it.
    """
    for k, v in model['logics'].get('size', {}).items():
        if 'value' not in v.keys():
            v['value'] = len(v['list'])
        elif 'list' not in v.keys():
            v['list'] = [i for i in range(v['value'])]
        else:
            if len(v['list']) != v['value']:
                raise Exception(f'{k} has inconsistent size and list! values')
    return model


def _change_categories_names(model):
    """
    Change the categories names to match the CHIMES conventions.

    Parameters
    ----------
    model : dict
        The model dictionary containing logic categories to be modified.

    Returns
    -------
    dict
        The updated model dictionary with modified logic categories.

    Notes
    -----
    This function iterates over the logic categories in the input model dictionary
    and changes their names to adhere to the CHIMES conventions. Specifically, it
    renames categories such as 'differentials', 'ODEs', 'statevars', and 'parameters'
    to 'differential', 'ODE', 'statevar', and 'parameter' respectively.

    Parameters
    ----------
    model : dict
        The model dictionary containing logic categories to be modified.

    Returns
    -------
    dict
        The updated model dictionary with modified logic categories.
    """
    categories = list(model['logics'].keys())
    poplist = []
    for category in categories:
        if category in ['differential', 'statevar', 'parameter']:
            pass
        elif category in ['differentials', 'ODEs', 'diff']:
            print(f'You named your category {category}. Please use "differential" instead. Automatic correction, but update your model.')
            model['logics']['differential'] = model['logics']
            poplist.append(category)
        elif category in ['statevars', 'state']:
            print(f'You named your category {category}. Please use "statevar" instead. Automatic correction, but update your model.')
            model['logics']['statevar'] = model['logics']
            poplist.append(category)
        elif category in ['parameters', 'param']:
            print(f'You named your category {category}. Please use "parameter" instead. Automatic correction, but update your model.')
            model['logics']['parameter'] = model['logics']
            poplist.append(category)
        elif category in ['size']:
            pass
        else:
            print('Warning: unknown category name', category)
    for p in poplist:
        model['logics'].pop(p)
    return model

# ####################################################
# ####################################################
# Generic function to get the list of available models
# ####################################################


def importmodel(name: str,
                from_user=False):
    '''
    Will read a model file and import : _LOGICS, _PRESETS, _SUPPLEMENTS, _DESCRIPTION
    '''

    _PATH_PRIVATE_MODELS = config.get_current('_PATH_PRIVATE_MODELS')

    model_name_convention = config.get_current('_MODEL_NAME_CONVENTION')
    _MODEL_FOLDER_HIDDEN = config.get_current('_MODEL_FOLDER_HIDDEN')
    # FIND THE PATH TO MODELS
    if from_user is True and _PATH_PRIVATE_MODELS not in [None, False]:
        path_models = _PATH_PRIVATE_MODELS
    else:
        path_models = config.get_current('_PATH_MODELS')

    # FIND THE ADRESSES
    for root, dir, files in os.walk(path_models):
        if (_MODEL_FOLDER_HIDDEN not in root and root.split("\\")[-1][0] != '_'):
            for ff in files:
                if ff.startswith(model_name_convention) and ff.endswith('.py'):
                    if ff[len(model_name_convention):ff.index('.py')] == name:
                        address = os.path.join(root, ff[:-3])
                        break

    pfe = os.path.join(path_models, address + '.py')
    spec = importlib.util.spec_from_file_location(address, pfe)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    try:
        supp = {k0: v0 for k0, v0 in foo._SUPPLEMENTS.items()}
    except BaseException:
        supp = {}

    try:
        preset_return = {k0: dict(v0) for k0, v0 in foo._PRESETS.items()}
    except BaseException:
        preset_return = {}

    return deepcopy({k0: dict(v0) for k0, v0 in foo._LOGICS.items()}), \
        deepcopy(preset_return), \
        deepcopy(supp)


def merge_model(recipient, dict_to_add, override=True, verb=False):
    '''
    Merge two models or add new auxiliary logics to an existing model.

    Parameters:
    -----------
    recipient : dict
        The base logic dictionary to which new elements will be added.
    dict_to_add : dict
        Dictionary containing the new elements to be merged into the recipient dictionary.
    override : bool, optional
        If True, replaces previous fields with new ones in case of conflicts. Defaults to True.
    verbose : bool, optional
        If True, prints verbose messages during merging process. Defaults to False.

    Returns:
    --------
    dict
        The updated logic dictionary after merging.

    Notes:
    ------
    This function merges two dictionaries of logic elements, allowing you to combine
    or extend the logic definitions for a model. It supports handling conflicts based on
    priority settings and provides verbose output if requested.

    Example:
    --------
    recipient = {'ODE': {'var1': lambda x: x**2}, 'statevar': {'var2': 0}}
    dict_to_add = {'ODE': {'var3': lambda x: x**3}, 'statevar': {'var2': 1}}
    merged_model = merge_model(recipient, dict_to_add, override=True, verbose=True)
    '''
    for mod in [recipient, dict_to_add]:
        for k1, v1 in mod.items():
            if k1 in ['differentials', 'ODEs', 'diff']:
                print(f'You named your category {k1}. Please use "differential" instead. I will change it for you.')
                mod['differential'] = mod.pop(k1)
            elif k1 in ['statevars', 'state']:
                print(f'You named your category {k1}. Please use "statevar" instead. I will change it for you.')
                mod['statevar'] = mod.pop(k1)
            elif k1 in ['parameters', 'param']:
                print(f'You named your category {k1}. Please use "parameter" instead. I will change it for you.')
                mod['parameter'] = mod.pop(k1)

    # EXPLORING WHAT IS ON THE MODEL WE USE AS A BASE
    typ = {}
    for k, v in {k: v.keys() for k, v in recipient.items()}.items():
        for vv in v:
            typ[vv] = k

    # SAME THING ON THE OTHER DICTIONNARY
    typ2 = {}
    for k, v in {k: v.keys() for k, v in dict_to_add.items()}.items():
        for vv in v:
            typ2[vv] = k

    # MERGING:
    for k, v in typ2.items():
        if k not in typ.keys():
            recipient[typ2[k]][k] = dict_to_add[typ2[k]][k]
            # print(k,'added !')
        else:
            if override:
                if verb:
                    print('Overriding', k)
                del recipient[typ[k]][k]
                recipient[typ2[k]][k] = dict_to_add[typ2[k]][k]
            else:
                print('potential conflict in merge')
                print(f'The variable {k} is already in the system')
                print(f'original definition:\n type :{typ[k]}, function: {recipient[typ[k]][k]}')
                print(f'new : {typ2[k]}, func: {dict_to_add[typ2[k]][k]}')
                print('overrid not activated')

    return recipient


def fill_dimensions(logics, dimensions, dim=None):
    '''Fill in sizes for fields based on dimensionality and complete missing categories.

    Parameters:
    -----------
    logics : dict
        Dictionary containing logic information for variables.
    dimensions : dict
        Dictionary with keys 'scalar', 'vector,'matrix' and corresponding lists of fields.
    dim : dict, optional
        Dictionary with sizes for different dimensions. Defaults to None.

    Returns:
    --------
    dict
        Updated logic dictionary with sizes filled in.

    Notes:
    ------
    This function adds sizes to fields based on dimensionality and completes missing categories if not provided.
    It updates the logic dictionary with size information for variables.

    Example:
    ---------
    dimensions = {
        'scalar': ['r', 'phinull', 'N', 'employmentAGG', 'w0', 'W', 'alpha', 'a0', 'Nprod', 'Phillips', 'rDh', 'gammai', 'n', 'ibasket', 'Dh'],
        'matrix': ['Gamma', 'Xi', 'Mgamma', 'Mxi', 'Minter', 'Minvest', 'MtransactY', 'MtransactI']
    }
    dim = {
        'scalar': ['__ONE__'],
        'vector': ['Nprod'],
        'matrix': ['Nprod', 'Nprod']
    }
    logics = fill_dimensions(logics, dimensions, dim)
    '''

    # Set default dimensions if not provided
    if not dim:
        dim = {
            'scalar': ['__ONE__'],
            'vector': ['Nprod'],
            'matrix': ['Nprod', 'Nprod']
        }

    # Find all variables in the model:
    all_fields = []
    for cat in logics.keys():
        all_fields += list(logics[cat].keys())

    # Complete the missing dimension if less than 3 dimensions provided
    if len(dimensions) < 3:
        missing_dim = [d for d in ['scalar', 'vector', 'matrix'] if d not in dimensions.keys()]
        setlist = set(all_fields)
        for k, v in dimensions.items():
            setlist -= set(v)
        dimensions[missing_dim[0]] = list(setlist)

    # Add sizes to logic dictionary
    added_vars = []
    for category, variables in dimensions.items():
        for cat2, dicts in logics.items():
            for variable, properties in dicts.items():
                if variable in variables:
                    properties['size'] = dim[category]
                    added_vars.append(variable)

    # Complete logic dictionary with missing parameters
    all_vars = [v for sublist in dimensions.values() for v in sublist]
    for var in list(set(all_vars) - set(added_vars)):
        for category, variables in dimensions.items():
            if var in variables:
                logics['parameter'][var] = {'size': dim[category]}

    return logics
