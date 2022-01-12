# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:35:39 2021

@author: Paul Valcke
"""

import pygemmes as pgm
import numpy as np
hub = pgm.Hub('GK-Reduced', verb=False)
changedic = {'Tmax': 20,
             'dt': 0.005,
             'lambda': np.linspace(.75, .99, 3),
             # 'omega': {'value': np.linspace(.85, .90, 2), 'grid': True},
             'd': 0,
             }
for k, v in changedic.items():
    hub.set_dparam(key=k, value=v, verb=False)
hub.set_dparam(key='omega', value=np.linspace(.85, .90, 2), grid=True)

# hub.set_dparam()
# hub.get_summary()


hub.run(verb=1.1)
hub.FillCyclesForAll(ref='lambda')
R = hub.get_dparam(returnas=dict)
