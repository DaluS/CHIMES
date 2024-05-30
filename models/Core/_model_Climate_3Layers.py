
'''This is a 3-Layer CLimate model, that gives temperature anomaly.'''

import copy
from chimes.libraries import Funcs, importmodel, merge_model
from chimes.libraries import Operators as O
import numpy as np
_DESCRIPTION = """
## Description

A 3-Layer climate model, with a simple atmosphere, an upper ocean and a lower ocean.
There are two temperature variables, one for the atmosphere and one for the ocean.
The model is not spatial, and the temperature is given as an anomaly, not an absolute value.

From the concentration in the atmosphere is deduced radiative forcing, which is the difference between the incoming and outgoing radiation.
From the forcing is deduced the temperature variation

Emission should be given in GtC/year, when not plugged to anything the emissions are in an exponential decay.

## Why is it interesting? 

This is too rough of a model to be used for anything quantititative, but it is a nice illustration of the carbon cycle. 
It shows that carbon is causing temperature variation, and that carbon is slowly moving from the atmosphere to the ocean. 
This phenomena has however some delays, and the temperature is not following the concentration in the atmosphere.

Importantly, if one stops the emissions (apart from specific scenarios), the temperature will quickly stabilize. 
The concentration however will slowly moves toward the ocean until the chemical potential of the ocean is equal to the one of the atmosphere.

## Expected behavior

Emissions are first entering in the atmosphere, then upper ocean and eventually lower ocean.
When a dirac of emission is sent to the system, it will take time for temperature to reach its equilibrium, same for the concentration in the atmosphere.

## What is important to remember

This model is not spatial. 
The output is the temperature anomaly, not the temperature itself.
"""

_TODO = ['Better models !']
_ARTICLE = " "
_DATE = "2021"
_CODER = "Paul Valcke"
_KEYWORDS = ['Climate', 'Module', 'Emission', 'Temperature']


# ######################## PRELIMINARY ELEMENTS #########################

# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        # ATMOSPHERE ODE
        'CO2AT': Funcs.Atmosphere.Three_LayersCO2AT,
        'CO2UP': Funcs.Atmosphere.Three_LayersCO2UP,
        'CO2LO': Funcs.Atmosphere.Three_LayersCO2LO,
        'T': Funcs.Atmosphere.Three_LayersT,
        'T0': Funcs.Atmosphere.Three_LayersT0,
    },
    'statevar': {
        'F': Funcs.Atmosphere.F,
        'Emission': {
            'func': lambda Emission0, deltaEmission, time: Emission0 * np.exp(-time * deltaEmission),
            'com': 'CO2 Emission rate ',
        },
    },
    'parameter': {},
    'size': {},
}


def prepare_sankey(hub) -> dict:
    """
    Prepare the Sankey Diagram for carbon flows. Return as a dict that you can send directly into Sankey
    """
    R = hub.dvalues(params=True)
    title = 'Carbon exchanges in a 3-Layer climate model'
    Units = ""
    Scale = ((1. / 3.666) * R['Emission'])
    Scale /= Scale[0]
    nodes = {k: i for i, k in enumerate([
        'Atmosphere',
        'Upper Ocean',
        'Lower Ocean',
        'Society',])}

    Links0 = [
        ['Emissions',        (1. / 3.666) * R['Emission'], nodes['Society'], nodes['Atmosphere'], 11],
        ['Atmosphere to Ocean', R['phi12']*R['CO2AT']-R['CO2UP']*(R['phi12']*R['CAT']/R['CUP']), nodes['Atmosphere'], nodes['Upper Ocean'], 7],
        ['Ocean stockage',  R['CO2UP']*R['phi23']+R['phi23']*R['CUP']/R['CLO']*R['CO2LO'], nodes['Upper Ocean'], nodes['Lower Ocean'], 2],
    ]
    return ({'title': title, 'Units': Units, 'Scale': Scale, 'nodes': nodes, 'Links0': Links0, 'time': R['time']})


_SUPPLEMENTS = {'prepare_sankey': prepare_sankey}

# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
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
            'Capacity': 1 / 0.098,
            'Capacity0': 3.52,
            'rhoAtmo': 3.681 / 3.1,
            'gammaAtmo': 0.0176,
            'T': 1,
            'T0': 0,
        },
        'com': ' Default run',
        'plots': {'nyaxis': [dict(y=[['CO2AT', 'CO2UP', 'CO2LO'],
                                     ['Emission'],
                                     ['T0', 'T']
                                     ],
                                  title='Carbon exchanges in a 3-Layer climate model'
                                  )
                             ]
                  },
    },
}

_PRESETS['dirac'] = copy.deepcopy(_PRESETS['default'])
_PRESETS['dirac']['com'] = 'A very intense emission at t=0 (x10 the default run), rapidly diminshing (10x the default run).'
_PRESETS['dirac']['fields']['Emission0'] *= 100
_PRESETS['dirac']['fields']['deltaEmission'] *= 100
