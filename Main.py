#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This python code has been created to simulate Goodwin-Keen simulations, with all the variants to it.
Do not worry about the number of section : the architecture is thought to be user-friendly and coder-friendly

The algorithm solve parNum['Nx'] system in parrallel : the idea is that later we will couple the systems altogether ("spatial/network properties").

For now, there is no much coupling, but you can use it to test many initial conditions and array of parameters values

The steps are :
    - Creation of the parameters dictionnaries
        * params   : The physical parameters
        * parNum   : The numerical parameters
        * initCond : The initial vector state
    - Translation into machine friendly variable y
    - Calculation of all the dynamics variable Y_s (the temporal loop)
    - Translation into user-friendly result in the dictionnary results
    - Additional analysis (period, slow enveloppe mouvement...)
    - Plot of variables and analysis through results

HOW TO IMPLEMENT YOUR TOY-MODEL ?
    0 Go in ClassesGoodwin
    1 Copy one version that looks alike (typically choose between intensive and extensive type)
    2 Change the name
    3 Change the list of hypothesis in the class description\
    4 Create your list of variables, parameters
    5 Code intermediary functions ( combination of variable and parameters that are practical)
    6 Add them in intermediaryfuncs
    7 Change the core ( self.f ) of the dynamics
    8 Change the list of plots

WHAT I AM (Paul) LOOKING FOR IN FURTHER DEVELOPMENT
* An Extensive dynamical model
* Add spatial operators which are non unstable ( I have implicit scheme elsewhere but it's a different kind of resolution, and much more work when you change a model)
* Have a list of all models existing in this framework (copingwithcollapse, Harmoney, predatory-prey...) and code them
* The plots are UGLY ! Let's do something nicer
* As Iloveclim and Dymends are not in python, prepare some bindings
"""

# Built-in
import os
import time                     # Time (run speed) printing
import argparse


# Library-specific
import Parameters as Par        # All the parameters of the system
import ClassesGoodwin as C      # Core of models
import Miscfunc as M            # All miscellaneous functions
import VariableDictionnary as VarD # Useful infos on variables
import plots as plts            # Already written plot functions

# Default parameter values
_PLOT = True
_TIMEIT = True
_SAVE = 'None'
_SAVEPATH = os.path.dirname(__file__)   # Not hard-coded, platform-independent

# #############################################################################
#                   Uilities In ArgParsing
# #############################################################################

def _str2bool(arg):
    if isinstance(arg, bool):
        return arg
    elif arg.lower() in ['yes', 'true', 'y', 't', '1']:
        return True
    elif arg.lower() in ['no', 'false', 'n', 'f', '0']:
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected!')


def _str2boolNone(arg):
    if isinstance(arg, bool):
        return arg
    elif arg.lower() in ['yes', 'true', 'y', 't', '1']:
        return True
    elif arg.lower() in ['no', 'false', 'n', 'f', '0']:
        return False
    elif arg.lower() in ['none']:
        return None
    else:
        raise argparse.ArgumentTypeError('Boolean value expected!')


def _check_bool(var=None, varname=None, vardef=None):
    """ Check conformity of bool argument """
    if var is None:
        var = vardef
    c0 = isinstance(var, bool)
    if not c0:
        msg = (
            "Arg {} must bea bool!\n".format(varname)
            + "You provided:\n\t{}".format(var)
        )
        raise Exception(msg)
    return var


def _check_inputs(
    plot=None,
    timeit=None,
    save=None,
    savepath=None,
):

    # plot
    plot = _check_bool(var=plot, varname='plot', vardef=_PLOT)

    # timeit
    timeit = _check_bool(var=timeit, varname='timeit', vardef=_TIMEIT)

    # save
    if save is None:
        save = _SAVE
    c0 = save in ['None', True, False]
    if not c0:
        msg = (
            "Arg save must be:\n"
            + "\t- 'None': falls back to param['Save']\n"
            + "\t- True: save data\n"
            + "\t- False: don't save data\n"
            + "You provided:\n\t{}".format(save)
        )
        raise Exception(msg)

    # savepath
    if savepath is None:
        savepath = _SAVEPATH
    c0 = isinstance(savepath, str) and os.path.isdir(savepath)
    if not c0:
        msg = (
            "Arg savepath must be a path to a valid directory!\n"
            + "You provided:\n\t{}".format(savepath)
        )
        raise Exception(msg)

    return plot, timeit, save, savepath

# #############################################################################
# #############################################################################
#                   Main function
# #############################################################################


def run(
    plot=None,
    timeit=None,
    save=None,
    savepath=None,
):
    """ Run the simulation

    Details

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

    """

    #  check inputs ###################
    # #################################    

    plot, timeit, save, savepath = _check_inputs(
        plot=plot,
        timeit=timeit,
        save=save,
        savepath=savepath,
    )

    #  Initialize system of equations #
    # #################################    
    eqsys = C.GK_Reduced()  

    # PARAMETERS INITIALISATION #######
    # #################################    

    parNum   = Par.parnum()                     # Value of numerical parameters 
    params   = Par.BasicParameters()            # Value of "Physical" parameters 
    params   = Par.Modifications (params, parNum) # Original modification you might want to do
    initCond = Par.initCond(params ,parNum)     # Values of the initial parameters
    op       = M.prepareOperators(parNum)       # Spatial operators initialisation
    params   = eqsys.keepUsefulParams( params )   # Cleaning the params dictionnary to be lighter 

    # VERBATIM FOR THE USER ###########
    ###################################
    if parNum['verb']:
        print(eqsys.description)
        eqsys.printParameters(params)
        M.PrintNumericalparameters(parNum)


    # TIME RESOLUTION #################
    ###################################
    if timeit is True:
        tim = time.time()
        print('Start simulation...', end='')

    y = eqsys.initializeY(initCond, parNum) # vector y contains all states of time t.
    Y_s, t_s = M.TemporalLoop(y, eqsys, op, parNum, params) # Calculation of all timesteps

    if timeit is True:
        time_elasped = time.time()-tim
        print('done! elapsed time: {} s'.format(time_elasped))


    # Results interpretation ##########
    # #################################

    """Now the simulation is done => translate results to more readable format
    r = expansion of Y_s into all relevant variables, as a dict
    Then, other parts are simply plots of the result"""
    results = eqsys.expandY_simple(Y_s, t_s, op, params)  # Result dictionnary 
    results = M.getperiods(results, parNum, op)         # Period measurements 

    UsefulVarDic, OrganisedVar = VarD.VariableDictionnary(results)


    # PLOTS ###########################
    # #################################

    if plot is True:
        # eqsys.plotlitst_simple(results,parNum)
        plts.AllUsefulVariablesSeparate(results, UsefulVarDic)
        # plts.OrganisedVar(results,UsefulVarDic, OrganisedVar)


# #############################################################################
# #############################################################################
#                   Handle bash
# #############################################################################


if __name__ ==  '__main__':

    # executable help
    msg = """Thus function does this and that"""

    # Instanciate parser                                                        
    parser = argparse.ArgumentParser(description=msg)

    # Define input arguments                                                                                 
    parser.add_argument(
        '-p',
        '--plot',
        type=_str2bool,
        help='flag indicating whether to plot figures',
        default=_PLOT,
        required=False,
    )
    parser.add_argument(
        '-t',
        '--timeit',
        type=_str2bool,
        help='flag indicating whether to time the computation',
        default=_TIMEIT,
        required=False,
    )
    parser.add_argument(
        '-s',
        '--save',
        type=_str2boolNone,
        help='flag indicating whether to save data',
        default=_SAVE,
        required=False,
    )
    parser.add_argument(
        '-sp',
        '--savepath',
        type=str,
        help='path where to save data',
        default=_SAVEPATH,
        required=False,
    )
    kwdargs = dict(parser.parse_args()._get_kwargs())

    # Call function                                                             
    run(**kwdargs)
