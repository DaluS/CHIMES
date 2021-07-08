# -*- coding: utf-8 -*-
"""
THIS CODE IS AN OVERLAY ON GEMMES TO CONTROL WHAT HAPPENS IN THE CODE 

THIS CODE SHOULD BE USED IN AN IPYTHON INTERFACE TO CONTROL IT
"""

import Main
import os 

########################### THE TYPICAL VARIABLES #############################
SystemOfEquation   = None
InitialDictionnary = None
Value_Changes      = { 'Initial conditions' : {},
                       'Parameters'         : {},
                       'ParNum'             : {},
                       'TypeOfArrays'       : 'lin' #log
                     }
plot               = True # True or False
verb               = True 
timeit             = True # True or False
save               = os.getcwd() # True or False
savepath           = None
returnAll          = False # True or False
Comments           = "Hi this is a test"
###############################################################################


'''
VALUE_Changes : If its one value                      , The code put a scalar
                If it is two values in a list         , The code will create a vector with value between these ( with an either logarithmic or exponential distrib)
                If more values in a list              , The code will fix parNum['Nx'] as the length of that vector
                
                If two definitions are defining parNum['Nx'] at the same time : the system must crash
'''

Value_Changes = { 'NumParameters'      : {},
                  'Initial conditions' : {},
                  'Parameters'         : {},
                  'TypeOfArrays'       : 'lin' #log
                  }



Result = Main.run(SystemOfEquation,   
                  InitialDictionnary,
                  Value_Changes,     
                  plot,               
                  timeit,             
                  save,                     
                  savepath,                  
                  returnAll,          
                  Comments,)          















def ListAvailableSystemOfEquation():
    '''
    Looks at the library of Systems one can solve and print them with :
        * description
        * parameters 
        * variables
    '''    
    return
    
def ListBasicNumericalParameters():
    '''
    Print All parameters values and type stored in the Parameters file
    '''

def ListBasicParametersValues():
    '''
    Print All parameters values and type stored in the Parameters file
    '''
    
def ListBasicInitialConditions():    
    '''
    Print All Initial conditions values and type stored in the Parameters file
    '''