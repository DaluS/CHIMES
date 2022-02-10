# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:30:11 2022

Here is an ensemble of small functions to explore basin of attractions

@author: Paul Valcke
"""

import pygemmes as pgm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


initial = {'lambda': 0.96753452,
           'omega': 0.84520232,
           'd': -0.07660271, }

dictforAttraction = {
    'model': 'GK-Reduced',
    'final': {k: v*1. for k, v in initial.items()},
    'limits': {'lambda': [0, 1-0.0001],
               'omega': [0, 1],
               'd': [-1, 10]},
    'Npts': 1000,
    'Rini': 0.015,
    'Niter': 1,
    'criteria': 0.05,
    'jump': 20,
    'kwargdics': {
        'Tmax': 100,
        'dt': 0.01}}

'''
1) Generate Nseed random initial point in the domain
2) Do a run for each
'''

finalpoints={'lambda':0.967297870750419,
            'omega':0.84547946985534,
            'd':-0.0771062162051694}

def StabilisationTimefrompoint(self,
                      finalpoints,
                      distance = 0.1):

    # Final step studies
    R = hub.get_dparam(key=[k for k in finalpoints]+['time'], returnas=dict)
    Coords = [R[k]['value']-finalpoints[k] for k in finalpoints.keys()]
    dist = np.linalg.norm(Coords, axis=0)

    # Fit using an exponential
    Nsys=np.shape(R['time']['value'][1])
    Typicaltime = [-1/np.polyfit(R['time']['value'][:,0],
                                 np.log(dist[:,i]),
                                 1,
                                 w=np.sqrt(dist[:,i])) for i in range(Nsys)]
    return Typicaltime


SensitivityDic = {
    'lambda': {'mu': 0.01,
               'sigma': 0.99,
               'type': 'uniform'},
    'omega': {'mu': 0.01,
              'sigma': .99,
              'type': 'uniform'},
    'd': {'mu': 0,
          'sigma': 2,
          'type': 'uniform'},
}





def _generateSpherecoordinates(dic, initial):
    '''
    Generate N-dimensional sphere coordinates and their normal vectors around a certain points
    '''
    coords = np.array([np.random.normal(0, 1, size=dic['Npts'])
                      for i in range(len(initial))])
    norm = np.linalg.norm(coords, axis=0)
    coords *= dic['Rini']/norm
    return {k: list(initial[k] + coords[i, :]) for i, k in enumerate(initial.keys())}, {k: list(coords[i, :]) for i, k in enumerate(initial.keys())}


def _generateSpacecoordinate(dic):
    '''
    Generate points in a N-dimensional square domain, with random normalised vector associated
    '''
    coords = np.array([np.random.uniform(dic['limits'][k][0], dic['limits'][k][1], size=dic['Npts'])
                      for k in dic['limits'].keys()])
    coords2 = np.array([np.random.normal(0, 1, size=dic['Npts'])
                        for i in range(len(initial))])
    norm2 = np.linalg.norm(coords, axis=0)
    coords2 *= dic['Rini']/norm2
    return {k:  coords[i, :] for i, k in enumerate(dic['limits'].keys())}, {k: list(coords2[i, :]) for i, k in enumerate(dic['limits'].keys())}


def _Determinetime(condini, dictforAttraction):
    '''
    For initial conditions, run all systems and then determine the characteristic time
    for stabilisation
    '''
    # Create preset for the system
    _DPRESETS = {'BOA':
                 {'fields': {
                 }, }, }
    for k, v in dictforAttraction['kwargdics'].items():
        _DPRESETS['BOA']['fields'][k] = v
    for k, v in condini.items():
        _DPRESETS['BOA']['fields'][k] = v

    # Load preset and run
    hub = pgm.Hub(dictforAttraction['model'], preset='BOA', dpresets=_DPRESETS, verb=False)
    hub.run()

    # Extract coordinates and look at the distance to final point
    R = hub.get_dparam(key=[k for k in initial.keys()]+['time'], returnas=dict)
    Coords = [R[k]['value']-dictforAttraction['final'][k] for k in initial.keys()]

    dist = np.linalg.norm(Coords, axis=0)
    dist /= dist[0, :]

    # Find minimal time to reach the criteria
    time = R['time']['value'][:, 0]
    Tcarac = [next((t for e, t in zip(dist[:, i], time) if e < dictforAttraction['criteria']), False)
              for i in range(np.shape(dist)[1])]

    return R, Tcarac


def _Propagatepoints(R, Tcarac, Allpoints, condini, vecs, dictforAttraction):
    '''
    Given a characteristic time, points and a direction,
    determine new positions and store information'''

    # Filter 1 : convergence in our time
    Tfilt = np.array(Tcarac) > 0
    # print(Tcarac)
    for k, v in condini.items():
        Allpoints[k] += list(np.array(v)[Tfilt])
    Allpoints['Tcarac'] += list(np.array(Tcarac)[Tfilt]*1)

    # Find new points
    # 1 : Expand previous one
    Expansion = dictforAttraction['jump']/np.array(Tcarac)[Tfilt]
    newcoords = {}
    for k in initial.keys():
        newcoords[k] = np.array(condini[k])[Tfilt] + \
            np.array(vecs[k])[Tfilt] * Expansion

    # Find new points 2 : If required, introduce new points (noot added yet)

    # Filter 2 : the points are outside the box
    boxdic = {k: np.array(v > dictforAttraction["limits"][k][0]) *
              np.array(v < dictforAttraction["limits"][k][1]) for k, v in newcoords.items()}
    filt2 = np.product([v for v in boxdic.values()], axis=0).astype(np.bool_)
    # print(filt2)

    newcoords2 = {k: v[filt2] for k, v in newcoords.items()}
    vecs2 = {k: np.array(v)[Tfilt][filt2] for k, v in vecs.items()}

    return Allpoints, newcoords2, vecs2


def basinofattraction_time(initial, dictforAttraction, initialtype='random'):
    '''
    Generate points in a domain, then run a dynamical system on those initial conditions.
    '''

    Allpoints = {k: [] for k in initial.keys()}
    Allpoints['Tcarac'] = []

    if initialtype == 'random':
        condini, vecs = _generateSpacecoordinate(dictforAttraction)
    else:
        condini, vecs = _generateSpherecoordinates(dictforAttraction, initial)

    fig = plt.figure('3D', figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.scatter(condini['lambda'],
               condini['omega'],
               condini['d'],
               c='k',
               s=0.5)

    for numb in range(dictforAttraction['Niter']):
        print(numb)
        R, Tcarac = _Determinetime(condini, dictforAttraction)
        Allpoints, condini, vecs = _Propagatepoints(
            R, Tcarac, Allpoints, condini, vecs, dictforAttraction)

    ax.scatter(dictforAttraction['final']['lambda'],
               dictforAttraction['final']['omega'],
               dictforAttraction['final']['d'],
               c='k',
               s=200)

    ax.scatter(Allpoints['lambda'],
               Allpoints['omega'],
               Allpoints['d'],
               c=Allpoints['Tcarac'],
               cmap='jet')

    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(
        vmin=np.amin(Allpoints['Tcarac']),
        vmax=np.amax(Allpoints['Tcarac']))

    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        ax=ax)
    cbar.ax.set_ylabel(r'$T_{carac}^{stab}$ (y)')

    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$\omega$')
    ax.set_zlabel('d')
    plt.suptitle('Characteristic time for stabilisation')
    plt.show()


##############################################################################
basinofattraction_time(initial, dictforAttraction)

##############################################################################
'''
PLOT BASIN WITH TRAJECTORIES CONVERGENCE
'''
condini, vecs = _generateSpacecoordinate(dictforAttraction)

# Create preset for the system
_DPRESETS = {'BOA':
             {'fields': {
             }, }, }
for k, v in dictforAttraction['kwargdics'].items():
    _DPRESETS['BOA']['fields'][k] = v
for k, v in condini.items():
    _DPRESETS['BOA']['fields'][k] = v

# Load preset and run
hub = pgm.Hub(dictforAttraction['model'], preset='BOA', dpresets=_DPRESETS, verb=False)
hub.run()
hub.reinterpolate_dparam(Npoints=200)

# Extract coordinates and look at the distance to final point
R = hub.get_dparam(key=[k for k in initial.keys()]+['time'], returnas=dict)


fig = plt.figure('3D', figsize=(10, 10))
ax = plt.axes(projection='3d')
for i in range(dictforAttraction['Npts']):
    if np.amax(R['d']['value'][-1, i]) < 1:
        ax.plot(R['lambda']['value'][:, i],
                R['omega']['value'][:, i],
                R['d']['value'][:, i], c='k', lw=0.5)
        ax.scatter(R['lambda']['value'][0, i],
                   R['omega']['value'][0, i],
                   R['d']['value'][0, i], c='k')
    else:
        # ax.plot(R['lambda']['value'][:, i],
        #        R['omega']['value'][:, i],
        #        R['d']['value'][:, i], c='r', lw=0.1)
        ax.scatter(R['lambda']['value'][0, i],
                   R['omega']['value'][0, i],
                   R['d']['value'][0, i], c='r')

plt.axis('tight')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([-1, 10])

ax.set_xlabel(r'$\lambda$')
ax.set_ylabel(r'$\omega$')
ax.set_zlabel('d')

plt.show()
