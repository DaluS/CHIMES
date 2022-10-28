# -*- coding: utf-8 -*-
"""

#####################################################################################
 _______            ______  ________  ____    ____  ____    ____  ________   ______
|_   __ \         .' ___  ||_   __  ||_   \  /   _||_   \  /   _||_   __  |.' ____  \
  | |__) |_   __ / .'   \_|  | |_ \_|  |   \/   |    |   \/   |    | |_ \_|| (___ \_|
  |  ___/[ \ [  ]| |   ____  |  _| _   | |\  /| |    | |\  /| |    |  _| _  _.____`.
 _| |_    \ '/ / \ `.___]  |_| |__/ | _| |_\/_| |_  _| |_\/_| |_  _| |__/ || \____) |
|_____| [\_:  /   `._____.'|________||_____||_____||_____||_____||________| \______.'
         \__.'
#####################################################################################

Welcome in Pygemmes, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models
You can find the files on https://github.com/DaluS/GEMMES
This library has been coded mostly by Didier Vezinet and Paul Valcke,
at the environmental justice program https://environmentaljustice.georgetown.edu/#
You can contact me at pv229@georgetown.edu
If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file in doc/tutorial.py and execute it line by line.

TO EXPLORE :
pgm.get_available_ then tab to see what is available
    examples :
    * pgm.get_available_fields()
    * pgm.get_available_models(details=False)
    * pgm.get_available_solvers()
    * pgm.get_available_functions()
pgm.Hub() to load a model
"""

# Here we decide what the user will see
#from ._private_pygemmes import create_private_pygemmes
# run private pygemmes creation, be conservative
# has to be done before other imports!
#create_private_pygemmes(reset=False, reset_hard=False)


# Here we decide what the user will see
from ._models import get_available_models, get_available_functions
from ._toolbox import *
from ._utilities._saveload import get_available_output, load
from ._utilities._solvers import get_available_solvers
from ._core import Hub
from . import _plots as plots



# MESSAGE LOGO ########################################
from ._config import __PRINTLOGO, __PRINTINTRO
import os
if __PRINTLOGO:
    print("""
#####################################################################################
 _______            ______  ________  ____    ____  ____    ____  ________   ______    
|_   __ \         .' ___  ||_   __  ||_   \  /   _||_   \  /   _||_   __  |.' ____  \   
  | |__) |_   __ / .'   \_|  | |_ \_|  |   \/   |    |   \/   |    | |_ \_|| (___ \_|  
  |  ___/[ \ [  ]| |   ____  |  _| _   | |\  /| |    | |\  /| |    |  _| _  _.____`.   
 _| |_    \ '/ / \ `.___]  |_| |__/ | _| |_\/_| |_  _| |_\/_| |_  _| |__/ || \____) |  
|_____| [\_:  /   `._____.'|________||_____||_____||_____||_____||________| \______.'  
         \__.'                           
#####################################################################################                                                                                                                                   
""")
if __PRINTINTRO:
    __Add= os.path.dirname(os.path.realpath(__file__))+r'doc\tutorial.py'
    __Add2 = os.path.dirname(os.path.realpath(__file__))+"\_config.py"
    __Add3 = os.path.dirname(os.path.realpath(__file__)) + "\_Presentation.ipynb"
    print(
f"""Welcome in Pygemmes, a modular library to prototype and study dynamical systems !
This library is oriented toward generation of macroeconomic complexity models 
You can find the files on https://github.com/DaluS/GEMMES
This library has been coded mostly by Didier Vezinet and Paul Valcke,
at the environmental justice program https://environmentaljustice.georgetown.edu/#
You can contact me at pv229@georgetown.edu 
If you find bugs, want some new extensions, or help us improve the library, please create a new issue on github
If this is the first time you open this library, please look at the tutorial file in doc/tutorial.py and execute it line by line. 
Its adress is {__Add}
The ipythonNotebook is at {__Add3}
If you want to customize pygemmes (advancer users) like removing this message, edit {__Add2}
Have fun !
######################################################################################################
"""   )
# ########################################

