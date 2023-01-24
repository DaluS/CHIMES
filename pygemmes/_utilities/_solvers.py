
# Checked December 2022

# built-in
import time

# common
import numpy as np
from copy import copy,deepcopy

# specific
from . import _class_checks


# #############################################################################
# #############################################################################
#                   Main entry point
# #############################################################################

def solve(
        #solver=None,
        dparam=None,
        dmisc=None,
        dverb=None,
        ComputeStatevarEnd=False,
):
    '''TEMPORAL SOLVER OF THE SYSTEM'''


    lode   = dmisc['dfunc_order']['differential'] # order of differential equations to be solver
    lstate = dmisc['dfunc_order']['statevar']     # Order of state variables to solver
    lparam = dmisc['dfunc_order']['parameter']+dmisc['dfunc_order']['parameters']+['dt'] # All parameters that can be usefull


    # Define initial state and all functions to iterate in order with their references
    y0, dydt_func= get_func_dydt(
        dparam=dparam,
        #dmisc=dmisc,
        lode=lode,
        lstate=lstate,
        lparam=lparam
    )

    # Temporal loop #######################
    y =deepcopy(y0) # initialize y

    # start loop on time
    t0 = time.time()
    for ii in range(1, dparam['nt']['value']):
        # print of wait
        if dverb['verb'] > 0: t0 = _class_checks._print_or_wait(ii=ii, nt=dparam['nt']['value'], t0=t0, **dverb)

        # compute ode variables from ii-1, using solver
        y,state = _rk4( dydt_func=dydt_func,
                        dt=dparam['dt']['value'],
                        y=y,)

        # dispatch to store result of ode
        for k0 in lode:   dparam[k0]['value'][ii, ...] = y[k0]
        if not ComputeStatevarEnd:
            for k0 in lstate: dparam[k0]['value'][ii, ...]= state[k0]


    # compute statevar functions, in good order
    if ComputeStatevarEnd:
        for k0 in lstate:
            dparam[k0]['value'][...] = dparam[k0]['func'](**{k:dparam[k]['value'][...] for k in dparam[k0]['kargs']})


    #return solver

def get_func_dydt(
    dparam=None, # Big dictionnary with values and dependencies
    lode  =None, # ordered list of differential equations
    lstate=None, # ordered list of state variables
    lparam=None  # list of existing parameters   
):
    y0 =      { k : dparam[k]['value'][0, ...] for k in lode}            # initial values
    dydt =    { k : np.full(np.shape(v), np.nan) for k,v in y0.items()}  # will contains time variation 
    dbuffer = { k0: dparam[k0]['value'][0, ...] for k0 in lode}#+lstate}   # buffer containing local calculations
    for k0 in lparam: dbuffer[k0]= dparam[k0]['value']

    def func(
        y,
        dbuffer=dbuffer,
        dydt=dydt,
        dparam=dparam,
    ):
        for k0 in lode:   dbuffer[k0] = y[k0]
        for k0 in lstate: dbuffer[k0] = dparam[k0]['func'](**{k:dbuffer[k] for k in dparam[k0]['kargs']})
        for k0 in lode:   dydt[k0]    = dparam[k0]['func'](**{k:dbuffer[k] for k in dparam[k0]['kargs']})

        #print(f"t    { y['time'][0,0,0,0]:.5f}",
        #      f"y    { y['y']   [0,0,0,0]:.5f}",
        #      f"dydt {dydt['y'] [0,0,0,0]:.5f}" )
        return copy(dydt),dbuffer

    return y0, func


def _eRK4_homemade(
    y0=None,
    dydt_func=None,
    dparam=None,
    lode=None,
    lstate=None,
    nt=None,
    dverb=None,
):
    """ Structure of the homemade rk4 solver, with time loop, intermediaries...
    """

    # initialize y
    y =deepcopy(y0)

    # start loop on time
    t0 = time.time()
    for ii in range(1, nt):
        # print of wait
        if dverb['verb'] > 0: t0 = _class_checks._print_or_wait(ii=ii, nt=nt, t0=t0, **dverb)

        # compute ode variables from ii-1, using solver
        y,state = _rk4( dydt_func=dydt_func,
                        dt=dparam['dt']['value'],
                        y=y,)

        # dispatch to store result of ode
        for k0 in lode:   dparam[k0]['value'][ii, ...] = y[k0]
        for k0 in lstate: dparam[k0]['value'][ii, ...]= state[k0]



def _rk4(dydt_func=None, dt=None, y=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step
    """

    dy1_on_dt,state = dydt_func( y)
    dy2_on_dt,_     = dydt_func({k: y[k] + dy1_on_dt[k] * dt / 2. for k in y.keys()})
    dy3_on_dt,_     = dydt_func({k: y[k] + dy2_on_dt[k] * dt / 2. for k in y.keys()})
    dy4_on_dt,_     = dydt_func({k: y[k] + dy3_on_dt[k] * dt / 1. for k in y.keys()})
    yend =  {k: y[k]+(  dy1_on_dt[k]
                    + 2*dy2_on_dt[k]
                    + 2*dy3_on_dt[k]
                    +   dy4_on_dt[k]) * dt/6  for k in y.keys()}
    '''
    print(f"t    { y['time'][0,0,0,0]:.5f}",
          f"y    { y['y']   [0,0,0,0]:.5f}",
          f"dydt {dy1_on_dt['y'][0,0,0,0]:.5f}" )

    print(f"t    { y['time'][0,0,0,0]+dt/2:.5f}",
          f"y    { y['y']   [0,0,0,0]+dy1_on_dt['y'][0,0,0,0]*dt / 2. :.5f}",
          f"dydt {dy2_on_dt['y'] [0,0,0,0]:.5f}" )

    print(f"t    { y['time'][0,0,0,0]+dt/2:.5f}",
          f"y    { y['y']   [0,0,0,0]+ dy2_on_dt['y'][0,0,0,0] * dt / 2.:.5f}",
          f"dydt {dy3_on_dt['y'] [0,0,0,0]:.5f}" )

    print(f"t    { y['time'][0,0,0,0]+dt:.5f}",
          f"y    { y['y']   [0,0,0,0]+ dy3_on_dt['y'][0,0,0,0] * dt:.5f}",
          f"dydt {dy4_on_dt['y'] [0,0,0,0]:.5f}" )

    print(f"t    { yend['time'][0,0,0,0]:.5f}",
          f"y    { yend['y']   [0,0,0,0]:.5f}")
    print('')
    '''
    return yend,state

def _rk1(dydt_func=None, dt=None, y=None):
    dy1_on_dt,state = dydt_func( y); 
    return {k: y[k] + dy1_on_dt[k] * dt  for k in y.keys()},state