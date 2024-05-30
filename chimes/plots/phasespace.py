
import numpy as np
from typing import Union, List, Tuple

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

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


def XY(
    hub, x: str, y: str,
    color='time',
    scaled=False,
    idx=0,
    Region=0,
    tini=False,
    tend=False,
    title='',
    returnFig=False
):
    """
    2D-phasespace plot (x,y), with the curve color being determined by the value of 'color'.

    Parameters
    ----------
    hub : Hub
        The Hub object containing the model and data.
    x : str
        The variable to be plotted on the x-axis.
    y : str
        The variable to be plotted on the y-axis.
    color : str, optional
        The variable determining the curve color. Default is 'time'.
    scaled : bool, optional
        If True, the plot is displayed with a scaled aspect ratio. Default is False.
    idx : int, optional
        Number of the system in parallel. Default is 0.
    Region : int, optional
        Number or ID of the system considered. Default is 0.
    tini : int, optional
        Initial time step for plotting. Default is False.
    tend : int, optional
        Final time step for plotting. Default is False.
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
    - The input variables 'x', 'y', and 'color' should be valid keys in the data parameter of the hub.
    - The curve color is determined by the values of the 'color' variable.
    - The plot can be displayed with a scaled aspect ratio by setting the 'scaled' parameter to True.

    Examples
    --------
    >>> XY(hub, 'variable_x', 'variable_y', color='time', scaled=False, idx=0, Region=0, tini=False, tend=False, title='Plot Title', returnFig=False)

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: OLD
    """
    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)

    # ## INPUT TRANSLATION #############
    R = hub.dfields
    x, xsect, xname = _key(R, x)
    y, ysect, yname = _key(R, y)
    color, csect, cname = _key(R, color)

    # ## PLOT #################
    allvars = hub.get_dfields(returnas=dict)
    t = allvars[color]['value'][idt0:idt1, idx, Region, csect, 0]
    yval = allvars[y]['value'][idt0:idt1, idx, Region, ysect, 0]
    xval = allvars[x]['value'][idt0:idt1, idx, Region, xsect, 0]

    points = np.array([xval, yval]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(t)
    lc.set_linewidth(2)

    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    line = ax.add_collection(lc)

    # BEAUTY
    fig.colorbar(line, ax=ax, label=allvars[color]['symbol'][:-1] + '_{' + cname + '}$')
    plt.xlabel(allvars[x]['symbol'][:-1] + '_{' + xname + '}$')
    plt.ylabel(allvars[y]['symbol'][:-1] + '_{' + yname + '}$')
    plt.xlim([np.nanmin(xval), np.nanmax(xval)])
    plt.ylim([np.nanmin(yval), np.nanmax(yval)])
    if scaled:
        plt.axis('scaled')
    # plt.loglog()
    plt.title(title)
    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig


def XYZ(
    hub, x, y, z,
        color='time',
        idx=0,
        Region=0,
        tini=False,
        tend=False,
        title='', returnFig=False):
    """
    Plot a 3D curve, with a fourth field as the color of the curve.

    Parameters:
    - hub (Hub): The Hub object containing data.
    - x (str): Key for x-coordinate data.
    - y (str): Key for y-coordinate data.
    - z (str): Key for z-coordinate data.
    - color (str, optional): Key for the field to be used as color. Default is 'time'.
    - idx (int, optional): Index for selecting specific data. Default is 0.
    - Region (int, optional): Index for selecting a specific region. Default is 0.
    - tini (bool, optional): Start time for data selection. Default is False.
    - tend (bool, optional): End time for data selection. Default is False.
    - title (str, optional): Title for the plot. Default is an empty string.
    - returnFig (bool, optional): If True, return the matplotlib figure object. Default is False.

    Returns:
    - If returnFig is False (default): None (displays the plot).
    - If returnFig is True: Matplotlib figure object.

    """

    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)

    # ## INPUT TRANSLATION #############
    R = hub.dfields

    x, xsect, xname = _key(R, x)
    y, ysect, yname = _key(R, y)
    z, zsect, zname = _key(R, z)
    color, csect, cname = _key(R, color)

    vx = R[x]['value'][idt0:idt1, idx, Region, xsect, 0]
    vy = R[y]['value'][idt0:idt1, idx, Region, ysect, 0]
    vz = R[z]['value'][idt0:idt1, idx, Region, zsect, 0]
    vc = R[color]['value'][idt0:idt1, idx, Region, csect, 0]

    points = np.array([vx, vy, vz]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(vc.min(), vc.max())

    fig = plt.figure()
    fig.set_size_inches(10, 5)
    ax = plt.axes(projection='3d')
    ax.plot(vx,
            vy,
            vz, lw=0.01, c='k')
    lc = Line3DCollection(segments, cmap='jet', norm=norm)
    lc.set_array(vc)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    cbar = fig.colorbar(lc, ax=ax)
    cbar.ax.set_ylabel(R[color]['symbol'][:-1] + '_{' + xname + '}$' if xname else R[color]['symbol'])
    ax.set_xlabel(R[x]['symbol'][:-1] + '_{' + xname + '}$' if xname else R[x]['symbol'])
    ax.set_ylabel(R[y]['symbol'][:-1] + '_{' + yname + '}$' if yname else R[y]['symbol'])
    ax.set_zlabel(R[z]['symbol'][:-1] + '_{' + zname + '}$' if zname else R[z]['symbol'])

    # print(R[x]['symbol'][:-1]+'_{'+xname+'}$')

    plt.tight_layout()
    # plt.legend()
    plt.title(title)
    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig


def PhaseSpace(
        hub,
        x: str = 'omega',
        y: str = 'employment',
        width: str = '_speed',
        color: Union[str, bool] = 'g',
        xlim: list[int, int] = [0, .99],
        ylim: list[int, int] = [0, .99],
        title: bool = 'Test',
        idx=0,
        Region=0,
        returnFig=False):
    ''' 
    Given that X and Y are differential variable, show a vector map of the plane X,Y showing the direction of the trajectory`    
    '''

    # Load all the value already in the system
    R = hub.get_dfields()

    # Check that type are correct
    x, xsect, xname = _key(R, x)
    y, ysect, yname = _key(R, y)
    typ1 = R[x]['eqtype']
    typ2 = R[y]['eqtype']
    if typ1 != typ2 != 'differential':
        message = f'Your input fields are not differential ! You have {typ1}, {typ2}'
        raise Exception(message)

    if color:
        color, csect, cname = _key(R, color)

    X, Y = np.meshgrid(np.linspace(xlim[0], xlim[1], 30),  # OMEGA
                       np.linspace(ylim[0], ylim[1], 30))  # EMPLOYMENT
    X.reshape(-1)
    Y.reshape(-1)

    ################

    defaultkeys = [k for k in R[key]['kargs'] if key not in [keys]]
    defaultval = {k: R[k]['value'] for k in defaultkeys if k in hub.dmisc['parameters']}
    defaultval.update({k: R[k]['value'][0, idx, Region, :, :]
                       for k in defaultkeys if k in hub.dmisc['dfunc_order']['statevar']})
    ################
    fig = plt.figure()
    fig.set_figwidth(8)
    fig.set_figheight(8)
    strm = plt.streamplot(X, Y, dXdt, dYdt, density=1, color=g, linewidth=lw)
    cb = fig.colorbar(strm.lines)
    cb.set_label(color, labelpad=-40, y=1.05, rotation=0)

    plt.xlabel(x)
    plt.ylabel(y)

    plt.title(title)
    plt.tight_layout()

    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig
