# -*- coding: utf-8 -*-
"""
Contains all the formulations one want to know
"""

# I MAKE SURE YOUR ENVIRONMENT IS READY ######################################
'''
# I.1 check that you have all the libraries

to get all the libraries you are going to need
`!pip freeze > requirement.txt -v`

# I.2 Tell python where pygemmes is
pygemmes has to be found by python so that it can loads it

there are two methods :
    a) Start your python terminal at the root of the library ( typically ...\\GitHub\\GEMMES )
or indicate it to spyder if you're using it (top-right folder)
    b) Indicate to the system path where it is. In my case I'd have to use the lines :

```
import sys  # a library that help python know where things are
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`
```

If you do a) you do it once and you're ready to go !
if you do b) you have to do it every time

########## ONCE IT'S DONE YOU SHOULD RESTART YOUR IPYTHON TERMINAL ###########
'''
import pygemmes as pgm  # we rename pygemmes as pgm to be shorter
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
path = "C:\\Users\\Paul Valcke\\Documents\\GitHub\\GEMMES"  # Where pygemmes is
sys.path.insert(0, path)  # we tell python to look at the folder `path`


# %% PYTHON 101
'''
Python is a user-friendly, flexible language, with a huge community (lot of libraries),
and incredibly powerful when used well

Here are a few practical examples
'''

# There are multiple types of variables

A = 'oneword'  # A string (characters)
B = "multiple words"  # A string too !
C = ''' A long description
That can be on multiple lines '''

D = 1
E = 1.1
F = True
G = E > F

H = {}
keyvar = 'key'
H[keyvar] = 42
H['test'] = C
H[C] = 0  # You can put anything as a list !
H[3] = 'plop'
I = {}
I['dictionnary'] = H  # A dictionnary inside a dictionnary

# Elements can be put together
J = (A, D, H)  # A tuple (a list that cannot be modified)
K = [A, D, H]  # A list

# Loops work with indentations
for i in [1, 2, 3, 4]:
    print(i)

# Dictionnaries are objects, and objects have methods associated :
for key, value in H.items():
    print(key, value)

# You can create your own objects


def IAmAFunction(x, hello=1):
    '''
    This is a description to explain what is in the function
    '''

    y = x+1  # y is created locally, once we leave the function we cannot acces y
    if hello:
        y *= 2  # we have a if loop for fun, hello=0, hello=False or hello=None does not go in this section
    return y-7  # the value that you get at the end


print(IAmAFunction(45))  # hello will take the value 1
print(IAmAFunction(34))
print(IAmAFunction(34, hello=False))  # hello is taking the non-default value

# USE ARRAYS !
A = np.linspace(0, 1, 100)
B = np.linspace(100, 200, 100)

C = A*B
D = np.zeros(100)  # create 100 zeros
for i in range(100):
    D[i] = A[i]*B[i]
print(C-D)

# %% OVERVIEWS : WHAT IS IN PYGEMMES ?
pgm.get_available_solvers()
pgm.get_available_models(details=True, verb=True)
pgm.get_available_output()
pgm.get_available_dfields()

listofsolver = pgm.get_available_solvers(returnas=list)
listofmodels = pgm.get_available_models(returnas=list)
listoffields = [v[0] for v in pgm.get_dfields_overview(returnas=list)]

# %% A FEW SIMPLE FUNCTIONS TO SHOW A FEW POSSIBILITIES
'''
Commented in the files, no use
'''
# pgm.comparesolver_Lorenz(dt=0.01, Npoints=10000)
# pgm.plot_one_run_all_solvers('LorenzSystem', preset='Canonical')
# pgm.plot_one_run_all_solvers('GK')
# pgm.testConvergence_DampOsc([1, 0.1, 0.01, 0.001], solver='eRK4-homemade')


# %% HUB : YOUR BEST FRIEND
hub = pgm.Hub('GK',)
# verb=False
# preset=None,
# dpresets=None,
# verb=None)

hub

pgm.Generate_network_logics('GK')
hub.equations_description()

hub.dmodel  # Gives the content of the model file
hub.dmisc  # gives multiple informations on the run and the variables

hub.get_summary()

hub.run(verb=0)  # solver=listofsolver[0],verb=1.1)
R = hub.get_dparam(returnas=dict)

hub.get_summary()

# Plots examples
dax = hub.plot()
dax2 = hub.plot(key=['lambda', 'omega', 'd'])  # Select the variables
dax3 = hub.plot(key=('GDP', 'a', 'Pi', 'kappa'))  # Remove some variables
pgm._plots.phasespace(hub, x='omega', y='lambda', color='d', idx=0)
hub.plot_preset(preset='default')

# Fill Cycles
hub.FillCyclesForAll(ref='lambda')
dax4 = hub.plot(mode='cycles')

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

# %% Example : gaussian system
hub_noise = pgm.Hub('Noise')
hub_noise.run()
dax = hub_noise.plot(key=['y'], label='-1')
for i in range(10):
    hub_noise.run()
    dax = hub_noise.plot(key=['y'], dax=dax, label=i)

# %% CHANGING VALUES
hub = pgm.Hub('GK', verb=False)
# One slowly
hub.set_dparam(key='dt', value=0.01)
hub.set_dparam(Tmax=50)

# Send a dictionnary
dparam = {'alpha': 0, 'n': 1}
hub.set_dparam(**dparam)

# Create N system in parrallel with different values
hub.set_dparam(alpha=[0, 0.01, 0.02, 0.03])

# Load a preset
hub = pgm.Hub('GK', verb=False)
hub.set_dparam(preset='default')

# %% COMPARING MODELS REDUCED AND NON-REDUCED
pgm.get_available_models(details=False)
pgm.Generate_network_logics('GK')
pgm.Generate_network_logics('GK-Reduced')
hub = pgm.create_preset_from_model_preset('GK', 'GK-Reduced')
hub.run()
hub.get_summary()
dax = hub.plot(label='Reduced')

BigHub = pgm.Hub('GK')
BigHub.run()
BigHub.get_summary()
dax = hub.plot(label='Full', dax=dax)

# %% Generate a dictionary of dictionary, with for each key:{'mean value", 'std' , 'distribution'}
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

# %% BASIN OF ATTRACTION
lambdavec = np.linspace(.5, .99, 10)
omegavec = np.linspace(.5, .99, 10)
dvec = np.linspace(3, 20, 10)
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
# hub.plot(idx=[0, 0, 0])

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
        plt.xlabel(r'$\lambda(t=0)$')
        plt.ylabel(r'$\omega(t=0)$')
        plt.colorbar()
        plt.pause(Pause)
    plt.show()


# %% Run everyyyyyyyyyyything
dmodels = pgm.get_available_models(returnas=dict, details=False, verb=True,)
dsolvers = pgm.get_available_solvers(returnas=list)
for _MODEL in dmodels.keys():
    hub = pgm.Hub(_MODEL)  # , preset=preset, verb=False)
    hub.run(verb=0)
    # for _SOLVER in dsolvers.keys():
        for preset in dmodels[_MODEL]['presets']:
            hub = pgm.Hub(_MODEL)  # , preset=preset, verb=False)
            hub.run(verb=0) solver = _SOLVER)
            hub.plot()

# %% EXERCICES ##########################################

'''
Exercise 1 : execute by yourself
    1. Loading library "From scratch", load pygemmes
    2. Access lists get the list of models, the list of solvers
    3. Load a model Load the model 'Goodwin', then with a preset directly loaded
    4. change value Run it with different timestep
    5. change solver Run it with different solvers
    6. Plots Plot only lambda, then everything but lambda, then with cycles analysis activated
    7. Exploring dparam structure print all the keys of one field in dparam, then all their values
    8. Getting dparam values Get the values of omega over time as an array, plot it manually
    9. Creating multiple process Create a preset with 5 values of the rate of productivity progres

Exercise 2 : editing
    1. Accessing your personal folder find your personal folder where all models are
    2. Copy-paste a file Copy the file model GK-Reduced, name it GK-CES-Reduced then reload
pygemmes to see if you can load id
    3. Modify the equations Use the equations for "lambda, omega, d" you find in McIsaac et al,
Minskyan classical growth cycles, Mathematics and Financial Economics with the introduction
of new parameters in _def_fields
    4. See the impact of a parameter (1) Do an ensemble of run with different elasticity values
    5. See the impact on cycles Show the impact of the elasticity value on the cycles
    6. See the impact on stability Do a stability analysis with different values

Exercise 3 : add on github
    1. Create an issue on the github page
    2. Once your model is ready, put it in pygemmes/_models
    3. Create a branch with your modifications and push it
    4. Create a Pull Request with it

'''

# %% TESTS ##########################################
# TO TEST THAT EVERYTHING IS WORKING WELL
# !pytest pygemmes/tests/test_01_Hub.py -v
# !pytest pygemmes/tests/test_00_get -v
# !pytest pygemmes/tests/test_02_Hub_Multiple -v
# !pytest pygemmes/tests/test_03_articles -v


'''
    def test02_test_all_solvers_2parrallel(self):

    def test03_initialize_and_run_all_models_all_preset_all_plots(self):

    def test04_relevant_prints_from_hub(self):

    def test05_fillcycles_onesystem(self):

    def test06_sensibility_test(self):
'''
