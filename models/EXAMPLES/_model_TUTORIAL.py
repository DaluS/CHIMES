"""Highly commented Template to write your model. This is the short description"""

# THERE ARE ONLY ONE FIELD WHICH IS REQUIRED : _LOGICS.
# The rest is a bonus, with comments!
# It's unnecessarily long, but it should contain all the local operations that can be done in a model
# You can check __MINITEMPLATE__ for the shortest version of the same structure

# %% I userfriendly description The fields directly under are optional
from chimes.libraries import importmodel      # Import another model _LOGICS, _PRESETS
from chimes.libraries import Operators as O   # Prewritten operators for multisectoral and multiregional coupling. `chm.get_available_Operators()`
from chimes.libraries import fill_dimensions   # When using multisectoral dynamics, fill automatically the sizes of fields
from chimes.libraries import merge_model       # Merge two model logics into each others
from chimes.libraries import Funcs            # Prewritten functions from CHIMES use `chm.get_available_Functions()`
import numpy as np                          # if you need exponential, pi, log

_DESCRIPTION = """A longer description in markdown format that explains: 
## What is this model ?
## Why is it interesting ? 
## what is the purpose of your model,
## Expected behavior
how it is constructed, and its expected behavior.
"""
_TODO = ['a list of tasks', 'that should be done']
_ARTICLE = " a link to the published article if existing"
_DATE = " YYYY/MM/DD model file creation"
_CODER = " Name of the coder"
_KEYWORDS = ['a list of relevant elements for classification', 'Documentation', 'Tutorial',]
_UNITS = []  # Optional: Adding accepted units for fields

# %% II.1 Useful imports. They are optional

# %% II.2 Intermediate functions used by "_LOGICS" when using long functions. See their impact below


def pop(N, n):
    N2 = N    # You can do functions with intermediary steps that are not possible using lambda functions
    return N2*n


def progress(a, alpha):
    return a*alpha


# %% III ##### THE ONLY MANDATORY PART: A DICT "_LOGICS" ############################
_LOGICS = dict(
    differential=dict(  # Differential variables are defined by their time derivative and not their value
        p=dict(       # Name of the variable
            func=lambda p, inflation: p*inflation,                  # Logics to link it with another variable
            initial=1,                                               # Initial value if differential
            units='$.Units^{-1}',                                   # Combination of units using latex formalism ^{-1} and .
            definition='nominal value per physical unit produced',  # Explaining what this field is about
            com='inflation driven',                                 # Explaining how the value is calculated
            symbol=r'$\mathcal{P}$',                                 # Latex symbol
            size=['__ONE__', '__ONE__']                             # Dimensions for multisectorality
        ),
        K=lambda K, delta: 0.1*K - delta*K,                          # When prototyping, you can put only the function
        N={'func': pop},                                             # Function can be a lambda function or an externa function
        a=progress,                                                  # Combination of both
    ),
    statevar=dict(  # State variables value are defined by their logic
        w0=lambda p, a, para: np.exp(p/a)*para,                      # They are constructed the same way as differential variables
        # The key 'initial' will not be use
    ),
    parameter=dict(  # Parameters have no logic, only a value
        delta={                                                 # They are constructed the same way as differential
            'value': 0.1                                           # Instead of 'func' and 'initial' they have a 'value'
        },
        para=3,                                                 # If not a dict, it will be interpreted as 'value'
    ),
    size={                                       # Additional tensor dimensions
        'Nprod': {'value': 5,                          # When defined in a
                  'definition': 'Number of sectors'},  # What this dimension is about
    },
)
############################################################################

# %% IV Adding dimensions when multisectoriality (optional)
'''This part will automatically fill the 'size' field of the models without having to write it'''
# Comment the line in 'Dimensions' you want to be filed by default.
# Then put in each other category the fields you want to be a vector, and the fields you want to be a matrix
# Finally, put in DIM the size you want for each field
# By default scalars are not changed : if you want to do something with multiple vectors, do it in two times with different dics

Dimensions = {
    # 'scalar': [],           # Since it is commented, all field will be non-multisectoral by default
    'vector': [],            # Typically vector of agents with same logics type (sector, households, species)
    'matrix': [],            # Correspond to coupling operators between agents
}
DIM = {'scalar': ['__ONE__'],  # Dimension for scalar values
       'vector': ['Nprod'],    # Dimension for vectors
       'matrix': ['Nprod', 'Nprod']}  # Dimension for matrices
# _LOGICS=fill_dimensions(_LOGICS,Dimensions,DIM)

# %% V Importing and merging models (optional)
'''You can import the content of another file model, then do operate to merge files.'''
# logicsgoodwin,presetgoodwin,supplementsgoodwin= importmodel('Goodwin') # Will import locally the content of the model named 'Goodwin'
# _LOGICS = merge_model(_LOGICS, logicsgoodwin, verb=False)     # Takes the equations of _LOGICS_GOODWIN and put them into _LOGICS

# The second model have the priority: if a field is in both, the definition in the second model is kept and the other erased
# Preset and supplement merges have to be done separately

# %% VI Supplements (optional)
""" supplements are an ensemble of functions that are accessible through the hub. 
Typically, plot methods, analysis methods, or method to create some initial conditions"""


def MethodForSupplements(var):
    '''This method can be accessible through hub.supplements'''
    print(f'var is : {var}')


_SUPPLEMENTS = {
    'MethodForSupplements': MethodForSupplements,  # using hub.supplements['MethodForSupplements'](var) to activate
    'plogics': _LOGICS['differential']['p']['func']  # an unorthodox way to get the value of 'p'
}

# %% VII Presets (optional)
""" Presets contains ensemble of determined value you can apply your model on.
It is typically a way to show other users specific cases of the models.
Each preset have a name,
    'fields' that contains all values
    'com' which is a comment on the preset properties
    'plots' which is the kwargs for each plot you want to show when executing the preset
"""
_PRESETS = {
    'preset0': {        # Preset named 'preset0'
        'fields': {
            'p': 1.2,        # p is here a differential: it changes the initial conditon
            'delta': 0,      # delta is a parameter: it changes its value
        },
        'com': 'change p and delta',  # the description of the preset impact. can be long
        'plots': {
            # Each key is a plot accessible in `chm.get_available_plots`
            # This command also give the kwargs you can use to control the plot
            # In this example we just give the full list of kwargs with their defautl values
            'Var': [  # To each name, is associated a list of dictionnaries.
                      # Each dictionnary contains the instruction for one plot
                {
                    # Plot-specific elements
                    'key': 'p',
                    'mode': False,  # sensitivity, cycles
                    'log': False,

                    # Kwargs you will find in any plots
                    'idx':   0,     # Index or name of the parrallel run for plot
                    'Region': 0,     # Index or name of the region plot
                    'tini':  False,  # First time plot value. False gives the minimal
                    'tend':  False,  # Last time plot value. False gives the maximal
                    'title': ''
                },
            ],
            'XY': [{'x': '',
                    'y': '',
                    'color': '',
                    'scaled': False,

                    'idx': 0,
                    'Region': 0,
                    'tini': False,
                    'tend': False,
                    'title': '',
                    },
                   ],
            'XYZ': [{'x': '',
                     'y': '',
                     'z': '',
                     'color': 'time',

                     'idx': 0,
                     'Region': 0,
                     'tini': False,
                     'tend': False,
                     'title': ''},
                    ],
            'cycles_characteristics': [{'xaxis': 'omega',
                                        'yaxis': 'employment',
                                        'ref': 'employment',
                                        'type1': 'frequency',
                                        'normalize': False,
                                        'Region': 0,
                                        'title': ''},
                                       ],
            'byunits': [{'filters_key': (),
                         'filters_units': (),
                         'filters_sector': (),
                         'separate_variables': {},
                         'lw': 1,

                         'idx': 0,
                         'Region': 0,
                         'tini': False,
                         'tend': False,
                         'title': ''}
                        ],
            'nyaxis': [{'y': [[], []],
                        'x': 'time',
                        'idx': 0,
                        'Region': 0,
                        'log': False,  # []
                        'title': '',
                        }
                       ],
        },
    },
}
