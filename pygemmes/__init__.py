# -*- coding: utf-8 -*-


# Here we decide what the user will see
from ._core import Hub
from ._models import get_available_models
from ._utilities._solvers import get_available_solvers
from ._utilities._saveload import get_available_output, load


def plot_one_run_all_solvers(_MODEL, preset=False, _DPRESET=False):
    '''
    Will compare up to seven solver that exist in pygemmes, using the model and preset you provide
    * if no preset, nor dictionary of preset the system takes default values
    * if preset and not dictionary preset, preset must be the name of one of the model preset
    * if preset and _dpreset, the system will load the preset in _dpreset

    Parameters
    ----------
    _MODEL : TYPE
        Name of the model for test
    preset : TYPE, optional
        Name of the preset. if none default value
    _DPRESET : TYPE, optional
        preset dictionary. if none/false, presets from the model

    Returns
    -------
    Print of all solvers super-imposed
    '''

    colors = ['y', 'k', 'm', 'r', 'g', 'b', 'c']
    dsolvers = get_available_solvers(returnas=dict, verb=False,)

    # key is solver name, value is hub
    dhub = {}
    for ii, solver in enumerate(dsolvers):
        print('Solver :', solver)

        # LOADING OF THE MODEL WITH THE CORRESPONDING PRESET
        # IF PRESET AND PRESET FILE GIVEN
        if preset and _DPRESET:
            dhub[solver] = Hub(_MODEL, preset=preset,
                               dpresets=_DPRESET, verb=False)

        # ELIF PRESET NAME GIVEN
        elif preset:
            dhub[solver] = Hub(_MODEL, preset=preset, verb=False)

        # ELSE USE OF BASIC VALUES
        else:
            dhub[solver] = Hub(_MODEL, verb=False)

        # RUN
        dhub[solver].run(verb=1.1, solver='eRK4-homemade')

        # PRINT
        # If first solver, creation of dax
        if ii == 0:
            dax = dhub[solver].plot(
                label=solver, color=colors[ii], wintit='Solver comparison on model'+_MODEL, tit='Solver comparison on model'+_MODEL)
        # Else use of dax
        else:
            dax = dhub[solver].plot(label=solver, ls='--',
                                    color=colors[ii], dax=dax)
