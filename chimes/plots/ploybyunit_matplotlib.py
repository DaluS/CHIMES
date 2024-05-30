# External library imports
from chimes.plots.tools._plot_tools import _LS, _plotly_dashstyle, _plotly_colors
import numpy as np

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib

# Internal imports
from chimes.plots.tools._plot_tools import _indexes
from chimes.plots.tools._plot_tools import value

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


def byunits(
        hub,
        filters_key=(),
        filters_units=(),
        filters_sector=(),
        separate_variables={},
        lw=1,
        idx=0,
        Region=0,
        tini=False,
        tend=False,
        title='',
        returnFig=False):
    '''
    Show all variables, with each unit on a different axis.

    There are three layers of filters, each of them has the same logic :
    if the filter is a tuple () it exclude the elements inside,
    if the filter is a list [] it includes the elements inside.

    Filters are the following :
    filters_units      : select the units you want
    filters_sector     : select the sector you want  ( '' is all monosetorial variables)
    filters_sector     : you can put sector names if you want them or not. '' corespond to all monosectoral variables
    separate_variables : key is a unit (y , y^{-1}... and value are keys from that units that will be shown on another graph,

    Region             : is, if there a multiple regions, the one you want to plot
    idx                : is the same for parrallel systems

    separate_variable : is a dictionnary, which will create a new plot with variables fron the unit selected
    (exemple: you have pi, epsilon and x which share the same units 'y', if you do separate_variables={'y':'x'}
    another figure will be added with x only on it, and pi and epsilon on the other one)

    Author
    ------
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-01-19
    '''
    hub, idx, Region, idt0, idt1 = _indexes(hub, idx, Region, tini, tend)

    # FILTERING THE KEYS
    grpfield = hub.get_dfields_as_reverse_dict(crit='units', eqtype=['differential', 'statevar'])
    # Key filters
    if type(filters_key) is list:
        groupsoffields = {k: [vv for vv in v if vv in filters_key if vv != 'time'] for k, v in grpfield.items() if
                          len(v) > 0}
    else:
        groupsoffields = {k: [vv for vv in v if vv not in filters_key if vv != 'time'] for k, v in grpfield.items() if len(v) > 0}
    # units filters
    if type(filters_units) is list:
        groupsoffields = {k: v for k, v in groupsoffields.items() if k in filters_units}
    else:
        groupsoffields = {k: v for k, v in groupsoffields.items() if k not in filters_units}

    # Separate some variables from the same axis
    separated = {}
    for k, v in separate_variables.items():
        separated[k] = [v2 for v2 in groupsoffields.get(k, []) if v2 in v]
        groupsoffields[k] = [v2 for v2 in groupsoffields.get(k, []) if v2 not in v]
        groupsoffields[k + ' '] = separated[k]
    groupsoffields = {k: v for k, v in groupsoffields.items() if len(v)}

    # PREPARING THE AXES
    Nax = len(groupsoffields.keys())
    Ncol = 2
    Nlin = Nax // Ncol + Nax % Ncol
    allvars = [item for sublist in groupsoffields.values() for item in sublist]
    fig = plt.figure()
    fig.set_size_inches(5 * Ncol, 3 * Nlin+0.1)
    dax = {key: plt.subplot(Nlin, Ncol, i + 1)
           for i, key in enumerate(groupsoffields.keys())}

    # GETTING THE DATA
    R = hub.get_dfields(keys=[allvars], returnas=dict)
    vx = R['time']['value'][idt0:idt1, idx, Region, 0, 0]
    vy = {}
    sectorname = {}
    index = 0
    for key, vvar in groupsoffields.items():
        # GET ALL VALUES
        ismulti = [v in hub.dmisc['dmulti']['vector'] for v in vvar]
        vy[key] = {}
        sectorname[key] = {}
        for ii, yyy in enumerate(vvar):
            if not ismulti[ii]:
                if ('' not in filters_sector and type(filters_sector) is tuple or '' in filters_sector and type(filters_sector) is list):
                    vy[key][yyy] = R[yyy]['value'][idt0:idt1, idx, Region, 0, 0]
                else:
                    vy[key][yyy] = R[yyy]['value'][idt0:idt1, idx, Region, 0, 0]
            else:
                sectors = R[R[yyy]['size'][0]]['list']
                if type(filters_sector) is tuple:
                    sectors = [(jj, x) for jj, x in enumerate(sectors) if x not in filters_sector]
                else:
                    sectors = [(jj, x) for jj, x in enumerate(sectors) if x in filters_sector]

                for jj, s in sectors:
                    vy[key][yyy + '_' + str(s)] = R[yyy]['value'][idt0:idt1, idx, Region, jj, 0]
                    sectorname[key][jj] = s

        # AXIS MAKEUP BEAUTY
        ax = dax[key]
        units = r'$\  ' + key.replace(r'$', r'\$') + r'  \ $'
        ylabel = units
        dax[key].set_ylabel(ylabel)
        ax.set_xlim(vx[0], vx[-1])

        if 1 < index < Nax - 2:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(r'$time (y)$')
        if index < 2:
            ax.xaxis.tick_top()
            # ax.xaxix.label_top()
        ax.grid(axis='x')
        if index % 2 == 1:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        color = np.array(plt.cm.turbo(np.linspace(0, 1, len(vy[key]))))
        # color[:,-1] *= 0.8

        # ADD EFFECTIVELY THE PLOTS
        j = -1
        mini = 1
        for j, key2 in enumerate(vy[key].keys()):
            symb = R[key2.split('_')[0]]['symbol'][:-1] + '_{' + key2.split('_')[1] + '}$' if '_' in key2 else R[key2]['symbol']
            dax[key].plot(vx,
                          vy[key][key2],
                          c=color[j, :],
                          label=symb,
                          ls=_LS[j % (len(_LS) - 1)],
                          lw=lw)
            mini = np.nanmin((mini, np.nanmin(vy[key][key2])))
        if j >= 0:
            dax[key].legend(ncol=1 + j // 4)
        index += 1

        ax.axhline(y=0, color='k', lw=0.5)

    # plt.suptitle(title)
    fig.tight_layout()

    plt.subplots_adjust(top=0.95, wspace=0.01, hspace=0)
    plt.suptitle(title)
    if not returnFig:
        plt.show()
    else:
        plt.close(fig)
        return fig
