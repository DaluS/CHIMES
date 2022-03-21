# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:53:27 2022

@author: Paul Valcke
"""

# classic libraries
import numpy as np
import inspect
import functools
import os
import importlib
import copy
import types

# library specific
from . import _class_check_2
from .. import _models
from ..__config import _LMODEL_ATTR, _DMODEL_KEYS, _LTYPES, _LTYPES_ARRAY, _LEQTYPES, _LEXTRAKEYS
from ..__config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS
from ..__config import _MODEL_NAME_CONVENTION

###############################################################################
#############                  MAIN FUNCTION                      #############
###############################################################################


def load_model(model=None, verb=None, from_user=None):
    """ Load a model from a model file

    model can be:
        - a model name:
            - from_user = False => loaded from the library
            - from_user = True => loaded the user's personal .pygemmes folder
        - the absolute path to an abitrary model file

    """

    # LOAD THE FILE AND THE LIBRARY ###########################################
    # _class_check_2.model_name(model, from_user, verb=verb)
    dmodel = load_dmodel(model, from_user=None)
    dfields = load_complete_DFIELDS(dmodel, verb=verb)
    # _class_check_2.dmodel(dmodel)

    # CREATE DPARAM ###########################################################
    dparam = logics_into_dparam(dmodel)
    dparam = add_numerical_group(dparam)

    '''Put all the default characteristics from dfield'''
    dparam = add_default_fields(dparam, dfields)

    """ Extract fixed-value parameters
    If relevant, the list of fixed-value parameters is extracted from
        the func kwdarg"""
    dparam, lparam = extract_parameters(dparam, verb=verb)

    # _class_check_2.dparam(dparam)

    '''Get all dependencies for each equations, find who can not be usefull
    Set args and kargs'''
    dparam = set_args_auxilliary(dparam)

    # _class_check_2.functions(dparam)

    '''Find order of resolution, parameters are just for same formalism'''
    dfunc_order = set_func_order(dparam, verb=verb)
    dfunc_order['parameters'] = lparam

    '''Initial values and shapes'''
    param = set_shapes_values(dparam, dfunc_order, verb=verb)

    '''Big dictionnary of pointers'''
    dargs = get_dargs_by_reference(dparam, dfunc_order=dfunc_order)

    return dmodel, dparam, dfunc_order, dargs

###############################################################################
#############                 SUB FUNCTION                        #############
###############################################################################


def load_dmodel(model, from_user=False):
    """
    Load the model from its file
    """

    # CHOOSE THE FOLDER
    if from_user is True and _PATH_PRIVATE_MODELS is not None:
        path_models = _PATH_PRIVATE_MODELS
    else:
        path_models = _PATH_MODELS

    # LOAD THE MODEL
    file_address = _MODEL_NAME_CONVENTION + model + '.py'
    pfe = os.path.join(path_models, file_address)
    spec = importlib.util.spec_from_file_location(file_address, pfe)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    dmodel = {
        'logics': {k0: dict(v0) for k0, v0 in foo._LOGICS.items()},
        'file': foo.__file__,
        'description': foo.__doc__,
        'presets': {k0: dict(v0) for k0, v0 in foo._PRESETS.items()},
        'name': model,
    }

    return dmodel


def load_complete_DFIELDS(dmodel, verb=False):
    '''
    Identify fields not existing in library, and add them to it, then complete
    '''
    DFIELDS = copy.deepcopy(_models._DFIELDS)

    dkout = {
        k0: [k1 for k1 in v0.keys() if k1 not in DFIELDS]
        for k0, v0 in dmodel['logics'].items()
        if any([k1 for k1 in v0.keys() if k1 not in DFIELDS])
    }
    if verb is True:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dkout.items()]
        print(
            f"Fields defined in the model but not it the library : \n    - {lstr} ")

    for k0, v0 in dkout.items():
        for k1 in v0:
            DFIELDS[k1] = dict(dmodel['logics'][k0][k1])
            # _models._DFIELDS[k1]['eqtype'] = k0
            # _models._DFIELDS[k1]['args'] = {key:[] for key in _LEQTYPES }
            # _models._DFIELDS[k1]['kargs']= []

    DFIELDS = _models._complete_DFIELDS(
        dfields=DFIELDS,
        complete=True,
        check=True,
    )
    return DFIELDS


def logics_into_dparam(dmodel):
    """
    Takes dmodel and translate the logics
    """
    # convert logics (new formalism) to dparam
    lk = [dict.fromkeys(v0.keys(), k0) for k0, v0 in dmodel['logics'].items()]
    for ii, dd in enumerate(lk[1:]):
        lk[0].update(dd)

    dparam = {
        k0: dict(dmodel['logics'][v0][k0]) for k0, v0 in lk[0].items()
    }

    # Add eqtype
    for k0 in dparam.keys():
        if lk[0][k0] not in ['param']:
            dparam[k0]['eqtype'] = lk[0][k0]
    return dparam


def add_numerical_group(dparam):
    """
    complete dparam with numerical parameters
    """
    # ---------------------------------------
    # add numerical parameters if not included

    lknum = [
        k0 for k0, v0 in _models._DFIELDS.items()
        if v0['group'] == 'Numerical'
    ]
    for k0 in lknum:
        if k0 not in dparam.keys():
            dparam[k0] = _models._DFIELDS[k0]

    if 'time' not in dparam.keys():
        dparam['time'] = dict(_models._DFIELDS['time'])

    return dparam


def add_default_fields(dparam, dfields):
    '''
    Put all the default characteristics from dfield
    '''
    for k0, v0 in dparam.items():

        # if value directly provided => put into dict
        if v0 is None or type(v0) in _LTYPES + _LTYPES_ARRAY + [str, bool]:
            dparam[k0] = {'value': v0}

        if isinstance(dparam[k0], dict):
            # set missing field to default
            for ss in dfields[k0].keys():
                if dparam[k0].get(ss) is None:
                    dparam[k0][ss] = dfields[k0][ss]

        # initial ODE handling
        if 'eqtype' in v0.keys():
            if v0['eqtype'] == 'ode' and not 'initial' in v0.keys():
                v0['initial'] = dfields[k0]['value']
    return dparam


def extract_parameters(dparam, verb=True):
    """ Extract fixed-value parameters

    If relevant, the list of fixed-value parameters is extracted from
        the func kwdargs
    """

    lpar = [k0 for k0, v0 in dparam.items() if v0.get('func') is None]
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
    lpar_new = []
    lfunc_new = []

    # ---------------------------------------
    # extract input args and check conformity
    keepon = True
    while keepon:
        lp, lf = _extract_par_from_func(
            lfunc=lfunc + lfunc_new,
            lpar=lpar + lpar_new,
            dparam=dparam,
        )
        if len(lp)+len(lf) > 0:
            if len(lp) > 0:
                lpar_new += lp
            if len(lf) > 0:
                lfunc_new += lf
        else:
            keepon = False

    if len(lpar_new + lfunc_new) > 0:
        dfail = {}
        for k0 in lpar_new + lfunc_new:
            key = 'lambda' if k0 == 'lamb' else k0
            if key not in _models._DFIELDS.keys():
                dfail[k0] = "Unknown parameter"
                continue
            dparam[key] = dict(_models._DFIELDS[key])

        # -------------------
        # Raise Exception if any
        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following unknown parameters have been identified:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    # -------------
    # print
    if verb is True:
        msg = (
            "The following fields are identified as parameters :\n"
            f"\t- param (fixed): {lpar_new}\n"
            f"\t- param (func.): {lfunc_new}"
        )
        print(msg)

    return dparam, lpar_new+lfunc_new


def _extract_par_from_func(lfunc=None, lpar=None, dparam=None):

    lpar_add, lfunc_add = [], []
    lkok = ['itself'] + lpar + lfunc
    for k0 in lfunc:
        key = 'lambda' if k0 == 'lamb' else k0

        if k0 in dparam.keys():
            kargs = inspect.getfullargspec(dparam[key]['func']).args
        else:
            kargs = inspect.getfullargspec(_models._DFIELDS[key]['func']).args

        # check if any parameter is unknown
        for kk in kargs:
            key = 'lambda' if kk == 'lamb' else kk
            if key not in lkok:
                if _models._DFIELDS[key].get('func') is None:
                    if key not in lpar_add:
                        lpar_add.append(key)
                elif key not in lfunc_add:
                    lfunc_add.append(key)

    return lpar_add, lfunc_add


def set_args_auxilliary(dparam, verb=True):
    '''
    Get all dependencies for each equations, find who can not be usefull
    Set args and kargs
    '''
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]

    # Put args and kargs
    for k0 in lfunc:
        # get the args
        v0 = dparam[k0]
        kargs = inspect.getfullargspec(v0['func']).args
        dparam[k0]['kargs'] = kargs
    for k0 in lfunc:
        kargs = [kk for kk in dparam[k0]['kargs'] if kk != 'itself']
        dparam[k0]['args'] = {
            None: [
                kk for kk in kargs
                if kk not in lfunc
            ],
            'param': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'param'
            ],
            'ode': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'ode'
            ],
            'statevar': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'statevar'
            ],
        }

    # Source reading
    for k0 in lfunc:
        sour = inspect.getsource(dparam[k0]['func']).replace(
            '    ', '').split('\n')[0]
        # Extract kargs and exp (for lambda only)
        if sour.replace(' ', '').count("'func':lambda") == 1:
            # clean-up source
            sour = sour.strip().replace(',\n', '').replace('\n', '')
            sour = sour[sour.index('lambda') + len('lambda'):]
            # separate keyword args from expression
            kargs, exp = sour.split(':')[:2]

            # store exp for lambda only
            dparam[k0]['source_exp'] = exp.strip()
        else:
            kargs = sour[sour.index('(') + 1:sour.index(')')]
            dparam[k0]['source_name'] = dparam[k0]['func'].__name__

        # store keyword args and cleaned-up expression separately
        kargs = [kk.strip() for kk in kargs.strip().split(',')]
        kargs = ', '.join(kargs)
        dparam[k0]['source_kargs'] = kargs

    # Find auxilliary
    keep = True
    while keep:
        News = []
        lfunc2 = [k0 for k0, v0 in dparam.items() if v0.get(
            'func') is not None and v0.get('isneeded', True)]
        for k0 in lfunc2:
            # check dependencies
            c0 = (
                not any([k0 in dparam[k1]['kargs'] for k1 in lfunc2])
            )
            if k0 == 'lambda':
                c0 = (
                    not any(['lamb' in dparam[k1]['kargs'] for k1 in lfunc2])
                )
            if c0:
                dparam[k0]['isneeded'] = False
                News += k0

            else:
                dparam[k0]['isneeded'] = True
        if len(News) == 0:
            keep = False

    if verb:
        print("The following variables are identified as auxilliary :")
        print(
            f"\t - ode : {[k for k in lfunc if (not dparam[k]['isneeded'] and dparam[k]['eqtype']=='ode')]}")
        print(
            f"\t - statevar : {[k for k in lfunc if (not dparam[k]['isneeded'] and dparam[k]['eqtype']!='ode')]}")
    return dparam


def set_func_order(dparam, verb=False):
    '''
    Find equation resolution order
    '''
    dfunc_order = {
        k0: _suggest_funct_order_by_group(eqtype=k0, dparam=dparam)
        for k0 in ['param', 'statevar', 'ode']
    }

    if verb is True:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfunc_order.items()]
        msg = (
            "The following order has been determined for functions:\n"
            + "\n".join(lstr)
        )
        print(msg)
    return dfunc_order


def _suggest_funct_order_by_group(eqtype=None, dparam=None):
    """ Here we find a natural order for function of the same group

    """

    # Prepare list of relevant functsions
    lf = [kk for kk, vv in dparam.items() if vv.get('eqtype') == eqtype]

    try:
        lfsort = []
        keepon = True
        ntry = 0
        while keepon:

            # Identify func that can be sorted
            for kk in lf:
                if kk in lfsort:
                    continue
                elif len(dparam[kk]['args'][eqtype]) == 0:
                    lfsort.append(kk)
                elif all([k1 in lfsort for k1 in dparam[kk]['args'][eqtype]]):
                    lfsort.append(kk)

            # evaluate termination condition
            ntry += 1
            if set(lf) == set(lfsort):
                keepon = False
            elif ntry == len(lf) - 1:
                msg = f"No sorting order of func could be found for {eqtype}"
                raise Exception(msg)

    except Exception as err:
        if eqtype == 'ode':
            # function order not necessary => pick any order
            lfsort = [
                kk for kk, vv in dparam.items()
                if vv.get('eqtype') == eqtype
            ]
        else:
            # For 'statevar' and 'param' a function order is necessary => raise
            raise err

    return lfsort


def get_dargs_by_reference(dparam, dfunc_order):
    '''
    Big dictionnary of pointers
    '''
    dargs = {
        k0: {
            k1: dparam[k1]['value']
            for k1 in (
                dparam[k0]['args']['ode']
                + dparam[k0]['args']['statevar']
            )
            if k1 != 'lambda'
        }
        for k0 in dfunc_order['statevar'] + dfunc_order['ode']
    }

    # Handle the lambda exception here to avoid test at every time step
    # if lambda exists and is a function
    c0 = (
        'lambda' in dparam.keys()
        and dparam['lambda'].get('func') is not None
    )
    # then handle the exception
    for k0, v0 in dargs.items():
        if c0 and 'lambda' in dparam[k0]['kargs']:
            dargs[k0]['lamb'] = dparam['lambda']['value']


def set_shapes_values(dparam, dfunc_order, verb=True):
    # run all param func to set their values
    for k0 in dfunc_order['param']:
        dargs = {
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args'][None]
        }
        dargs.update({
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args']['param']
        })
        dparam[k0]['value'] = dparam[k0]['func'](**dargs)

    # ------------------
    # copy func to avoid passing by reference
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
    for k0 in lfunc:
        dparam[k0]['func'] = copy_func(dparam[k0]['func'])

    # --------------------------------
    # set default values of parameters to their real values
    # this way we don't have to feed the parameters value inside the loop
    _update_func_default_kwdargs(lfunc=lfunc, dparam=dparam)

    # -------------------------------------------
    # Create variables for all varying quantities
    shape = tuple(np.r_[dparam['nt']['value'], 1])
    for k0 in lfunc:
        if dparam[k0]['eqtype'] not in ['param']:
            dparam[k0]['value'] = np.full(shape, np.nan)
    return dparam


def copy_func(func):
    """
    Based on:
        http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)
        https://stackoverflow.com/questions/13503079 (unutbu)
    """
    func2 = types.FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )
    func2 = functools.update_wrapper(func2, func)
    func2.__kwdefaults__ = func.__kwdefaults__
    return func2


def _update_func_default_kwdargs(lfunc=None, dparam=None):
    """ Here we update the default valuee of all functions """

    # For each function (ode and statevar)
    for k0 in lfunc:
        # get defaults
        kargs = dparam[k0]['source_kargs'].split(', ')
        defaults = len(kargs)*[0]

        print(k0, dparam[k0]['args'])
        # update using fixed param (eqtype = None)
        for k1 in dparam[k0]['args'][None]:
            key = 'lambda' if k1 == 'lamb' else k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[key]['value']

            ind = [ii for ii, vv in enumerate(
                kargs) if k1 == vv.split('=')[0]]

            print(k1, defaults, kargs, ind)

            if len(ind) != 1:
                msg = f"Inconsistency in (fixed) kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[key]['value'])  # test

        # update using param
        for k1 in dparam[k0]['args']['param']:
            key = 'lamb' if k1 == 'lambda' else k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key in vv]
            if len(ind) != 1:
                msg = f"Inconsistency in (func) kargs for {k0}, {k1}"
                raise Exception(msg)
            kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])

        # update
        dparam[k0]['func'].__defaults__ = tuple(defaults)
        # dparam[k0]['source_kargs'] = ', '.join(kargs)
    return dparam
