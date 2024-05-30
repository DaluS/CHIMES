# Standard library imports
from chimes.plots.tools.plotbyunits import PlotByUnits
from chimes.plots.tools.filter import IncludeKeyFilter, ExcludeKeyFilter, IncludeUnitFilter, ExcludeUnitFilter, IncludeSectorFilter, ExcludeSectorFilter
from chimes.plots.tools.plotbyunits import PlotByUnits

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib


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


def byunits_plotly(
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
    returnFig=False,
):
    '''
    Plotly version of plot_by_units. Wrap of Stephen's plotly code.

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
    Stephen Kent
    Paul Valcke

    Last Modified
    -------------
    Date: 2024-03-04
    '''
    plot = PlotByUnits()
    plot = PlotByUnits()
    plot.load_variables(hub)

    if type(filters_key) is list:
        plot.set_filters([IncludeKeyFilter(k) for k in filters_key])
    elif type(filters_key) is tuple:
        plot.set_filters([ExcludeKeyFilter(k) for k in filters_key])

    if type(filters_units) is list:
        plot.set_filters([IncludeUnitFilter(k) for k in filters_key])
    elif type(filters_units) is tuple:
        plot.set_filters([ExcludeUnitFilter(k) for k in filters_key])

    if type(filters_sector) is list:
        plot.set_filters([IncludeSectorFilter(k) for k in filters_key])
    elif type(filters_sector) is tuple:
        plot.set_filters([ExcludeSectorFilter(k) for k in filters_key])

    plot.generate(title=title,
                  separate_variables=separate_variables,
                  lw=lw,
                  idx=idx,
                  tini=tini,
                  tend=tend,
                  )
    if returnFig:
        return plot
    else:
        plot.show()
