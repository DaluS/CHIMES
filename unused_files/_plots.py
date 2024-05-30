"""
CHIMES Plotting Toolbox

This file contains plotting functions designed to be called directly in CHIMES. These functions are tailored
to work seamlessly with the CHIMES Hub architecture. Some plots are general-purpose, while others are crafted
for specific analyses.

For a list of available plots, you can use `chm.get_available_plots()`. Access individual plots using 
`chm.Plots.NAME_OF_THE_PLOT`.

Author: Paul Valcke

Last Modified: 2024-03-11
"""

from ..chimes.plots.nyaxis import nyaxis
from ..chimes.plots.convergence import convergence
from ..chimes.plots.byunits_plotly import byunits_plotly
from ..chimes.plots.cycles_characteristics import cycles_characteristics
from ..chimes.plots.var import Var
from ..chimes.plots.sensitivity import Showsensitivity
from ..chimes.plots.sankey import Sankey
from ..chimes.plots.ploybyunit_matplotlib import byunits
from ..chimes.plots.phasespace import XY, XYZ
from ..chimes.plots.repartition import repartition

import pandas as pd
import inspect
import types


###############################################################################################################################
"""
This part will be automatized soon. For now, we have to manually add each plot to the list of available plots.
"""
# Plots Locals
AllPlots = [byunits,
            Sankey,
            Showsensitivity,
            Var,
            cycles_characteristics,
            byunits_plotly,
            convergence,
            nyaxis,
            XY, XYZ,
            repartition]
###############################################################################################################################


class PlotsClass:
    """
    Plots contains all the different plotting functions available in CHIMES.
    You can type `chm.get_available_plots()` to see the list of available plots.
    You can access individual plots using `chm.Plots.NAME_OF_THE_PLOT`.
    To get the documentation of a specific plot, use `chm.Plots.NAME_OF_THE_PLOT.__doc__`.
    """

    def __init__(self):

        # Load each plot into the class
        for plot in AllPlots:
            setattr(self, plot.__name__, types.MethodType(plot, self))

        # Create a documentation dataframe
        methods = [method for method in dir(self) if '__' not in method]
        result = {}
        for method in methods:
            Docs = getattr(self, method).__doc__
            signature = inspect.signature(getattr(self, method))
            if Docs:
                Docs = Docs.split('\n')
                result[method] = {'short description': Docs[1][8:],
                                  'signature': signature}
            else:
                print('No docstring found for method: ', method)
        self.documentation = pd.DataFrame(result).transpose()
        self.description = "CHIMES Plotting Toolbox. check `chm.Plots.documentation` for more information."


Plots = PlotsClass()
