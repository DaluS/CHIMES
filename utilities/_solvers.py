# -*- coding: utf-8 -*-


import numpy as np
import scipy.integrate as scpinteg


# #############################################################################
# #############################################################################
#                   Home-made
# #############################################################################


def _eRK4_homemade(
    dparam=None,
    lode=None,
    dargs=None,
    ii=None,
):
    for k0 in lode:
        kwdargs = {
            k1: dparam[k1]['value'][ii, :] for k1 in dargs[k0]
        }
        if 'lambda' in dargs[k0]:
            kwdargs['lamb'] = kwdargs['lambda']
            del kwdargs['lambda']

        dparam[k0]['value'][ii+1, :] = (
            dparam[k0]['value'][ii, :]
            + _rk4(
                dparam=dparam,
                k0=k0,
                y=dparam[k0]['value'][ii, :],
                kwdargs=kwdargs,
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
    return (dy1 + 2*dy2 + 2*dy3 + dy4) * dparam['dt']['value']/6.


# #############################################################################
# #############################################################################
#                   scipy
# #############################################################################


def _eRK4_scipy(
    dparam=None,
    lode=None,
    linter=None,
    dargs=None,
    atol=None,
    rtol=None,
    verb=None,
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

    # -----------------
    # define y0

    y0 = np.array([
        dparam[k0]['value'][0, 0] for k0 in lode
    ])

    # -----------------
    # define f(t, y) (using pre-allocated array for speed

    dydt = np.full((len(lode,)), np.nan)
    def func(t, y, dydt=dydt, dparam=dparam):
        """ dydt = f(t, y)

        Where y is a (n,) array
        y[0] = fisrt ode
        y[1] = second ode
        ...
        y[n] = last ode

        """

        # ------------
        # First update intermediary functions bqsed on provided y
        for ii, k0 in enumerate(linter):
            kwdargs = {
                k1: dparam[k1]['value'][0, 0] for k1 in dargs[k0]
            }
            if 'lambda' in dargs[k0]:
                kwdargs['lamb'] = kwdargs['lambda']
                del kwdargs['lambda']

            dparam[k0]['value'][0, 0] = dparam[k0]['func'](**kwdargs)


        # ------------
        # Then compute derivative functions (ode)

        for ii, k0 in enumerate(lode):
            kwdargs = {
                k1: dparam[k1]['value'][0, 0]
                for k1 in dargs[k0]
                if k1 in linter
            }
            kwdargs.update({
                k1: y[lode.index(k1)]
                for k1 in dargs[k0]
                if k1 in lode
            })
            if 'lambda' in dargs[k0]:
                kwdargs['lamb'] = kwdargs['lambda']
                del kwdargs['lambda']

            if 'itself' in dparam[k0]['kargs']:
                dydt[ii] = dparam[k0]['func'](itself=y[ii], **kwdargs)
            else:
                dydt[ii] = dparam[k0]['func'](**kwdargs)

        return dydt

    t_span = [dparam['time']['initial'], dparam['Tmax']['value']]

    sol = scpinteg.solve_ivp(
        func,
        t_span,
        y0,
        method='RK45',
        t_eval=np.linspace(t_span[0], t_span[1], dparam['nt']['value']),
        max_step=2.*dparam['dt']['value'],
        rtol=rtol,
        atol=atol,
        vectorized=False,
        first_step=dparam['dt']['value'],
    )

    # ----------------
    # verbosity
    if verb > 0:
        msg = (
            f"{sol.message}\nSuccess: {sol.success}"
        )
        print(msg)

    # ---------------------
    # dispatch results

    dparam['time']['value'] = sol.t
    for ii, k0 in enumerate(lode):
        if k0 == 'time':
            continue
        dparam[k0]['value'][:, 0] = sol.y[ii, :]

    return sol
