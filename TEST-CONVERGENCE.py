# -*- coding: utf-8 -*-
'''
This small test to see how well the solvers functions
'''

import matplotlib.pyplot as plt
import numpy as np
import pygemmes as pgm

_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2, with adaptative steps)
# _SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4, with adaptative steps)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8, with adaptative steps)

##############################################################################
### CONVERGENCE TEST #########################################################
printindividualTrajectory = False

Error = {}
for dt in [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, ]:
    _DPRESETS = {'Convergence test':
                 {'fields': {'Tmax': 20,
                             'dt': dt,
                             'gamma': 1,
                             'Omega': 10,
                             'Final': 0,
                             'theta': 1,
                             'thetap': 0,
                             },
                  },
                 }
    # Load and preset
    hub = pgm.Hub('DampOscillator', preset='Convergence test',
                  dpresets=_DPRESETS)
    hub.run(verb=1.1, solver=_SOLVER)

    # Get the informations right
    R = hub.get_dparam(returnas=dict)
    gamma = R['gamma']['value']
    Omega = R['Omega']['value']
    Final = R['Final']['value']
    theta0 = R['theta']['value'][0]
    thetap0 = R['thetap']['value'][0]
    t = R['time']['value']
    thetanum = R['theta']['value']

    # Comparing strategies
    thetaTheo = np.real(theta0*np.exp(-gamma*t) *
                        np.cos(np.sqrt(Omega**2-gamma**2)*t))
    Error[dt] = np.mean(np.sqrt((thetanum-thetaTheo)**2))

    # Plot the trajectory
    if printindividualTrajectory:
        plt.plot(t, thetaTheo, label='Theoretical')
        plt.plot(t, thetanum, c='r', label='Numerical')
        plt.legend()
        plt.show()

################################
dtlist = Error.keys()
errorlist = [Error[k] for k in Error.keys()]

Z = sorted(zip(dtlist, errorlist))

dtlist = [x for x, y in Z]
errorlist = [y for x, y in Z]

plt.loglog(dtlist, errorlist, '-*')
plt.axis('scaled')
plt.ylabel('mean error')
plt.xlabel('dt')
plt.title('Convergence test for RK4 Homemade')
plt.show()

##############################################################################
### QUALITATIVE TEST #########################################################

_MODEL = 'LorenzSystem'
dmodels = pgm.get_available_models(returnas=dict, details=False, verb=True,)

Coor = {}

for solver in pgm.get_available_solvers(returnas=dict, verb=False,).keys():
    for preset in dmodels[_MODEL]['presets']:
        hub = pgm.Hub(_MODEL, preset=preset)
        hub.run(verb=1.1, solver=solver)

        R = hub.get_dparam(returnas=dict)
        Coor[solver] = {'x': R['x']['value'],
                        'y': R['y']['value'],
                        'z': R['z']['value'], }

fig = plt.figure('', figsize=(10, 10))
ax = plt.axes(projection='3d')
for solver in pgm.get_available_solvers(returnas=dict, verb=False,).keys():
    if solver in ['eRK4-homemade', 'eRK2-scipy']:
        lw = 3
    else:
        lw = 0.5
    ax.plot(Coor[solver]['x'][:, 0],
            Coor[solver]['y'][:, 0],
            Coor[solver]['z'][:, 0], label=solver, lw=lw)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.tight_layout()
plt.legend()
plt.show()
