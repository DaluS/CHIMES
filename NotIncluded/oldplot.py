# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 13:47:24 2022

@author: Paul Valcke
"""


# #############################################################################
# #############################################################################
#                       DEPRECATED
# #############################################################################


# DEPRECATED ?
def AllVar(
    hub,
    ncols=None,
    idx=None,
    sharex=None,
    tit=None,
    wintit=None,
    dmargin=None,
    fs=None,
    show=None,
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

    if ncols is None:
        ncols = 3
    if idx is None:
        idx = 0
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
        wintit = 'All variables'
    if fs is None:
        fs = (20, 20)
    if show is None:
        show = True

    # -----------
    # Prepare data to be plotted

    dpar = hub.get_dparam(returnas=dict)
    t = dpar['time']['value'][:, idx]
    lkeys_notime = hub.get_dparam(
        returnas=list,
        eqtype=['ode', 'statevar'],
        key=('time',),
    )
    nkeys = len(lkeys_notime)

    # derive nrows
    nrows = nkeys // ncols + 1

    # -----------
    # Prepare figure and axes dict

    fig = plt.figure(figsize=fs)
    fig.canvas.set_window_title(wintit)
    fig.suptitle(tit)

    # axes coordinates array
    gs = gridspec.GridSpec(ncols=ncols, nrows=nrows, **dmargin)

    dax = {}
    shx = None
    for ii, key in enumerate(lkeys_notime):

        # create axes and store in dict
        row = ii % nrows
        col = ii // nrows
        dax[key] = fig.add_subplot(gs[row, col], sharex=shx)

        # sharex if relevant
        if ii == 0 and sharex is True:
            shx = dax[key]

        # set ylabels
        if dpar[key]['symbol'] is None:
            ylab = key
        else:
            ylab = dpar[key]['symbol']
        if dpar[key]['units'] not in [None, '']:
            ylab += f" ({dpar[key]['units']})"
        dax[key].set_ylabel(ylab)

        # set xlabel if at bottom
        if row == nrows - 1 or ii == nkeys - 1:
            xlab = f"time ({dpar['time']['units']})"
            dax[key].set_xlabel(xlab)

    # -----------
    # plot data on axes

    for ii, key in enumerate(lkeys_notime):
        dax[key].plot(t, dpar[key]['value'][:, idx])

    # -----------
    # show and return axes dict

    if show is True:
        plt.show()
    return dax


# DEPRECATED ?
def AllPhaseSpace(sol, variablesREF, idx=0):
    plt.figure('All Phasespace', figsize=(10, 7))
    fig = plt.gcf()
    leng = len(variablesREF)
    NumbOfSubplot = int(leng * (leng - 1) / 2)

    idd = 1
    for ii, var1 in enumerate(variablesREF):
        for var2 in variablesREF[ii + 1:]:

            allvars = sol.get_dparam(returnas=dict)
            xval = allvars[var1]['value'][:, idx]
            yval = allvars[var2]['value'][:, idx]
            t = allvars['time']['value'][:, idx]

            points = np.array([xval, yval]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            norm = plt.Normalize(t.min(), t.max())
            lc = LineCollection(segments, cmap='viridis', norm=norm)
            lc.set_array(t)
            lc.set_linewidth(2)

            plt.subplot(2, NumbOfSubplot, idd)
            ax = plt.gca()
            line = ax.add_collection(lc)
            plt.xlabel(var1)
            plt.ylabel(var2)
            plt.xlim([np.amin(xval), np.amax(xval)])
            plt.ylim([np.amin(yval), np.amax(yval)])
            plt.axis('scaled')
            idd += 1
    fig.colorbar(line, ax=ax, label='time')
    suptit = (
        f"All Phasespace for model {sol.dmodel['name']}, system {idx}"
    )
    plt.suptitle(suptit)
    plt.show()


def plot3yaxis(hub, x, y1, y2, y3=[], idx=0):
    '''

    DEPRECIATED
    plot variables on multiple y axis (up to 3)
    x must be a variable name
    y must be a list of variable names

    for the moment only 9 variables are accepted per list !
    '''
    color1 = plt.cm.jet(0)
    color2 = plt.cm.jet(0.3)
    color3 = plt.cm.jet(.9)

    #########
    allvarname = [x]+y1+y2+y3
    R = hub.get_dparam(keys=[allvarname], returnas=dict)

    fig, host = plt.subplots(figsize=(8, 5))
    p = {}
    host.set_xlabel(R[x]['symbol']+r'($ '+R[x]['units'].replace('$', '\$')+'$)')
    vx = R[x]['value'][:, idx]
    host.set_xlim(vx[0], vx[-1])

    vy1 = {y: R[y]['value'][:, idx] for y in y1}
    y1min = np.amin([np.amin(v) for v in vy1.values()])
    y1max = np.amax([np.amax(v) for v in vy1.values()])
    units = r'($'+R[y1[-1]]['units']+'$)'
    ylabel1 = ''.join([R[x]['symbol']+' ' for x in y1])  # +units

    host.set_ylabel(ylabel1)
    for i, key in enumerate(y1):
        p[key], = host.plot(vx, vy1[key],    color=color1, label=R[key]['symbol'], ls=_LS[i])
    host.yaxis.label.set_color(color1)
    host.set_ylim(y1min, y1max)

    par1 = host.twinx()
    vy2 = {y: R[y]['value'][:, idx] for y in y2}
    y2min = np.amin([np.amin(v) for v in vy2.values()])
    y2max = np.amax([np.amax(v) for v in vy2.values()])
    ylabel2 = ''.join([R[x]['symbol']+' ' for x in y2]) + \
        r'($ '+R[y2[-1]]['units'].replace('$', '\$')+'$)'
    par1.set_ylabel(ylabel2)
    for i, key in enumerate(y2):
        p[key], = par1.plot(vx, vy2[key],    color=color2, label=R[key]['symbol'], ls=_LS[i])
    par1.yaxis.label.set_color(color2)
    par1.set_ylim(y2min, y2max)

    if len(y3):
        par2 = host.twinx()
        vy3 = {y: R[y]['value'][:, idx] for y in y3}
        y3min = np.amin([np.amin(v) for v in vy3.values()])
        y3max = np.amax([np.amax(v) for v in vy3.values()])
        ylabel3 = ''.join([R[x]['symbol']+' ' for x in y3]) + \
            r'($ '+R[y3[-1]]['units'].replace('$', '\$')+'$)'
        par2.set_ylabel(ylabel3)
        for i, key in enumerate(y3):
            p[key], = par2.plot(vx, vy3[key],    color=color3, label=R[key]['symbol'], ls=_LS[i])

        # right, left, top, bottom
        par2.spines['right'].set_position(('outward', 60))
        par2.xaxis.set_ticks([])
        par2.yaxis.label.set_color(color3)
        par2.set_ylim(y3min, y3max)
        # Sometimes handy, same for xaxis
        # par2.yaxis.set_ticks_position('right')

        # Move "Velocity"-axis to the left
        # par2.spines['left'].set_position(('outward', 60))
        # par2.spines['left'].set_visible(True)
        # par2.yaxis.set_label_position('left')
        # par2.yaxis.set_ticks_position('left')

    host.legend(handles=p.values(), loc='best')

    plt.show()
