# -*- coding: utf-8 -*-
'''
THIS COCKPIT ALLOW ONE TO TEST IF HIS MODEL IS GIVING BACK
'''

import imageio
import cv2
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt


##############################################################################
_PATH_OUTPUT_REF = os.path.join('pygemmes', 'tests', 'output_ref')


### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=True,
)

_MODEL = 'GK'
_MODEL_REDUCED = _MODEL+"-Reduced"


Basefields = {
    'dt': 0.01,
    'a': 1,
    'N': 1,
    'K': 2.7,
    'D': 0.2,
    'w': .85,
    'p': 1,
    'eta': 0.01,
    'gammai': 0.5,
    'alpha': 0.02,
    'beta': 0.025,
    'nu': 3,
    'delta': .005,
    # 'phinull': .04,
    'k0': -0.0065,
    'k1': np.exp(-5),
    'k2': 20,
    'r': 0.03,
}

# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=False,
)
_SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
# _SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


# PRESET ####################################################################


_DPRESET = {'default': {
    'fields': Basefields,
    'com': '',
    'plots': [],
},
}


# %% LOADING AND COPYING MODELS #############################################

blueprint = 'GK'
model = 'GK-Reduced'
preset = 'default'

hub = pgm.Hub(blueprint, preset='default', dpresets=_DPRESET, verb=False)
hub_reduced = pgm.Hub(model, verb=False)

# COPY OF THE PARAMETERS INTO A NEW DICTIONNARY
FieldToLoad = hub_reduced.get_dparam(returnas=dict, eqtype=[None, 'ode'],
                                     group=('Numerical',),)
R = hub.get_dparam(returnas=dict)
tdic = {}
for k, v in FieldToLoad.items():
    val = R[k]['value']
    if 'initial' in v.keys():
        tdic[k] = val[0][0]
    else:
        tdic[k] = val

_DPRESETS = {'Copy'+_MODEL: {'fields': tdic, }, }

# LOADING THE MODEL WITH A NEW MODEL
hub_reduced = pgm.Hub(_MODEL_REDUCED, preset='Copy'+_MODEL,
                      dpresets=_DPRESETS)

# RUNS
hub_reduced.run(verb=0, solver=_SOLVER)
hub.run(verb=0, solver=_SOLVER)

# PLOTS
R = hub.get_dparam(returnas=dict)
Rr = hub_reduced.get_dparam(returnas=dict)

Tocompare = ['lambda', 'omega', 'd',
             'phillips', 'kappa', 'inflation', 'pi', 'g']

plt.figure()
for i, k in enumerate(Tocompare):
    plt.subplot(4, 2, i+1)
    plt.plot(R['time']['value'], R[k]['value'], label='Full')
    plt.plot(Rr['time']['value'], Rr[k]['value'], ls='--', label='Reduced')
    plt.ylabel(k)
plt.suptitle('Comparison model GK Full and Reduced')
plt.show()


# %% November 22 : Iteratively going grom Goodwin to GK

# 1) We also remove investment and interest ##################################
'''
no debt means that kappa(pi)=pi
in GK kappa(pi)=k_0 + k_1 exp(pi*k_2)

First order DL gives kappa(pi)= k_0 + k_1 ( 1 + pi k_2) = k1+k0 + pi k_1 k_2, while pi*k_2 << 1

k0 = k1
k1 k2 = 1
k2 must be small

so we take for example k2 = 0.001, k1 = 1000, k0 = -1000

and r = 0
'''

for dt in [0.01, 0.001, 0.0001]:

    FieldsGKasG = Basefields.copy()
    FieldsGKasG['dt'] = dt
    FieldsGKasG['Tmax'] = 15
    FieldsGKasG['eta'] = 0.01
    FieldsGKasG['r'] = 0
    FieldsGKasG['D'] = 0
    FieldsGKasG['k0'] = -10000
    FieldsGKasG['k1'] = 10000
    FieldsGKasG['k2'] = 1/10000
    _DPRESET['FieldsGKasG'] = {'fields': FieldsGKasG,
                               'com': '',
                               'plots': [], }

    blueprint = 'GK'
    model = 'GK-Reduced'
    preset = 'FieldsGKasG'

    # LOADING AND COMPARING
    hub = pgm.Hub(blueprint, preset=preset, dpresets=_DPRESET, verb=False)
    hub_reduced = pgm.Hub(model, verb=False)

    FieldToLoad = hub_reduced.get_dparam(returnas=dict, eqtype=[None, 'ode'],
                                         group=('Numerical',),)
    R = hub.get_dparam(returnas=dict)
    tdic = {}
    for k, v in FieldToLoad.items():
        val = R[k]['value']
        if 'initial' in v.keys():
            tdic[k] = val[0][0]
        else:
            tdic[k] = val
    tdic['Tmax'] = FieldsGKasG['Tmax']

    _DPRESETS = {'Copy'+_MODEL: {'fields': tdic, }, }

    # LOADING THE MODEL WITH A NEW MODEL
    hub_reduced = pgm.Hub(_MODEL_REDUCED, preset='Copy'+_MODEL,
                          dpresets=_DPRESETS)

    # RUNS
    hub_reduced.run(verb=0, solver=_SOLVER)
    hub.run(verb=0, solver=_SOLVER)

    # PLOTS
    R = hub.get_dparam(returnas=dict)
    Rr = hub_reduced.get_dparam(returnas=dict)

    Tocompare = ['lambda', 'omega', 'd',
                 'phillips', 'kappa', 'inflation', 'pi', 'g']

    # TRAJECTORIES-TIME

    plt.figure('TimeTrajectories')
    for i, k in enumerate(Tocompare):
        plt.subplot(4, 2, i+1)
        plt.plot(R['time']['value'], R[k]['value'], label='Full')
        plt.plot(Rr['time']['value'], Rr[k]['value'], ls='--', label='Reduced')
        plt.ylabel(k)
    plt.suptitle('Comparison model GK Full and Reduced')
    plt.show()

    # TRAJECTORIES - PHASESPACE
    Listphasespace = [['omega', 'lambda'],
                      ['lambda', 'd'],
                      ['omega', 'd'],
                      ['kappa', 'pi'],
                      ['omega', 'inflation'],
                      ['pi', 'd'], ]

    plt.figure('Phasespace')
    for i, k in enumerate(Listphasespace):
        # lambda-omega
        plt.subplot(3, 2, i+1)

        plt.plot(R[k[0]]['value'], R[k[1]]['value'], label='Full')
        plt.plot(Rr[k[0]]['value'], Rr[k[1]]['value'], ls='--', label='Reduced')
        plt.xlabel(k[0])
        plt.ylabel(k[1])
    plt.suptitle('Comparison model GK Full and Reduced')
    # plt.axis('scaled')
    plt.show()

    # %%
    hub.get_summary()
    print(100*'###')
    hub_reduced.get_summary()

    # COMPARING GK WITH ITS OWN REDUCED VARIABLES
    omegap = np.gradient(R['omega']['value'][:, 0], FieldsGKasG['dt'])
    omegapp = np.gradient(omegap, FieldsGKasG['dt'])
    lambdap = np.gradient(R['lambda']['value'][:, 0], FieldsGKasG['dt'])
    lambdapp = np.gradient(lambdap, FieldsGKasG['dt'])
    dp = np.gradient(R['d']['value'][:, 0], FieldsGKasG['dt'])
    dpp = np.gradient(dp, FieldsGKasG['dt'])
    omegaptheo = np.array(R['omega']['value']*(R['phillips']['value'] - (
        1 - R['gammai']['value'])*R['inflation']['value']-R['alpha']['value']))[:, 0]
    lambdaptheo = np.array(R['lambda']['value'] * (R['g']
                           ['value'] - R['alpha']['value'] - R['beta']['value']))[:, 0]
    dptheo = np.array(R['kappa']['value'] - R['pi']['value'] - R['d']
                      ['value']*(R['g']['value']+R['inflation']['value']))[:, 0]
    gtheo = np.array(R['kappa']['value'] / R['nu']
                     ['value'] - R['delta']['value'])[:, 0]
    gp = np.gradient(R['g']['value'][:, 0], FieldsGKasG['dt'])

    plt.figure('compare theo')
    ax1 = plt.subplot(221)
    ax12 = plt.twinx(ax1)
    ax1.plot(R['time']['value'], (omegap-omegaptheo)/dt, c='b')
    ax12.plot(R['time']['value'], omegapp, c='k', ls='--')
    ax1.set_ylabel('omegap effective - theo')
    ax12.set_ylabel('omegapp')
    ax1.set_xlabel('t')

    ax2 = plt.subplot(222)
    ax22 = plt.twinx(ax2)
    ax2.plot(R['time']['value'], (lambdap-lambdaptheo)/dt, c='b')
    ax22.plot(R['time']['value'], lambdapp, c='k', ls='--')
    ax2.set_ylabel('lambdap effective - theo')
    ax2.set_ylabel('lambdapp')
    ax2.set_xlabel('t')

    ax3 = plt.subplot(223)
    ax32 = plt.twinx(ax3)
    ax2.plot(R['time']['value'], (dp-dptheo)/dt, c='b')
    ax32.plot(R['time']['value'], dpp, c='k', ls='--')
    ax3.set_ylabel('dp effective - theo')
    ax32.set_ylabel('dpp')
    ax3.set_xlabel('t')

    ax4 = plt.subplot(224)
    ax42 = plt.twinx(ax4)
    ax4.plot(R['time']['value'], R['g']['value'][:, 0]-gtheo)
    ax42.plot(['time']['value'], gp, c='k', ls='--')
    plt.ylabel('dp effective - theo')
    plt.xlabel('t')
    plt.show()


plt.figure()
plt.subplot(121)
plt.plot(R['phillips']['value'][1:-1, 0], (lambdap-lambdaptheo)[1:-1]/dt)
plt.subplot(122)
plt.plot(R['kappa']['value'][1:-1, 0], (lambdap-lambdaptheo)[1:-1]/dt)
plt.show()
