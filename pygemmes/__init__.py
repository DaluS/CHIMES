# -*- coding: utf-8 -*-


# Here we decide what the user will see
from ._core import Hub
from ._models import get_available_models
from ._utilities._solvers import get_available_solvers
from ._utilities._saveload import get_available_output, load

# should be removed once Lorenz plot transfered in plot
import matplotlib.pyplot as plt


def create_preset_from_model_preset(targetmodel,
                                    outputmodel,
                                    targetpreset=False,
                                    targetdpreset=False,
                                    returnas='hub'):
    '''
    Open targetmodel, with or without preset/dpreset, and then gives all necessary
    values to outputmodel so that, if they solve the same equations on different approaches,
    they give the same result

    Please note that if they have different mechanism inside with different
    parameters, you have to manually set them so that they have the same behavior.


    Parameters
    ----------
    targetmodel : model name of the model we will copy the value
        DESCRIPTION.
    targetpreset : the preset name for targetmodel. Optional
        DESCRIPTION. The default is False.
    targetdpreset : the dictionnary preset for targetpreset
        DESCRIPTION. The default is False.
    outputmodel : the name of the model we will use after
        DESCRIPTION.
    returnas : (dict,'hub','dpreset') gives different type of output depending of the situation :
        * dict is a dict of field : value
        * hub is outputmodel loaded with the preset
        * dpreset is a dictionnary with this preset inside
        The default is 'hub'.

    Returns
    -------
    None.

    '''
    # LOADING TARGET
    # IF PRESET AND PRESET FILE GIVEN
    if targetpreset and targetdpreset:
        hub = Hub(targetmodel, preset=targetpreset,
                  dpresets=targetdpreset, verb=False)

    # ELIF PRESET NAME GIVEN
    elif targetpreset:
        hub = Hub(targetmodel, preset=targetpreset, verb=False)

    # ELSE USE OF BASIC VALUES
    else:
        hub = Hub(targetmodel, verb=False)

    hub_output = Hub(outputmodel, verb=False)

    # COPY OF THE PARAMETERS INTO A NEW DICTIONNARY
    FieldToLoad = hub_output.get_dparam(returnas=dict, eqtype=[None, 'ode'])
    # group=('Numerical',),)
    R = hub.get_dparam(returnas=dict)
    tdic = {}
    for k, v in FieldToLoad.items():
        val = R[k]['value']
        if 'initial' in v.keys():
            tdic[k] = val[0][0]
        else:
            tdic[k] = val
    _DPRESETS = {'Copy'+targetmodel: {'fields': tdic, }, }

    if returnas == dict:
        return tdic
    if returnas == 'hub':
        return Hub(outputmodel, preset='Copy'+targetmodel,
                   dpresets=_DPRESETS, verb=False)
    if returnas == 'preset':
        return _DPRESETS


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
        dhub[solver].run(verb=1.1, solver=solver)

        # PRINT
        # If first solver, creation of dax
        if ii == 0:
            dax = dhub[solver].plot(
                label=solver, color=colors[ii],
                wintit='Solver comparison on model'+_MODEL,
                tit='Solver comparison on model'+_MODEL)
        # Else use of dax
        else:
            dax = dhub[solver].plot(label=solver,
                                    color=colors[ii], dax=dax)


def comparesolver_Lorenz(dt=0.01):
    Coor = {}
    _MODEL = 'LorenzSystem'
    dmodels = get_available_models(returnas=dict, details=False, verb=False,)
    for solver in get_available_solvers(returnas=dict, verb=False,).keys():
        for preset in dmodels[_MODEL]['presets']:
            hub = Hub(_MODEL, preset=preset, verb=False)
            hub.set_dparam(key='dt', value=dt, verb=False)
            hub.run(verb=0, solver=solver)

            R = hub.get_dparam(returnas=dict)
            Coor[solver] = {'x': R['x']['value'],
                            'y': R['y']['value'],
                            'z': R['z']['value'], }

    fig = plt.figure('', figsize=(10, 10))
    ax = plt.axes(projection='3d')
    for solver in get_available_solvers(returnas=dict, verb=False,).keys():
        ax.plot(Coor[solver]['x'][:, 0],
                Coor[solver]['y'][:, 0],
                Coor[solver]['z'][:, 0], label=solver, lw=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.tight_layout()
    plt.legend()
    plt.show()


def testConvergence_DampOsc(vecdt, solver, returnas='plot'):
    '''
        '''
    import numpy as np
    Error = {}

    for dt in vecdt:
        print("dt:", dt)
        _DPRESETS = {'Convergence test':
                     {'fields': {'Tmax': 20,
                                 'dt': dt,
                                 'gamma': 1,
                                 'Omega': 10,
                                 'Final': 0,
                                 'theta': 1,
                                 'thetap': 0,
                                 },
                      },
                     }
        # Load and preset
        hub = Hub('DampOscillator', preset='Convergence test',
                  dpresets=_DPRESETS, verb=False)
        hub.run(verb=0, solver=solver)

        # Get the informations right
        R = hub.get_dparam(returnas=dict)
        gamma = R['gamma']['value']
        Omega = R['Omega']['value']
        Final = R['Final']['value']
        theta0 = R['theta']['value'][0]
        thetap0 = R['thetap']['value'][0]
        t = R['time']['value']
        thetanum = R['theta']['value']

        # Comparing strategies
        thetaTheo = np.real(theta0*np.exp(-gamma*t) *
                            np.cos(np.sqrt(Omega**2-gamma**2)*t))
        Error[dt] = np.mean(np.sqrt((thetanum-thetaTheo)**2))

    ################################
    dtlist = Error.keys()
    errorlist = [Error[k] for k in Error.keys()]

    Z = sorted(zip(dtlist, errorlist))

    dtlist = [x for x, y in Z]
    errorlist = [y for x, y in Z]

    if returnas == 'plot':
        plt.figure('Convergence')
        plt.loglog(dtlist, errorlist, '-*')
        plt.axis('scaled')
        plt.ylabel('mean error')
        plt.xlabel('dt')
        plt.title('Convergence test for'+solver)
        plt.show()
    else:
        return Error
