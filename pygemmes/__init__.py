
"""
pyIDEE

* Version 0.9
* Last update 2023/01/03
* Developped at the environmental justice program https://environmentaljustice.georgetown.edu/#
* Contact : Paul Valcke pv229@georgetown.edu

Welcome in PyIDEE, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models

If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file in doc/tutorial.py or better, and execute it line by line.
"""
from ._models import get_available_models, get_available_functions
from ._toolbox import *
from ._core import Hub
from . import _plots as plots

# MESSAGE LOGO ########################################
from ._config import __PRINTLOGO, __PRINTINTRO
import os

if __PRINTINTRO:
    print(__doc__)
    __Add2 = os.path.dirname(os.path.realpath(__file__))+"\_config.py"
    __Add3 = os.path.dirname(os.path.realpath(__file__)) + "\doc\TUTORIALS\TUTORIAL.ipynb"
    print(
f"""The ipythonNotebook is at : {__Add3}
If you want to customize pyIDEE (advancer users) like removing this message, edit : {__Add2}""")