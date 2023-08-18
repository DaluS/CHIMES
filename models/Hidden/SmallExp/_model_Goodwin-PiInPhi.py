
'''Goodwin with profit impacting Philips curve'''

_DESCRIPTION="""
DESCRIPTION :

    This is a small modificaiton of Goodwin, with a slightly different wage
    negociation : now the wage increase rate depends of the profit

    $ \dfrac{\partial w}{\partial t}= w \Phi(\lambda) \pi^{z_{\pi}}$

LINKTOARTICLE:

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel

# ######################## LOGICS #######################################
_LOGICS,_PRESETS0,_SUPPLEMENTS_G= importmodel('Goodwin')
# We simply do a few modifications on a previous model : we load it as a basis
_LOGICS['statevar']['phillips']= {
                        'func': lambda phi0,phi1,zpi,employment,pi: -phi0+(pi**zpi)*phi1/(1-employment)**2,
                        'com': 'Philips modified to take into account profit'}
_LOGICS['parameter']['zpi'] = {'value': 0.5,
                           'definition': 'impact of profit in salary negociation'}

# ####################### PRESETS #######################################
_PRESETS = {
    'zpi': {
        'fields': {
            'dt': 0.01,
            'nx':4,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': .5*1.2,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
            'zpi': [0.5, 1, 2, 5]
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'plotnyaxis': [{'x': 'time',
                           'y': [['employment', 'omega'],
                                 ['K'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'XY': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            'XYZ': [{'x': 'employment',
                        'y': 'omega',
                        'z': 'time',
                        'color': 'pi',
                        'idx': 0,
                        'title': ''}],
            'plotbyunits': [],
        },
    },
}
