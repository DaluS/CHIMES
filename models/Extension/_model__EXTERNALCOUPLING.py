"""Homemade API for external coupling, on a dummy model"""

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O


_DESCRIPTION = """
CHIMES can be coupled with external structures and models, with a simple API. THis is an example

Here we create the API inside the model file, eventually they can be imported separately.
The class structure can be used for various models later.

The class has te following elements: 
1. Flags 
2. a `get_var` method that if required will do a timestep of the external model and give the output
3. a `set_var` that can send information to the external module
4. a `_TrueInit` that will initialize the external model and run it until it's ready for the rest of the system 
5. a `_simulate` that will do internal calculations to the module

To call the class in a CHIMES model, one add a function with the same structure as giveINPUT_getOUTPUT
The sizes nr,nt,nx do not have to be sent in each function, only in the first one that will be executed as they are required for the initialisation.
"""
# ################ IMPORTS ##################################################


# ################ External model Gestion ###########################################
# from [...] import [...] # for the external library to call

class EXTERNAL_API():
    ##################### INITIATION ###############
    def __init__(self):
        '''A fake init to create the object, but not necessarily doing all 
        the long loading (this should be done at the first run iteration, to allow fast loading)
        '''
        self.flags = {
            'ready': False,
            'year': False,
            'dimension': False,
        }

    def _TrueInit(self, year, nx, nr, nt, dt):
        '''Where The library is truely initializing the external library'''

        # INITIALISATION
        self.flags['dimensions'] = {'nx': nx,  # dimensions used by the system
                                    'nt': nt,
                                    'nr': nr}
        self._zero = np.zeros((nx, nr, 1, 1))  # dimension of the output if monosectoral
        self.updatetimestep = dt
        self.value = {}  # In this fake example the values are in this dictionnary

        # IF THE SYSTEM HAS TO RUN BEFORE THE START
        '''Where the initialisation is executed'''
        self.value['output'] = 10
        self.flags['year'] = year

        # Finally the system is ready
        self.ready = True

    ##################### TALKING TO MATTER #########
    def _simulate(self, time):
        '''Run the simulation until year 'time' is reached'''
        if self.flags['year'] <= time + self.updatetimestep:  # if we are in between mater timestep
            self.value['output'] += np.random.normal(size=np.shape(self._zero))  # Fake value, here simply a random choice
        else:
            pass  # could be interpolation or just keeping the actual value

        # Change the flag
        self.flags['year'] = time
        pass

    def set_var(self, varname, value, time):
        '''Send a value to Mater on the channel varname, with the value "value" at time "time"'''
        self.value[varname] = value

    def get_var(self, varname, time):
        '''Ask matter for a variable "varname" at a time "time"'''
        self._simulate(time)
        return self.value[varname]


_EXTERNAL = EXTERNAL_API()


def giveINPUT_getOUTPUT(LocalCalc, time, nx, nr, nt, dt):
    global _EXTERNAL
    """send GDP to the module, get 'output' field"""
    time = time[0, 0, 0, 0]

    # If there has not been any true initialisation
    if not _EXTERNAL.flags['ready']:
        _EXTERNAL._TrueInit(time, nx, nr, nt, dt)

    # Sending new values
    _EXTERNAL.set_var('input', LocalCalc, time)

    # Getting new values
    return _EXTERNAL.get_var('output', time)


################## ALL THE NEW FIELDS LOGICS ###############################
_LOGICS = {'size': {},
           'differential': {'Stock': {'func': lambda Flow: Flow,
                                      'initial': 1}},
           'statevar': {'LocalCalc': lambda time, g: 10*np.exp(g*time),
                        'Flow': giveINPUT_getOUTPUT},
           'parameter': {'g': 0.01}, }


################## ADDING DIMENSIONS TO VARIABLES IF NOT DONE BEFORE #######
'''
Comment the line in 'Dimensions' you want to be filled by default. 
The system does not handle automatically multiple types of matrix/vector dimensions. do it manually
Modify DIM 
'''
Dimensions = {
    # 'scalar': [],
    'matrix': [],
    'vector': [],       #
}
# DIM= {'scalar':['__ONE__'],
#      'vector':['Nprod'],
#      'matrix':['Nprod','Nprod']  }
# _LOGICS=fill_dimensions(_LOGICS,Dimensions,DIM)

################### SUPPLEMENTS IF NEEDED ###################################


def acces_External(_EXTERNAL):
    return _EXTERNAL


_SUPPLEMENTS = {'access_External': acces_External}

################### DEFIMING PRESETS WITH THEIR SUPPLEMENTS #################
_PRESETS = {
    'preset0': {
        'fields': {},
        'com': '',
        'plots': {
            'Var': [{'key': '',
                     'mode': False,  # sensitivity, cycles
                     'log': False,
                     'idx': 0,
                     'Region': 0,
                     'tini': False,
                     'tend': False,
                     'title': ''},
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
