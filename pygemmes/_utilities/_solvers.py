
# Checked December 2022

# built-in
import time

# common
import numpy as np
from copy import deepcopy

# specific
from . import _class_checks


# #############################################################################
# #############################################################################
#                   Main entry point
# #############################################################################

def solve(
        solver=None,
        dparam=None,
        dmisc=None,
        dverb=None,
):
    # -----------
    # check input
    #solver = _check_solver(solver)
    lode   = dmisc['dfunc_order']['differential']
    lstate = dmisc['dfunc_order']['statevar']

    # -----------
    # Define the function that takes/returns all functions
    y0, dydt_func= get_func_dydt(
        dparam=dparam,
        dmisc=dmisc,
    )

    # -------------
    # dispatch to relevant solver to solve ode using dydt_func
    _eRK4_homemade(
        y0=y0,
        dydt_func=dydt_func,
        dparam=dparam,
        lode=lode,
        lstate=lstate,
        nt=dparam['nt']['value'],
        dverb=dverb,
    )

    return solver


def get_func_dydt(
    dparam=None,
    dmisc=None,
):
    lode = dmisc['dfunc_order']['differential']
    lstate = dmisc['dfunc_order']['statevar']
    lparam = dmisc['dfunc_order']['parameter']+dmisc['dfunc_order']['parameters']+['dt']

    y0 =      { k : dparam[k]['value'][0, ...] for k in lode}
    dydt =    { k : np.full(np.shape(v), np.nan) for k,v in y0.items()}
    dbuffer = { k0: dparam[k0]['value'][0, ...] for k0 in lode+lstate}
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
        return dydt,dbuffer
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
    for k0 in lode: dparam[k0]['value'][0, ...] = y0[k0]


def _rk4(dydt_func=None, dt=None, y=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step
    """
    dy1_on_dt,state = dydt_func( y); y1 = {k: y[k] + dy1_on_dt[k] * dt / 2. for k in y.keys()}
    dy2_on_dt,_     = dydt_func(y1); y2 = {k: y[k] + dy2_on_dt[k] * dt / 2. for k in y.keys()}
    dy3_on_dt,_     = dydt_func(y2); y3 = {k: y[k] + dy3_on_dt[k] * dt / 1. for k in y.keys()}
    dy4_on_dt,_     = dydt_func(y3)
    return {k: y[k] +(    dy1_on_dt[k]
                    + 2*dy2_on_dt[k]
                    + 2*dy3_on_dt[k]
                    +   dy4_on_dt[k]) * dt/6  for k in y.keys()},state
