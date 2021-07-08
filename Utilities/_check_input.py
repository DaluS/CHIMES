# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 17:06:50 2021

@author: Paul Valcke
"""
import argparse
import os

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
            _DEFAULTPARAMETERS,
            SystemOfEquation=None,
            InitialDictionnary=None,
            Value_Changes=None,
            plot=None,
            timeit=None,      
            save=None,             
            savepath=None,        
            returnALL=None,       
            Comments=None,
):
    
    """ verification of input validity.
    
    #!#!#! 
    SystemOfEquation   NOT CHECKED FOR THE MOMENT
    InitialDictionnary NOT CHECKED FOR THE MOMENT NOT EVEN IMPLEMENTED
    Value_Changes      NOT CHECKED FOR THE MOMENT a dic of dic quite complex
    returnALL          NOT CHECKED FOR THE MOMENT should be a bool
    Comments           NOT CHECKED FOR THE MOMENT should be a string
    """

    # SystemOfEquations
    #if SystemOfEquation is None:
    SystemOfEquation =_DEFAULTPARAMETERS['SystemOfEquation']

    # InitialDictionnary
    if InitialDictionnary is None:
        InitialDictionnary=_DEFAULTPARAMETERS['InitialDictionnary']  
        
    # Value_Changes   
    if Value_Changes is None:
        Value_Changes = _DEFAULTPARAMETERS['Value_Changes']
 
    # returnALL 
    if returnALL is None:
        returnALL     = _DEFAULTPARAMETERS['returnALL'] 
    
    # Comments
    if Comments is None:
        Comments      = _DEFAULTPARAMETERS['Comments']  
 
    # plot
    plot = _check_bool(var=plot, varname='plot', vardef=_DEFAULTPARAMETERS['plot'])

    # timeit
    timeit = _check_bool(var=timeit, varname='timeit', vardef=_DEFAULTPARAMETERS['timeit'])

    # save
    if save is None:
        save = _DEFAULTPARAMETERS['save']
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
        savepath = _DEFAULTPARAMETERS['savepath']
    c0 = isinstance(savepath, str) and os.path.isdir(savepath)
    if not c0:
        msg = (
            "Arg savepath must be a path to a valid directory!\n"
            + "You provided:\n\t{}".format(savepath)
        )
        raise Exception(msg)
        

    return {'SystemOfEquation' : SystemOfEquation,
            #InitialDictionnary,
            'Value_Changes' : Value_Changes,
            'plot' : plot,
            'timeit' : timeit,
            'save' : save,
            'savepath' : savepath,
            'returnALL' : returnALL,
            'Comments' : Comments
            }