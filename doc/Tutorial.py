# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 16:54:33 2022

@author: Paul Valcke
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np
import pygemmes as pgm  # we rename pygemmes as pgm to be shorter
import sys  # a library that help python know where things are

path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`


# %% OVERVIEWS
pgm.get_dfields_overview()
pgm.get_available_solvers()
pgm.get_available_models(details=True, verb=True)
pgm.get_available_output()

# %% A GK WITH A FEW PLOTS

hub = pgm.Hub('GK')  # verb=False
# preset=None,
# dpresets=None,
# verb=None)

listofsolver = pgm.get_available_solvers(returnas=list)
hub.run(verb=0)  # solver=listofsolver[0])#solver=None,verb=1.1

# Descriptions
hub.get_summary()
hub.equations_description()
pgm.generate_html_network_logics('GK')
R = hub.get_dparam(returnas=dict)

# Plots examples
dax = hub.plot()
dax2 = hub.plot(key=['lambda', 'omega', 'd'])  # Select the variables
dax3 = hub.plot(key=('GDP', 'a', 'Pi', 'kappa'))  # Remove some variables
pgm._plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)

# Fill Cycles
hub.FillCyclesForAll(ref='lambda')
dax4 = hub.plot(mode='cycles')

# %%
# A FEW SIMPLE FUNCTIONS TO SHOW A FEW POSSIBILITIES
pgm.comparesolver_Lorenz(dt=0.01, Npoints=10000)
pgm.plot_one_run_all_solvers('LorenzSystem', preset='Canonical')
pgm.plot_one_run_all_solvers('GK')
pgm.testConvergence_DampOsc([1, 0.1, 0.01, 0.001], solver='eRK4-homemade')

# More informations
hub.dmodel  # Gives the content of the model file
hub.dmisc  # gives multiple informations on the run and the variables


# %%
# One slowly
hub.set_dparam(key='dt', value=0.01)
hub.set_dparam(Tmax=50)

# Send a dictionnary
dparam = {'alpha': 0, 'beta': 1}
hub.set_dparam(dparam=dparam)

# Send a dictionnary (alternative)
dparam_changes = {'alpha': 0., 'delta': 0.}
hub.set_dparam(dparam_changes)

# Create N system in parrallel with different values
hub.set_dparam(alpha=[0, 0.01, 0.02, 0.03])

# Load a preset
hub = pgm.Hub('GK', verb=False)
hub.set_dparam(preset='default')

# %%
# Generate a dictionary of dictionary, with for each key : { 'mean value", 'std' , 'distribution' }
SensitivityDic = {
    'alpha': {'mu': .02,
              'sigma': .12,
              'type': 'log'},
    'k2': {'mu': 20,
           'sigma': .12,
           'type': 'log'},
    'mu': {'mu': 1.3,
           'sigma': .12,
           'type': 'log'},
}


presetSimple = pgm.GenerateIndividualSensitivity(
    'alpha', 0.02, .2, disttype='log', N=10)
presetCoupled = pgm.GenerateCoupledSensitivity(SensitivityDic, N=10, grid=False)

_DPRESETS = {'SensitivitySimple': {'fields': presetSimple, 'com': ''},
             'SensitivityCoupled': {'fields': presetCoupled, 'com': ''},
             }

hub = pgm.Hub('GK', preset='SensitivityCoupled', dpresets=_DPRESETS)
hub.run(verb=1.1)
hub.CalculateStatSensitivity()
dax = hub.plot(mode='sensitivity')

# %%
lambdavec = np.linspace(.5, .99, 10)
omegavec = np.linspace(.5, .99, 10)
dvec = np.linspace(10, 40, 10)
dt = 0.005
Tmax = 20

_DPRESETS = {'BasinOfAttraction':
             {'fields': {'Tmax': Tmax,
                         'dt': dt,
                         'lambda': lambdavec,
                         'omega': {'value': omegavec, 'grid': True},
                         'd': {'value': dvec, 'grid': True},
                         }, }, }

hub = pgm.Hub('GK-Reduced', preset='BasinOfAttraction', dpresets=_DPRESETS)
hub.run(verb=1.1)
hub.plot(idx=[0, 0, 0])

# Extracting the infos we are looking for fron dparam
R = hub.get_dparam(key=['lambda', 'omega', 'd', 'nt', 'dt', 'time'], returnas=dict)
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
    plt.show()

# %%
pgm.get_available_models(details=False)
pgm.generate_html_network_logics('GK')
pgm.generate_html_network_logics('GK-Reduced')
hub = pgm.create_preset_from_model_preset('GK', 'GK-Reduced')
hub.run()
hub.get_summary()
dax = hub.plot(label='Reduced')

BigHub = pgm.Hub('GK')
BigHub.run()
BigHub.get_summary()
dax = hub.plot(label='Full', dax=dax)


# %% Practical things about get_dparam
'''
get_dparam(self,
           condition=None,
           verb=None,
           returnas=None,
           **kwdargs):
        """
        Return a copy of the input parameters dict as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)
        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing
        """
        lcrit = ['key', 'dimension', 'units', 'type', 'group', 'eqtype']
        lprint = ['parameter', 'value', 'units', 'dimension', 'symbol',
            'type', 'eqtype', 'group', 'comment',
        ]
'''
R = hub.get_dparam(returnas=dict)
groupsoffields = hub.get_dparam_as_reverse_dict(crit='units', eqtype=['ode', 'statevar'])
print(groupsoffields)

# %%
# Run everyyyyyyyyyyything
dmodels = pgm.get_available_models(returnas=dict, details=False, verb=True,)
dsolvers = pgm.get_available_solvers(returnas=list)
for _MODEL in dmodels.keys():
    for _SOLVER in dsolvers.keys():
        for preset in dmodels[_MODEL]['presets']:
            hub = pgm.Hub(_MODEL)  # , preset=preset, verb=False)
            hub.run(verb=0, solver=_SOLVER)
            hub.plot()

########## EXERCICES 

'''Exercise 1 : execute by yourself

    Loading library "From scratch", load pygemmes
    Access lists get the list of models, the list of solvers
    Load a model Load the model 'Goodwin', then with a preset directly loaded
    change value Run it with different timestep
    change solver Run it with different solvers
    Plots Plot only lambda, then everything but lambda, then with cycles analysis activated
    Exploring dparam structure print all the keys of one field in dparam, then all their values
    Getting dparam values Get the values of omega over time as an array, plot it manually
    Creating multiple process Create a preset with 5 values of the rate of productivity progress

Exercise 2 : editing

    Accessing your personal folder find your personal folder where all models are
    Copy-paste a file Copy the file model GK-Reduced, name it GK-CES-Reduced then reload pygemmes to see if you can load id
    Modify the equations Use the equations for "lambda, omega, d" you find in McIsaac et al, Minskyan classical growth cycles, Mathematics and Financial Economics with the introduction of new parameters in _def_fields
    See the impact of a parameter (1) Do an ensemble of run with different elasticity values
    See the impact on cycles Show the impact of the elasticity value on the cycles
    See the impact on stability Do a stability analysis with different values

Exercise 3 : add on github

    Create an issue on the github page
    Once your model is ready, put it in pygemmes/_models
    Create a branch with your modifications and push it
    Create a Pull Request with it

'''