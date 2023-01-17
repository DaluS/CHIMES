
"""
Created on Fri Mar  4 12:46:42 2022

@author: Paul Valcke
"""

import copy
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec


# ############################################################################
# ############## SUBFUNCTIONS ################################################


def _multiline(xs, ys, c, ax=None, **kwargs):
    """Plot lines with different colorings

    Parameters
    ----------
    xs : iterable container of x coordinates
    ys : iterable container of y coordinates
    c : iterable container of numbers mapped to colormap
    ax (optional): Axes to plot on.
    kwargs (optional): passed to LineCollection

    Notes:
        len(xs) == len(ys) == len(c) is the number of line segments
        len(xs[i]) == len(ys[i]) is the number of points for each line (indexed by i)

    Returns
    -------
    lc : LineCollection instance.
    """

    # find axes
    ax = plt.gca() if ax is None else ax

    # create LineCollection
    segments = [np.column_stack([x, y]) for x, y in zip(xs, ys)]
    lc = LineCollection(segments, **kwargs)

    # set coloring of line segments
    #    Note: I get an error if I pass c as a list here... not sure why.
    lc.set_array(np.asarray(c))

    # add lines to axes and rescale
    #    Note: adding a collection doesn't autoscalee xlim/ylim
    ax.add_collection(lc)
    ax.autoscale()
    return lc

def _indexes(hub,idx,Region,tini,tend):
    R=hub.dparam
    print('idx',idx,'region',Region,'tini',tini,'tend',tend)
    # RUN
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()


    # idx input
    if type(idx)==int: pass 
    elif type(idx)==str:
        try : idx=hub.dparam['nx']['list'].index(idx)
        except BaseException:
            liste=hub.dparam['nx']['list']
            raise Exception(f'the parrallel system cannot be found !\n you gave {idx} in {liste}')
    else: raise Exception(f'the parrallel index cannot be understood ! you gave {idx}')

    # Region input 
    if type(Region)==int: pass 
    elif type(Region)==str:
        try : Region=hub.dparam['nr']['list'].index(Region)
        except BaseException:
            liste=hub.dparam['nr']['list']
            raise Exception(f'the parrallel system cannot be found !\n you gave {idx} in {liste}')
    else: raise Exception(f'the parrallel index cannot be understood ! you gave {idx}')

 
    # time input
    time = R['time']['value'][:,idx,Region,0,0]
    if tini: idt0=np.argmin(np.abs(time-tini))
    else : idt0=0

    if tend: idt1=np.argmin(np.abs(time-tend))
    else : idt1=-1

    return hub,idx,Region,idt0,idt1

def _key(key):
    if type(key) is list :
        keysect=R[R[key[0]]['size'][0]]['list'].index(key[1])
        key,keyname=key[0],key[1]
    else : keysect,keyname=0,''
    return keysect,keyname