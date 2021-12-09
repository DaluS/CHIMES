# -*- coding: utf-8 -*-
'''
This small test to see how well the solvers functions
'''

import matplotlib.pyplot as plt
import numpy as np
import pygemmes as pgm

_SOLVER = 'eRK1-homemade'  # (One we created by ourself, that we can tweak)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2, with adaptative steps)
# _SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4, with adaptative steps)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8, with adaptative steps)

##############################################################################
### CONVERGENCE TEST #########################################################
printindividualTrajectory = True


def testConvergence_DampOsc(vecdt, solver, returnas='plot'):
    '''
        '''

    Error = {}

    dtlogspace = np.logspace(-1, -4, 7)

    for dt in dtlogspace:
        print("dt:", dt)
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
                      dpresets=_DPRESETS, verb=False)
        hub.run(verb=0, solver=_SOLVER)

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

    ################################
    dtlist = Error.keys()
    errorlist = [Error[k] for k in Error.keys()]

    Z = sorted(zip(dtlist, errorlist))

    dtlist = [x for x, y in Z]
    errorlist = [y for x, y in Z]

    plt.figure('Convergence')
    plt.loglog(dtlist, errorlist, '-*')
    plt.axis('scaled')
    plt.ylabel('mean error')
    plt.xlabel('dt')
    plt.title('Convergence test for'+_SOLVER)
    plt.show()
