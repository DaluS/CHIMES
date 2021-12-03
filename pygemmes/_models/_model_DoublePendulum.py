# -*- coding: utf-8 -*-
"""
Two pendulums one on the other. This is creating a chaotic movement.
This set of equation assume m1=m2 and l1=l2

https://en.wikipedia.org/wiki/Double_pendulum

"""
import numpy as np

_FUNC_ORDER = None


_LOGICS = {
    # FIELDS DEFINED BY ODE
    'ode': {
        # Household properties
        't1': {
            'func': lambda dt1=0: dt1,
            'com': 'Upper pendulum angle',
            'initial': np.pi/4},
        't2': {
            'func': lambda dt2=0: dt2,
            'com': 'lower pendulum angle',
            'initial': np.pi/4},
        'pt1': {
            'func': lambda dt1=0, dt2=0, t1=0, t2=0, m=0, l=1, gravity=0: -m*l**2/2 * (dt1*dt2 * np.sin(t1-t2) + 3 * gravity/l * np.sin(t1)),
            'com': 'Upper pendulum impulsion',
            'initial': 0},
        'pt2': {
            'func': lambda dt1=0, dt2=0, t1=0, t2=0, m=0, l=1, gravity=0: -m*l**2/2 * (-dt1*dt2 * np.sin(t1-t2) + gravity/l * np.sin(t2)),
            'com': 'Lower pendulum impulsion',
            'initial': 0},

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
        'y1': {
            'func': lambda t1=0, l=0: l*np.cos(t1),
            'com': 'x coordinate upper pendulum'},
        'x1': {
            'func': lambda t1=0, l=0: l*np.sin(t1),
            'com': 'x coordinate upper pendulum'},
        'y2': {
            'func': lambda y1=0, t2=0, l=0: y1+l*np.cos(t2),
            'com': 'x coordinate lower pendulum'},
        'x2': {
            'func': lambda x1=0, t2=0, l=0: x1+l*np.sin(t2),
            'com': 'x coordinate lower pendulum'},
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'm': 1,
        'l': 1,
        'gravity': 1,
        't1': np.pi/2,
        't2': np.pi/2,
        'pt1': 0,
        'pt2': 0},
    'com': 'Default run'},
}
