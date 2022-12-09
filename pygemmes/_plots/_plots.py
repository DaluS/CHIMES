# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:16:01 2021
@author: Paul Valcke

"""

from ._plot_timetraces import plot_timetraces
from ._plot_tools import _multiline

import copy
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

from mpl_toolkits.mplot3d.art3d import Line3DCollection

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec


__USETEX=False

_LS = [
    (0, ()),
    (0, (1, 1)),
    (0, (5, 1)),  # densely dashed
    (0, (3, 1, 1, 1, 1, 1)),
    (0, (5, 5)),
    (0, (3, 5, 1, 5)),
    (0, (3, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdot
    (0, (1, 5)),  # dotted
    (0, (5, 10)),
    (0, (5, 5))
]

matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
plt.rcParams.update({'font.size': 15})
params = {'legend.fontsize': 10,
          'legend.handlelength': 2,
          'legend.borderpad':0,
          'legend.labelspacing':0.0}
SIZETICKS = 20
SIZEFONT = 25
LEGENDSIZE = 20
LEGENDHANDLELENGTH = 2

if __USETEX:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=SIZEFONT)
    plt.rcParams.update({'figure.autolayout': True})
    plt.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath} \usepackage{libertine}"]
    ticksfontProperties = {'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'weight': 'medium',}
plt.rcParams.update(params)





__all__ = [
    #'slices_wholelogic',
    #'plot_variation_rate',
    'plot_timetraces',
    'plotnyaxis',
    'phasespace',
    'plot3D',
    'plotbyunits',
    'Var',
    'cycles_characteristics',
    'repartition'
]

# ############################################################################
# ############## IMPORTANT PLOTS #############################################

def plotbyunits(hub,
               filters_key=(),
               filters_units=(),
               filters_sector=(),
               separate_variables={},
               lw=1,
               idx=0,
               Region=0,
               title=''):
    '''
    generate one subfigure per set of units existing.

    There are three layers of filters, each of them has the same logic :
    if the filter is a tuple () it exclude the elements inside,
    if the filter is a list [] it includes the elements inside.

    Filters are the following :
    filters_units      : select the units you want
    filters_sector     : select the sector you want  ( '' is all monosetorial variables)
    filters_sector     : you can put sector names if you want them or not. '' corespond to all monosectoral variables
    separate_variables : key is a unit (y , y^{-1}... and value are keys from that units that will be shown on another graph,

    Region             : is, if there a multiple regions, the one you want to plot
    idx                : is the same for parrallel systems



    separate_variable : is a dictionnary, which will create a new plot with variables fron the unit selected
    (exemple: you have pi, epsilon and x which share the same units 'y', if you do separate_variables={'y':'x'}
    another figure will be added with x only on it, and pi and epsilon on the other one)

    '''
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()

    ### FILTERING THE KEYS
    grpfield = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['differential', 'statevar'])
    ### Key filters
    if type(filters_key)==list:
        groupsoffields = {k: [vv for vv in v if vv in filters_key if vv != 'time'] for k, v in grpfield.items() if
                          len(v) > 0}
    else:
        groupsoffields = {  k:[vv for vv in v if vv not in filters_key if vv != 'time'] for k,v in grpfield.items() if len(v)>0}
    ### units filters
    if type(filters_units)==list:
        groupsoffields = {k: v for k, v in groupsoffields.items() if k in filters_units}
    else:
        groupsoffields = {k: v for k, v in groupsoffields.items() if k not in filters_units}

    ### Separate some variables from the same axis
    separated = {}
    for k,v in separate_variables.items():
        separated[k]=[v2 for v2 in groupsoffields.get(k,[]) if v2 in v]
        groupsoffields[k]=[v2 for v2 in groupsoffields.get(k,[]) if v2 not in v]
        groupsoffields[k+' ']=separated[k]
    groupsoffields = {k : v for k,v in groupsoffields.items() if len(v)}

    # PREPARING THE AXES
    Nax = len(groupsoffields.keys())
    Ncol = 2
    Nlin = Nax // Ncol + Nax % Ncol
    allvars = [item for sublist in groupsoffields.values() for item in sublist]
    fig = plt.figure()
    fig.set_size_inches(10*Ncol, 3*Nlin)
    dax = {key: plt.subplot(Nlin, Ncol, i+1)
           for i, key in enumerate(groupsoffields.keys())}

    # GETTING THE DATA
    R = hub.get_dparam(keys=[allvars], returnas=dict)
    vx = R['time']['value'][:, idx,Region,0,0]
    vy = {}
    sectorname={}
    index = 0
    for key, vvar in groupsoffields.items():
        ## GET ALL VALUES
        ismulti = [v in hub.dmisc['dmulti']['vector'] for v in vvar  ]
        vy[key]= {}
        sectorname[key]={}
        for ii,yyy in enumerate(vvar):
            if not ismulti[ii]:
                if ('' not in filters_sector and type(filters_sector)==tuple or
                    '' in filters_sector and type(filters_sector)==list):
                    vy[key][yyy]=R[yyy]['value'][:, idx,Region,0,0]
                else :
                    vy[key][yyy] = R[yyy]['value'][:, idx, Region, 0, 0]
            else:
                sectors = R[R[yyy]['size'][0]]['list']
                if type(filters_sector)==tuple:
                    sectors=[ (jj,x) for jj,x in enumerate(sectors) if x not in filters_sector]
                else:
                    sectors=[ (jj,x) for jj,x in enumerate(sectors) if x in filters_sector]

                for jj,s in sectors:
                    vy[key][yyy+'_'+str(s)]=R[yyy]['value'][:, idx,Region,jj,0]
                    sectorname[key][jj]=s

        ## AXIS MAKEUP BEAUTY
        ax = dax[key]
        units = r'$\  '+key.replace('$', '\$')+'  \ $'
        ylabel = units
        dax[key].set_ylabel(ylabel)
        ax.set_xlim(vx[0], vx[-1])


        if 1 < index < Nax-2:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(r'$time (y)$')
        if index < 2:
            ax.xaxis.tick_top()
            # ax.xaxix.label_top()
        ax.grid(axis='x')
        if index % 2 == 1:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        color = np.array(plt.cm.turbo(np.linspace(0,1,len(vy[key]))))
        #color[:,-1] *= 0.8

        ### ADD EFFECTIVELY THE PLOTS
        j=-1
        mini=1
        for j, key2 in enumerate(vy[key].keys()):
            symb= R[key2.split('_')[0]]['symbol'][:-1] + '_{'+key2.split('_')[1]+'}$' if '_' in key2 else R[key2]['symbol']
            dax[key].plot(vx,
                          vy[key][key2],
                          c=color[j,:],
                          label=symb ,
                          ls=_LS[j % (len(_LS)-1)],
                          lw=lw)
            mini=np.nanmin((mini,np.nanmin(vy[key][key2])))
        if j >= 0:
            dax[key].legend(ncol=1+j//4)
        index += 1

        ax.axhline(y=0, color='k', lw=0.5)

    #plt.suptitle(title)
    fig.tight_layout()

    plt.subplots_adjust(wspace=0.01, hspace=0)
    plt.suptitle(title)
    plt.show()


def plotnyaxis(hub,  y=[[]],x='time', idx=0,Region=0, log=False, title='', lw=2):
    '''
    x must be a variable name (x axis organisation)
    y must be a list of list of variables names (each list is a shared axis)

    example :
        pgm.plots.plotnyaxis(hub, x='time',
                     y=[['employment', 'omega'],
                        ['pi'],
                        ],
                     idx=0,
                     title='',
                     lw=2)
    '''
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()

    if type(log) in [str,bool]:
        log=[log for l in y]
    if len(log)!=len(y):
        raise Exception(f'The length of the log list ({len(log)}) does not correspond to the length of the axes ({len(y)})!')

    ### INITIALIZE FIGURE
    fig = plt.figure()
    fig.set_size_inches(10, 5)
    ax = plt.gca()

    allvarname = [x]+[item for sublist in y for item in sublist]
    R = hub.get_dparam(keys=[allvarname], returnas=dict)
    p = {}  # dictionnary of curves
    # Prepare x axis
    vx = R[x]['value'][:, idx,Region,0,0]
    units = r'$(  '+R[x]['units']+'  )$'
    ax.set_xlabel(R[x]['symbol']+units)
    ax.set_xlim(vx[0], vx[-1])

    # set ax dictionnary
    Nyaxis = len(y)
    dax = {0: ax}
    for i in range(1, Nyaxis):
        dax[i] = ax.twinx()

    # set for each subyaxis
    vy = {}
    for ii, vlist in enumerate(y):
        ## PREPARE DATA AND SYMBOLS
        vy[ii]={}
        symbolist = []
        for yyy in vlist:
            ### Monosectorial entry
            if type(yyy) is str:
                vy[ii][yyy]= R[yyy]['value'][:, idx,Region,0,0]
                symbolist.append( R[yyy]['symbol'])
                name=yyy
            ### Multisectorial entry
            else:
                name=yyy[0]
                if type(yyy[1]) is str:
                    sectornumber= R[R[name]['size'][0]]['list'].index(yyy[1])
                    sectorname = yyy[1]
                else:
                    sectorname= str(yyy[1])
                    sectornumber= yyy[1]

                vy[ii][name+sectorname]=R[name]['value'][:, idx,Region,sectornumber,0]
                symbolist.append(R[yyy[0]]['symbol'][:-1]+'_{'+sectorname+'}$')

        units = r'$(' + R[name]['units'].replace('$', '\$') + ')$'

        ## Work on the limit
        ymin = np.nanmin([np.nanmin(v) for v in vy[ii].values()])
        ymax = np.nanmax([np.nanmax(v) for v in vy[ii].values()])
        dax[ii].set_ylim(ymin, ymax)

        ## Work on the colors
        color = np.array(plt.cm.turbo(ii/Nyaxis))
        color[:-1] *= 0.8
        color = tuple(color)

        ## Add the curves

        for j, val in enumerate(vy[ii].values()):
            p[symbolist[j]], = dax[ii].plot(vx, val,    color=color,
                                   label=symbolist[j], ls=_LS[j % (len(_LS)-1)], lw=lw)

        ## Fill and Move y axes
        side = 'right' if ii % 2 else 'left'

        if units == '$()$': units=''
        ylabel = r''.join([xx+', ' for xx in symbolist])[:-2] + units

        dax[ii].set_ylabel(ylabel,labelpad=-40 if side=='right' else 0)#,loc='bottom', rotation=0
        dax[ii].spines[side].set_position(('outward', np.amax((0, 60*(ii//2)))))
        if side == 'left':
            dax[ii].yaxis.tick_left()
            dax[ii].yaxis.set_label_position('left')
        dax[ii].yaxis.label.set_color(color)
        dax[ii].tick_params(axis='y', colors=color)

        if log[ii]:
            dax[ii].set_yscale('log')
    dax[ii].legend(handles=p.values(), loc='best')
    plt.title(title)
    plt.tight_layout()
    plt.show()


def phasespace(hub, x, y, color='time', idx=0,Region=0):
    '''
    Plot of the trajectory of the system in a 2dimensional phase-space

    Parameters
    ----------
    sol : hub after a run
    x   : key for the variable on x axis, The default is 'omega'.
    y   : key for the variable on y axis, The default is 'lambda'.
    idx : number of the system taken to be plot, The default is 0

    EXAMPLE :
    pgm.plots.phasespace(hub,'employment',['pi','Capital'],color=['omega','Consumption'])
    '''
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()


    R=hub.dparam
    if type(x) is list :
        xsect=R[R[x[0]]['size'][0]]['list'].index(x[1])
        xname=x[1]
        x=x[0]
    else :
        xsect=0
        xname=''
    if type(y) is list :
        ysect=R[R[y[0]]['size'][0]]['list'].index(y[1])
        yname=y[1]
        y=y[0]
    else :
        ysect=0
        yname =''
    if type(color) is list :
        colorsect=R[R[color[0]]['size'][0]]['list'].index(color[1])
        colorname=color[1]
        color=color[0]
    else :
        colorsect=0
        colorname =''

    allvars = hub.get_dparam(returnas=dict)
    yval = allvars[y]['value'][:, idx,Region,ysect,0]
    xval = allvars[x]['value'][:, idx,Region,xsect,0]
    t = allvars[color]['value'][:, idx,Region,colorsect,0]

    points = np.array([xval, yval]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(t.min(), t.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(t)
    lc.set_linewidth(2)

    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax, label=allvars[color]['symbol'][:-1]+'_{'+colorname+'}$')
    plt.xlabel(allvars[x]['symbol'][:-1]+'_{'+xname+'}$')
    plt.ylabel(allvars[y]['symbol'][:-1]+'_{'+yname+'}$')
    plt.xlim([np.nanmin(xval), np.nanmax(xval)])
    plt.ylim([np.nanmin(yval), np.nanmax(yval)])
    plt.axis('scaled')
    plt.title('Phasespace ' + x + '-' + y + ' for model : '
              + hub.dmodel['name'] + '| system number' + str(idx))

    plt.show()


def plot3D(hub, x, y, z, color, cmap='jet', index=0,Region=0, title=''):
    '''
    Plot a 3D curve, with a fourth information on the colour of the curve

    x,y,z,cinf are names of your variables
    cmap your colormap
    title is your graph title

    example, with two sectors 'Capital','Consumption'
    pgm.plots.plot3D(hub,'employment',
                         ['pi','Capital'],
                         ['rd','Capital'],
                         color=['omega','Consumption'])

    '''
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()

    R=hub.get_dparam()
    if type(x) is list :
        xsect=R[R[x[0]]['size'][0]]['list'].index(x[1])
        xname=x[1]
        x=x[0]
    else :
        xsect=0
        xname=''
    if type(y) is list :
        ysect=R[R[y[0]]['size'][0]]['list'].index(y[1])
        yname=y[1]
        y=y[0]
    else :
        ysect=0
        yname =''
    if type(z) is list :
        zsect=R[R[z[0]]['size'][0]]['list'].index(z[1])
        zname=z[1]
        z=z[0]
    else :
        zsect=0
        zname =''
    if type(color) is list :
        colorsect=R[R[color[0]]['size'][0]]['list'].index(color[1])
        colorname=color[1]
        color=color[0]
    else :
        colorsect=0
        colorname =''

    vx = R[x]['value'][:, index,Region,xsect,0]
    vy = R[y]['value'][:, index,Region,ysect,0]
    vz = R[z]['value'][:, index,Region,zsect,0]
    vc = R[color]['value'][:, index,Region,colorsect,0]

    points = np.array([vx, vy, vz]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(vc.min(), vc.max())

    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = plt.axes(projection='3d')
    ax.plot(vx,
            vy,
            vz, lw=0.01, c='k')
    lc = Line3DCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(vc)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    cbar = fig.colorbar(lc, ax=ax)
    cbar.ax.set_ylabel(R[color]['symbol'][:-1]+'_{'+xname+'}$' if xname else R[color]['symbol'])
    ax.set_xlabel(R[x]['symbol'][:-1]+'_{'+xname+'}$' if xname else R[x]['symbol'])
    ax.set_ylabel(R[y]['symbol'][:-1]+'_{'+yname+'}$' if yname else R[y]['symbol'])
    ax.set_zlabel(R[z]['symbol'][:-1]+'_{'+zname+'}$' if zname else R[z]['symbol'])

    #print(R[x]['symbol'][:-1]+'_{'+xname+'}$')

    plt.tight_layout()
    # plt.legend()
    plt.title(title)
    plt.show()


def Var(hub, key, idx=0,Region=0, mode=False, log=False,title=''):
    '''
    Just one variable plot, with possibly cycles analysis to be shown
    if you put [key,sectorname] it will load the specific sector
    if mode = 'sensitivity' the system will show statistical variance between parrallel run of nx
    if mode = 'cycles' the system will show cycles within the evolution of the variable with their characteristics
    '''

    ### CHECKS
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()
    if (mode=='sensitivity' and not hub.dmisc.get('sensitivity',False)):
        print('the system is calculating statsensitivity...')
        hub.calculate_StatSensitivity()
        print('done')
    if (mode=='cycles' and not hub.dmisc.get('cycles',False)):
        print('Calculation of cycles on each field as ref...')
        hub.calculate_Cycles()
        print('done')

    R=hub.get_dparam()
    if type(key) is list :
        keysect=R[R[key[0]]['size'][0]]['list'].index(key[1])
        keyname=key[1]
        key=key[0]
    else :
        keysect=0
        keyname =0

    fig = plt.figure()
    fig.set_size_inches(10, 5)
    ax = plt.gca()

    # PLOT OF THE BASE
    allvars = hub.get_dparam(returnas=dict)
    y = allvars[key]['value'][:, idx,Region,keysect,0]
    t = allvars['time']['value'][:,idx,Region,0,0]

    if mode in [False,'cycles']:
        plt.plot(t, y, lw=2, ls='-', c='k')

    # PLOT OF THE CYCLES
    if mode == 'cycles':
        cycleindex=idx   *(R['nx']['value']*R['nr']['value']*R[R[key]['size'][0]]['value'])+\
                   Region*(                 R['nr']['value']*R[R[key]['size'][0]]['value'])+keysect

        cyclvar = allvars[key]['cycles'][cycleindex]
        #for k,v in cyclvar.items():print(k,v)
        tmcycles = cyclvar['t_mean_cycle']

        # Plot of each period by a rectangle
        miny = np.nanmin(y)
        maxy = np.nanmax(y)

        for car in cyclvar['period_T_intervals'][::2]:
            ax.add_patch(
                Rectangle((car[0], miny), car[1]-car[0], maxy-miny, facecolor='k', alpha=0.1))

        # Plot of enveloppe (mean-max)
        vmin = cyclvar['minval']
        vmax = cyclvar['maxval']
        plt.plot(tmcycles, vmin, ls='dashdot', label='min value')
        plt.plot(tmcycles, vmax, ls='dashdot', label='max value')

        # Plot of the mean value evolution
        meanv = np.array(cyclvar['meanval'])
        plt.plot(tmcycles, cyclvar['meanval'], ls='dashdot', label='mean value')
        plt.plot(tmcycles, cyclvar['medval'],
                 ls='dashdot', label='median value')

        # Plot of the standard deviation around the mean value
        stdv = np.array(cyclvar['stdval'])
        ax.fill_between(tmcycles, meanv - stdv, meanv + stdv, alpha=0.2)
        plt.legend()

    if mode == 'sensitivity':
        time = hub.dparam['time']['value'][:, idx,Region,keysect,0]

        V = hub.dparam[key]['sensitivity'][Region][keyname]


        ## Plot all trajectory

        for jj in range(len(allvars[key]['value'][0, :,0,0,0])):
            ax.plot(time, hub.dparam[key]['value'][:, jj,Region,0,0]
                         , c='k', ls='--', lw=0.5)
            if jj==30:
                print('WARNING: plotvar should be coded with a linecollection...')

        # Plot mean an median
        ax.plot(time, V['mean'], c='orange', label='mean')
        ax.plot(time, V['median'], c='orange', ls='--', label='median')
        ax.plot(time, V['max'], c='r', lw=0.4, label='maxmin')
        ax.plot(time, V['min'], c='r', lw=0.4)

        for j in np.arange(0.5, 5, 0.2):
            ax.fill_between(time, V['mean'] - j * V['stdv'],
                                 V['mean'] + j * V['stdv'], alpha=0.02, color='blue')
        ax.fill_between(time, V['mean'],
                             V['mean'], alpha=0.5, color='blue', label=r'$\mu \pm 5 \sigma$')

        ax.set_xlim([time[0], time[-1]])
        ax.set_ylim([np.nanmin(V['min']), np.nanmax(V['max'])])

        ax.fill_between(time, V['mean'] - V['stdv'],
                             V['mean'] + V['stdv'], alpha=0.4, color='r', label=r'$\mu \pm \sigma$')


    if log is True: ax.set_yscale('log')
    plt.title(title)
    plt.ylabel(R[key]['symbol'][:-1]+'_{'+keyname+'}$' if type(keyname) is str else
               R[key]['symbol'] )
    plt.xlabel('time (y)')
    if mode: ax.legend()
    plt.show()

# #################################### TOOLBOX PLOTS ########################################

def cycles_characteristics(hub,
                           xaxis='omega',
                           yaxis='employment',
                           ref='employment',
                           type1='frequency',
                           normalize=False,
                           Region=0,
                           title=''):
    '''
    Plot frequency and harmonicity for each cycle found in the system

    xaxis='omega',
    yaxis='employment',
    ref='employment',
   type1 and type2 should be in 't_mean_cycle':
                                'period_T':,
                                'medval': ,
                                'stdval':,
                                'minval':,
                                'maxval':  ,
                                'frequency':,
                                'Coeffs':
                                'Harmonicity': }
    '''
    if not hub.dmisc['run']:
        raise Exception('NO RUN DONE YET, RUN BEFORE DOING A PLOT')

    if not hub.dmisc.get('cycles',False):
        print('Calculation of cycles on each field as ref...')
        hub.calculate_Cycles(ref=ref)

    ####
    fig = plt.figure()
    ax1 = plt.subplot(111)


    xsector=xaxis[1] if type(xaxis) is list else 0
    ysector=yaxis[1] if type(xaxis) is list else 0
    xaxis=xaxis[0] if type(xaxis) is list else xaxis
    yaxis=yaxis[0] if type(xaxis) is list else yaxis

    AllX = []
    AllY = []
    AllC1 = []
    AllC2 = []
    R = hub.get_dparam()
    cycs = R[ref]['cycles_bykey']

    for i in range(hub.dparam['nx']['value']):  # loop on parrallel system
        for j, ids in enumerate(cycs['period_indexes'][i]):  # loop on cycles decomposition
            AllX.append(R[xaxis]['value'][ids[0]:ids[1], i,Region,xsector])
            AllY.append(R[yaxis]['value'][ids[0]:ids[1], i,Region,ysector])
            AllC1.append(cycs[type1][i][j])


    if normalize:
        AllC1/=np.amax(AllC1)

    lc1 = _multiline(AllX, AllY, AllC1, ax=ax1, cmap='jet', lw=2)

    ax1.set_xlabel(R[xaxis]['symbol'])
    ax1.set_ylabel(R[yaxis]['symbol'])
    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(lc1, cax=cax1, orientation='vertical')
    ax1.set_title(type1)


    plt.suptitle(title+'Period analysis on : '+R[ref]['symbol'])
    plt.show()



def repartition(hub ,
                keys : list ,
                sector = '' ,
                sign= '+',
                ref = '',
                refsign = '+',
                title= '',
                idx=0,
                region=0,
                removetranspose=False):
    """
    Temporal visualisation of a composition.
    Recommended use on stock-flow consistency and budget repartition.

    Variables :
    * hub
    * keys : list of fields considered in the decomposition
    * sector : the sector you want to verify. Monosectoral is ''
    * sign : either '+','-' or a list of ['+','-'], to apply for each key. Must be a list of same length.
    * ref : the reference level to compare to the components. Typically in the case of debt stock-flow, ref is dotD.
    * title : title,
    * idx : number of the system in parrallel
    * region : number or id of the system considered
    * removetranspose : if there is a matrix of transaction (from i to j), add negatively the transpose of the matrix terms

    Will create a substack of the different component you put in.

    Example on a multisectoral :
    repartition(hub,['pi','rd','xi','gamma','omega'],sector='Consumption')
    repartition(hub,['pi','rd','xi','gamma','omega'],sector='Capital')

    Same as repartition, but will take matrices as inputs
    """
    if not hub.dmisc['run']:
        print('NO RUN DONE YET, SYSTEM IS DOING A RUN WITH GIVEN FIELDS')
        hub.run()


    ### SIGNS HANDING
    # Signs repartition
    if type(sign) in [int,str]:
        sign=[sign for l in keys]
    if len(sign)!=len(keys):
        raise Exception(f'The length of the sign list ({len(sign)}) does not correspond to the length of the elements ({len(keys)})!')
    sign = [ 1 if s in ['+',1] else -1 for s in sign]
    # refsign handling
    if refsign in ['+',1]: refsign=1
    else : refsign=-1


    R=hub.get_dparam()
    # Sector names ##################################################
    if sector in ['',False,None]:
        sectindex = 0
        sectname = ''
    elif type(sector) is int :
        sectindex = sector*1
        sectname = R[R[keys[0]]['size'][0] ]['list'][sectindex]
    else:
        sectname = str(sector)
        sectindex = R[R[keys[0]]['size'][0] ]['list'].index(sectname)


    dicvals= {} # Dictonnary of entries #############################
    for enum,k in enumerate(keys):                                          # For each entry
        Nsects = R[R[k]['size'][1]].get('list',[''])                        # We check if it has components
        for enum2, sect2name in enumerate(Nsects):                          # Decomposition for matrices

            sectname2 = '-'+sect2name if len(Nsects)>1 else ''              # Name of matrix sector
            entryname =  R[k]['symbol'][:-1]+'_{'+sectname+sectname2+'}$'   # Name in the dictionnary

            # if the entry is non-zero
            if np.max(np.abs(R[k]['value'][:,idx,region,sectindex,enum2]))!=0:
                dicvals[entryname]=  sign[enum]*R[k]['value'][:,idx,region,sectindex,enum2]

            if (removetranspose and R[k]['size'][1]!='__ONE__'):
                entrynameT=R[k]['symbol'][:-1] + '_{' + sectname2[1:] +'-' +sectname + '}$'

                # If the entry is non-zero
                if np.max(np.abs(R[k]['value'][:, idx,region,enum2,sectindex]))!=0:
                    dicvals[entrynameT] = -sign[enum] * R[k]['value'][:, idx,region,enum2,sectindex]

    color = list(plt.cm.turbo(np.linspace(0,1,len(keys)+1)))
    dicvalpos = { k : np.maximum(v,0) for k,v in dicvals.items()}
    dicvalneg = { k : np.minimum(v,0) for k,v in dicvals.items()}
    time = R['time']['value'][:,0,0,0,0]

    plt.figure()
    fig=plt.gcf()
    fig.set_size_inches(15, 10 )
    ax=plt.gca()
    if len(ref):
        name = R[ref]['symbol'][:-1]+'_{'+sectname+'}$'
        ax.plot(time,refsign*R[ref]['value'][:,idx,region,sectindex,0],c='r',ls='--',lw=2,label=name)
    ax.stackplot(time,dicvalpos.values(),labels=dicvals.keys(),colors=color)
    ax.legend(loc='upper left')
    ax.stackplot(time, dicvalneg.values(),lw=3,colors=color)

    plt.ylabel('Repartition $ '+R[keys[0]]['units'].replace('$', '\$')+' $ ' if len(R[keys[0]]['units']) else 'Repartition')
    plt.xlabel('Time (y)')
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


# %% DEPRECIATED ##################################################################
###################################################################################

def __slices_wholelogic(hub, key='', axes=[[]], N=100, tid=0, idx=0,Region=0):
    '''
    Take the logic of a field, and calculate a slice given two of the argument fields that are modified

    Example :
        plotfunction(hub,key='Hid',axes=[['Omega',0,2]],N=100,tid=0,idx=0)
        plotfunction(hub,key='Hid',axes=[['Omega',0,2],['x',0,100]],N=100,tid=0,idx=0)

    Parameters
    ----------
    key  : str. name of the field you are introspecting
    axes : [[str,valmin,valmax]] or [[str,valmin,valmax],[str,valmin,valmax]] for 2D
    N    : int, number of points in grid
    tid  : index of
    idx : TYPE, optional
        DESCRIPTION. The default is 0.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.
    '''

    R = hub.get_dparam()

    if len(axes) > 2:
        raise Exception('Too many dimensions to plot !')
    elif len(axes) == 2:
        axx = axes[0]
        axy = axes[1]

        ## If the axes contains a sector
        if len(axx)==4: RegionX=axx[1]
        else : RegionX=0
        if len(axy)==4: RegionY=axy[1]
        else : RegionY=0

        ### CREATE THE GRID
        XX, YY = np.meshgrid(np.linspace(axx[-2], axx[-1], N),
                             np.linspace(axy[-2], axy[-1], N))


        keys = [axes[0][0], axes[1][0]]
        defaultkeys = [k for k in R[key]['kargs'] if k not in keys]

        defaultval = {k: R[k]['value'] for k in defaultkeys if k in hub.dmisc['parameters']}
        defaultval.update({k: R[k]['value'][tid, idx,Region,:,0]
                          for k in defaultkeys if k in hub.dmisc['dfunc_order']['statevar']})
        defaultval0 = copy.deepcopy(defaultval)
        defaultval[keys[0]][:,RegionX] = XX
        defaultval[keys[1]][:,RegionY] = YY

        Z = R[key]['func'](**defaultval)

        plt.figure(f'Function: {key} 2D')
        plt.pcolormesh(XX, YY, Z, cmap='jet')
        plt.xlabel(R[axes[0][0]]['symbol'])
        plt.ylabel(R[axes[1][0]]['symbol'])
        plt.title(R[key]['symbol']+f'\n {defaultval0}')
        plt.colorbar()
        plt.show()
    elif len(axes) == 1:
        XX = np.linspace(axes[0][1], axes[0][2], N)
        if len(axes[0])==4: RegionX=axes[0][1]
        else : RegionX=0

        defaultkeys = [k for k in R[key]['kargs'] if k not in [key]]

        defaultval = {k: R[k]['value'] for k in defaultkeys if k in hub.dmisc['dfunc_order']['parameters']}

        defaultval.update({k: R[k]['value'][tid, idx,Region,:,0]
                          for k in defaultkeys if k in hub.dmisc['dfunc_order']['statevar']})
        defaultval0 = copy.deepcopy(defaultval)

        defaultval[axes[0][0]][:] = XX

        Z = R[key]['func'](**defaultval)

        plt.figure(f'Function: {key} 1D')
        plt.plot(XX, Z)
        plt.xlabel(R[axes[0][0]]['symbol'])
        plt.ylabel(R[key]['symbol'])
        plt.title(f'{defaultval0}')
        plt.show()


def __plot_variation_rate(hub, varlist, title='', idx=0):
    '''
    Allow one to observe the time variation and the contribution of each dependency.
    Useful for debugging or understanding where are the main loops

    THE SYSTEM NEEDS :
        1) a run
        2) calculate_variation_rate

    for each field in varlist (ex : ['Y','L','w']) it will :
        * Print the variable time evolution
        * Print its relative growth rate
        * if it is a Statevar, its time derivate, and the contribution of each of its dependency to its time derivate
        * if it is an ODE, its second time derivate and the contribution of each of its dependency
    '''
    R = hub.get_dparam()

    fig = plt.figure()
    fig.set_size_inches(15, 5*len(varlist))
    t = R['time']['value'][:, 0]
    gs = GridSpec(len(varlist), 3)

    # Axis for value and relative growth
    ax0 = {key: fig.add_subplot(gs[i, 0]) for i, key in enumerate(varlist)}
    ax02 = {key: ax0[key].twinx() for key in varlist}

    # Axis for derivative and their contributions
    ax = {key: fig.add_subplot(gs[i, 1:]) for i, key in enumerate(varlist)}

    for key in varlist:
        # ##################################
        # Left Curves (y, relative growth)
        ax02[key].plot(t, R[key]['value'][:, idx], c='b')
        ax0[key].plot(t[1:-1], R[key]['time_log_derivate'][1:-1, idx], ls='--', c='g')
        ax0[key].axhline(y=0, color='k', lw=0.5)

        # Ylim management
        sort = np.sort(R[key]['time_log_derivate'][1:-1, idx])[int(0.05*len(t)):-int(0.05*len(t))]
        ax0[key].set_ylim([1.3*np.nanmin(sort), 1.3*np.nanmax(sort)])
        # Left side axis management
        ax02[key].set_ylabel(R[key]['symbol'])
        ax02[key].spines['left'].set_position(('outward',  80))

        ax02[key].yaxis.tick_left()
        ax02[key].yaxis.set_label_position('left')
        ax02[key].spines['left'].set_color('blue')
        ax02[key].tick_params(axis='y', colors='blue')
        symb = R[key]['symbol'].replace('$', '')
        label = r'$\dfrac{\dot{'+symb+r'}}{'+symb+'}$'
        ax0[key].spines['left'].set_color('green')
        ax0[key].tick_params(axis='y', colors='green')
        ax0[key].set_ylabel(label)

        # ##################################
        # Right side (Derivates)

        # Full curve
        if R[key]['eqtype'] == 'ode':
            ax[key].plot(t[2:-2], R[key]['time_dderivate'][2:-2, idx],
                         c='black', label=r'$\dfrac{d^2 '+symb+r'}{dt^2}$')
            label = r'$\ddot{'+R[key]['symbol'].replace('$', '')+r'}$'
        else:
            ax[key].plot(t[1:-1], R[key]['time_derivate'][1:-1, idx],
                         c='black', label=r'$\dfrac{d '+symb+r'}{dt}$')
            label = r'$\dot{'+R[key]['symbol'].replace('$', '')+r'}$'
        ax[key].spines['right'].set_color('black')
        ax[key].axhline(y=0, color='k', lw=0.5)

        #  Contribution
        vv = R[key]['partial_contribution']
        for i, k2 in enumerate(vv.keys()):
            symb2 = R[k2]['symbol'].replace('$', '')
            if R[key]['eqtype'] == 'ode':
                lab = r'$\dfrac{\partial \dot{'+symb+r'}}{\partial '+symb2+'}\dot{'+symb2+r'}$'
            else:
                lab = r'$\dfrac{\partial '+symb+r'}{\partial '+symb2+'}\dot{'+symb2+r'}$'
            ax[key].plot(t[1:-1], vv[k2][1:-1, idx],
                         label=lab)

        # Axis management
        ax[key].yaxis.tick_right()
        ax[key].yaxis.set_label_position('right')
        ax[key].set_ylabel(label)
        ax[key].legend()

    # Figure management
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.suptitle(title)
    plt.show()


# #############################################################


_DPLOT = {
    #'Slice_logic': __slices_wholelogic,
    #'variation_rate': plot_variation_rate,
    'timetrace': plot_timetraces,
    'nyaxis': plotnyaxis,
    'phasespace': phasespace,
    '3D': plot3D,
    'byunits': plotbyunits,
    'Onevariable': Var,
    'cycles_characteristics': cycles_characteristics,
    'repartition':repartition}



