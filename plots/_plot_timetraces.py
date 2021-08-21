# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021

@author: Paul Valcke
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec


# default legend
_DLEG = {
    'loc': 'upper right',
    'frameon': True,
    'shadow': False,
    'framealpha': 0.3,
}


# #############################################################################
# #############################################################################
#                   check inputs
# #############################################################################


def _plot_timetraces_check(
    hub_id=None,
    idx=None,
    color=None,
    label=None,
    dleg=None,
    show=None,
    eqtype=None,
    dax=None,
):

    # -----------
    # Prepare figure and axes dict

    if idx is None:
        idx = 0

    if color is not None and not mcolors.is_color_like(color):
        msg = (
            f"Arg color for Hub ({hub_id}) is not a valid matplotlib color!\n"
            f"Provided: {color}"
        )
        raise Exception(msg)

    if label is None:
        label = hub_id

    if dleg is None:
        dleg = False if dax is None else _DLEG
    if not (dleg is False or isinstance(dleg, dict)):
        msg = (
            "Arg dleg must be either:\n"
            + "\t- False: no legend plotted\n"
            + "\t- dict: a dict of legend properties"
        )
        raise Exception(msg)

    if show is None:
        show = True

    # ---------------
    # for data selection

    if idx is None:
        idx = 0

    if eqtype is None:
        eqtype = ['ode', 'statevar']
    if isinstance(eqtype, str):
        eqtype = [eqtype]
    for ii, eq in enumerate(eqtype):
        if eq not in ['ode', 'statevar']:
            eqtype.pop(ii)

    return idx, color, label, dleg, show, eqtype


def _plot_timetraces_check_dax(
    hub=None,
    dpar=None,
    idx=None,
    dax=None,
    ncols=None,
    sharex=None,
    tit=None,
    wintit=None,
    dmargin=None,
    fs=None,
):

    # -----------
    # Prepare figure and axes dict

    if dax is None:
        nkeys = len(dpar)

        # check basic args
        if ncols is None:
            # by default try put all ode in the first column
            node = len([
                k0 for k0, v0 in dpar.items()
                if v0.get('eqtype') == 'ode'
            ])
            if node == 0:
                node = 4
            ncols = (nkeys - 1) // node + 1
        if dmargin is None:
            dmargin = {
                'left': 0.05, 'right': 0.98,
                'bottom': 0.06, 'top': 0.90,
                'wspace': 0.15, 'hspace': 0.20,
            }
        if sharex is None:
            sharex = True
        if tit is None:
            model = hub.dmodel['name']
            preset = hub.dmodel['preset']
            solver = hub.dmisc['solver']
            tit = f'{model} - {preset} - {solver}\nsystem number: {idx}'
        if wintit is None:
            wintit = 'Time traces'
        if fs is None:
            fs = (20, 20)

        # derive nrows
        nrows = (nkeys - 1) // ncols + 1

        # create figure
        fig = plt.figure(figsize=fs)
        fig.canvas.set_window_title(wintit)
        fig.suptitle(tit)

        # axes coordinates array
        gs = gridspec.GridSpec(ncols=ncols, nrows=nrows, **dmargin)

        dax = {}
        shx = None
        for ii, (k0, v0) in enumerate(dpar.items()):

            # create axes and store in dict
            row = ii % nrows
            col = ii // nrows
            dax[k0] = fig.add_subplot(gs[row, col], sharex=shx)

            # sharex if relevant
            if ii == 0 and sharex is True:
                shx = dax[k0]

            # set ylabels
            ylab = v0['symbol']
            if v0['units'] not in [None, '']:
                ylab += f" ({v0['units']})"
            dax[k0].set_ylabel(ylab)

            # set xlabel if at bottom
            if row == nrows - 1 or ii == nkeys - 1:
                xlab = f"time ({hub.dparam['time']['units']})"
                dax[k0].set_xlabel(xlab)

    # ---------------------
    # check dax if provided

    if isinstance(dax, dict):
        NoneType = None.__class__
        dfail = {
            k0: dax.get(ss).__class__
            for ss in dpar.keys()
            if not issubclass(dax.get(ss).__class__, (NoneType, plt.Axes))
        }
    else:
        dfail = {}

    if not isinstance(dax, dict) or len(dfail) > 0:
        lstr = [f'\t- {k0}: {v0.__class__}' for k0, v0 in dfail.items()]
        msg = (
            "Arg dax must be a dict, and the following keys must be axes:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    return dax


# #############################################################################
# #############################################################################
#                   Main plotting function
# #############################################################################


def plot_timetraces(
    hub,
    # for forcing a color / label
    color=None,
    label=None,
    # for figure creation
    dax=None,
    ncols=None,
    sharex=None,
    tit=None,
    wintit=None,
    dmargin=None,
    fs=None,
    dleg=None,
    show=None,
    # for selection of data
    idx=None,
    eqtype=None,
    **kwdargs,
):
    '''
    Plot all the variables in the system on a same figure

    Parameters
    ----------
    hub : The hub of the system
        DESCRIPTION.
    ncols : the number of column in the figure
        DESCRIPTION. The default is 2.
    idx : the index of the system you want to print
        DESCRIPTION. The default is 0.
    dmargin: dict
        dict defining the margins to be used for defining the axes

    Returns
    -------
    None.

    '''

    # -----------
    # Check inputs

    # build hub id
    hub_id = (
        f"{hub.dmodel['name']}-{hub.dmodel['preset']}-{hub.dmisc['solver']}"
    )

    # check
    idx, color, label, dleg, show, eqtype = _plot_timetraces_check(
        hub_id=hub_id,
        idx=idx,
        color=color,
        label=label,
        dleg=dleg,
        show=show,
        eqtype=eqtype,
        dax=dax,
    )

    # -----------
    # Prepare data to be plotted

    dpar = hub.get_dparam(
        returnas=dict,
        eqtype=eqtype,
        **kwdargs,
    )
    if len(dpar) == 0:
        return dax
    if 'time' in dpar.keys():
        del dpar['time']
    t = hub.dparam['time']['value'][:, idx]

    # -----------------------------------
    # Prepare dax or check it if provided

    dax = _plot_timetraces_check_dax(
        hub=hub,
        dpar=dpar,
        idx=idx,
        dax=dax,
        ncols=ncols,
        sharex=sharex,
        tit=tit,
        wintit=wintit,
        dmargin=dmargin,
        fs=fs,
    )

    # -----------
    # plot data on axes

    for k0, v0 in dpar.items():
        if dax.get(k0) is None:
            continue
        dax[k0].plot(
            t,
            v0['value'][:, idx],
            color=color,
            label=label,
        )

    # -----------
    # show and return axes dict

    if dleg is not False:
        for k0 in dpar.keys():
            if dax.get(k0) is None:
                continue
            dax[k0].legend(**dleg)

    if show is True:
        plt.show()
    return dax
