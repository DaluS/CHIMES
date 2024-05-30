from typing import Union, List, Tuple
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib


# Plotly imports
import plotly.graph_objects as go

# Internal imports
from chimes.plots.tools._plot_tools import _indexes, _key
from chimes.plots.tools._plot_tools import value
from chimes.plots.tools._plot_tools import _plotly_dashstyle, _plotly_colors

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


def nyaxis(
        hub,
        y: List[List[str]] = [[]],
        x: str = 'time',
        log: Union[str, List[str]] = 'linear',
        idx: Union[str, int] = 0,
        Region: Union[str, int] = 0,
        tini: int = False,
        tend: int = False,
        title: str = '',
        lw: float = 2,
        sensitivity: bool = True,
        returnFig: bool = False):
    """
    Create a Plotly figure with multiple y-axes for a CHIMES simulation. It is a practical way to display variables that have different units or scales. 

    Parameters
    ----------
    - hub (object): The Hub object containing the model and data.
    - y (List[List[str]]): A list of lists of strings representing the variables to be plotted on the y-axes.
    - x (str, optional): The variable for the x-axis.
    - log (Union[str, List[str]], optional): The type of scale for the y-axes. Can be a string or a list of strings, each element specifying 'linear' or 'log'.
    If a list, it should have the same length as y.
    - idx (Union[str, int], optional): The index for the parallel run.
    - Region (Union[str, int], optional): The region considered for all variables.
    - tini (int, optional): The initial time for the data. By default 0.
    - tend (int, optional): The end time for the data. By default, the end of the run.
    - title (str, optional): The title of the plot.
    - lw (float, optional): The line width for the plot.
    - sensitivity (bool, optional): If True, and if the system did run sensitivity analysis, add the standard deviation around the curve.
    - returnFig (bool, optional): If True, returns the Plotly figure. Otherwise, displays the figure.

    Returns
    -------
    - If returnFig is True, returns the Plotly figure. Otherwise, None (displays the figure).

    Example
    -------
    >>> nyaxis(hub, y=[['employment','omega'],['pi'],['d'],['kappa']], returnFig=True, title='test') with a Goodwin-Keen

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    """
    print(hub)
    print(y)

    if len(y) > 5:
        return "ERROR: too many axes for readibility ! Please do multiple figu"

    # Input cleaning
    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)
    if type(log) is not list:
        log = 5*[log]
    for i, l in enumerate(log):
        if l == False:
            log[i] = 'linear'
        elif l == True:
            log[i] = 'log'
    for l in log:
        if l not in ['linear', 'log']:
            raise Exception(f'log type input not understood! Each element must be "linear" or "log". You gave: {l}')
    while len(log) < 5:
        log.append('linear')

    # Local organisation
    allvarname = [x] + [item for sublist in y for item in sublist]
    R = hub.get_dfields(keys=[allvarname], returnas=dict)
    # Prepare x axis
    vx = value(R, x, idt0, idt1, idx, Region)

    # Figure initialisation
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        width=800)

    vy = {}
    for ii, vlist in enumerate(y):
        # PREPARE DATA AND SYMBOLS
        vy[ii] = {}
        for iii, yyy in enumerate(vlist):
            # Monosectorial entry
            if type(yyy) is str:
                name = yyy
                sectornumber = 0
                sectorname = ''
                symbol = R[yyy]['symbol']

            # Multisectorial entry
            else:
                name = yyy[0]
                if type(yyy[1]) is str:
                    sectornumber = R[R[name]['size'][0]]['list'].index(yyy[1])
                    sectorname = yyy[1]
                else:
                    sectorname = str(yyy[1])
                    sectornumber = yyy[1]

                symbol = name[:-1] + '_{' + sectorname + '}$'

            if sensitivity and ('sensitivity' in hub.dfields[name].keys()):
                stdy = R[name]['sensitivity'][Region]['']['stdv'][idt0:idt1]
                vy[ii][yyy] = R[name]['sensitivity'][Region]['']['mean'][idt0:idt1]

            else:
                vy[ii][yyy] = value(R, name, idt0, idt1, idx, Region, sectornumber)
                stdy = vy[ii][yyy]*0

            fig.add_trace(go.Scatter(
                x=vx,
                y=vy[ii][yyy],
                name=symbol,
                legendgroup=ii,
                legendgrouptitle_text='$'+R[name]['units']+'$' if R[name]['units'] != '' else 'dimensionless',
                line=dict(color=_plotly_colors[ii],
                          width=lw,
                          dash=_plotly_dashstyle[iii],),
                yaxis='y'+str(ii+1) if ii != 0 else 'y'))
            fig.add_trace(go.Scatter(
                x=np.concatenate([vx, vx[::-1]]),
                y=np.concatenate([vy[ii][yyy]-stdy, vy[ii][yyy][::-1]+stdy[::-1]]),
                fill='toself',  # This fills the area between the curves
                fillcolor=str(_plotly_colors[ii]),  # Adjust the color and opacity as needed
                line=dict(color='rgba(255,255,255,0)'),  # Make the line invisible
                showlegend=False,
                yaxis='y'+str(ii+1) if ii != 0 else 'y')
            )

    fig.update_layout(
        xaxis=dict(
            domain=[0, 0.8],
        ),

        xaxis_title=R[x]['symbol'][:-1]+' ('+R[x]['units']+')$',
        yaxis=dict(
            titlefont=dict(color=_plotly_colors[0]),
            tickfont=dict(color=_plotly_colors[0]),
            type=log[0],
            ticks='outside',
            tickmode="sync",
        ),
        yaxis2=dict(
            titlefont=dict(color=_plotly_colors[1]),
            tickfont=dict(color=_plotly_colors[1]),
            type=log[1],
            anchor="free",
            ticks='outside',
            overlaying="y",
            side="right",
            autoshift=True,
            tickmode="sync",
        ),
        yaxis3=dict(
            titlefont=dict(color=_plotly_colors[2]),
            tickfont=dict(color=_plotly_colors[2]),
            type=log[2],
            anchor="free",
            overlaying="y",
            side="left",
            autoshift=True,
            ticks='inside',
            tickmode="sync",
        ),
        yaxis4=dict(
            titlefont=dict(color=_plotly_colors[3]),
            tickfont=dict(color=_plotly_colors[3]),
            type=log[3],
            anchor="free",
            overlaying="y",
            side="right",
            autoshift=True,
            ticks='inside',
            tickmode="sync",
        ),
        yaxis5=dict(
            titlefont=dict(color=_plotly_colors[4]),
            tickfont=dict(color=_plotly_colors[4]),
            type=log[4],
            anchor="free",
            overlaying="y",
            side="left",
            autoshift=True,
            ticks='inside',
            tickmode="sync",
        ),
    )

    fig.update_layout(legend=dict(groupclick="toggleitem"))
    if returnFig:
        return fig
    else:
        fig.show()
