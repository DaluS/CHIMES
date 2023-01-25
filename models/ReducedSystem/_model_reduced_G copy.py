
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
        'y': {'func' : lambda y,time: y*np.sin(time),
              'initial': 1,
    },
    'statevar': { 
    },
    'parameter': {},
    'size': {},
}
}

_SUPPLEMENTS={}
_PRESETS = {}
