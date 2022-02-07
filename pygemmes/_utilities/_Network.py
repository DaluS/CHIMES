# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 09:46:30 2022

@author: Paul Valcke
"""

from pyvis.network import Network


def Network_pyvis(hub,
                  screensize=1080,
                  custom=False,
                  smoothtype='dynamic'):
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

    R = hub.get_dparam(returnas=dict)

    ODENodes = hub.dfunc_order['ode']
    ODENodes.remove('time')
    StatevarNodes = hub.dfunc_order['statevar']

    net = Network(directed=True, height=screensize, width=screensize,
                  heading=hub.dmodel['name']+' Logical network')

    for key in ODENodes:
        v = R[key]
        Title = ''
        Title += 'Units        :' + v['units']+'<br>'
        Title += 'Equation     :'+f'd{key}/dt=' + v['source_exp'].replace(
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

    for k in ODENodes+StatevarNodes:
        v = R[k]
        for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
            net.add_edge(k2, k)
        if 'itself' in v['kargs']:
            net.add_edge(k, k)

    net.set_edge_smooth('dynamic')

    net.repulsion(node_distance=100, spring_length=200)
    if custom:
        net.show_buttons(filter_=False)

    # net.prep_notebook()
    net.show(hub.dmodel['name']+'.html')
