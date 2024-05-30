# Standard library imports
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib


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


def repartition(
    hub,
    keys: list,
    sector='',
    sign='+',
    ref='',
    stock=False,
    refsign='+',
    removetranspose=False,
    title='',
    idx=0,
    Region=0,
    tini=False,
    tend=False,
    returnFig=False
):
    """
    Temporal visualization of a composition, recommended for use on stock-flow consistency and budget repartition.

    Parameters
    ----------
    hub : Hub
        The Hub object containing the model and data.
    keys : list
        List of fields considered in the decomposition.
    sector : str or int, optional
        The sector you want to verify. Monosectoral is ''.
    sign : str, int, or list, optional
        Either '+', '-', or a list of ['+', '-'], to apply for each key. Must be a list of the same length as keys.
    ref : str, optional
        The reference level to compare to the components. Typically in the case of debt stock-flow, ref is dotD.
    stock : bool, optional
        If True, a secondary y-axis will be added for the stock variable.
    refsign : str or int, optional
        The sign of the reference level. Either '+', '-', 1, or -1.
    removetranspose : bool, optional
        If there is a matrix of transactions (from i to j), add negatively the transpose of the matrix terms.
    title : str, optional
        Title of the plot.
    idx : int, optional
        Number of the system in parallel.
    Region : int, optional
        Number or ID of the system considered.
    tini : int, optional
        Initial time step for plotting.
    tend : int, optional
        Final time step for plotting.
    returnFig : bool, optional
        If True, return the matplotlib figure without displaying it.

    Returns
    -------
    matplotlib.figure.Figure or None
        If returnFig is True, returns the matplotlib figure. Otherwise, displays the figure.

    Raises
    ------
    ValueError
        If the length of the sign list does not correspond to the length of the elements.

    Notes
    -----
    - If the specified run has not been performed, an exception is raised.
    - If a cycle information is not available, it is calculated using the specified reference variable.

    Examples
    --------
    Example on a multisectoral:
    >>> repartition(hub, ['pi', 'rd', 'xi', 'gamma', 'omega'], sector='Consumption')
    >>> repartition(hub, ['pi', 'rd', 'xi', 'gamma', 'omega'], sector='Capital')

    Same as repartition, but will take matrices as inputs.

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: OLD
    """
    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)

    # SIGNS HANDING
    # Signs repartition
    if type(sign) in [int, str]:
        sign = [sign for l in keys]
    if len(sign) != len(keys):
        raise Exception(f'The length of the sign list ({len(sign)}) does not correspond to the length of the elements ({len(keys)})!')
    sign = [1 if s in ['+', 1] else -1 for s in sign]
    # refsign handling
    if refsign in ['+', 1]:
        refsign = 1
    else:
        refsign = -1

    R = hub.get_dfields()
    # Sector names ##################################################
    if sector in ['', False, None]:
        sectindex = 0
        sectname = ''
    elif type(sector) is int:
        sectindex = sector * 1
        sectname = R[R[keys[0]]['size'][0]]['list'][sectindex]
    else:
        sectname = str(sector)
        sectindex = R[R[keys[0]]['size'][0]]['list'].index(sectname)

    dicvals = {}  # Dictonnary of entries #############################
    for enum, k in enumerate(keys):                                          # For each entry
        Nsects = R[R[k]['size'][1]].get('list', [''])                        # We check if it has components
        for enum2, sect2name in enumerate(Nsects):                          # Decomposition for matrices

            sectname2 = '-' + sect2name if len(Nsects) > 1 else ''              # Name of matrix sector
            entryname = R[k]['symbol'][:-1] + '_{' + sectname + sectname2 + '}$'   # Name in the dictionnary

            # if the entry is non-zero
            if np.nanmax(np.abs(R[k]['value'][:, idx, Region, sectindex, enum2])) != 0:
                dicvals[entryname] = sign[enum] * R[k]['value'][idt0:idt1, idx, Region, sectindex, enum2]

            if (removetranspose and R[k]['size'][1] != '__ONE__'):
                entrynameT = R[k]['symbol'][:-1] + '_{' + sectname2[1:] + '-' + sectname + '}$'

                # If the entry is non-zero
                if np.max(np.abs(R[k]['value'][:, idx, Region, enum2, sectindex])) != 0:
                    dicvals[entrynameT] = -sign[enum] * R[k]['value'][idt0:idt1, idx, Region, enum2, sectindex]

    color = list(plt.cm.nipy_spectral(np.linspace(0, 1, len(dicvals.keys()) + 1)))
    dicvalpos = {k: np.maximum(v, 0) for k, v in dicvals.items()}
    dicvalneg = {k: np.minimum(v, 0) for k, v in dicvals.items()}
    time = R['time']['value'][idt0:idt1, 0, 0, 0, 0]

    plt.figure()
    fig = plt.gcf()
    # fig.set_size_inches(15, 10 )
    ax = plt.gca()
    if len(ref):
        name = R[ref]['symbol'][:-1] + '_{' + sectname + '}$'
        ax.plot(time, refsign * R[ref]['value'][idt0:idt1, idx, Region, sectindex, 0], c='k', ls='-', lw=2, label=name)
        ax.plot(time, refsign * R[ref]['value'][idt0:idt1, idx, Region, sectindex, 0], c='w', ls='--', lw=2)
    ax.stackplot(time, dicvalpos.values(), labels=dicvals.keys(), colors=color)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')
    ax.stackplot(time, dicvalneg.values(), lw=3, colors=color)

    plt.ylabel('$ ' + R[keys[0]]['units'].replace('$', r'\$') + ' $ ' if len(R[keys[0]]['units']) else 'Repartition')
    plt.xlabel('Time (y)')

    if stock:
        ax2 = plt.twinx(ax)
        ax2.plot(time, R[stock]['value'][idt0:idt1, idx, Region, sectindex, 0], c='r', ls='-', lw=1)

        ax2.set_ylabel(R[stock]['symbol'][:-1] + '_{' + sectname + '}$')

        ax2.tick_params(axis='y', colors='red')
        ax2.yaxis.label.set_color('red')

    plt.suptitle(title)
    plt.tight_layout()
    if not returnFig:
        plt.show()
    else:
        return fig
