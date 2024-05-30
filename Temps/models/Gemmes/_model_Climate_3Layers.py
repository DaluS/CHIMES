
'''This is a 3-Layer CLimate model, that gives temperature anomaly.'''

_DESCRIPTION = """
* **Article :** 
* **Author  :** 
* **Coder   :** Paul Valcke

## Description
It takes carbon emissions as an input, and let them evolves in three layers ( upper ocean, lower ocean, atmosphere)
The atmosphere concentration is driving radiative forcing, changing temperature of atmosphere
Atmosphere is changing its temperature and exchanging energy with ocean

Should be called in an economic model. Typically : 
* Input as "Emission"
* Output as "T"
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np
from chimes._models import Funcs, importmodel,mergemodel
from chimes._models import Operators as O

# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        # ATMOSPHERE ODE
        'CO2AT': Funcs.Atmosphere.Three_Layers.CO2AT,
        'CO2UP': Funcs.Atmosphere.Three_Layers.CO2UP,
        'CO2LO': Funcs.Atmosphere.Three_Layers.CO2LO,
        'T': Funcs.Atmosphere.Three_Layers.T,
        'T0': Funcs.Atmosphere.Three_Layers.T0,
    },
    'statevar': {
        'F': Funcs.Atmosphere.F,
        'Emission': {
            'func': lambda Emission0, deltaEmission, time: Emission0*np.exp(-time*deltaEmission),
            'com': 'CO2 Emission rate ',
        },
    },
    'parameter': {},
    'size': {},
}

_SUPPLEMENTS={}

# ####################### PRESETS #######################################
_PRESETS = {'default': {
    'fields': {
        'Emission0': 38,
        'deltaEmission': 0.01,
        'F2CO2': 3.681,
        'CO2AT': 851,
        'CO2UP': 460,
        'CO2LO': 1740,
        'CUP': 460,
        'CAT': 588,
        'CLO': 1720,
        'phi12': 0.024,
        'phi23': 0.001,
        'Capacity': 1/0.098,
        'Capacity0': 3.52,
        'rhoAtmo': 3.681/3.1,
        'gammaAtmo': 0.0176,
        'T': 1,
        'T0': 0,
    },
    'com': ' Default run',
    'plots': {},
},
}
