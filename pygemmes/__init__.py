
"""
CHIMES:
Core for Holistic Intertwined Models of Ecological Sustainability

* Version 0.1
* Last update 2023/08/10
* Developped at the environmental justice program https://environmentaljustice.georgetown.edu/#
* Contact : Paul Valcke pv229@georgetown.edu

Welcome in CHIMES, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models for ecological sustainability

If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file in doc/tutorial.py or better, and execute it line by line.
"""
from ._models import get_available_models, get_available_functions,get_model_documentation,get_available_operators
from ._toolbox import *
from ._core import Hub
from . import _plots as plots

# MESSAGE LOGO ########################################
from ._config import __PRINTINTRO
import os as _os

if __PRINTINTRO:
    print(__doc__)
    __Add2 = _os.path.dirname(_os.path.realpath(__file__))+"\_config.py"
    __Add3 = _os.path.dirname(_os.path.realpath(__file__)) + "\doc\TUTORIALS\TUTORIAL.ipynb"
    print(
f"""The ipythonNotebook is at : {__Add3}
If you want to customize pyIDEE (advancer users) like removing this message, edit : {__Add2}""")


