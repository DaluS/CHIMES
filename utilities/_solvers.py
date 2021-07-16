# -*- coding: utf-8 -*-


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















