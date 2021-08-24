# -*- coding: utf-8 -*-


# built-in
import time
import warnings


# common
import numpy as np
import scipy.integrate as scpinteg
import matplotlib.pyplot as plt     # DB


# specific
from . import _utils
from . import _class_checks


_SCIPY_URL_BASE = 'https://docs.scipy.org/doc/scipy/reference/generated/'
_SCIPY_URL = (
    _SCIPY_URL_BASE
    + 'scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp'
)


_DSOLVERS = {
    'eRK4-homemade': {
        'type': 'explicit',
        'step': 'fixed',
        'com': 'Runge_Kutta order 4',
        'source': __file__,
    },
    'eRK2-scipy': {
        'scipy': 'RK23',
        'type': 'explicit',
        'step': 'variable',
        'com': 'Runge_Kutta order 2',
        'source': _SCIPY_URL,
    },
    'eRK4-scipy': {
        'scipy': 'RK45',
        'type': 'explicit',
        'step': 'variable',
        'com': 'Runge_Kutta order 4',
        'source': _SCIPY_URL,
    },
    'eRK8-scipy': {
        'scipy': 'DOP853',
        'type': 'explicit',
        'step': 'variable',
        'com': 'Runge_Kutta order 8',
        'source': _SCIPY_URL,
    },
}


_SOLVER = 'eRK4-homemade'


# #############################################################################
# #############################################################################
#                   user-interface to display solvers
# #############################################################################


def get_available_solvers(returnas=None, verb=None):

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
    lode=None,
    lstate=None,
    dargs=None,
    nt=None,
    rtol=None,
    atol=None,
    max_time_step=None,
    dverb=None,
):

    # -----------
    # check input

    solver = _check_solver(solver)

    # -----------
    # create buffer for temp
    dargs_temp = {
        k0: {k1: v1[-1, ...] for k1, v1 in v0.items()}
        for k0, v0 in dargs.items()
    }

    # -----------
    # Define the function that takes/returns all functions

    dydt_func, lode_solve = get_func_dydt(
        dparam=dparam, dargs_temp=dargs_temp,
        lode=lode, lstate=lstate,
        inc_time='homemade' in solver,
    )

    # -----------
    # initialize y
    y0 = np.array([dparam[k0]['value'][0, ...] for k0 in lode_solve])

    # -------------
    # dispatch to relevant solver to solve ode using dydt_func

    if solver == 'eRK4-homemade':
        _eRK4_homemade(
            y0=y0,
            dydt_func=dydt_func,
            dparam=dparam,
            lode=lode_solve,
            lstate=lstate,
            nt=nt,
            dverb=dverb,
        )

    else:
        # scipy takes one-dimensional y only
        y0 = y0[:, 0]

        _solver_scipy(
            y0=y0,
            dydt_func=dydt_func,
            dparam=dparam,
            lode=lode_solve,
            lstate=lstate,
            atol=atol,
            rtol=rtol,
            max_time_step=max_time_step,
            solver=solver,
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
    dargs_temp=None,
    lode=None,
    lstate=None,
    inc_time=None,
):

    # ---------------
    # check inputs

    if inc_time is None:
        inc_time = True

    # ---------------
    # Get list of ode except time

    if inc_time:
        lode_solve = lode
    else:
        lode_solve = [k0 for k0 in lode if k0 != 'time']

    # ---------------------
    # prepare array to be used as buffer
    # (to avoid a new array creation everytime the function is called)

    dydt = np.full((len(lode_solve), dparam['nx']['value']), np.nan)

    # -----------------
    # get func

    def func(
        t,
        y,
        dydt=dydt,
        dparam=dparam,
        dargs_temp=dargs_temp,
        lode_solve=lode_solve,
        lstate=lstate,
    ):
        """ dydt = f(t, y)

        Where y is a (n,) array
        y[0] = fisrt ode
        y[1] = second ode
        ...
        y[n] = last ode

        All intermediate values ae stored in dparam[k0]['value'][-1, 0]

        """

        # ------------
        # update cache => also updates dargs and dargs_temp by reference
        # used by dargs_temp (by reference)
        for ii, k0 in enumerate(lode_solve):
            dparam[k0]['value'][-1, ...] = y[ii, ...]

        # ------------
        # First update intermediary functions based on provided y
        # The last time step is used as temporary buffer
        # used by dargs_temp (by reference)
        for ii, k0 in enumerate(lstate):
            dparam[k0]['value'][-1, ...] = dparam[k0]['func'](**dargs_temp[k0])

        # ------------
        # Then compute derivative dydt (ode)

        for ii, k0 in enumerate(lode_solve):
            if 'itself' in dparam[k0]['kargs']:
                dydt[ii, ...] = dparam[k0]['func'](
                    itself=y[ii, ...], **dargs_temp[k0],
                )
            else:
                dydt[ii, ...] = dparam[k0]['func'](**dargs_temp[k0])

        return dydt

    return func, lode_solve


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
):
    """ Structure of the homemade rk4 solver, with time loop, intermediaries...
    """

    # initialize y
    y = np.copy(y0)

    # start loop on time
    t0 = time.time()
    for ii in range(1, nt):

        # print of wait
        if dverb['verb'] > 0:
            t0 = _class_checks._print_or_wait(ii=ii, nt=nt, t0=t0, **dverb)

        # compute ode variables from ii-1, using solver
        y += _rk4(
            dydt_func=dydt_func,
            dt=dparam['dt']['value'],
            y=y,
            t=np.nan,
        )

        # dispatch to store result of ode
        for jj, k0 in enumerate(lode):
            dparam[k0]['value'][ii, ...] = y[jj, ...]


def _rk4(dydt_func=None, dt=None, y=None, t=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step
    """
    dy1_on_dt = dydt_func(t, y)
    dy2_on_dt = dydt_func(t + dt/2., y + dy1_on_dt * dt/2.)
    dy3_on_dt = dydt_func(t + dt/2., y + dy2_on_dt * dt/2.)
    dy4_on_dt = dydt_func(t + dt, y + dy3_on_dt*dt)
    return (dy1_on_dt + 2*dy2_on_dt + 2*dy3_on_dt + dy4_on_dt) * dt/6.


# #############################################################################
# #############################################################################
#                   scipy
# #############################################################################


def _solver_scipy(
    y0=None,
    dydt_func=None,
    dparam=None,
    lode=None,
    lstate=None,
    atol=None,
    rtol=None,
    dverb=None,
    max_time_step=None,
    solver=None,
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
        max_time_step = 10. * dparam['dt']['value']

    if dparam['nx']['value'] > 1:
        msg = (
            "scipy solvers only implemented for nx = 1"
        )
        raise Exception(msg)

    # -----------------
    # define t_span, t_eval

    t_span = [dparam['time']['initial'], dparam['Tmax']['value']]
    t_eval = np.linspace(t_span[0], t_span[1], dparam['nt']['value'])

    # -----------------
    # define y0, t_span, t_eval

    sol = scpinteg.solve_ivp(
        dydt_func,
        t_span,
        y0,
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
    if sol.success is True:
        indmax = dparam['nt']['value']
        if dverb['verb'] > 0:
            msg = (
                f"{sol.message}\nSuccess: {sol.success}\n"
                f"Nb. fev: {sol.nfev} for {sol.t.size} time steps"
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
            msg = (
                f"Solver stoped at t = {sol.t.max()} "
                f"({sol.t.size} / {dparam['nt']['value']} time steps) "
                "=> divergence?"
            )
            warnings.warn(msg)
        else:
            msg = f"Solver failed with status {sol.status}: {sol.message}"
            raise Exception(msg)

    # ---------------------
    # dispatch results

    for ii, k0 in enumerate(lode):
        dparam[k0]['value'][:indmax, 0] = sol.y[ii, ...]
    dparam['time']['value'][:indmax, ...] = np.repeat(
        sol.t[:, None],
        dparam['nx']['value'],
        axis=1,
    )

    return sol
