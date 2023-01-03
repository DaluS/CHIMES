# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 09:46:30 2022

@author: Paul Valcke
"""

from pyvis.network import Network
from copy import deepcopy
from .._config import _PATH_HERE
import os

def find_auxiliary(hub):

    R = hub.get_dparam()
    kargs = {k: [j.replace('itself', k)
                 for j in R[k]['kargs']
                 if j not in hub.dmisc['dfunc_order']['parameters']]
             for k in R.keys() if
             ('kargs' in R[k].keys()
              and k not in hub.dmisc['dfunc_order']['parameter'])}



    # SEE WHAT VARIABLE IMPACT WHAT
    impact = {k: [] for k in kargs.keys()}
    for k, v in kargs.items():
        for v2 in [v2 for v2 in v if v2 in impact.keys()]:
            impact[v2] += [k]


    return kargs, impact



def filter_kargs(hub, filters,redirect):
    '''
    remove
    '''
    kargs, impact = find_auxiliary(hub)
    # Reverse filters if it is a list
    #print(type(filters))
    if type(filters) is str:
        filters=tuple(list(filters))
    if type(filters) is not tuple:
        filters=tuple(set([k for k in kargs.keys()])-set(filters))
    # REMOVE THE KEY
    if redirect:
        if type(filters) is tuple:
            for ii in range(len(filters)):
                for key in filters:  # For each key in filters
                    klist = impact[key]
                    for k in klist:  # For each impacted field
                        kargs[k] = kargs[k]+kargs[key]
                        kargs[k] = list(set([v2 for v2 in kargs[k]]))
            for k, v in kargs.items():
                kargs[k] = [k for k in list(set(v)) if k not in filters]

    return kargs,filters


def Network_pyvis(hub,
                  filters = (),
                  auxilliary=False,
                  screensize=1080,
                  custom=False,
                  redirect=False,
                  plot_params=True):
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

    '''
    # PREPARE THE DATA
    R = hub.get_dparam(returnas=dict)
    kargs, impact = find_auxiliary(hub)
    kargs,filters = filter_kargs(hub, filters,redirect)


    ODENodes = deepcopy(hub.dfunc_order['differential'])
    ODENodes.remove('time')

    StatevarNodes = deepcopy(hub.dfunc_order['statevar'])
    Parameters = deepcopy(hub.dmisc['dfunc_order']['parameters'])+deepcopy(hub.dmisc['dfunc_order']['parameter'])
    Parameters.remove('nt')


    # REMOVE ALL UNNECESSARY ELEMENTS
    if not auxilliary:
        for key in ODENodes:
            if not R[key]['isneeded']:
                ODENodes.remove(key)
        for key in StatevarNodes:
            if not R[key]['isneeded']:
                StatevarNodes.remove(key)
    for e in filters :
        for key in [k for k in ODENodes if k==e]:
            ODENodes.remove(key)
        for key in [k for k in StatevarNodes if k==e]:
            StatevarNodes.remove(key)
        for key in [k for k in Parameters if k==e]:
            Parameters.remove(key)

    # UPDATE ALL KARGS WITH NEW DICTIONNARY
    for k in ODENodes:
        R[k]['kargs']=kargs[k]
    for k in StatevarNodes:
        R[k]['kargs']=kargs[k]



    net = Network(directed=True, height=screensize, width=screensize,
                  heading=hub.dmodel['name']+f' Logical network, hidden:{filters}',
                  notebook=True)


    if plot_params:
        for key in Parameters:

            v = R[key]
            if (v['group']!='Numerical' and v.get('eqtype',False) != 'size'):
                Title = ''
                Title += 'Units        :' + v['units']+'<br>'
                Title += 'definition   :' + v['definition']+'<br>'
                net.add_node(key,
                             label=key,  # R[key]['symbol'],
                             color=['#3da831'],
                             title=Title.replace(' ', '&nbsp;'),
                             group='Parameters',
                             level=2,
                             shape='ellipse')
    else :
        net.add_node('',
                     label='',
                     color=['#3da831'],
                     title='',
                     group='Parameters',
                     level=2,
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
                v1['units']+(10-len(v1['units']))*' '+v1['definition']+'<br>'

        net.add_node(key,
                     label=key,  # R[key]['symbol'],
                     color=['#3da831'],
                     title=Title.replace(' ', '&nbsp;'),
                     group='STATEVAR',
                     level=2,
                     shape='ellipse')

    for key in ODENodes:
        v = R[key]
        Title = f"""
Units        :{v['units']}<br>
Equation     :d{key}/dt={v['source_exp'].replace('itself', key).replace('lamb','lambda')}<br>
definition   :{v['definition']}<br>
Comment      :{v['com']}<br>
Dependencies :<br>
"""
        for key2 in [v2 for v2 in v['kargs'] if v2 != 'itself']:
            v1 = hub.dparam[key2]
            Title += '    '+key2 + (8-len(key2))*' ' + \
                v1['units']+(10-len(v1['units']))*' '+v1['definition']+'<br>'

        net.add_node(key,
                     label=key,  # R[key]['symbol'],
                     color=['#1dc831'],
                     title=Title.replace(' ', '&nbsp;'),
                     group='ODE',
                     level=2,
                     shape='ellipse')


    listconnect = ODENodes+StatevarNodes



    for k in ODENodes+StatevarNodes:
        v = R[k]
        for k2 in [k3 for k3 in v['kargs'] if k3 in listconnect]:
            net.add_edge(k2, k)
        if 'itself' in v['kargs']:
            net.add_edge(k, k)
        if plot_params:
            for typ in [None,'parameter']:
                for k2 in v['args'][typ]:
                    if k2 not in filters:
                        net.add_edge(k2,k)

    ## Add parameters connections
    if plot_params:
        for key in list(set(Parameters)):
            v = R[key]
            if v.get('eqtype',False) == 'parameter':
                for k2 in v['kargs']:
                    net.add_edge(k2,key)

    # DYNAMIC APPEARANCE
    net.set_edge_smooth('dynamic')
    net.repulsion(node_distance=100, spring_length=200)
    if custom:
        net.show_buttons(filter_=False)

    # net.prep_notebook()

    address = os.path.join(_PATH_HERE[:-9],'doc',hub.dmodel['name']+'.html').replace('/','\\')
    #print(address)
    #net.save_graph('network.html')
    #f = open('network.html', "r")
    
    #return f
    from IPython.core.display import display, HTML
    import tempfile

    def pyvis_deepnote_show(nt):
        #tmp_output_filename = tempfile.NamedTemporaryFile(suffix='.html').name
        nt.save_graph('network.html')

        f = open('network.html', "r")
        display(HTML(f.read()))
    pyvis_deepnote_show(net)