# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:02:26 2022

@author: Paul Valcke
"""

import numpy as np

class Phillips :
    """
    The Phillips function is linking the relative wage share increase rate to the
    employement.
    The phenomena behind is a class struggle : as the
    """

    def expo(phiexp0=0, phiexp1=0, phiexp2=0, lamb=0):
        return phiexp0 + phiexp1 * np.exp(phiexp2 * lamb)

    def div(phi0=0, phi1=0, phi2=0, lamb=0):
        return -phi0 + phi1 / (1 - lamb)**2

    def lin(philinConst=0, philinSlope=0, lamb=0):
        return philinConst + philinSlope * lamb,

class kappa :
    def kappa_lin(kappalinConst=0, kappalinSlope=0, pi=0):
        return kappalinConst + kappalinConst * pi

    def kappa_exp(k0=0, k1=0, k2=0, pi=0):
        return k0 + k1 * np.exp(k2 * pi)
