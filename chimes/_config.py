"""
_config : default configuration and configuration handler for user modifications

In this file is declared the class that is handling the configuration. 
Both the default values and the definitions.
User should not modify this file but they can use chimes to do modify the configuration values

Author
------
Initial implementation: Weiye Zhu
Design, documentation: Paul Valcke 

Last Update
-----------
2024-01-22
"""

import os
# import cloudpickle
import yaml
import pandas as pd
import numpy as np
from typing import Union, List, Optional, Any, Dict
import importlib

_PATH_HERE = os.path.dirname(__file__)
# DEFAULT CONFIGURATION VALUES AND THEIR DEFINITION
_DEFAULT_CONFIG = dict(
    _VERB=dict(  # PASSED
        definition='Default verbose for all function',
        default=True
    ),
    __PRINTINTRO=dict(  # PASSED
        definition='When importing the library, show a welcome message',
        default=False,
    ),
    _FIELDS_EXPLOREMODEL=dict(  # PASSED
        definition='Flag for `chm.get_available_fields. If True, CHIMES is loading each model to track locally defined fields',
        default=False,
    ),
    _FROM_USER=dict(  # PASSED
        definition='',
        default=False,
    ),
    _MODEL_NAME_CONVENTION=dict(  # PASSED
        definition='',
        default='_model_',
    ),
    _MODEL_FOLDER_HIDDEN=dict(  # PASSED
        definition='',
        default='Hidden',
    ),
    _SAVE_FOLDER=dict(  # PASSED
        definition='Where files are saved',
        default='saves',
    ),
    _DMODEL_KEYS=dict(  # PASSED
        definition='',
        default={'logics': dict, 'presets': dict, 'file': str, 'description': str, 'name': str},
    ),
    _LTYPES=dict(  # PASSED
        definition='',
        default=[int, float],
    ),
    _LTYPES_ARRAY=dict(  # PASSED
        definition='',
        default=[list, tuple],
    ),
    _LEQTYPES=dict(  # PASSED
        definition='Type of equations understood in model file _LOGICS',
        default=['differential', 'statevar', 'parameter', 'size'],
    ),
    _SOLVER=dict(  # PASSED
        definition='Solver used for time resolution',
        default='rk4',
    ),
    _LEXTRAKEYS=dict(  # PASSED
        definition='Added properties that can be found in dfields',
        default=['func', 'kargs', 'args', 'initial', 'source_exp', 'isneeded', 'analysis', 'size'],
    ),
    _LOCAL_MODEL=dict(  # PASSED
        definition='Path toward your local models not from the library',
        default=None,
    ),
    _PATH_HERE=dict(  # PASSED
        definition='Path toward chimes',
        default=os.path.dirname(__file__),
    ),
    _PATH_USER_HOME=dict(  # PASSED
        definition='Local adress when useful',
        default=os.path.expanduser('~'),
    ),
    _PATH_PRIVATE_MODELS=dict(
        definition='Folder that contains your models.',
        default=None,
    ),
    _PATH_MODELS=dict(
        definition='CHIMES folder that contains the models.',
        default=os.path.join(os.path.dirname(_PATH_HERE), 'models'),
    ),
    _DEFAULTSIZE=dict(  # PASSED
        definition='Field name that is used to signify monosectoral',
        default='__ONE__',
    ),
    __DEFAULTFIELDS=dict(  # PASSED
        definition='Automatic filling of fields when the information is not given',
        default={
            'value': {  # Initial values
                'default': None,
                'type': (int, float, np.int_, np.float_, np.ndarray, list),
                'allowed': None,
            },
            'definition': {  # Description of the field
                'default': '',
                'type': str,
                'allowed': None,
            },
            'com': {  # Comment of the field
                'default': '',
                'type': str,
                'allowed': None,
            },
            'units': {  # Field unit
                'default': 'undefined',
                'type': str,
                'allowed': [
                    # Any physical quantity of something (capital, ressources...)
                    'Units',
                    'y',       # Time
                    '$',       # Money
                    'C',       # Carbon Concentration
                    'Tc',      # Temperature (Celsius)
                    'Humans',  # Population
                    'W',       # Energy
                    'L',       # Length
                    '',        # Dimensionless
                ],
            },
            'minmax': {  # Sliders autofilling
                'default': [0, 1],
                'type': list,
                'allowed': None},
            'symbol': {  # Latex symbol
                'default': '',
                'type': str,
                'allowed': None,
            },
            'group': {  # Classification
                'default': '',
                'type': str,
                'allowed': None,
            },
            'multisect': {  # Flag that precise if multisectoral or not
                'default': '',
                'type': str,
                'allowed': None,
            },
            'size': {  # Default size
                'default': ['__ONE__', '__ONE__'],
                'type': list,
                'allowed': None
            }
        }
    )
)


class Config:
    '''
    Config class
    Contains global values that configure CHIMES itself. 
    The default values and definition are stored in the init.
    The methods for users are: 
        * get: return a DataFrame with the config values and properties
        * set: change the configuration
        * reset: reset the configuration to its default values.

    Author
    ------
    Weiye Zhu: initial push
    Paul Valcke: added functionality and documentation

    Date
    ----
    2024/01/22
    '''

    def __init__(self):
        # Default configuration values
        self._default_config_data = _DEFAULT_CONFIG

        # Add the default types
        for k, v in self._default_config_data.items():
            if 'type' not in v.keys():
                v['type'] = type(v['default'])
            v['current'] = v['default']
        self._config_data = self._load_user_config()

    def read_local_config(self):
        '''
        Read the modifications done on the config file
        '''
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")

        if os.path.exists(config_file):
            with open(config_file, "rb") as file:
                print('##############')
                print(config_file)
                print('##############')
                user_config = yaml.safe_load(file)
                print(user_config if user_config else 'Empty or invalid YAML file.')
        else:
            print('No config file found !')

    def interpret_type(type_str):
        """
        Converts a fully qualified type name (e.g., 'builtins.str') into a type object.

        Parameters:
        - type_str: A string representing the fully qualified name of a type.

        Returns:
        - The type object corresponding to the given type name.
        """
        module_name, _, type_name = type_str.rpartition('.')
        if not module_name:  # Handle built-in types
            module_name = 'builtins'
        module = importlib.import_module(module_name)
        return getattr(module, type_name)

    def _load_user_config(self):
        config_data = self._default_config_data.copy()
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")

        try:
            if os.path.exists(config_file):
                with open(config_file, "r") as file:
                    # Using yaml.load() with Loader=yaml.FullLoader for better safety
                    user_config = yaml.load(file, Loader=yaml.FullLoader)
                    for key, value in user_config.items():
                        if key in config_data:
                            config_data[key]['current'] = value
        except EOFError:
            self.reset()

        return config_data

    def get_current(self, key):
        """
        return the current value for the key 
        """
        return self._config_data[key]['current']

    def get(self, key: Union[str, List[str]] = 'all') -> pd.DataFrame:
        """
        Return a DataFrame with the configuration data to inspect the current state.

        Parameters
        ----------
        key : str or list of str, optional, default: 'all'
            If specified:
            - If a string, return information for the specified configuration key.
            - If a list of strings, return information for the specified configuration keys.
            If 'all', return information for all configuration keys. Defaults to 'all'.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing information about the configuration keys, including current values,
            definitions, defaults, and types.

        Raises
        ------
        KeyError
            If any of the specified keys are not found in the configuration data.

        Notes
        -----
        - If `key` is specified, the returned DataFrame will include information only for the specified key(s).
        - If `key` is 'all', the DataFrame will include information for all configuration keys.

        Examples
        --------
        # Get information for all configuration keys
        get()

        # Get information for a specific key
        get('verbose')

        # Get information for multiple keys
        get(['verbose', 'solver'])

        """
        config_items = []
        for k, v in self._config_data.items():
            current_val_repr = repr(v['current'])
            default_val_repr = repr(v['default'])
            is_modified = current_val_repr != default_val_repr
            type_str = v['type'].__name__  # Get the name of the type
            config_items.append({
                'key': k,
                'current': current_val_repr,
                'default': default_val_repr,
                'type': type_str,
                'definition': v['definition'],
                'modified': is_modified
            })

        config_df = pd.DataFrame(config_items)

        if key == 'all':
            return config_df
        elif isinstance(key, str):
            return config_df[config_df['key'] == key]
        elif isinstance(key, list):
            return config_df[config_df['key'].isin(key)]
        else:
            raise TypeError(f"Invalid type for 'key': {key}. Expected str, list of str, or 'all'.")

    def set_value(self, key: Union[str, List[str], Dict[str, Any]],
                  value: Optional[Union[Any, List[Any]]] = False,
                  _force_type: bool = False):
        """
        Assign a new value for the specified configuration key(s).

        The new value is locally stored in `config.json` and does not need to be set at every library import.

        Parameters
        ----------
        key : str, list of str, or dict
            The configuration key(s) to be setd. Can be a single key (str),
            a list of keys, or a dictionary of key-value pairs.

        value : any or list of any, optional, default: False
            The value(s) to assign to the specified key(s). If updating a single key,
            `value` can be a single value. If updating multiple keys, it should be a list
            with the same length as the `key` list. Defaults to False.

        _force_type : bool, optional, default: False
            If True, type checking will be bypassed. Use only if you are certain about the input types.

        Raises
        ------
        Exception
            If the input lengths are inconsistent.

        TypeError
            If the assigned value does not match the expected type for the specified key.

        KeyError
            If the specified key is not found in the configuration data.

        Notes
        -----
        - If updating multiple keys, `key` and `value` should be lists of the same length.
        - If updating a single key, `value` can be a single value.

        Examples
        --------
        # Update a single key
        set('verbose', True)

        # Update multiple keys
        set(['verbose', 'solver'], [False, 'rk4'])

        # Update using a dictionary
        set({'verbose': False, 'solver': 'rk4'})

        # Bypass type checking (use with caution)
        set('key', 'value', _force_type=True)

        Author
        ------
        Weiye Zhu: initial push
        Paul Valcke: added functionnality and documentation

        Date
        ----
        2024/01/22
        """

        if isinstance(key, str):
            keyslist = [key]
            valueslist = [value]
        elif isinstance(key, dict):
            keyslist = list(key.keys())
            valueslist = list(key.values())
        else:
            keyslist = key
            valueslist = value

        # Sanity check: length
        if len(keyslist) != len(valueslist):
            raise Exception(f'Your input seems inconsistent in length: {key} and {value}')

        # Applying the value
        for key, value in zip(keyslist, valueslist):
            if key in self._config_data:
                expected_type = type(self._config_data[key]['default'])  # Assuming 'type' key holds the default value's type
                if _force_type or isinstance(value, expected_type):
                    self._config_data[key]['current'] = value
                else:
                    raise TypeError(f"Expected type {expected_type.__name__} for {key}, got {type(value).__name__}")
            else:
                raise KeyError(f"Config key {key} not found. keys available: {list(self._config_data.keys())}")

        # Saving the updated configuration
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")  # Adjust to save as YAML
        with open(config_file, "w") as file:  # Open file in write mode
            yaml_config = {k: self._to_yaml_friendly(v['current']) for k, v in self._config_data.items()}
            # Inside set_value, right before yaml.safe_dump
            print("YAML Config to be saved:", yaml_config)
            yaml.safe_dump(yaml_config, file, default_flow_style=False)

    def _to_yaml_friendly(self, value):
        if isinstance(value, type):
            # Simply return the type's name as a string
            return value.__name__
        elif isinstance(value, dict):
            return {k: self._to_yaml_friendly(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            return [self._to_yaml_friendly(v) for v in value]
        else:
            return value

    def reset(self, key: Optional[Union[str, None, list]] = None):
        """
        Reset the configuration to its default values.

        Parameters
        ----------
        key : str, list of str, or None, optional, default: None
            If specified:
            - If a string, reset only the specified configuration key to its default value.
            - If a list of strings, reset all specified configuration keys to their default values.
            If 'all', reset all configuration keys to their default values. If None, reset
            all configuration keys to their defaults. Defaults to None.

        Raises
        ------
        KeyError
            If any of the specified keys are not found in the configuration data.
        TypeError
            If an invalid type is provided for the 'key' parameter.

        Notes
        -----
        - If `key` is specified, only those keys (or all keys if 'all') will be reset.
        - If `key` is None, all configuration keys will be reset to their default values.

        Examples
        --------
        # Reset all configuration keys to defaults
        reset()

        # Reset a specific key to its default value
        reset('verbose')

        # Reset multiple keys to defaults
        reset(['verbose', 'solver'])

        # Reset all keys to defaults
        reset('all')

        Author
        ------
        Weiye Zhu: initial push
        Paul Valcke: added functionnality and documentation

        Date
        ----
        2024/01/22
        """
        if key is None or key == 'all':
            # Reset all configuration to defaults
            for k in self._config_data:
                self._config_data[k]['current'] = self._default_config_data[k]['default']
        elif isinstance(key, str):
            # Reset a specific configuration key to its default
            if key in self._config_data:
                self._config_data[key]['current'] = self._default_config_data[key]['default']
            else:
                raise KeyError(f"Config key {key} not found.")
        elif isinstance(key, list):
            # Reset a list of configuration keys to their defaults
            for single_key in key:
                if single_key in self._config_data:
                    self._config_data[single_key]['current'] = self._default_config_data[single_key]['default']
                else:
                    raise KeyError(f"Config key {single_key} not found.")
        else:
            raise TypeError("Invalid type for 'key'. Expected str, list of str, or None.")

        # Save the updated configuration to the YAML file
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
        with open(config_file, "w") as file:  # Open file in write mode
            yaml_config = {k: v['current'] for k, v in self._config_data.items()}
            yaml.dump(yaml_config, file)  # Dump the updated configuration as YAML

    def _reset_single_key(self, key: str):
        if key in self._config_data:
            self._config_data[key]['current'] = self._config_data[key]['default']
        else:
            raise KeyError(f"Config key {key} not found.")

    def __repr__(self):
        return 'CHIMES CONFIGURATION FILES. use .get() for values'


config = Config()

# def _to_yaml_friendly(self, value):
#     if isinstance(value, (dict, list, tuple, set, str, int, float, bool)):
#         if isinstance(value, dict):
#             return {k: self._to_yaml_friendly(v) for k, v in value.items()}
#         elif isinstance(value, (list, tuple, set)):
#             return [self._to_yaml_friendly(v) for v in value]
#         else:
#             return value
#     elif isinstance(value, type):
#         # Convert type object to its name as a string
#         return f"{value.__module__}.{value.__name__}"
#     else:
#         # Fallback for other types: convert to string
#         return str(value)

# def _load_user_config(self):
#     config_data = self._default_config_data.copy()
#     config_file = os.path.join(os.path.dirname(__file__), "config.yml")

#     try:
#         if os.path.exists(config_file):
#             with open(config_file, "rb") as file:
#                 user_config = yaml.safe_load(file)
#                 for key, value in user_config.items():
#                     if key in config_data:
#                         config_data[key]['current'] = value
#     # except EOFError:
#     #     # Handle empty or invalid file by resetting to default configuration
#     #     with open(config_file, "wb") as file:
#     #         cloudpickle.dump({}, file)
#     #     config_data = self._default_config_data.copy()
#     except EOFError:
#         # Handle empty or invalid file by resetting to default configuration
#         self.reset()

#     return config_data
