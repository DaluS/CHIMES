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


import pandas as pd
import inspect
import types

import os
import importlib


class PlotsClass:
    """
    Plots contains all the different plotting functions available in CHIMES.
    You can type `chm.get_available_plots()` to see the list of available plots.
    You can access individual plots using `chm.Plots.NAME_OF_THE_PLOT`.
    To get the documentation of a specific plot, use `chm.Plots.NAME_OF_THE_PLOT.__doc__`.
    """

    def __init__(self):

        #################################################################

        dir_path = os.path.join(os.path.dirname(__file__), 'plots')

        # Get list of .py files in the directory
        py_files = [file for file in os.listdir(dir_path) if file.endswith('.py') and file != '__init__.py']

        for file_name in py_files:
            module_name = os.path.splitext(file_name)[0]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(dir_path, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Iterate over objects in the module
            module_functions = [func for name, func in inspect.getmembers(module, inspect.isfunction)
                                if func.__module__ == module_name]
            for func in module_functions:
                # Add the function as a method to the class
                setattr(self, func.__name__, func)

        #################################################

        # Create a documentation dataframe
        methods = [method for method in dir(self) if '__' not in method]
        result = {}
        for method in methods:
            Docs = getattr(self, method).__doc__
            signature = inspect.signature(getattr(self, method))
            if Docs:
                Docs = Docs.split('\n')
                result[method] = {'short description': Docs[1],
                                  'signature': signature}
            else:
                print('PlotClass: No docstring found for method: ', method)
        self.documentation = pd.DataFrame(result).transpose()
        self.description = "CHIMES Plotting Toolbox. check `chm.Plots.documentation` for more information."


Plots = PlotsClass()
