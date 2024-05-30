# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 09:46:30 2022

@author: Paul Valcke
"""

import webbrowser
from pylatexenc.latex2text import LatexNodes2Text
from pyvis.network import Network
from copy import deepcopy
# from .._config import _PATH_HERE
from .._config import config
import os


def find_auxiliary(hub):
    """
    Identifies auxiliary variables in the model and their impacts.

    This function scans the model's parameters and identifies auxiliary variables, i.e., variables that are not 
    necessary for a run but may be used for additional calculations or outputs. It also determines what other 
    variables each auxiliary variable impacts.

    Parameters
    ----------
    hub : object
        The model object to scan for auxiliary variables.

    Returns
    -------
    kargs : dict
        A dictionary where each key is an auxiliary variable in the model and the value is a list of other variables 
        that the key variable depends on.
    impact : dict
        A dictionary where each key is an auxiliary variable in the model and the value is a list of other variables 
        that are impacted by the key variable.
    """
    R = hub.get_dfields()
    kargs = {k: [j.replace('itself', k)
                 for j in R[k]['kargs']
                 if j not in hub.dmisc['dfunc_order']['parameters']]
             for k in R.keys() if
             ('kargs' in R[k].keys() and k not in hub.dmisc['dfunc_order']['parameter'])}

    # SEE WHAT VARIABLE IMPACT WHAT
    impact = {k: [] for k in kargs.keys()}
    for k, v in kargs.items():
        for v2 in [v2 for v2 in v if v2 in impact.keys()]:
            impact[v2] += [k]

    return kargs, impact


def filter_kargs(hub, filters, redirect):
    """
    Filters the arguments of a model based on provided filters.

    This function removes or redirects certain arguments of the model based on the provided filters. 
    If 'redirect' is True, the dependencies of the removed arguments are transferred to the arguments they impact.

    Parameters
    ----------
    hub : object
        The model object whose arguments are to be filtered.
    filters : str, list or tuple
        The arguments to be removed. If a string is provided, it is converted to a tuple. 
        If a list is provided, it is converted to a tuple of arguments not in the list.
    redirect : bool
        If True, the dependencies of the removed arguments are transferred to the arguments they impact.

    Returns
    -------
    kargs : dict
        The filtered arguments of the model.
    filters : tuple
        The final set of filters used.
    """
    kargs, impact = find_auxiliary(hub)

    # Convert filters to a tuple if it's a string or a list
    filters = tuple(filters) if type(filters) in [str, tuple] else tuple(set(kargs.keys()) - set(filters))

    # Redirect the dependencies of the removed arguments if redirect is True
    if redirect:
        for key in filters:  # For each key in filters
            klist = impact.get(key, [])
            for k in klist:  # For each impacted field
                kargs[k] = list(set(kargs.get(k, []) + kargs.get(key, [])))
        for k, v in kargs.items():
            kargs[k] = [k for k in v if k not in filters]

    return kargs, filters


def show(net, name, local=True):
    """
    Writes a static HTML file and saves it locally before opening.

    :param: name: the name of the html file to save as
    :type name: str
    """
    write_html(net, name, local)
    webbrowser.open(name)


def write_html(self, name, local=True, notebook=False):
    """
    This method gets the data structures supporting the nodes, edges,
    and options and updates the template to write the HTML holding
    the visualization.
    :type name_html: str
    """
    self.html = self.generate_html(notebook=notebook)

    with open(name, "w+") as out:
        out.write(self.html)


def Network_pyvis(hub,
                  filters=(),
                  auxilliary=False,
                  screensize=600,
                  screenheight=None,
                  screenwidth=None,
                  custom=False,
                  redirect=False,
                  plot_params=True,
                  returnFig=True):
    '''
    Generate an HTML file showing you interactively how are variables linked with their adequate units

    Parameters
    ----------
    _MODEL : Model name you want to show
    screensize : TYPE, optional
        DESCRIPTION. The default is 1080.
    auxilliary : Bool, if False they will not be shown
    filters : list (only the fields kept) or tuple (fields removed)
    custom : TYPE, optional
        DESCRIPTION. The default is False.
    smoothtype :    Possible options: 'dynamic', 'continuous',
                    'discrete', 'diagonalCross', 'straightCross',
                    'horizontal', 'vertical', 'curvedCW',
                    'curvedCCW', 'cubicBezier'.
                    When using dynamic, the edges will have an
                    invisible support node guiding the shape.
                    This node is part of the physics simulation.
                    Default is set to continous.

    Returns
    -------
    None.

    Author
    ------
    Paul Valcke

    Date
    ----
    2023
    '''

    _PATH_HERE = config.get_current('_PATH_HERE')
    # Prepare the data
    R = hub.get_dfields(returnas=dict)
    kargs, impact = find_auxiliary(hub)
    kargs, filters = filter_kargs(hub, filters, redirect)

    ODENodes = [node for node in hub.dfunc_order['differential'] if node != 'time']
    StatevarNodes = hub.dfunc_order['statevar'].copy()
    Parameters = hub.dmisc['dfunc_order']['parameters'].copy() + hub.dmisc['dfunc_order']['parameter'].copy()
    Parameters.remove('nt')

    # Remove all unnecessary elements
    if not auxilliary:
        ODENodes = [key for key in ODENodes if R[key]['isneeded']]
        StatevarNodes = [key for key in StatevarNodes if R[key]['isneeded']]

    ODENodes = [key for key in ODENodes if key not in filters]
    StatevarNodes = [key for key in StatevarNodes if key not in filters]
    Parameters = [key for key in Parameters if key not in filters]

    # Update all kargs with new dictionary
    for k in ODENodes + StatevarNodes:
        R[k]['kargs'] = kargs[k]

    # Determine network size params
    # Use screenheight and/or screenwidth if either or set
    if screenheight is not None or screenwidth is not None:
        height = screenheight
        width = screenwidth
    # Default to a square window of screensize if not
    else:
        height = screensize
        width = screensize

    # Create a new Network object
    net = Network(directed=True, height=height, width=width, heading='', notebook=True)

    # Add parameter nodes to the network
    if plot_params:
        for key in Parameters:
            v = R[key]
            # Exclude numerical and size parameters
            if (v['group'] != 'Numerical' and v.get('eqtype', False) != 'size'):
                # Create a title for the node
                Title = f"""{key}
    'Units        :' {v['units']}
    'definition   :' {v['definition']}
                """
                # Add the node to the network
                net.add_node(key,
                             label=LatexNodes2Text().latex_to_text(R[key]['symbol']),
                             color=['#3da831'],
                             title=Title,
                             group='Parameters',
                             level=2,
                             shape='ellipse')
    else:
        # Add a placeholder node if no parameters are to be plotted
        net.add_node('',
                     label='',
                     color=['#3da831'],
                     title='',
                     group='Parameters',
                     level=2,
                     shape='ellipse')

    # Add state variable nodes to the network
    for key in StatevarNodes:
        v = R[key]
        # Create a title for the node
        Title = f"""{key}
    Units        :{v['units']}
    Equation     :{key}={v['source_exp'].replace('itself', key)}
    definition   :{v['definition']}
    Comment      :{v['com']}
    Dependencies :
    """
        # Add dependencies to the title
        for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
            v1 = hub.dfields[key2]
            Title += f"    {key2:<8}{v1['units']:<10}{v1['definition']}\n"

        # Add the node to the network
        net.add_node(key,
                     label=LatexNodes2Text().latex_to_text(R[key]['symbol']),
                     color=['#3da831'],
                     title=Title,
                     group='STATEVAR',
                     level=2,
                     shape='ellipse')

    # Add ODE nodes to the network
    for key in ODENodes:
        v = R[key]
        # Create a title for the node
        Title = f"""{key}
    Units        :{v['units']}
    Equation     :d{key}/dt={v['source_exp'].replace('itself', key)}
    definition   :{v['definition']}
    Comment      :{v['com']}
    Dependencies :
    """
        # Add dependencies to the title
        for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
            v1 = hub.dfields[key2]
            Title += f"    {key2:<8}{v1['units']:<10}{v1['definition']}\n"

        # Add the node to the network
        net.add_node(key,
                     label=LatexNodes2Text().latex_to_text(R[key]['symbol']),
                     color=['#1dc831'],
                     title=Title,
                     group='ODE',
                     level=2,
                     shape='ellipse')

    # List of nodes to connect
    listconnect = ODENodes + StatevarNodes

    # Add edges to the network
    for k in listconnect:
        v = R[k]
        # Add edges from dependencies to the node
        for k2 in [k3 for k3 in v['kargs'] if k3 in listconnect]:
            net.add_edge(k2, k)
        # Add self-loop if the node depends on itself
        if 'itself' in v['kargs']:
            net.add_edge(k, k)
        # Add edges from parameters to the node
        if plot_params:
            for typ in [None, 'parameter']:
                for k2 in v['args'][typ]:
                    if k2 not in filters:
                        net.add_edge(k2, k)

    # Add parameter connections
    if plot_params:
        for key in list(set(Parameters)):
            v = R[key]
            if v.get('eqtype', False) == 'parameter':
                for k2 in v['kargs']:
                    net.add_edge(k2, key)

    # Set dynamic appearance
    net.set_edge_smooth('dynamic')
    net.repulsion(node_distance=100, spring_length=200)
    if custom:
        net.show_buttons(filter_=False)

    # Prepare the address for saving the network
    address = os.path.join(_PATH_HERE, '../', 'docs', 'networks', hub.dmodel['name'] + '.html')
    if returnFig:
        show(net, address)
    else:
        return net
