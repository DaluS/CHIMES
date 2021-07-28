#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MAIN LOOP FOR NUMERICAL RESOLUTION. SEE README OR Overlay.py for documentation 
"""

# Built-in
import os
import time                     # Time (run speed) printing
import argparse

# Library-specific
import Parameters as Par        # All the parameters of the system
import Class as C               # Core of resolution
import VariableDictionnary as VarD # Useful infos on variables
import plots as plts            # Already written plot functions

import utilities._check_input as CheckInput # Verify the argparsed elements

# IMPORTATION OF ALL THE SYSTEM OF EQUATIONS 
#!#!#! FOR THE MOMENT ONLY ONE SYSTEM IS IMPORTED 
import SystemOfEquations.GK_Noinflation as GK_Noinflation


# Default parameter values for main control
_DEFAULTPARAMETERS = {
            'SystemOfEquation'  : GK_Noinflation.MODEL(),
            'InitialDictionnary': None,
            'Value_Changes'     :{'NumParameters'      : {},
                                  'Initial conditions' : {},
                                  'Parameters'         : {},
                                  'ParNum'             : {},
                                  'TypeOfArrays'       : 'lin' #log
                                  },
            'plot'              : True,
            'timeit'            : True,        
            'save'              : False,         
            'savepath'          : os.path.dirname(__file__),
            'returnAll'         : False,
            'Comments'          : "",
                    }


# #############################################################################
# #############################################################################
#                   Main function
# #############################################################################
def run(
    SystemOfEquation   =_DEFAULTPARAMETERS['SystemOfEquation'],
    InitialDictionnary =_DEFAULTPARAMETERS['InitialDictionnary'],
    Value_Changes      =_DEFAULTPARAMETERS['Value_Changes'],
    plot               =_DEFAULTPARAMETERS['plot'],
    timeit             =_DEFAULTPARAMETERS['timeit'],         
    save               =_DEFAULTPARAMETERS['save'],             
    savepath           =_DEFAULTPARAMETERS['savepath'],        
    returnAll          =_DEFAULTPARAMETERS['returnAll'],       
    Comments           =_DEFAULTPARAMETERS['Comments'],  
):
    """ Run the simulation 

    parameters
    ----------
    plot:       bool
        Flag indicating whether to plot figure
    timeit:       bool
        Flag indicating whether to time the simulation
    save:       bool
        Flag indicating whether to save output
    savepath:   str
        Path where to save data
        
    SystemOfEquation : object
        #!#!#!#!#! FOR THE MOMENT IT'S AN OBJECT. THAT IS A PROBLEM FOR ARGPARSER
        Define which equations are going to be solved in the system
        
    InitialDictionnary : NOT CODED YET #!#!#!#!
    
    Value_Changes : dictionnary of dictionnary 
        Dictionary of dictionnary that contains all the changes in variable/parameters   
        
    returnAll : bool     
        Flag indicating if Main should return variables    
        
    Comments : string    

    """

    # CHECK OF USER WILL  ###################
    '''
    Looks at the input ( _DEFAULTPARAMETERS, or through argparser, or through 
    '''

    #!#!#!#! MOST CHECKS ARE NOT DONE IN THIS VERSION
    MainParameters = CheckInput._check_inputs(
        _DEFAULTPARAMETERS,
        SystemOfEquation    ,
        InitialDictionnary  ,
        Value_Changes       ,
        plot                ,
        timeit              ,         
        save                ,             
        savepath            ,        
        returnAll           ,       
        Comments            ,  
    )



    # LOAD #############################  
    parNum   = Par.parnum         (MainParameters['Value_Changes'])     # Value of numerical parameters 
    params   = Par.BasicParameters(MainParameters['InitialDictionnary'],
                                   MainParameters['Value_Changes'])     # Value of "Physical" parameters 
    initCond = Par.initCond(params ,
                            parNum,
                            MainParameters['Value_Changes'])            # Value of the initial parameters 


    # PREPARE ##########################                      
    CORE     = C.CORE(MainParameters['SystemOfEquation'],params,parNum) # The core of the system for resolution and parameters
    
    
    # ANNOUNCEMENT #####################
    if parNum['verb']: 
        print(CORE.description)
        CORE.printParameters()


    # COMPUTATION #######################
    if timeit is True:
        tim = time.time()
        print('Start simulation...', end='')

    y = CORE.initializeY(initCond) # vector y contains all states of time t.
    Y_s, t_s = CORE.TemporalLoop(y) # Calculation of all timesteps

    if timeit is True:
        time_elasped = time.time()-tim
        print('done! elapsed time: {} s'.format(time_elasped))


    # RESULT EXPANSION ################
    results = CORE.expandY_simple(Y_s, t_s)  # Result dictionnary 
    #results = M.getperiods(results, parNum)         # Period measurements 
    UsefulVarDic, OrganisedVar = VarD.VariableDictionnary(results)

    if MainParameters['plot']:
        #eqsys.plotlitst_simple(results,parNum)
        plts.AllUsefulVariablesSeparate(results, UsefulVarDic)

    # OUTPUT ###########################
    if MainParameters['returnALL']: 
        CORE.results=results 
        CORE.Comments = MainParameters['Comments']
        return CORE

    if MainParameters['save']:
        Savefold = MainParameters['savepath']
        
        
        
        
        
# #############################################################################
# #############################################################################
#                   Handle bash
# #############################################################################


if __name__ ==  '__main__':

    #!#!#!#! THERE ARE ARGUMENTS MISSING FOR THE MOMENT 
    
    # executable help
    msg = """Thus function does this and that"""

    # Instanciate parser                                                        
    parser = argparse.ArgumentParser(description=msg)

    # Define input arguments                                                                                 
    parser.add_argument(
        '-p',
        '--plot',
        type=CheckInput._str2bool,
        help='flag indicating whether to plot figures',
        default=_DEFAULTPARAMETERS['plot'],
        required=False,
    )
    parser.add_argument(
        '-t',
        '--timeit',
        type=CheckInput._str2bool,
        help='flag indicating whether to time the computation',
        default=_DEFAULTPARAMETERS['timeit'],
        required=False,
    )
    parser.add_argument(
        '-s',
        '--save',
        type=CheckInput._str2boolNone,
        help='flag indicating whether to save data',
        default=_DEFAULTPARAMETERS['save'],
        required=False,
    )
    parser.add_argument(
        '-sp',
        '--savepath',
        type=str,
        help='path where to save data',
        default=_DEFAULTPARAMETERS['savepath'],
        required=False,
    )
    kwdargs = dict(parser.parse_args()._get_kwargs())

    # Call function                                                             
    run(**kwdargs)




