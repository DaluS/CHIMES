# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 09:46:30 2022

@author: Paul Valcke
"""

from pyvis.network import Network
from copy import deepcopy

def Network_pyvis(hub,
                  screensize=1080,
                  custom=False,
                  smoothtype='dynamic',
                  plot_params=True):
    '''
    Generate an HTML file showing you interactively how are variables linked with their adequate units

    Parameters
    ----------
    _MODEL : Model name you want to show
    screensize : TYPE, optional
        DESCRIPTION. The default is 1080.
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

    '''
    ### PREPARE THE DATA
    R = hub.get_dparam(returnas=dict)

    ODENodes = deepcopy(hub.dfunc_order['ode'])
    ODENodes.remove('time')

    StatevarNodes = deepcopy(hub.dfunc_order['statevar'])

    Parameters = deepcopy(hub.dmisc['parameters'])

    net = Network(directed=True, height=screensize, width=screensize,
                  heading=hub.dmodel['name']+' Logical network')

    for key in ODENodes:
        v = R[key]
        Title = f"""
Units        :{v['units']}<br>
Equation     :+d{key}/dt={v['source_exp'].replace('itself', key).replace('lamb','lambda')}<br>
definition   :' + v['definition']+'<br>
Comment      :' + v['com']+'<br>
Dependencies :'+'<br>
"""
        for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
            v1 = hub.dparam[key2]
            Title += '    '+key2 + (8-len(key2))*' ' + \
                v1['units']+(8-len(v1['units']))*' '+v1['definition']+'<br>'

        net.add_node(key,
                     label=key,  # R[key]['symbol'],
                     color=['#3da831'],
                     title=Title.replace(' ', '&nbsp;'),
                     group='ODE',
                     level=1,
                     shape='ellipse')

    for key in StatevarNodes:

        v = R[key]
        Title = ''
        Title += 'Units        :' + v['units']+'<br>'
        Title += 'Equation     :'+f'{key}=' + v.get('source_exp', 'f()').replace(
            'itself', key).replace('lamb', 'lambda')+'<br>'
        Title += 'definition   :' + v['definition']+'<br>'
        Title += 'Comment      :' + v['com']+'<br>'
        Title += 'Dependencies :'+'<br>'
        for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
            v1 = hub.dparam[key2]
            Title += '    '+key2 + (8-len(key2))*' ' + \
                v1['units']+(8-len(v1['units']))*' '+v1['definition']+'<br>'

        net.add_node(key,
                     label=key,  # R[key]['symbol'],
                     color=['#3da831'],
                     title=Title.replace(' ', '&nbsp;'),
                     group='STATEVAR',
                     level=2,
                     shape='ellipse')

    if plot_params:
        for key in Parameters:
            v = R[key]
            Title = ''
            Title += 'Units        :' + v['units']+'<br>'
            Title += 'definition   :' + v['definition']+'<br>'
            net.add_node(key,
                         label=key,  # R[key]['symbol'],
                         color=['#1dc831'],
                         title=Title.replace(' ', '&nbsp;'),
                         group='Parameters',
                         level=2,
                         shape='ellipse')

    listconnect = ODENodes+StatevarNodes
    if plot_params:listconnect+=Parameters

    for k in ODENodes+StatevarNodes:
        v = R[k]
        for k2 in [k3 for k3 in v['kargs'] if k3 in listconnect]:
            net.add_edge(k2, k)
        if 'itself' in v['kargs']:
            net.add_edge(k, k)

    ### DYNAMIC APPEARANCE
    net.set_edge_smooth('dynamic')
    net.repulsion(node_distance=100, spring_length=200)
    if custom:
        net.show_buttons(filter_=False)


    #net.prep_notebook()
    net.show(hub.dmodel['name']+'.html')
