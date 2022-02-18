# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:54:19 2022

@author: Paul Valcke
"""

import pygemmes as pgm

hub=pgm.Hub('G')
hub.set_dparam(**{'N':[.905,0.91,0.92,0.93,.94,.95,.96,.97,.98,1]})
hub.run()
hub.Calculate_Cycles(ref='lambda')
