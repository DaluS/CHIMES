# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 17:20:32 2022

@author: Paul Valcke
"""


def showVariableGraph(model, prog='neato'):
    '''
    Plot a graph of all variable dependencies

    neato
    dot
    twopi
    circo
    fdp
    nop

    Parameters
    ----------
    model : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    import networkx as nx
    import pygraphviz

    hub = Hub(model, verb=False)
    R = hub.get_dparam(returnas=dict)
    # %% GENERATING THE NETWORK ######
    G = nx.DiGraph()

    # Nodes from ODE
    ODENodes = hub.dfunc_order['ode']
    StatevarNodes = hub.dfunc_order['statevar']
    listedgeODE = []
    for k in ODENodes:
        v = R[k]
        G.add_node(R[k]['symbol'], color='red')
        for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
            # listedgeODE.append([k2, k])
            G.add_edge(R[k2]['symbol'], R[k]['symbol'], color='k', weight=1)
    # G.add_edges_from(listedgeODE)

    listedgeStatevar = []
    for k in StatevarNodes:
        v = R[k]
        # print(k)
        G.add_node(R[k]['symbol'], color='gray')
        for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
            G.add_edge(R[k2]['symbol'], R[k]['symbol'],
                       color='k', weight=1, label='Test')

    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    weights = [G[u][v]['weight'] for u, v in edges]
    colorsN = [node[1]['color'] for node in G.nodes(data=True)]

    #pos = nx.nx_agraph.graphviz_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.spring_layout(G, scale=500)

    from networkx.drawing.nx_pydot import graphviz_layout

    pos = graphviz_layout(G, prog=prog)

    plt.figure(model)
    nx.draw(G, pos,
            with_labels=True,
            font_weight='bold',
            edge_color=colors,
            width=weights,
            node_size=1000,
            node_color=colorsN,
            font_size=15,
            arrowstyle='Fancy',)
    plt.show()
