"""
CHIMES:
Core for Holistic Intertwined Models of Ecological Sustainability

* Last update 2023/08/17
* Developped at the environmental justice program https://environmentaljustice.georgetown.edu/#
* Contact : Paul Valcke pv229@georgetown.edu

Welcome in CHIMES, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models for ecological sustainability. 

If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file and execute it line by line.

If you change code and functionality in the chimes folder, please do: 
* Update the tutorial 
* Update the unit tests in `tests\test_00_BASIC.py`
* Update the interface.ipynb  
"""
import os as _os
from ._chm_get import get_available_plots
from ._chm_get import get_plot_documentation
from ._chm_get import get_available_fields
from ._chm_get import get_available_config
from ._chm_get import get_available_models
from ._chm_get import get_available_functions
from ._chm_get import get_available_operators
from ._chm_get import get_model_documentation
from ._chm_get import get_available_saves
from ._chm_get import create_models_readme
from ._toolbox import generate_dic_distribution, load_saved
from ._core import Hub
# from . import _plots as _plots
from ._plot_class import Plots

from ._config import config


# MESSAGE LOGO ########################################
if config.get_current('__PRINTINTRO'):
    print(__doc__)
    __Add2 = _os.path.dirname(_os.path.realpath(__file__)) + "\_config.py"
    __Add3 = _os.path.dirname(_os.path.realpath(__file__)) + "\doc\TUTORIALS\TUTORIAL.ipynb"
    print(
        f"""The ipythonNotebook is at : {__Add3}
If you want to customize pyIDEE (advancer users) like removing this message, edit : {__Add2}""")
