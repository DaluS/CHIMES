# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 12:25:02 2021

@author: Paul Valcke
"""

import _core

Solvers = ['eRK4-homemade',
           'eRK2-scipy',
           'eRK4-scipy',
           'eRK8-scipy',
           ]

for sol in Solvers:
    sol = _core.Hub('GK')
    sol.run(verb=0)
