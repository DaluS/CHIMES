
'''2-dimensional reduced Goodwin dynamics'''

_DESCRIPTION ="""
It is the reduced version of a Goodwin model, with another writing : when the model is established,
one can rather than calculate (N,a,K,w), calculate the dynamics only on employment and wage share.
In consequence it is a 2- differential equation model, but with the same dynamics as _model_goodwin.

The rest of the documentation is in _model_Goodwin

* **Article :**  1967. ‘A growth cycle’, in: Carl Feinstein, editor, Socialism, capitalism and economic growth. Cambridge, UK: Cambridge University Press.
* **Author  :** Goodwin, Richard,
* **Coder   :** Paul Valcke
* **Date    :** 2023/08/21

TODO:
*
"""

import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O

_LOGICS = {
    'differential': {
        'employment': {'func' : lambda employment, alpha,n,delta,omega,nu: employment*( (1-omega)/nu - alpha - n - delta)},
        'omega'     : {'func' : lambda omega, phillips,alpha: omega*(phillips-alpha),},
        #'omega'     : {'func' : lambda omega, employment, phi0, phi1, alpha: omega*((-phi0 + phi1 / (1 - employment)**2)-alpha),}, 
    },
    'statevar': { 
        'phillips': Funcs.Phillips.div,
        'g': {'func': lambda omega,delta,nu: (1-omega)/nu-delta }
    },
    'parameter': {},
    'size': {},
}

def FIND_EQ_Gr(hub=None,dic=False):
    if not dic:
        R=hub.get_dparam()
        d={v:R[v]['value'] for v in R.keys()}
    else:
        d=dic

    fm1 = lambda x : 1-np.sqrt(x)
    return {'omega': 1-d['nu']*(d['delta']+d['alpha']+d['n']),
            'employment': fm1( -d['Phi1']/(d['Phi0']+d['alpha']) )}

_SUPPLEMENTS={'equilibrium':FIND_EQ_Gr}

plots={
    'XY':[{'x':'omega',
           'y':'employment'}]
}

_PRESETS = {
'00equilibrium':{
    'fields':{
        'employment':0.01,
        'omega':0.01,
    },
    'com':"Start close to the (0,0) equilibrium. This is explosive",
    'plots':plots,    
},
'NontrivialEQ':{
    'fields':{
        'delta':0.05,
        'alpha':0.02,
        'n':0.025,
        'nu':3,
        'Phi1': 0.0010101,
        'Phi0': -0.1010101
    },
    'com':"Start almostat the non-trivial equilibrium",
    'plots':plots
},
'farfromEQ': {
    'fields':{'employment':.6,
              'omega':0.4,
              'dt':0.01,'Tmax':100},
    'com': "Start far from EQ",
    'plots':plots
}
}
_PRESETS['NontrivialEQ']['fields']['employment']=FIND_EQ_Gr(0,dic=_PRESETS['NontrivialEQ']['fields'])['employment']
_PRESETS['NontrivialEQ']['fields']['omega']     =FIND_EQ_Gr(0,dic=_PRESETS['NontrivialEQ']['fields'])['omega']