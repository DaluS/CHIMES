
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
from .._config import _LMODEL_ATTR
from .._config import _LTYPES
from .._config import _LTYPES_ARRAY
from .._config import _LEQTYPES
from .._config import _LEXTRAKEYS
from .._config import _FROM_USER, _PATH_PRIVATE_MODELS, _PATH_MODELS
from .._config import _MODEL_NAME_CONVENTION
from .._config import _DEFAULTSIZE

###############################################################################
#############                  MAIN FUNCTION                      #############
###############################################################################

# %% MAIN FUNCTION : LOAD MODEL
def load_model(model=None, verb=None, from_user=None):
    """ Load a model from a model file

    model can be:
        - a model name:
            - from_user = False => loaded from the library
            - from_user = True => loaded the user's personal .pygemmes folder
        - the absolute path to an abitrary model file
    """

    # LOAD THE FILE AND THE LIBRARY ###########################################
    #_class_check_2.model_name(model, from_user, verb=verb)

    dmodel = load_dmodel(model, from_user=None)
    dfields = load_complete_DFIELDS(dmodel, verb=verb)
    _class_check_2.dmodel(dmodel)


    # CREATE DPARAM ###########################################################
    dparam = logics_into_dparam(dmodel)
    dparam = add_numerical_group_default_fields(dparam, dfields)

    """ Extract fixed-value parameters"""
    dparam, lparam = extract_parameters(dparam, dfields, verb=verb)
    dparam = set_args_auxilliary(dparam,verb=verb)
    dfunc_order = set_func_order(dparam, verb=verb)
    dfunc_order['parameters'] = lparam

    #_class_check_2.dparam(dparam)

    # Initial values and shapes
    dparam = set_shapes_values(dparam, dfunc_order, verb=verb)

    # Big dictionnary of pointers
    dargs = get_dargs_by_reference(dparam, dfunc_order=dfunc_order)

    return dmodel, dparam, dfunc_order, dargs

# #############################################################################
# ###########                 SUB FUNCTION                        #############
# #############################################################################

# %% 1) LOAD_DMODEL
def load_dmodel(model, from_user=False):
    """
    Load the model from its file
    """

    path_models,_DMODEL = _models._get_DMODEL(model)

    if model not in _DMODEL.keys():
        modellist = "".join(['* '+str(f)+"\n" for f in list(_DMODEL.keys())])
        raise Exception(f'The model you asked, {model}, cannot be found. Found models are \n{modellist}'
                        f'...Maybe you mispelled it ?')
    dmodel=_DMODEL[model]
    dmodel['preset']=None
    dmodel['name'] = model

    # %% Complete size vector
    for k,v in dmodel['logics'].get('size',{}).items():
        if 'value' not in v.keys():
            v['value']= len(v['list'])
        elif 'list' not in v.keys():
            v['list']= [i for i in range(v['value'])]
        else :
            if len(v['list'])!=v['value']:
                raise Exception(f'{k} has inconsistent size and list !')


    return dmodel



def load_complete_DFIELDS(dmodel, verb=False):
    '''
    Identify fields not existing in library, and add them to it, then complete
    '''
    # %% a) get access to dfields
    DFIELDS = copy.deepcopy(_models._DFIELDS)

    # %% b) find what needs to be added
    dkout = {
        k0: [k1 for k1 in v0.keys() if k1 not in DFIELDS]
        for k0, v0 in dmodel['logics'].items()
        if any([k1 for k1 in v0.keys() if k1 not in DFIELDS])
    }
    if verb is True:
        lstr = [f'\t- {k0}: {v0}' for k0, v0 in dkout.items()]
        print(
            f"The following fields are defined in the model but not it the library :")
        for k0, v0 in dkout.items():
            print(f'\t- {k0}: {v0}')

    # %% c) add them
    for k0, v0 in dkout.items():
        for k1 in v0:
            #print(k0,v0,k1)
            #print(dmodel['logics'][k0])
            DFIELDS[k1] = dict(dmodel['logics'][k0][k1])
            # _models._DFIELDS[k1]['eqtype'] = k0
            # _models._DFIELDS[k1]['args'] = {key:[] for key in _LEQTYPES }
            # _models._DFIELDS[k1]['kargs']= []



    # %% d) use dfields autocompletion
    DFIELDS2 = _models._complete_DFIELDS(
        dfields=DFIELDS,
        complete=True,
        check=True,
    )

    return DFIELDS2


# %% 3) LOGICS INTO DPARAM

def logics_into_dparam(dmodel):
    """
    Takes dmodel and translate the logics
    """

    # %% a) convert logics formalism into dparam formalism
    lk = [dict.fromkeys(v0.keys(), k0) for k0, v0 in dmodel['logics'].items()]
    for ii, dd in enumerate(lk[1:]):
        lk[0].update(dd)

    dparam = {
        k0: dict(dmodel['logics'][v0][k0]) for k0, v0 in lk[0].items()
    }



    # %% b) Add eqtype
    for k0 in dparam.keys():
        if lk[0][k0] not in ['parameter']:
            dparam[k0]['eqtype'] = lk[0][k0]

    # %% c) Add correct size
    for k0 in dparam.keys():
        if len(dparam[k0].get('size',[_DEFAULTSIZE]))<2 :
            dparam[k0]['size']=[dparam[k0].get('size',[_DEFAULTSIZE])[0],
                                _DEFAULTSIZE ]


        
    return dparam


# %% 4) ADD NUMERICAL GROUP AND DEFAULT FIELDS

def add_numerical_group_default_fields(dparam, dfields):
    """
    complete dparam with numerical parameters
    """
    # %% a) add numerical parameters if not included

    lknum = [
        k0 for k0, v0 in dfields.items()
        if v0['group'] == 'Numerical'
    ]
    for k0 in lknum:
        if k0 not in dparam.keys():
            dparam[k0] = dfields[k0]

    if 'time' not in dparam.keys():
        dparam['time'] = dict(dfields['time'])



    # %% b) add default fields
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
            if v0['eqtype'] == 'differential' and not 'initial' in v0.keys():
                v0['initial'] = dfields[k0]['value']
    return dparam

# %% 5) EXTRACT PARAMETERS


def extract_parameters(dparam, dfields, verb=None):
    """ Extract fixed-value parameters

    If relevant, the list of fixed-value parameters is extracted from
        the func kwdargs
    """

    # %% a) Identify what is a parameter or not from start
    lpar = [k0 for k0, v0 in dparam.items() if v0.get('func') is None]
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]
    lpar_new = []
    lfunc_new = []


    # %% b) try to check if their inputs corresponds and add them if necessary
    keepon = True
    while keepon:
        lp, lf = _extract_par_from_func(
            lfunc=lfunc + lfunc_new,
            lpar=lpar + lpar_new,
            dparam=dparam,
            dfields=dfields
        )
        if len(lp)+len(lf) > 0:
            if len(lp) > 0:
                lpar_new += lp
            if len(lf) > 0:
                lfunc_new += lf
        else:
            keepon = False
        

    # %% c) if a key is unknown form dfields but exit in model, add it
    if len(lpar_new + lfunc_new) > 0:
        dfail = {}
        for k0 in lpar_new + lfunc_new:
            key =  k0
            if key not in _models._DFIELDS.keys():
                dfail[k0] = "Unknown parameter"
                continue
            dparam[key] = dict(_models._DFIELDS[key])

        # Error message
        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following unknown parameters have been identified:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    # print
    if verb is True:
        msg = (
            "The following fields are identified as parameters :\n"
            f"\t- independant : {lpar_new}\n"
            f"\t- function of other parameters : {lfunc_new}"
        )
        print(msg)

    for k0 in dparam.keys():
        if len(dparam[k0].get('size',[_DEFAULTSIZE]))<2 :
            dparam[k0]['size']=[dparam[k0].get('size',[_DEFAULTSIZE])[0],
                                _DEFAULTSIZE ]
    return dparam, lpar_new+lfunc_new+lpar


def _extract_par_from_func(lfunc=None, lpar=None, dparam=None, dfields=None):
    '''
    Subroutine of extract_parameters using inspection
    '''
    lpar_add, lfunc_add = [], []
    lkok = lpar + lfunc
    ERRORS=[]
    for k0 in lfunc:
        key =  k0

        if k0 in dparam.keys():
            kargs = inspect.getfullargspec(dparam[key]['func']).args
        else:
            kargs = inspect.getfullargspec(dfields[key]['func']).args
        

        # check if any parameter is unknown
        for kk in kargs:
            key = kk
            if key not in lkok:
                try:
                    if _models._DFIELDS[key].get('func') is None:
                        if key not in lpar_add:
                            lpar_add.append(key)
                    elif key not in lfunc_add:
                        lfunc_add.append(key)
                except BaseException:
                    ERRORS.append([key])
    if ERRORS:
        raise Exception(f'Some fields cannot be found, check your model file and `def_fields` !: {ERRORS}')
    return lpar_add, lfunc_add

# %% 6) SET ARGS, KARGS, FIND AUXILLIARIES


def set_args_auxilliary(dparam, verb=False):
    '''
    Get all dependencies for each equations, find who can not be usefull
    Set args and kargs
    '''
    lfunc = [k0 for k0, v0 in dparam.items() if v0.get('func') is not None]

    # %% a) find args and kargs
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
            'parameter': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'parameter'
            ],
            'differential': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'differential'
            ],
            'statevar': [
                kk for kk in kargs
                if kk in lfunc
                and dparam[kk]['eqtype'] == 'statevar'
            ],
        }

    # %% b) write source material
    for k0 in lfunc:
        sour = inspect.getsource(dparam[k0]['func']).replace(
            '    ', '').split('\n')[0]

        
        # Extract kargs and exp (for lambda only)
        if sour.replace(' ', '').count("'func':lambda") == 1:
            # clean-up source
            sour = sour.strip().replace(',\n', '').replace('\n', '')
            sour = sour[sour.index("lambda") + len("lambda"):]
            # separate keyword args from expression
            kargs, exp = sour.split(':')[:2]

            #print(k0,lfunc)

            # store exp for lambda only
            dparam[k0]['source_exp'] = exp.strip().split('#')[0].split('}')[0][:]
        else:
            kargs = sour[sour.index('(') + 1:sour.index(')')]
            dparam[k0]['source_exp'] = dparam[k0]['func'].__name__

        # store keyword args and cleaned-up expression separately
        kargs = [kk.strip() for kk in kargs.strip().split(',')]
        kargs = ', '.join(kargs)
        #
        # dparam[k0]['source_kargs'] = kargs


    # %% c) find auxilliary
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
            if c0:
                dparam[k0]['isneeded'] = False
                News += k0

            else:
                dparam[k0]['isneeded'] = True
        if len(News) == 0:
            keep = False



    # print
    if verb:
        print("The following variables are identified as auxilliary :")
        print(
            f"\t - differential : {[k for k in lfunc if (not dparam[k].get('isneeded',False) and dparam[k]['eqtype']=='differential')]}")
        print(
            f"\t - state variable : {[k for k in lfunc if (not dparam[k].get('isneeded',False) and dparam[k]['eqtype']=='statevar')]}")

    return dparam

def set_func_order(dparam, verb=False):
    '''
    Find equation resolution order
    '''
    # %% a) subroutine for each group
    dfunc_order = {
        k0: _suggest_funct_order_by_group(eqtype=k0, dparam=dparam)
        for k0 in ['parameter', 'statevar', 'differential']
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
                msg+= f"Sorted :{lfsort} \n remaining {list(set(lf)-set(lfsort))}"
                raise Exception(msg)

    except Exception as err:
        if eqtype == 'differential':
            # function order not necessary => pick any order
            lfsort = [
                kk for kk, vv in dparam.items()
                if vv.get('eqtype') == eqtype
            ]
        else:
            # For 'statevar' and 'parameter' a function order is necessary => raise
            raise err

    return lfsort

# %% 8) GET DARCS


def get_dargs_by_reference(dparam, dfunc_order):
    '''
    Big dictionnary of pointers
    '''
    # %% a) create the dictionnary of pointers
    #for k0 in dfunc_order['statevar'] + dfunc_order['differential']:
    #    print(k0,dparam[k0]['args'].keys())

    dargs = {
        k0: {
            k1: dparam[k1]['value']
            for k1 in (
                dparam[k0]['args']['differential']
                + dparam[k0]['args']['statevar']
                + dparam[k0]['args'][None]
            )
        }
        for k0 in dfunc_order['statevar'] + dfunc_order['differential']
    }

    return dargs

# %% 8) INITIALISE SHAPE


def set_shapes_values(dparam, dfunc_order, verb=True):

    # run all parameters func to set their values
    for k0 in dfunc_order['parameter']:
        dargs = {
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args'][None]
        }
        dargs.update({
            k1: dparam[k1]['value']
            for k1 in dparam[k0]['args']['parameter']
        })
        dparam[k0]['value'] = dparam[k0]['func'](**dargs)

    # ------------------
    # copy func to avoid passing by reference
    lfunc = [k0 for k0, v0 in dparam.items() if (v0.get('func') is not None)]
    lpar = [k0 for k0, v0 in dparam.items() if (v0.get('func') is None
                                                and not (v0.get('eqtype') == 'size'
                                                or v0.get('group') == 'Numerical')) ]
    # --------------------------------
    # set default values of parameters to their real values
    # this way we don't have to feed the parameters value inside the loop
    _update_func_default_kwdargs(lfunc=lfunc, dparam=dparam)

    # -------------------------------------------
    # Create variables for all varying quantities

    for k0 in lfunc:
        sizes = [ dparam[f]['value'] for f in dparam[k0]['size']]

        shape = tuple(np.r_[dparam['nt']['value'],  # Time dimension
                            dparam['nx']['value'],  # Parrallel
                            dparam['nr']['value'],  # Regions
                            sizes
                            ])

        if dparam[k0]['eqtype'] not in ['parameter']:
            dparam[k0]['value'] = np.full(shape, np.nan)
        if dparam[k0]['eqtype']=='differential':
            dparam[k0]['initial']=np.full(shape[1:], dparam[k0]['initial'])

    for k0 in lpar:
        sizes = [ dparam[f]['value'] for f in  dparam[k0]['size']]
        shape = tuple(np.r_[dparam['nx']['value'],  # Parrallel
                            dparam['nr']['value'],  # Regions
                            sizes
                            ])

        #### THIS PART SHOULD BE REMOVED, BAD PATCH
        if len(shape)==len(np.shape(dparam[k0]['value'])):
            shp = np.shape(dparam[k0]['value'])
            change=False

            for ii,k in enumerate(shape):
                if (shp[ii]!=k and shp[ii]!=1):
                    print(f'WARNING : projection of {k0} on first scalar value. Are you sure about your dimensions ?')
                    change=True
                    break
            if change:
                #print(dparam[k0]['value'])
                dparam[k0]['value']= dparam[k0]['value'][0,0,0,0]


        dparam[k0]['value'] = np.full(shape, dparam[k0]['value'])

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
        kargs = dparam[k0]['kargs']
        defaults = len(kargs)*[0]

        # update using fixed param (eqtype = None)

        for k1 in dparam[k0]['args'][None]:
            key = k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[key]['value']

            ind = [ii for ii, vv in enumerate(
                kargs) if k1 == vv.split('=')[0]]

            if len(ind) != 1:
                msg = f"Inconsistency in (fixed) kargs for {k0}, {k1}"
                raise Exception(msg)

            #kargs[ind[0]] = "{}={}".format(key, dparam[key]['value'])  # test

        # update using param


        for k1 in dparam[k0]['args']['parameter']:
            key =  k1
            defaults[dparam[k0]['kargs'].index(k1)] = dparam[k1]['value']
            ind = [ii for ii, vv in enumerate(kargs) if key in vv]
            if len(ind) != 1:
                msg = f"Inconsistency in (func) kargs for {k0}, {k1}"
                raise Exception(msg)
            #kargs[ind[0]] = "{}={}".format(key, dparam[k1]['value'])



        # update
        dparam[k0]['func'].__defaults__ = tuple(defaults)
        # dparam[k0]['source_kargs'] = ', '.join(kargs)
    return dparam
