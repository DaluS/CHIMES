# -*- coding: utf-8 -*-
'''
This Example shows how to compute a Basin of Attraction for a Goodwin-Keen system
'''

import imageio  # Library to record gif of construction
import cv2  # To detect basin limit
import numpy as np

import pygemmes as pgm
import matplotlib.pyplot as plt

##############################################################################

# Model and solver
_MODEL = 'GK-Reduced'  # 'GK',  #
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)

# Coordinates we explore
lambdavec = np.linspace(.5, .99, 20)
omegavec = np.linspace(.5, .99, 20)
dvec = np.linspace(10, 40, 30)
dt = 0.005
Tmax = 20

##############################################################################


# Creation of a dpreset containing the basin of attraction we study
_DPRESETS = {'BasinOfAttraction':
             {'fields': {'Tmax': Tmax,
                         'dt': dt,
                         'lambda': lambdavec,
                         'omega': {'value': omegavec, 'grid': True},
                         'd': {'value': dvec, 'grid': True},
                         }, }, }

# Loading and running the model
hub = pgm.Hub(_MODEL, preset='BasinOfAttraction', dpresets=_DPRESETS)
hub.run(verb=1.1, solver=_SOLVER)

# Glimpse at one trajectory
hub.plot(idx=[0, 0, 0])

# Extracting the infos we are looking for fron dparam
R = hub.get_dparam(key=['lambda', 'omega', 'd'], returnas=dict)
lambdaXYZ = R['lambda']['value']
omegaXYZ = R['omega']['value']
dXYZ = R['d']['value']


# FINDING THE LINES IN THE VALLEY OF STABILITY

FrontierD = {}  # Dictionnary containing all the positions of the line
for i in range(0, len(dvec)):

    # Loading the initial situation on d
    deq = dXYZ[0, 0, 0, i]
    # finding where the debt ratio is bigger at the end
    img = (dXYZ[-1, :, :, i] > deq).astype(np.uint8)

    # Extracting coordinates from the limit
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


# PLOTTING THE TEMPORARY EVOLUTION
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
#filenames = os.listdir('plot')
'''
with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread('plot//'+filename)
        writer.append_data(image)
'''
