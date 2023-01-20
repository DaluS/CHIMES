'''GK with affine kappa and philips, with US data'''

_DESCRIPTION = """

"""
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O
import numpy as np

_LOGICS = {
    'size': {},
    ###################################################################
    'differential': {
        'omega'         :{'func': lambda omega,Phillips,alpha: omega*(Phillips-alpha)},
        'employment'    :{'func': lambda employment,nu,delta,alpha,beta,kappa : employment*(kappa/nu - delta - alpha - beta)},
        #'debt'          :{'func': lambda debt, r,Delta,kappa,nu,delta,omega: debt*(r*(1-Delta)-kappa/nu+delta+(kappa-(1-omega*(1-Delta)))/debt)},
        'debt'          :{'func': lambda debt, r,Delta,kappa,nu,delta,omega: debt*(r*(1-Delta)-kappa/nu+delta)+(kappa-(1-omega*(1-Delta)))},

    },
    'statevar': {
        'beta'          :{'func': lambda n:n},
        'pi'            :{'func': lambda omega,r,debt: 1-omega-r*debt},
        'kappa'         :{'func': lambda pi,k0,k1: k0+k1*pi },
        'Phillips'      :{'func': lambda employment,gamma,rho: gamma+rho*employment},
        },
    'parameter': {
        'rho': {'value':0},
    },
}




########################### SUPPLEMENTS ################################################
'''Specific parts of code that are accessible'''
_SUPPLEMENTS= {}


############################ PRESETS #####################################################




_PRESETS = {
    'FredValues': {
        'fields': 
        {
            #'alpha': ,
            #'beta': ,
            'gamma': -0.5768167   ,
            'rho': 0.624795 ,
            'k0': -0.0419826,
            'k1': 0.9851812 ,
            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,
            'Delta': 0.2780477,
            'omega': 0.6900101,
            'employment': 0.9383604 ,
            'debt': 0.5282786 ,
        },
        'com': ('Data given by F.Mortier on US calibration'),
        'plots': {},
    },
    'Goodwin': {
        'fields': 
        {
            #'alpha': ,
            #'beta': ,
            'gamma': -0.5768167   ,
            'rho': 0.624795 ,
            'k0': 0,
            'k1': 1 ,
            'nu': 3.844391,
            'r': 0.02083975,
            'delta': 0.04054871,
            'Delta': 0,
            'omega': 0.6900101,
            'employment': 0.9383604 ,
            'debt': 0 ,
        },
        'com': ('Data given by F.Mortier on US calibration'),
        'plots': {},
    },
}