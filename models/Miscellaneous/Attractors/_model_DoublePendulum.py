"""Double Uniform Pendulum Chaotic Dynamics"""


_DESCRIPTION ="""
Two pendulums one on the other. This is creating a chaotic movement.
This set of equation assume m1=m2 and l1=l2

* **Name :** Double Uniform Pendulum Chaotic Dynamics
* **Article :** https://en.wikipedia.org/wiki/Double_pendulum
* **Author  :** /
* **Coder   :** Paul Valcke

** TODO:**
* Create good plots 
* Find equation for two different pendulum
* Explore more cases 

"""
import numpy as np

_FUNC_ORDER = None


_LOGICS = {
    # FIELDS DEFINED BY ODE
    'ode': {
        # Household properties
        't1': {
            'func': lambda dt1=0: dt1,
            'com': 'Upper pendulum angle'},
        't2': {
            'func': lambda dt2=0: dt2,
            'com': 'lower pendulum angle'},
        'pt1': {
            'func': lambda dt1=0, dt2=0, t1=0, t2=0, m=0, l=1, g=0: -m*l**2/2 * (dt1*dt2 * np.sin(t1-t2) + 3 * g/l * np.sin(t1)),
            'com': 'Upper pendulum impulsion'},
        'pt2': {
            'func': lambda dt1=0, dt2=0, t1=0, t2=0, m=0, l=1, g=0: -m*l**2/2 * (-dt1*dt2 * np.sin(t1-t2) + g/l * np.sin(t2)),
            'com': 'Lower pendulum impulsion'},

    },

    # FIELDS DEFINED BY OTHER VARIABLES
    'statevar': {
        # Production function related quantities
        'dt1': {
            'func': lambda pt1=0, pt2=0, t1=0, t2=0, m=1, l=1: (6/m*l**2) * (2*pt1 - 3 * np.cos(t1-t2)*pt2)/(16 - 9 * np.cos(t1-t2)**2),
            'com': 'Upper Angle variation'},
        'dt2': {
            'func': lambda pt1=0, pt2=0, t1=0, t2=0, m=1, l=1: (6/m*l**2) * (8*pt1 - 3 * np.cos(t1-t2)*pt1)/(16 - 9 * np.cos(t1-t2)**2),
            'com': 'lower angle variation'},
    },
}

################### SUPPLEMENTS IF NEEDED ###################################
_SUPPLEMENTS={}

# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
'default': {
    'fields': {
        'm': 1,
        'l': 1,
        'g': 1,
        'theta1': np.pi/2,
        'theta2': np.pi/2,
        'ptheta1': 0,
        'ptheta2': 0},
    'com': 'Default run',
    'plots': {'XYZ': [{ 'x':'t1',
                       'y':'t2',
                       'z':'pt1', 
                       'color':'pt2', 
                       'idx':0, 
                       'Region':0, 
                       'tini':False, 
                       'tend':False, 
                       'title':''}]
            }
    },
}