# built-in
import time
from copy import copy, deepcopy

# common
import numpy as np

# specific
from . import _hub_check


def solve(
        dfields=None,
        dmisc=None,
        stepini=0,
        stepend=0,
        dverb=None,
        ComputeStatevarEnd=False,
        solver='rk4'
):
    """
    Temporal solver of the system.

    This function solves the system of differential equations over a specified time range using the specified solver. 
    It initializes the system state, then enters a loop where it computes the state at each time step and stores the 
    results. If ComputeStatevarEnd is True, it recomputes all state variables at the end.

    Parameters
    ----------
    dfields : dict, optional
        Dictionary of parameters for the differential equations.
    dmisc : dict, optional
        Dictionary of miscellaneous data.
    stepini : int, optional
        The initial time step. Default is 0.
    stepend : int, optional
        The final time step. Default is 0.
    dverb : dict, optional
        Dictionary of verbosity settings.
    ComputeStatevarEnd : bool, optional
        Whether to recompute all state variables at the end. Default is False.
    solver : str, optional
        The solver to use. Default is 'rk4'.

    Returns
    -------
    stepend : int
        The final time step.
    time : float
        The time at the final time step.

    Author
    ------
    Paul Valcke

    Date
    ----
    End 2023 for conputestatevar
    """

    # Retrieve the order of differential equations, state variables, and parameters
    lode = dmisc['dfunc_order']['differential']
    lstate = dmisc['dfunc_order']['statevar']
    lparam = dmisc['dfunc_order']['parameter'] + dmisc['dfunc_order']['parameters'] + ['dt']

    # Define initial state and all functions to iterate in order with their references
    y0, dydt_func = get_func_dydt(
        dfields=dfields,
        lode=lode,
        lstate=lstate,
        lparam=lparam,
        stepini=stepini
    )

    # Initialize y
    y = deepcopy(y0)

    # Get the current time
    t0 = time.time()

    ii = 0
    # Start loop on time
    for ii in range(stepini + 1, stepend):
        # Print or wait if verbosity is greater than 0
        if dverb['verb'] > 0:
            t0 = _hub_check._print_or_wait(ii=ii, nt=dfields['nt']['value'], t0=t0, **dverb)

        # Compute ode variables from ii-1, using solver
        if solver == 'rk1':
            y, state = _rk1(dydt_func=dydt_func, dt=dfields['dt']['value'], y=y)
        else:
            y, state = _rk4(dydt_func=dydt_func, dt=dfields['dt']['value'], y=y)

        # Store result of ode
        for k0 in lode:
            dfields[k0]['value'][ii, ...] = y[k0]

        # Store state variables if not computing at the end
        if not ComputeStatevarEnd:
            for k0 in lstate:
                dfields[k0]['value'][ii, ...] = state[k0]

    # Print or wait if verbosity is greater than 0
    # if dverb['verb']:
    #    dverb['timewait'] = False
    #    _hub_check._print_or_wait(ii=ii, nt=dfields['nt']['value'], t0=t0, **dverb)

    # Compute statevar functions, in good order, if computing at the end
    if ComputeStatevarEnd:
        for k0 in lstate:
            dfields[k0]['value'][...] = dfields[k0]['func'](**{k: dfields[k]['value'][...] for k in dfields[k0]['kargs']})

    # Return the final time step and the time at the final time step
    return stepend, dfields['time']['value'][ii, 0, 0, 0, 0]


def get_func_dydt(
    dfields=None,  # Big dictionnary with values and dependencies
    lode=None,  # ordered list of differential equations
    lstate=None,  # ordered list of state variables
    lparam=None,  # list of existing parameters
    stepini=0
):
    """
    Generate initial values and a function for computing time derivatives.

    This function generates initial values for the differential equations and a function for computing the time 
    derivatives of these equations. The function uses the provided parameters, state variables, and differential 
    equations.

    Parameters
    ----------
    dfields : dict, optional
        A dictionary containing the values and dependencies for the differential equations. Each key should be the name 
        of a differential equation, and the value should be another dictionary containing the 'value' of the equation 
        and any 'func' and 'kargs' used to compute it.
    lode : list, optional
        An ordered list of the names of the differential equations.
    lstate : list, optional
        An ordered list of the names of the state variables.
    lparam : list, optional
        A list of the names of the existing parameters.
    stepini : int, optional
        The initial time step. Default is 0.

    Returns
    -------
    y0 : dict
        A dictionary containing the initial values of the differential equations.
    func : function
        A function that computes the time derivatives of the differential equations.

    Author
    ------
    Didier Vezinet
    Paul Valcke: comments, restructuration, and optimization

    Date
    ----
    End 2023 
    """
    # Initialize the values for the differential equations at the initial time step
    y0 = {k: dfields[k]['value'][stepini, ...] for k in lode}

    # Initialize a dictionary to store the time variation of each differential equation
    dydt = {k: np.full(np.shape(v), np.nan) for k, v in y0.items()}

    # Initialize a buffer to store local calculations for each differential equation
    dbuffer = {k0: dfields[k0]['value'][stepini, ...] for k0 in lode}

    # Add the values of the parameters to the buffer
    for k0 in lparam:
        dbuffer[k0] = dfields[k0]['value']

    # Define a function to compute the time derivatives of the differential equations
    def func(y, dbuffer=dbuffer, dydt=dydt, dfields=dfields):
        # Update the buffer with the current values of the differential equations
        for k0 in lode:
            dbuffer[k0] = y[k0]

        # Compute the current values of the state variables and update the buffer
        for k0 in lstate:
            dbuffer[k0] = dfields[k0]['func'](**{k: dbuffer[k] for k in dfields[k0]['kargs']})

        # Compute the time derivatives of the differential equations
        for k0 in lode:
            dydt[k0] = dfields[k0]['func'](**{k: dbuffer[k] for k in dfields[k0]['kargs']})

        # Return a copy of the time derivatives and the buffer
        return copy(dydt), dbuffer

    # Return the initial values and the function to compute the time derivatives
    return y0, func


def _rk4(dydt_func=None, dt=None, y=None):
    """
    a traditional RK4 scheme, with:
        - y = array of all variables (all ode)
        - dt = fixed time step

    Author
    ------
    Paul Valcke

    Date
    ----
    2022
    """
    dy1_on_dt, state = dydt_func(y)
    dy2_on_dt, _ = dydt_func({k: y[k] + dy1_on_dt[k] * dt / 2. for k in y.keys()})
    dy3_on_dt, _ = dydt_func({k: y[k] + dy2_on_dt[k] * dt / 2. for k in y.keys()})
    dy4_on_dt, _ = dydt_func({k: y[k] + dy3_on_dt[k] * dt / 1. for k in y.keys()})
    yend = {k: y[k] + (dy1_on_dt[k] + 2 * dy2_on_dt[k] + 2 * dy3_on_dt[k] + dy4_on_dt[k]) * dt / 6 for k in y.keys()}
    return yend, state


def _rk1(dydt_func=None, dt=None, y=None):
    dy1_on_dt, state = dydt_func(y)
    return {k: y[k] + dy1_on_dt[k] * dt for k in y.keys()}, state
