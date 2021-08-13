# -*- coding: utf-8 -*-

import time
import numpy as np
import scipy.integrate as scpinteg


from . import _class_checks


# #############################################################################
# #############################################################################
#                   Home-made
# #############################################################################


def _eRK4_homemade(
    dparam=None,
    lode=None,
    lpde=None,
    linter=None,
    laux=None,
    dargs=None,
    nt=None,
    verb=None,
    timewait=None,
    end=None,
    flush=None,
    compute_auxiliary=None,
):
    """ Structure of the homemade rk4 solver, with time loop, intermediaries...
    """
    t0 = time.time()
    for ii in range(1, nt):

        # print of wait
        if verb > 0:
            t0 = _class_checks._print_or_wait(
                ii=ii, nt=nt, verb=verb,
                timewait=timewait, end=end, flush=flush,
                t0=t0,
            )
            
        # compute ode variables from ii-1, using solver
        for k0 in lode + lpde:
            kwdargs = {
                k1: v1[ii-1, :] for k1, v1 in dargs[k0].items()
            }

            dparam[k0]['value'][ii] = (
                dparam[k0]['value'][ii-1]
                + _rk4(
                    dparam=dparam,
                    k0=k0,
                    y=dparam[k0]['value'][ii-1],
                    kwdargs=kwdargs,
                )
            )

        # compute intermediary functions, in good order
        # Now that inermediary functions are computed at t=0 in reset()
        # we have to reverse the order of resolution:
        # first ode then intermediary
        for k0 in linter:
            kwdargs = {
                k1: v1[ii, :]
                for k1, v1 in dargs[k0].items()
            }
            dparam[k0]['value'][ii, :] = (
                dparam[k0]['func'](
                    **kwdargs,
                )
            )

        # Since the computation is fast we can also compute auxiliary
        # TBC: there might be a function order here too!
        if compute_auxiliary:
            for k0 in laux:
                kwdargs = {
                    k1: v1[ii, :]
                    for k1, v1 in dargs[k0].items()
                }
                dparam[k0]['value'][ii, :] = (
                    dparam[k0]['func'](
                        **kwdargs
                    )
                )


def _rk4(dparam=None, k0=None, y=None, kwdargs=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables
        - p = parameter dictionnary
    dt is contained within p
    """
    if 'itself' in dparam[k0]['kargs']:
        dy1 = dparam[k0]['func'](itself=y, **kwdargs)
        dy2 = dparam[k0]['func'](itself=y+dy1/2., **kwdargs)
        dy3 = dparam[k0]['func'](itself=y+dy2/2., **kwdargs)
        dy4 = dparam[k0]['func'](itself=y+dy3, **kwdargs)
    else:
        dy1 = dparam[k0]['func'](**kwdargs)
        dy2 = dparam[k0]['func'](**kwdargs)
        dy3 = dparam[k0]['func'](**kwdargs)
        dy4 = dparam[k0]['func'](**kwdargs)
    # DEBUG
    if k0 == 'W':
        print(", ".join([f"{k}: {v}" for k, v in kwdargs.items()]))
        print(f"W: {y}, W': {dy1}")
    return (dy1 + 2*dy2 + 2*dy3 + dy4) * dparam['dt']['value']/6.


# #############################################################################
# #############################################################################
#                   scipy
# #############################################################################


def _solver_scipy(
    dparam=None,
    lode=None,
    linter=None,
    dargs=None,
    atol=None,
    rtol=None,
    verb=None,
    max_time_step=None,
    solver_scipy=None,
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

    lode_notime = [k0 for k0 in lode if k0 != 'time']

    # -----------------
    # define f(t, y) (using pre-allocated array for speed

    dydt = np.full((len(lode_notime,)), np.nan)

    def func(t, y, dydt=dydt, dparam=dparam, lode_notime=lode_notime):
        """ dydt = f(t, y)

        Where y is a (n,) array
        y[0] = fisrt ode
        y[1] = second ode
        ...
        y[n] = last ode

        All intermediate values ae stored in dparam[k0]['value'][-1, 0]

        """

        # ------------
        # update cache
        for ii, k0 in enumerate(lode_notime):
            dparam[k0]['value'][-1, :] = y[ii, :]

        # ------------
        # First update intermediary functions based on provided y
        for ii, k0 in enumerate(linter):
            # build kwdargs
            kwdargs = {
                k1: v1[-1, :]
                for k1, v1 in dargs[k0].items()
            }

            dparam[k0]['value'][-1, :] = dparam[k0]['func'](**kwdargs)

        # ------------
        # Then compute derivative functions (ode)

        for ii, k0 in enumerate(lode_notime):
            # build kwdargs
            kwdargs = {
                k1: v1[-1, :]
                for k1, v1 in dargs[k0].items()
            }

            if 'itself' in dparam[k0]['kargs']:
                dydt[ii] = dparam[k0]['func'](itself=y[ii], **kwdargs)
            else:
                dydt[ii] = dparam[k0]['func'](**kwdargs)

        return dydt

    # -----------------
    # define y0, t_span, t_eval

    y0 = np.array([
        dparam[k0]['value'][0, 0]
        for k0 in lode_notime
    ])

    t_span = [dparam['time']['initial'], dparam['Tmax']['value']]
    t_eval = np.linspace(t_span[0], t_span[1], dparam['nt']['value'])

    # -----------------
    # define y0, t_span, t_eval

    sol = scpinteg.solve_ivp(
        func,
        t_span,
        y0,
        method=solver_scipy,
        t_eval=t_eval,
        max_step=max_time_step,
        rtol=rtol,
        atol=atol,
        vectorized=True,
        first_step=dparam['dt']['value'],
    )

    # ----------------
    # verbosity
    if verb > 0:
        msg = (
            f"{sol.message}\nSuccess: {sol.success}\n"
            f"Nb. fev: {sol.nfev} for {sol.t.size} time steps"
            f" ({sol.nfev/sol.t.size} per time step)"
        )
        print(msg)

    # ---------------------
    # dispatch results

    for ii, k0 in enumerate(lode_notime):
        dparam[k0]['value'][:, 0] = sol.y[ii, :]
    dparam['time']['value'] = np.repeat(
        sol.t[:, None],
        dparam['nx']['value'],
        axis=1,
    )

    return sol
