# -*- coding: utf-8 -*

import pandas as pd
import pygraphviz
import numpy as np
import pygemmes as pgm
import networkx as nx
import matplotlib.pyplot as plt
from graph_tools import Graph
import graph_tools as gt
import pygraphviz as pgv
A = pgv.AGraph(directed=True,)
model = 'GK'

hub = pgm.Hub(model, verb=False)
R = hub.get_dparam(returnas=dict)

# Nodes from ODE
ODENodes = hub.dfunc_order['ode']
StatevarNodes = hub.dfunc_order['statevar']
listedgeODE = []
for k in ODENodes:
    v = R[k]
    #G.add_node(R[k]['symbol'], color='red')
    for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
        # listedgeODE.append([k2, k])
        # , color='k', weight=1)
        A.add_edge(R[k2]['symbol'], R[k]['symbol'])
    # G.add_edges_from(listedgeODE)

listedgeStatevar = []
for k in StatevarNodes:
    v = R[k]
    # print(k)
    #A.add_node(R[k]['symbol'], color='gray')
    for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
        A.add_edge(R[k2]['symbol'], R[k]['symbol'])  # ,
#                       color='k', weight=1, label='Test')

#    edges = G.edges()
#    colors = [G[u][v]['color'] for u, v in edges]
#    weights = [G[u][v]['weight'] for u, v in edges]
#    colorsN = [node[1]['color'] for node in G.nodes(data=True)]
A.draw("subgraph.png", prog="neato")

pos = nx.nx_agraph.graphviz_layout(G)
#pos = nx.shell_layout(G)
#pos = nx.spring_layout(G, scale=500)


# %% EXTRACT MODEL DATA ##########
# hub = pgm.Hub('GK-Reduced')


showVariableGraph('GK')

model = 'GK'


gt.draw.planar_layout(G)

# Plot a graph using Graph-tool


G = Graph()
ODENodes = hub.dfunc_order['ode']
StatevarNodes = hub.dfunc_order['statevar']
for k in ODENodes:
    v = R[k]
    G.add_vertex(R[k]['symbol'])
    for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
        # listedgeODE.append([k2, k])
        G.add_edge(R[k2]['symbol'], R[k]['symbol'])

for k in StatevarNodes:
    v = R[k]
    G.add_vertex(R[k]['symbol'])
    for k2 in [k3 for k3 in v['kargs'] if k3 in ODENodes+StatevarNodes]:
        G.add_edge(R[k2]['symbol'], R[k]['symbol'])

gt.graph_draw(G, vertex_text=g.vertex_index, output="test.pdf")

# %% ALTERNATIVE VERSIOn

# Build a dataframe with your connections
df = pd.DataFrame({'from': ['A', 'B', 'C', 'A'], 'to': ['D', 'A', 'E', 'C']})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to')

# Graph with Custom nodes:
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue",
        node_shape="s", alpha=0.5, linewidths=40)
plt.show()
