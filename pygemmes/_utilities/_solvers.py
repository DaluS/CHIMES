# -*- coding: utf-8 -*-


# built-in
import time
import warnings


# common
import numpy as np
import scipy.integrate as scpinteg
import matplotlib.pyplot as plt     # DB
from copy import deepcopy

# specific
from . import _utils
from . import _class_checks

from .._config import _SOLVER


_DSOLVERS = {
    'eRK4-homemade': {
        'type': 'explicit',
        'step': 'fixed',
        'com': 'Runge_Kutta order 4',
        'source': __file__,
    },
}


# #############################################################################
# #############################################################################
#                   user-interface to display solvers
# #############################################################################


def get_available_solvers(returnas=None, verb=None):

    print('IN THIS VERSION, ONLY THE RK4 HOMEMADE SOLVER IS ACTIVE')

    # ----------------
    # check inputs

    if returnas is None:
        returnas = False
    lreturnok = [False, list, dict]
    if returnas not in lreturnok:
        msg = (
            f"Arg returnas must be in {lreturnok}\n"
            f"Provided: {returnas}"
        )

    if verb is None:
        verb = returnas is False

    # ----------------
    # print or return

    if verb is True:
        def make_source(k0, dsolvers=_DSOLVERS):
            if 'scipy' in k0:
                method = dsolvers[k0]['scipy']
                source = f"scipy.integrate.solve_ivp(method='{method}')"
            else:
                source = dsolvers[k0]['source']
            return source

        col = ['key', 'type', 'step', 'comments', 'source']
        ar = [
            [
                f"'{k0}'",
                v0['type'],
                v0['step'],
                v0['com'],
                make_source(k0),
            ]
            for k0, v0 in _DSOLVERS.items()
        ]
        return _utils._get_summary(
            lar=[ar],
            lcol=[col],
            verb=verb,
            returnas=False,
        )
    elif returnas is dict:
        return {k0: dict(v0) for k0, v0 in _DSOLVERS.items()}
    else:
        return list(_DSOLVERS.keys())


# #############################################################################
# #############################################################################
#                   check
# #############################################################################


def _check_solver(solver):

    if solver is None:
        solver = _SOLVER

    c0 = (
        isinstance(solver, str)
        and solver in _DSOLVERS.keys()
    )
    if not c0:
        msg = (
            "Arg solver must be among the avaible solver keys:\n"
            + get_available_solvers(verb=False, returnas=str)
            + f"\n\nProvided: '{solver}'"
        )
        raise Exception(msg)

    return solver


# #############################################################################
# #############################################################################
#                   Main entry point
# #############################################################################


def solve(
        solver=None,
        dparam=None,
        dmisc=None,
        lode=None,
        lstate=None,
        dargs=None,
        dverb=None,
):
    # -----------
    # check input
    solver = _check_solver(solver)
    lode   = dmisc['dfunc_order']['differential']
    lstate = dmisc['dfunc_order']['statevar']

    # -----------
    # Define the function that takes/returns all functions
    y0, dydt_func= get_func_dydt(
        dparam=dparam,
        dargs=dargs,
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

    # ----------------------
    # Post-treatment
    # compute statevar functions, in good order
    for k0 in lstate:
        dparam[k0]['value'][...] = dparam[k0]['func'](**dargs[k0])

    return solver


# #############################################################################
# #############################################################################
#               Common utility: define dydt = f(y, t)
# #############################################################################


def get_func_dydt(
    dparam=None,
    dargs=None,
    dmisc=None,
):
    lode = dmisc['dfunc_order']['differential']
    lstate = dmisc['dfunc_order']['statevar']
    lparam = dmisc['dfunc_order']['parameter']+dmisc['dfunc_order']['parameters']+['dt']

    y0 = { k: dparam[k]['value'][0, ...] for k in lode}
    dydt = {k : np.full(np.shape(v), np.nan) for k,v in y0.items()}
    dbuffer = { k0: dparam[k0]['value'][0, ...] for k0 in lode+lstate}
    for k0 in lparam: dbuffer[k0]= dparam[k0]['value']

    def func(
        t,
        y,
        dbuffer=dbuffer,
        dydt=dydt,
        dparam=dparam,
    ):
        for k0 in lode:   dbuffer[k0] = y[k0]
        for k0 in lstate: dbuffer[k0] = dparam[k0]['func'](**{k:dbuffer[k] for k in dparam[k0]['kargs']})
        for k0 in lode:   dydt[k0] = dparam[k0]['func']   (**{k:dbuffer[k] for k in dparam[k0]['kargs']})

        return dydt

    return y0, func


# #############################################################################
# #############################################################################
#                   Home-made
# #############################################################################


def _eRK4_homemade(
    y0=None,
    dydt_func=None,
    dparam=None,
    lode=None,
    lstate=None,
    nt=None,
    dverb=None,
    dictpos={},
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

        # Estimate dt (for future variable time step versions)
        # dt =

        # compute ode variables from ii-1, using solver
        y = _rk4(
            dydt_func=dydt_func,
            dt=dparam['dt']['value'],
            y=y,
            t=np.nan,
        )

        # dispatch to store result of ode
        for k0 in lode: dparam[k0]['value'][ii, ...] = y[k0]
    for k0 in lode: dparam[k0]['value'][0, ...] = y0[k0]

def _rk4(dydt_func=None, dt=None, y=None, t=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step
    """
    dy1_on_dt = dydt_func(t, y)
    y1 = {k: y[k] + dy1_on_dt[k] * dt / 2. for k in y.keys()};dy2_on_dt = dydt_func(t + dt/2., y1)
    y2 = {k: y[k] + dy2_on_dt[k] * dt / 2. for k in y.keys()};dy3_on_dt = dydt_func(t + dt/2., y2)
    y3 = {k: y[k] + dy3_on_dt[k] * dt / 1. for k in y.keys()};dy4_on_dt = dydt_func(t + dt, y3)
    y4 = {k: y[k] +(    dy1_on_dt[k]
                    + 2*dy2_on_dt[k]
                    + 2*dy3_on_dt[k]
                    +   dy4_on_dt[k]) * dt/6  for k in y.keys()}
    return y4


# ###########################################
#       eRK1
# ###########################################


def _eRK1_homemade(
    y0=None,
    dydt_func=None,
    dparam=None,
    lode=None,
    lstate=None,
    nt=None,
    dverb=None,
):
    """ Structure of the homemade rk1 solver, with time loop, intermediaries...
    Coded as debugging for the rk1
    """

    # initialize y
    y = np.copy(y0)

    # start loop on time
    t0 = time.time()
    for ii in range(1, nt):

        # print of wait
        if dverb['verb'] > 0:
            t0 = _class_checks._print_or_wait(ii=ii, nt=nt, t0=t0, **dverb)

        # Estimate dt (for future variable time step versions)
        # dt =

        # compute ode variables from ii-1, using solver
        y += _rk1(
            dydt_func=dydt_func,
            dt=dparam['dt']['value'],
            y=y,
            t=np.nan,
        )

        # dispatch to store result of ode
        for jj, k0 in enumerate(lode):
            dparam[k0]['value'][ii, ...] = y[jj, ...]


def _rk1(dydt_func=None, dt=None, y=None, t=None):
    """
    a traditional euler scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step
    """
    dy1_on_dt = dydt_func(t, y)

    return (dy1_on_dt) * dt

# #############################################################################
# #############################################################################
#                   scipy
# #############################################################################


def _solver_scipy(
    y0=None,
    dydt_func=None,
    dparam=None,
    dargs_temp=None,
    lode=None,
    lstate=None,
    atol=None,
    rtol=None,
    dverb=None,
    max_time_step=None,
    solver=None,
    dmulti=None,
    vectorized=None,
):
    """ scipy.RK45 solver, for cross-checking

    First try: with a unique system (nx = 1)

    issue: how do we update intermediary functions?
    alogorithm only seems to allow ode...

    Beware: here variable time steps are possible and should be handled

    """

    # -----------------
    # check inputs
    if rtol is None:
        rtol = 1.e-3
    if atol is None:
        atol = 1.e-6
    if max_time_step is None:
        max_time_step = dparam['dt']['value'] * 10.

    # -----------------
    # define t_span, t_eval

    t_span = [dparam['time']['initial'], dparam['time']
              ['initial'] + dparam['Tmax']['value']]
    t_eval = np.linspace(t_span[0], t_span[1], dparam['nt']['value'])

    # -----------------
    # define y0, t_span, t_eval

    nx = dparam['nx']['value']
    if nx == 1:

        # solve
        sol = scpinteg.solve_ivp(
            dydt_func,
            t_span,
            y0.ravel(),
            method=_DSOLVERS[solver]['scipy'],
            t_eval=t_eval,
            max_step=max_time_step,
            rtol=rtol,
            atol=atol,
            vectorized=True,
            first_step=dparam['dt']['value'],
        )

        # ----------------
        # verbosity
        indmax = _scipy_verb(
            sol, dparam=dparam, lind=(0,), t_span=t_span,
            ii=0, nx=nx, dverb=dverb,
        )

        # ---------------------
        # dispatch results

        for ii, k0 in enumerate(lode):
            dparam[k0]['value'][..., 0] = sol.y[ii, ...]

        dparam['time']['value'][..., 0] = sol.t

    else:

        # dict of param that will need updating
        dkup = {}
        for k0 in dargs_temp.keys():
            for ii, k1 in enumerate(dmulti['keys']):

                lk = [
                    kk for kk in [k1] + dmulti['dparfunc'][k1]
                    if kk in dparam[k0]['kargs']
                ]
                if len(lk) > 0:
                    if dkup.get(k0) is None:
                        dkup[k0] = dict.fromkeys(lk, ii)
                    else:
                        dkup[k0].update(dict.fromkeys(lk, ii))

        # prepare tools for indices
        indj = np.zeros((len(dmulti['shape']),), dtype=int)
        shape = np.array(dmulti['shape'])
        rat = np.concatenate(([1], np.cumprod(shape)[:-1]))

        # start loop
        for ii in range(nx):

            # get correct set of indices and slice
            lind = list((ii // rat) % shape)

            # update dargs_temp with multiple-values parameters!
            if len(dmulti['shape']) > 1:
                for k0, v0 in dkup.items():
                    for k1, jj in v0.items():
                        if dparam[k1].get('eqtype') == 'ode':
                            # ode initial values are not parameters
                            continue
                        key = 'lamb' if k1 == 'lambda' else k1
                        indj[jj] = lind[jj]
                        dargs_temp[k0][key] = dparam[k1]['value'][tuple(indj)]
                        indj[jj] = 0
            else:
                for k0, v0 in dkup.items():
                    for k1, jj in v0.items():
                        if dparam[k1].get('eqtype') == 'ode':
                            continue
                        key = 'lamb' if k1 == 'lambda' else k1
                        dargs_temp[k0][key] = dparam[k1]['value'][ii]

            # solve
            slic = tuple([slice(0, len(lode))] + lind)
            sol = scpinteg.solve_ivp(
                dydt_func,
                t_span,
                y0[slic],
                method=_DSOLVERS[solver]['scipy'],
                t_eval=t_eval,
                max_step=max_time_step,
                rtol=rtol,
                atol=atol,
                vectorized=True,
                first_step=dparam['dt']['value'],
                args=(dargs_temp,),
            )

            # ----------------
            # verbosity
            indmax = _scipy_verb(
                sol, dparam=dparam, lind=lind, t_span=t_span,
                ii=ii, nx=nx, dverb=dverb,
            )

            # ---------------------
            # dispatch results

            slic = tuple([slice(0, indmax)] + lind)
            for ii, k0 in enumerate(lode):
                dparam[k0]['value'][slic] = sol.y[ii, ...]

            dparam['time']['value'][slic] = sol.t

    return sol


def _scipy_verb(
    sol,
    dparam=None,
    lind=None,
    t_span=None,
    ii=None,
    nx=None,
    dverb=None,
):
    if sol.success is True:
        indmax = dparam['nt']['value']
        if dverb['verb'] > 0:
            msg = (
                f"System {ii+1} / {nx} ({lind}) - Success: {sol.success}"
                f"\tNb. fev: {sol.nfev} for {sol.t.size} time steps"
                f" ({sol.nfev/sol.t.size} per time step)"
            )
            print(msg)
    else:
        c0 = (
            sol.message == (
                'Required step size is less than spacing between numbers.'
            )
            and sol.t.max() < t_span[1]
            and sol.t.size > 0
        )
        if c0:
            indmax = sol.t.size
            # keep the first steps until it failed + warn
            tmax = round(sol.t.max(), ndigits=2)
            msg = (
                f"System {ii+1} / {nx} ({lind}) - stopped at t = {tmax} "
                f"({sol.t.size} / {dparam['nt']['value']} time steps) "
                "=> divergence?"
            )
            print(msg)
        else:
            msg = (
                f"System {ii+1} / {nx} ({lind}) - Success: {sol.success}"
                f"\tstatus {sol.status}: {sol.message}"
            )
            raise Exception(msg)
    return indmax
