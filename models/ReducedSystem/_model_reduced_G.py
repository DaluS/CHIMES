
'''2-dimensional reduced Goodwin dynamics'''

_DESCRIPTION ="""
It is the reduced version of a Goodwin model, with another writing : when the model is established,
one can rather than calculate (N,a,K,w), calculate the dynamics only on employment and wage share.
In consequence it is a 2- differential equation model, but with the same dynamics as _model_goodwin.

The rest of the documentation is in _model_Goodwin

* **Name :** Reduced Goodwin
* **Article :** 
* **Author  :** Goodwin, Richard, 1967. ‘A growth cycle’, in: Carl Feinstein, editor, Socialism, capitalism and economic growth. Cambridge, UK: Cambridge University Press.
* **Coder   :** Paul Valcke

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
    },
    'statevar': { 
        'phillips': Funcs.Phillips.div,
    },
    'parameter': {},
    'size': {},
}

_SUPPLEMENTS={}
_PRESETS = {}
