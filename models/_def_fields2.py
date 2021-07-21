# -*- coding: utf-8 -*-
"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

"""

import numpy as np  
import itertools 

_DFIELDS = { 
    
    'Numerical' : {
        'Tmax' : {
            'value' : 100,
            'units' : 'y',
            'com' : 'Total simulated time',
            },
        'dt' : {
            'value' : 0.01,
            'units' : 'y',
            'com' : 'time between two steps',
            },
        'nt' : {
            'func': lambda Tmax=0, dt=1: int(Tmax / dt),
            'units' : None,
            'com' : 'Total simulated time',
            },
        'nx' : {
            'value' : 100,
            'units' : 'y',
            'com' : 'Total simulated time',
            },
        'time': {
            'value' : 0,
            'ode' : lambda dt=0: 1.,
            'com': 'Time vector',
            'units': 'y',
            },
        },
    
    'CORE' : {
        # Population    
        'N': {
            'ode': lambda beta=0, itself=0: beta * itself,
            'value': 1.,
            'com': 'Exogenous population as an exponential',
            },
        'beta': {
            'value': 0.025,
            'com': 'Rate of population growth',
            'units': 'y^{-1}',   
            },
        
        # Productivity
        'a': {
            'ode': lambda alpha=0, itself=0: alpha * itself,
            'value': 1,
            'com': 'Exogenous technical progress as an exponential',
        },        
        'alpha': {
            'value': 0.02,
            'com': 'Rate of productivity increase',
            'units': 'y^{-1}',
            },    
        'W': {
            'ode': lambda itself=0, phillips=0: itself * phillips,
            'value': 0.85,
            'com': 'Wage evolution through phillips curve',
        },

        
        # Capital
        'delta': {
            'value': 0.005,
            'com': 'Rate of capital depletion',
            'units': 'y^{-1}',
            },
        'nu': {
            'value': 3,
            'com': 'Kapital to output ratio',   
            'units': None,
            },
        'K': {
            'ode': lambda I=0, itself=0, delta=0: I - itself * delta,
            'value': 2.7,
            'com': 'Capital evolution from investment and depreciation',
        },        
        
        
       'pi': {
            'value': None,
            'com': 'relative profit',
            'units': '',
            'symbol': r'$\pi$',
            },
        'g': {
            'value': None,
            'com': 'Relative growth',
            'units': 'y^{-1}',
            },       
        'Y': {
            'value': None,
            'com': 'GDP in output quantity',
            'units': 'Real units',
            },
        'L': {
            'value': None,
            'com': 'Workers',
            'units': 'Humans',
            },
        'I': {
            'value': None,
            'com': 'Investment',
            'units': 'Dollars',
            },    
        'Pi': {
            'value': None,
            'com': 'Absolute profit',
            'units': 'Dollars',
            },
        },

    'Salary Negociation':{
        'phillips': {
            'value': None,
            'com': 'Wage inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$\phi$',
            },
        'phinull': {
            'value' : 0.04,
            'com': 'Unemployment rate with no salary increase',
            'units': None,
            },
        'phi0': {
            'func': lambda phinull=0: phinull / (1 - phinull**2),
            'com': '',
            'units': None,
            },
        'phi1': {
            'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
            'com': '',
            'units': None,
            },
        },
                
   'Investment': {
        'kappa': {
            'value': None,
            'com': 'Part of GDP in investment',
            'units': '',
            'symbol': r'$\kappa$',
        },    
       'k0': {
           'value': -0.0065,
           'com': 'Percent of GDP invested when profit is zero',
           'units': None,
        },
        'k1': {
            'value': np.exp(-5),
            'com': 'Investment slope',
            'units': None,
        },
        'k2': {
            'value': 20,
            'com': 'Investment power in kappa',
            'units': None,
        },
    },
   
    'Debt' : { 
        'r': {
            'value': .03,
            'com': 'Interest at the bank',
            'units': 'y^{-1}',
        },
        'D': {
            'ode': lambda I=0, Pi=0: I - Pi,
            'value': 0.1,
            'com': 'Debt as Investment-Profit difference',
            'units': 'Dollars',
        'd': {
            'func': lambda GDP=0, D=0: D/GDP,
            #'value': 0.1,
            'com': 'relative deby',

        },
    },
    
    'Prices' : {
        'mu' : {
            'value' : 2 ,
            'com' : 'Markup on prices', 
            'units' : None,
            },
        'eta' : {
            'value' : 1 ,
            'com' : 'timerate of price adjustment',
            'units' : 'y^{-1}'},
        'GDP': {          
            'value': None,
            'com': 'GDP in nominal term',
            'units': 'Dollars',
            },
        
    },
        
    
    'MISC' : {
        'Coucou' : {
            'value': 0,
            'com' : 'I am just a test',
            'units' :None,
            },
    },
}

def CHECK_DFIELDS(dic):
    ''' 
    This function check the consistency for each definition 
    * Unity of value declaration
    * Consistency of the field declared 
    '''
    
    Errormessage = ''
    Warningmessage = ''
    
    # 1) ### CHECK THAT NO FIELD DEFINITION ARE AT TWO PLACES 
    listoflistofkeys = [[ keys2 for keys2 in dic[keys1].keys()] 
                                for keys1 in dic.keys()        ]
    listofkeys =  list(itertools.chain(*listoflistofkeys))
    duplicates = set([x for x in listofkeys if listofkeys.count(x) > 1])
    
    if len(duplicates) > 0 : 
        msg= "keys defined in multiple groups !"+str(duplicates)
        Errormessage+=msg+'\n'
        
    # 2) ### CHECK THAT THE BEHAVIOR FIELDS ARE CONSISTENT
    for group in dic.keys() : 
        for field in dic[group].keys() :
            subject = dic[group][field]
            
            # We want that either : 
                # there is function and no value 
                # there is an ode and and a value 
                # there is a value and nothing else 
            if ( 'func' in subject.keys() and 'value' in subject.keys() ):  
                msg = str(field)+' in '+str(group)+' have both function and value'
                Errormessage+=msg+'\n'
            elif ( 'ode' in subject.keys() and not 'value' in subject.keys() ):
                msg = str(field)+' in '+str(group)+' is an ODE with no initial condition'
                Errormessage+=msg+'\n'
            elif ( 'func' not in subject.keys() and 'value' not in subject.keys() ): 
                msg = str(field)+' in '+str(group)+' is a parameter with no value'
                Errormessage+=msg+'\n'
                
            # We can also check if there are comments and units fields
            if 'com' not in subject.keys(): 
                msg = str(field)+' in '+str(group)+' has no comment'
                Warningmessage+=msg+'\n'
            if 'units' not in subject.keys():    
                msg = str(field)+' in '+str(group)+' has no unit'
                Warningmessage+=msg+'\n'
        # Check that all fields are well located 
        print(group, len(dic[group].keys()))
        if (group=='MISC' and len(dic[group].keys())>0):
            msg ='MISC group contains field that should be classified'          
                    
                
    if len(Warningmessage) :
        raise Warning(Warningmessage)
    if len(Errormessage):
        raise ValueError(Errormessage)                

def describe_dfields(dic):
    '''
    Return simple characteristics of d_fields
    '''
    
    


CHECK_DFIELDS(_DFIELDS)