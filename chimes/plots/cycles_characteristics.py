
# Standard library imports
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Internal imports
from chimes.plots.tools._plot_tools import _multiline

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


def cycles_characteristics(
        hub,
        xaxis='omega',
        yaxis='employment',
        ref='employment',
        type1='frequency',
        normalize=False,
        Region=0,
        title='',
        returnFig=False):
    '''
    Plot the frequency and harmonicity characteristics for each cycle found in the system.

    Parameters
    ----------
    hub : Hub
        The Hub object containing the model and data.
    xaxis : str or list, optional
        The variable for the x-axis. If a list, the second element specifies the sector.
    yaxis : str or list, optional
        The variable for the y-axis. If a list, the second element specifies the sector.
    ref : str, optional
        The reference variable for cycle calculations.
    type1 : str, optional
        The type of characteristic to be plotted. Options: 't_mean_cycle', 'period_T', 'medval', 'stdval', 'minval',
        'maxval', 'frequency', 'Coeffs', 'Harmonicity'.
    normalize : bool, optional
        If True, normalize the values of type1.
    Region : int, optional
        The region to plot for multiple regions.
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
    - If the specified run has not been performed, an exception is raised.
    - If cycle information is not available, it is calculated using the specified reference variable.

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: OLD
    '''
    if not hub.dflags['run'][0]:
        print('NO RUN DONE YET, DO RUN ON THE SYSTEM STATE')
        hub.run()

    if not hub.dmisc.get('cycles', False):
        print('Calculation of cycles on each field as ref...')
        hub.calculate_Cycles(ref=ref)

    ####
    fig = plt.figure()
    ax1 = plt.subplot(111)

    xsector = xaxis[1] if type(xaxis) is list else 0
    ysector = yaxis[1] if type(xaxis) is list else 0
    xaxis = xaxis[0] if type(xaxis) is list else xaxis
    yaxis = yaxis[0] if type(xaxis) is list else yaxis

    AllX = []
    AllY = []
    AllC1 = []
    R = hub.get_dfields()
    cycs = R[ref]['cycles_bykey']

    for i in range(hub.dfields['nx']['value']):  # loop on parallel system
        for j, ids in enumerate(cycs['period_indexes'][i]):  # loop on cycles decomposition
            AllX.append(R[xaxis]['value'][ids[0]:ids[1], i, Region, xsector])
            AllY.append(R[yaxis]['value'][ids[0]:ids[1], i, Region, ysector])
            AllC1.append(cycs[type1][i][j])

    if normalize:
        AllC1 /= np.amax(AllC1)

    lc1 = _multiline(AllX, AllY, AllC1, ax=ax1, cmap='jet', lw=2)

    ax1.set_xlabel(R[xaxis]['symbol'])
    ax1.set_ylabel(R[yaxis]['symbol'])
    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(lc1, cax=cax1, orientation='vertical')
    ax1.set_title(type1)

    plt.suptitle(title + 'Period analysis on : ' + R[ref]['symbol'])
    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig
