
'''Goodwin model + Court-McIsaac style population endogenization '''

_DESCRIPTION = """
* **Article :** 
* **Author  :** Goodwin
* **Coder   :** Simon Lebastard

This is a basic Goodwin model :
    * Two sectors
    * Exogenous technical progress, exogenous population
    * Capital accumulation through investment of profits
    * Consumption through salary
    * Salary-Profit through Philips curve
    * No money, no inflation
    * No loan possibility

The interesting things :
    * growth is an emergent property
    * Economic cycles (on employment and wage share) are an emergent property
    * trajectories are closed in the phasespace (employment, omega) employment - wageshare

It is written with a price p=1 for homogeneity issues

ENDEGENOUS POPULATION
---------------------
Population N is split into 4 age groups: N = N1 + N2 + N3 + N4
N1: population of 0-14 yo   Not employable  Not fertile
N2: population of 15-54 yo  Employable      Fertile
N3: population of 55-64 yo  Employable      Not fertile
N4: population of 65+ yo    Not employable  Not fertile
For the dynamics of the population in each age group, see
Victor Court & Florent McIsaac, A Representation of the World Population Dynamics for Integrated Assessment Models, March 2020

@author: Paul Valcke, Simon Lebastard
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel

################# DEFINING NEW FUNCTIONS ####################################
def dem_transition(y, lvl_min, ampl, y_crit, std):
    """
    Implements the Court-McIsaac model of demographics transition.
    BR can be either a birth rate or a death rate,
    potentially specific to an age-group. No power on the denominator for now, to be added later
    """
    return lvl_min + ampl/(1 + np.exp(std*(y-y_crit)))

def demo_4d_G1(y, N1, N2, G2_BR_low, G2_BR_high, G2_y_crit_BR, G2_BR_std):
    "4D demographics transition function: Age group 1/4"
    return dem_transition(y,G2_BR_low, G2_BR_high, G2_y_crit_BR, G2_BR_std)*N2 - N1

def demo_4d_G2(y, N1, N2, G1_DR_low, G1_DR_high, G1_y_crit_DR, G1_DR_std):
    "4D demographics transition function: Age group 2/4"
    return (1-dem_transition(y,G1_DR_low, G1_DR_high, G1_y_crit_DR, G1_DR_std))*N1 - N2

def demo_4d_G3(y, N2, N3, G2_DR_low, G2_DR_high, G2_y_crit_DR, G2_DR_std):
    "4D demographics transition function: Age group 3/4"
    return (1-dem_transition(y,G2_DR_low, G2_DR_high, G2_y_crit_DR, G2_DR_std))*N2 - N3

def demo_4d_G4(y, N3, N4, G3_DR_low, G3_DR_high, G3_y_crit_DR, G3_DR_std, G4_DR_low, G4_DR_high, G4_y_crit_DR, G4_DR_std):
     "4D demographics transition function: Age group 4/4"
     return (1-dem_transition(y,G3_DR_low, G3_DR_high, G3_y_crit_DR, G3_DR_std))*N3 - dem_transition(y,G4_DR_low, G4_DR_high, G4_y_crit_DR, G4_DR_std)*N4

# ######################## LOGICS #######################################
_LOGICS = {
    'differential': {
        'a': {'func': lambda a,alpha    : a*alpha },
        'N1': {'func': demo_4d_G1, 'units': 'Humans'},
        'N2': {'func': demo_4d_G2, 'units': 'Humans'},
        'N3': {'func': demo_4d_G3, 'units': 'Humans'},
        'N4': {'func': demo_4d_G4, 'units': 'Humans'},
        'K': {'func': lambda K,Ir,delta : Ir-delta*K },
        'w': {'func': lambda w,phillips : w*phillips },
    },

    # Intermediary relevant functions
    'statevar': {
        'N': {
            'func': lambda N1, N2, N3, N4: N1+N2+N3+N4,
            'definition': 'Total population, currently assumed to be employable (TO REFINE)'
        },
        'y': {'func': lambda Y,N : Y/N },

        'beta1': {
            'func': demo_4d_G1,
            'definition': '4D demographics transition function: Age group 1/4',
            'units': 'y^{-1}',
        },
        'beta2': {
            'func': demo_4d_G2,
            'definition': '4D demographics transition function: Age group 2/4',
            'units': 'y^{-1}',
        },
        'beta3': {
            'func': demo_4d_G3,
            'definition': '4D demographics transition function: Age group 3/4',
            'units': 'y^{-1}',
        },
        'beta4': {
            'func': demo_4d_G4,
            'definition': '4D demographics transition function: Age group 4/4',
            'units': 'y^{-1}',
        },

        'pi' :   {'func': lambda p,Y,Pi : Pi /(p*Y) },
        'omega' :{'func': lambda p,Y,w,L: w*L/(p*Y) },
        'employment' :{'func': lambda L,N: L/N },
        'g' :{'func': lambda Ir,K,delta: Ir/K-delta },      
        
        'Y' :{'func': lambda K,nu: K/nu },
        'Pi':{'func': lambda p,Y,w,L: p*Y-w*L},
        'C' :{'func': lambda Y,Ir: Y-Ir },
        'Ir':{'func': lambda Pi: Pi },
        'L' :{'func': lambda Y,a: Y/a },

        'phillips'  :{'func': lambda employment, philinConst, philinSlope: philinConst + philinSlope * employment,},
    },
    'parameter': {
        'p': {'value':1},
        'philinConst': {'value': 0.02},
        'G1_DR_low': {'value': 2.31e-03, 'units': 'y^{-1}'},
        'G1_DR_high': {'value': 1.08e-01, 'units': 'y^{-1}'},
        'G1_y_crit_DR': {'value': 3.33e+02, 'units': '$.Humans^{-1}'},
        'G1_DR_std': {'value': 3.65e-04, 'units': 'Humans.$^{-1}'},
        'G2_BR_low': {'value': 2.61e-01, 'units': 'y^{-1}'},
        'G2_BR_high': {'value': 5.22e-01, 'units': 'y^{-1}'},
        'G2_y_crit_BR': {'value': 6.13e+03, 'units': '$.Humans^{-1}'},
        'G2_BR_std': {'value': 1.11e-03, 'units': 'Humans.$^{-1}'},
        'G2_DR_low': {'value': 2.27e-03, 'units': 'y^{-1}'},
        'G2_DR_high': {'value': 4.53e-03, 'units': 'y^{-1}'},
        'G2_y_crit_DR': {'value': -3.88e+03, 'units': '$.Humans^{-1}'},
        'G2_DR_std': {'value': 4.58e-04, 'units': 'Humans.$^{-1}'},
        'G3_DR_low': {'value': 8.78e-03, 'units': 'y^{-1}'},
        'G3_DR_high': {'value': 1.76e-02, 'units': 'y^{-1}'},
        'G3_y_crit_DR': {'value': 1.88e+03, 'units': '$.Humans^{-1}'},
        'G3_DR_std': {'value': 3.49e-04, 'units': 'Humans.$^{-1}'},
        'G4_DR_low': {'value': 4.50e-02, 'units': 'y^{-1}'},
        'G4_DR_high': {'value': 9.00e-02, 'units': 'y^{-1}'},
        'G4_y_crit_DR': {'value': 2.50e+03, 'units': '$.Humans^{-1}'},
        'G4_DR_std': {'value': 4.36e-04, 'units': 'Humans.$^{-1}'},
    },
    'size': {},
}

_SUPPLEMENTS={}

# ####################### PRESETS #######################################
_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N1': 0.24, # approximate 2020 share of 0-14yo
            'N2': 0.52, # approximate 2020 share of 15-54yo
            'N3': 0.14, # approximate 2020 share of 55-64yo
            'N4': 0.1, # approximate 2020 share of 65+yo
            'K': 2,
            'D': 0,
            'w': .6,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': '',
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'XY': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            'XYZ': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'time',
                    'color': 'pi',
                    'idx': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'nx':5,
            'dt': 0.01,
            'a': 1,
            'N1': 0.24, # approximate 2020 share of 0-14yo
            'N2': 0.52, # approximate 2020 share of 15-54yo
            'N3': 0.14, # approximate 2020 share of 55-64yo
            'N4': 0.1, # approximate 2020 share of 65+yo
            'K': 2.9,
            'D': 0,
            'w': [.5, .5*1.2, .5*1.3, .5*1.5, .5*1.7],
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        'plots': {
            'timetrace': [{'keys': ['employment', 'omega']}],
            'nyaxis': [],
            'phasespace': [{'x': 'employment',
                           'y': 'omega',
                            'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}