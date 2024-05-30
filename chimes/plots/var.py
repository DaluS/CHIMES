from typing import Union
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Rectangle

# Internal imports
from chimes.plots.tools._plot_tools import _multiline
from chimes.plots.tools._plot_tools import _indexes, _key
from chimes.plots.tools._plot_tools import value
from chimes.plots.tools._plot_tools import _LS, _plotly_dashstyle, _plotly_colors

# Matplotlib RCParams useful elements
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
plt.rcParams.update({'font.size': 10})
params = {'legend.fontsize': 6,
          'legend.handlelength': 0,
          'legend.borderpad': 0,
          'legend.labelspacing': 0.0}
SIZETICKS = 20
SIZEFONT = 10
LEGENDSIZE = 20
LEGENDHANDLELENGTH = 2


def Var(
    hub,
        key: str,
        mode: str = False,
        log: bool = False,
        idx: Union[int, str] = 0,
        Region: Union[int, str] = 0,
        tini: int = False,
        tend: int = False,
        title: str = '',
        returnFig: bool = False):
    '''
    Generate a plot for a single variable with optional cycles analysis and sensitivity.

    Parameters
    ----------
    hub : Hub
        The Hub object containing the model and data.
    key : str
        The variable to be plotted.
    mode : str, optional
        The plot mode. Options: 'sensitivity', 'cycles', or False.
    log : bool, optional
        If True, use a logarithmic scale for the y-axis.
    idx : int or str, optional
        Index for the parallel run.
    Region : int or str, optional
        The region to plot for multiple regions.
    tini : int, optional
        Initial time for the data.
    tend : int, optional
        End time for the data.
    title : str, optional
        Title of the plot.
    returnFig : bool, optional
        If True, return the matplotlib figure without displaying it.

    Returns
    -------
    matplotlib.figure.Figure or None
        If returnFig is True, returns the matplotlib figure. Otherwise, displays the figure.

    Notes
    -----
    - If mode is 'sensitivity', statistical variance between parallel runs is shown.
    - If mode is 'cycles', cycles within the evolution of the variable are shown.

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    '''
    # CHECKS
    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)
    if (mode == 'sensitivity' and not hub._dflags.get('sensitivity', False)):
        print('The system is calculating sensitivity...')
        hub.calculate_StatSensitivity()
        print('Done')
    if (mode == 'cycles' and not hub._dflags.get('cycles', False)):
        print('Calculation of cycles on each field as ref...')
        hub.calculate_Cycles()
        print('Done')

    R = hub.dfields
    key, keysect, keyname = _key(R, key)

    fig = plt.figure()
    fig.set_size_inches(10, 5)
    ax = plt.gca()

    # PLOT OF THE BASE
    allvars = hub.get_dfields(returnas=dict)
    y = allvars[key]['value'][idt0:idt1, idx, Region, keysect, 0]
    t = allvars['time']['value'][idt0:idt1, idx, Region, 0, 0]

    if mode in [False, 'cycles']:
        plt.plot(t, y, lw=2, ls='-', c='k')

    # PLOT OF THE CYCLES
    if mode == 'cycles':
        cycleindex = idx * (R['nx']['value'] * R['nr']['value'] * R[R[key]['size'][0]]['value']) +\
            Region * (R['nr']['value'] * R[R[key]['size'][0]]['value']) + keysect

        cyclvar = allvars[key]['cycles'][cycleindex]
        tmcycles = cyclvar['t_mean_cycle']

        # Plot of each period by a rectangle
        miny = np.nanmin(y)
        maxy = np.nanmax(y)

        for car in cyclvar['period_T_intervals'][::2]:
            ax.add_patch(
                Rectangle((car[0], miny), car[1] - car[0], maxy - miny, facecolor='k', alpha=0.1))

        # Plot of enveloppe (mean-max)
        vmin = cyclvar['minval']
        vmax = cyclvar['maxval']
        plt.plot(tmcycles, vmin, ls='dashdot', label='min value')
        plt.plot(tmcycles, vmax, ls='dashdot', label='max value')

        # Plot of the mean value evolution
        meanv = np.array(cyclvar['meanval'])
        plt.plot(tmcycles, cyclvar['meanval'], ls='dashdot', label='mean value')
        plt.plot(tmcycles, cyclvar['medval'],
                 ls='dashdot', label='median value')

        # Plot of the standard deviation around the mean value
        stdv = np.array(cyclvar['stdval'])
        ax.fill_between(tmcycles, meanv - stdv, meanv + stdv, alpha=0.2)
        plt.legend()

    if mode == 'sensitivity':
        time = hub.dfields['time']['value'][idt0:idt1, idx, Region, keysect, 0]

        V = hub.dfields[key]['sensitivity'][Region][keyname]

        # Plot all trajectory

        for jj in range(len(allvars[key]['value'][0, :, 0, 0, 0])):
            ax.plot(time, hub.dfields[key]['value'][idt0:idt1, jj, Region, 0, 0], c='k', ls='--', lw=0.5)
            if jj == 30:
                print('WARNING: plotvar should be coded with a linecollection...')

        # Plot mean an median
        ax.plot(time, V['mean'][idt0:idt1], c='orange', label='mean')
        ax.plot(time, V['median'][idt0:idt1], c='orange', ls='--', label='median')
        ax.plot(time, V['max'][idt0:idt1], c='r', lw=0.4, label='maxmin')
        ax.plot(time, V['min'][idt0:idt1], c='r', lw=0.4)

        for j in np.arange(0.5, 5, 0.2):
            ax.fill_between(time, V['mean'][idt0:idt1] - j * V['stdv'][idt0:idt1],
                            V['mean'][idt0:idt1] + j * V['stdv'][idt0:idt1], alpha=0.02, color='blue')
        ax.fill_between(time, V['mean'][idt0:idt1],
                        V['mean'][idt0:idt1], alpha=0.5, color='blue', label=r'$\mu \pm 5 \sigma$')

        ax.set_xlim([time[0], time[-1]])
        ax.set_ylim([np.nanmin(V['min'][idt0:idt1]), np.nanmax(V['max'][idt0:idt1])])

        ax.fill_between(time, V['mean'][idt0:idt1] - V['stdv'][idt0:idt1],
                        V['mean'][idt0:idt1] + V['stdv'][idt0:idt1], alpha=0.4, color='r', label=r'$\mu \pm \sigma$')

    if log is True:
        ax.set_yscale('log')
    plt.title(title)
    plt.ylabel(R[key]['symbol'][:-1] + '_{' + keyname + '}$' if type(keyname) is str else
               R[key]['symbol'])
    plt.xlabel('time (y)')
    if mode:
        ax.legend()
    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig
