import plotly.graph_objects as go
import numpy as np

def sankey(hub,
           matrix='Gamma',
           indt=-1,
           nx=0,
           region=0):
    R=hub.get_dparam()

    d0 = R[matrix]
    values = d0['value'][nx,region,:,:]
    names = R[d0['size'][0]]['list']
    names2= R[d0['size'][1]]['list']

    source=names*len(names2)
    target=np.array([ [n]*len(names) for n in names2]).reshape(-1)
    value=values.reshape(-1)


