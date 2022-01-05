# -*- coding: utf-8 -*-
'''
Contains all the possibilities of each _core interaction
# !pytest pygemmes/tests/test_01_Hub.py -v

'''

import imageio
import cv2
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt


def groupofvariables(hub):
    ''' Gives from the hub a dictionnary of all the variables that shares the same units'''
    groupsoffields = hub.get_dparam_as_reverse_dict(crit='units')
    hub.get_dparam_as_reverse_dict(crit='eqtype')
    return {k: [v for v in vals if v in hub.dargs.keys()]
            for k, vals in groupsoffields.items()}


##############################################################################
_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')
_MODEL = 'GK-Reduced'  # 'GK',  #
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
##############################################################################

lambdavec = np.linspace(.5, .99, 20)
omegavec = np.linspace(.5, .99, 20)
dvec = np.linspace(10, 20, 11)

_DPRESETS = {'BasinOfAttraction':
             {'fields': {'Tmax': 20,
                         'dt': 0.005,
                         'lambda': lambdavec,
                         'omega': {'value': omegavec,
                                   'grid': True},
                         'd': {'value': dvec,
                               'grid': True},
                         },
              },
             }


# %% SHORT RUN ###############################################################
hub = pgm.Hub(_MODEL, preset='BasinOfAttraction', dpresets=_DPRESETS)
hub.run(verb=1.1, solver=_SOLVER)
# hub.plot(idx=[0, 0,0])

R = hub.get_dparam(returnas=dict)
lambdaXYZ = R['lambda']['value']
omegaXYZ = R['omega']['value']
dXYZ = R['d']['value']


# FINDING THE LINES IN THE VALLEY OF STABILITY
FrontierD = {}
for i in range(0, len(dvec)):
    deq = dXYZ[0, 0, 0, i]
    Omesh, Lmesh = np.meshgrid(omegavec, lambdavec)
    img = (dXYZ[-1, :, :, i] > deq).astype(np.uint8)
    contours, _ = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        XY = np.reshape(contours, (-1, 2))[1:, :]
        FrontierD[deq] = {'omega': (omegavec[XY[:, 0]]),  # +omegavec[1+XY[:, 0]])/2,
                          'lambda': (lambdavec[XY[:, 1]])}  # +lambdavec[1+XY[:, 1]])/2 }

#  Plotting all the lines
for k, v in FrontierD.items():
    plt.plot(v['omega'], v['lambda'], label="d(t=0)="+f"{k:.2f}")
plt.axis('scaled')
plt.legend()
plt.show()

# PLOTTING THE EVOLUTION
Step = 1
Pause = 0.05
plt.figure('', figsize=(10, 10))
for j in range(0, len(dvec)):
    for i in range(0, R['nt']['value'], int(Step/R['dt']['value'])):
        plt.clf()
        date = R['time']['value'][i, -1, -1, -1]
        plt.title("t ="+f"{date:.2f}"+" years, d(t=0)="+f"{dvec[j]:.2f}")
        plt.pcolormesh(omegavec, lambdavec,
                       dXYZ[i, :, :, j], vmin=0, vmax=dvec[j], cmap='jet', shading='auto')
        # plt.plot(omegavec[XY[:, 0]], lambdavec[XY[:, 1]], c='k')
        plt.xlabel('$\lambda(t=0)$')
        plt.ylabel('$\omega(t=0)$')
        plt.colorbar()
        plt.pause(Pause)
        # plt.savefig(
        #    'plot//'+str(int(10*dvec[j])).zfill(4)+'-'+str((int(10*date))).zfill(4)+'.png')
    plt.show()

# Transform into a GIF
filenames = os.listdir('plot')
with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread('plot//'+filename)
        writer.append_data(image)
