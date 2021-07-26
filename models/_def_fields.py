# -*- coding: utf-8 -*-

"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

---- 

This file contains : 
    _DFIELDS the big dictionnary with basic information on 
        * Variables 
        * Parameters
        * Numerical parameters
        
    _DALLOWED_FIELDS : Contains all the restrictions on each field for each 
    element in _DFIELD
    _DEFAULTFIELDS : The value that will be added if none are 
    
    __DOTHECHECK Flag to check or not the dictionnary
    __FILLDEFAULTVALUES Flag to fill the defaultfields
"""


import warnings


import numpy as np

__DOTHECHECK = False
__FILLDEFAULTVALUES = True

# #############################################################################
# #############################################################################
#                   FIELDS OF FIELDS AND EXPECTED VALUES
# #############################################################################
# dict of default value in fields 
_DEFAULTFIELDS = {
    'value'    : None,
    'com'      : 'No comment',
    'dimension': 'undefined',
    'units'    : 'undefined',
    'type'     : 'undefined',
    'group'    : None,  
    #'symbol' : this is the key of the variable
    }

# dict of allowed fields (None => no restriction)
_DALLOWED_FIELDS = {
    'value': None,
    'com': None,
    'units': [
        'Units',  # 
        'y',      # Time
        '$',      # Money
        'C',      # Concentration
        'Humans', # Population
    ],
    'type': ['intensive', 'extensive', 'dimensionless'],
    'symbol': None,
    'group': None, #[
        #'Numerical',
        #'Population',
        #'Prices', 'Capital', 'Philips', 'Gemmes',
        #'Keen', 'Dividends', 'Economy', 'Production',
        #'Coupling',
        #'RelaxBuffer',
        #'Climate', 'Damage',
    #],
}

# #############################################################################
# #############################################################################
#                   Dict of default fields
# #############################################################################


_DFIELDS = {
    
    # --------------
    # Numerical
    'Tmax': {
        'value': 100,
        'com': 'Duration of simulation',
        'dimension': 'time',
        'units': 'y',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'dt': {
        'value': 0.01,
        'com': 'Time step (fixed timestep method)',
        'dimension': 'time',
        'units': 'y',
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'nt': {
        'func': lambda Tmax=0, dt=1: int(Tmax / dt),  # Dynamically allocated
        'eqtype': 'intermediary',
        'com': 'Number of temporal iteration',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },
    'nx': {
        'value': 1,
        'com': 'Number of similar systems evolving in parrallel',
        'dimension': None,
        'units': None,
        'type': None,
        'symbol': None,
        'group': 'Numerical',
    },


    # --------------
    # Time vector
    'time': {
        'func': lambda dt=0: 1.,
        'com': 'Time vector',
        'dimension': 'time',
        'units': 'y',
        'type': 'extensive',
        'symbol': r'$t$',
        'group': 'Time',
        'eqtype': 'ode',
        'initial': 0,
    },

    # PARAMETERS #############################################################
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    # Population evolution
    'beta': {
        'value': 0.025,
        'com': 'Rate of population growth',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$beta$',
        'group': 'Population',
    },
    'alpha': {
        'value': 0.02,
        'com': 'Rate of productivity increase',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$alpha$',
        'group': 'Population',
    },

    # --------------
    # Capital properties
    'delta': {
        'value': 0.005,
        'com': 'Rate of capital depletion',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\delta$',
        'group': 'Capital',
    },

    # --------------
    # Production
    'nu': {
        'value': 3,
        'com': 'Kapital to output ratio',   
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'\nu',
        'group': 'Production',
    },


    # --------------
    # INTEREST / Price
    'r': {
        'value': .03,
        'com': 'Interest at the bank',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': None,
        'group': 'Prices',
    },


    # --------------
    # PHILIPS CURVE (employement-salary increase)
    'phinull': {
        'value': 0.04,
        'com': 'Unemployment rate that stops salary increase (no inflation)',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },
    'phi0': {
        'value': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': '',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },
    'phi1': {
        'value': None,
        'com': '',
        'dimension': None,
        'units': None,
        'type': '',
        'symbol': r'$\phi_0$',
        'group': 'Philips',
    },

    # --------------
    # KEEN INVESTMENT FUNCTION (profit-investment function)
    'k0': {
        'value': -0.0065,
        'com': 'Percent of GDP invested when profit is zero',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_0$',
        'group': 'Keen',
    },
    'k1': {
        'value': np.exp(-5),
        'com': 'Investment slope',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_1$',
        'group': 'Keen',
    },
    'k2': {
        'value': 20,
        'com': 'Investment power in kappa',
        'dimension': None,
        'units': None,
        'type': 'intensive',
        'symbol': r'$k_2$',
        'group': 'Keen',
    },

    # DYNAMICAL VARIABLES ####################################################
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    ### Classic dimensionless for phase-space
    'omega': {
        'value': .578,
        'com': 'Wage share of the economy',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$\omega$',
        'group': 'Economy',
    },
    'lambda': {
        'value': .675,
        'com': 'employment rate',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$\lambda$',
        'group': 'Economy',
    },

    'd': {
        'value': 1.53,
        'com': 'relative private debt',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$d$',
        'group': 'Economy',
    },

    ### Intensive dynamic variable
    'a': {
        'value': None,
        'com': 'productivity per worker',
        'dimension': 'Productivity',
        'units': 'Output Humans^{-1}',
        'type': 'intensive',
        'symbol': r'$a$',
        'group': 'Economy',
    },
    'N': {
        'value': 4.83,
        'com': 'Population',
        'dimension': 'Humans',
        'units': 'Humans',
        'type': 'extensive',
        'symbol': r'$N$',
        'group': 'Population',
    },
    
    
    'K': {
        'value': None,
        'com': 'Capital',
        'dimension': 'Real Units',
        'units': 'Real Units',
        'type': 'extensive',
        'symbol': r'$K$',
        'group': 'Economy',
    },
    'W': {
        'value': None,
        'com': 'Salary',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$W$',
        'group': 'Economy',
    },
    'D': {
        'value': None,
        'com': 'Absolute private debt',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$D$',
        'group': 'Economy',
    },

    # INTERMEDIARY VARIABLES #################################################
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    
    # From functions
    'kappa': {
        'value': None,
        'com': 'Part of GDP in investment',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$\kappa$',
        'group': 'Economy',
    },    
    'phillips': {
        'value': None,
        'com': 'Wage inflation rate',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$\phi$',
        'group': 'Economy',
    },


    
    'pi': {
        'value': None,
        'com': 'relative profit',
        'dimension': '',
        'units': '',
        'type': 'dimensionless',
        'symbol': r'$\pi$',
        'group': 'Economy',
    },
    'g': {
        'value': None,
        'com': 'Relative growth',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$g$',
        'group': 'Economy',
    },
    'GDP': {          
        'value': None,
        'com': 'GDP in nominal term',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$GDP$',
        'group': 'Economy',
    },
    'Y': {
        'value': None,
        'com': 'GDP in output quantity',
        'dimension': 'Real Units',
        'units': 'Real units',
        'type': 'extensive',
        'symbol': r'$Y$',
        'group': 'Missing',
    },
    'L': {
        'value': None,
        'com': 'Workers',
        'dimension': 'Humans',
        'units': 'Humans',
        'type': 'extensive',
        'symbol': r'$L$',
        'group': 'Missing',
    },
    'I': {
        'value': None,
        'com': 'Investment',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$I$',
        'group': 'Economy',
    },
    'Pi': {
        'value': None,
        'com': 'Absolute profit',
        'dimension': 'Money',
        'units': 'Dollars',
        'type': 'extensive',
        'symbol': r'$\Pi$',
        'group': 'Economy',
    },
    
    'i': {
        'value': None,
        'com': 'Inflation rate',
        'dimension': 'time rate',
        'units': 'y^{-1}',
        'type': 'intensive',
        'symbol': r'$i$',
        'group': 'Economy',
    },
}


# #############################################################################
# #############################################################################
#               Conformity checks (for saefty, to detect typos...)
# #############################################################################


def Complete_DFIELDS(_DFIELDS,_DEFAULTFIELDS): 
    for k in _DFIELDS.keys():
        kkey = _DFIELDS[k].keys()
        basekeys = ['value',
                    'dimension',
                    'symbol',
                    'com',
                    'units',
                    'type',
                    'group']
        for v in basekeys:
            if v not in kkey : _DFIELDS[k][v]= _DEFAULTFIELDS[v]
        if 'symbol'    not in kkey : _DFIELDS[k]['symbol']    = k   
    return _DFIELDS     
        

def Check_DFIELDS(_DFIELDS,_DALLOWED_FIELDS):
    # List non-conform keys in dict, for detailed error printing
    dk0 = {
        k0: [
            v0[ss] for ss in _DALLOWED_FIELDS.keys()
            if _DALLOWED_FIELDS[ss] is not None and not (
                v0[ss] is None
                or v0[ss] == ''
                or v0[ss] in _DALLOWED_FIELDS[ss]
            )
        ]
        for k0, v0 in _DFIELDS.items()
        if not (
            isinstance(v0, dict)
            and sorted(_DALLOWED_FIELDS) == sorted(v0.keys())
            and all([
                v0[ss] is None
                or v0[ss] == ''
                or v0[ss] in _DALLOWED_FIELDS[ss]
                for ss in _DALLOWED_FIELDS.keys()
                if _DALLOWED_FIELDS[ss] is not None
            ])
        )
    }
    
    
    # Raise warning if any non-conformity
    # Include details per key
    if len(dk0) > 0:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dk0.items()]
        msg = (
            "The following keys of _DFIELDS are non-conform:\n"
            + "\n".join(lstr)
        )
        warnings.warn(msg)

if __FILLDEFAULTVALUES : _DFIELDS = Complete_DFIELDS(_DFIELDS,_DEFAULTFIELDS  )
if __DOTHECHECK        :            Check_DFIELDS   (_DFIELDS,_DALLOWED_FIELDS)