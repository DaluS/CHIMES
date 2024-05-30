hub.plot(filters_key=('p'),
         filters_units=('Units'),
         filters_sector=(),
         separate_variables={'': ['employment', 'omega']},
         idx=0,
         Region=0,
         title='',
         lw=2)


# %% EXERCICES ###############################################################
'''
Exercise 1 : execute by yourself
    1. Loading library "From scratch", load chimes
    2. Access lists get the list of models, the list of solvers
    3. Load a model, then with a preset directly loaded
    4. change value : Run it with different timestep
    5. change solver : Run it with different solvers
    6. Plots : Plot only lambda, then everything but lambda, then with cycles analysis activated
    7. Exploring dfields structure : print all the keys of one field in dfields, then all their values
    8. Getting dfields values : Get the values of omega over time as an array, plot it manually
    9. Creating multiple process : Create a preset with 5 values of the rate of productivity progres
'''


# ########################################################################### #
# %%#####################  LEVEL 2 : MODELLER ############################### #
# ########################################################################### #
'''
Exercise 2 : editing
    1. Copy-paste a file Copy the file model GK-CES name it GK-NEW then reload
chimes to see if you can load id
    2. Modify the equations Use the equations for "lambda, omega, d" you find in McIsaac et al,
Minskyan classical growth cycles, Mathematics and Financial Economics with the introduction
of new parameters in _def_fields
    3. See the impact of a parameter : Do an ensemble of run with different elasticity values
    4. See the impact on cycles : Show the impact of the elasticity value on the cycles
    5. See the impact on stability : Do a stability analysis with different values

Exercise 3 : add on github
    1. Create an issue on the github page
    2. Once your model is ready, put it in chimes/_models
    3. Create a branch with your modifications and push it
    4. Create a Pull Request with it
'''

**C**ore
**H**olistic
**I**intertwined
**M**odels
**E**ecological 
**S**implexity

CHIMES is a numerical core. It goals are the following:
* Library of models in the litterature based on differential equations
* Methodology to couple them
* Set of tools to prototype, run, compare, analyze.

In consequence it is composed of :
* A `Model` base of files that contains  description, the mathematical logical links they are composed of, preset values, and supplements
* A `Field` base (any quantity measurable in the real world) with its name, unit and default value
* A `Data` base that contains value of the real world related to models (WIP)
* A method to load models and interact with it
* A solver library for high-speed simulation with a C core using an RK4 method
* An analysis library for statistical elements on runs
* A plot library to explore the output of simulation
* An interface to user-friendly experience


**ALWAYS USE TAB, AUTOINDENTATION, HELP( ), ? When exploring a library**

## <a id='toc1_4_'></a>[Doing the real stuff: Hub](#toc0_)

Now we will load a model, and see what we can do with it

The **MOST IMPORTANT** element of chimes is the **Hub**. You will call it with a model inside of it, then interact with the model through the Hub.

A model is : 
* an ensemble of fields, quantities describing physical or informational values (temperature, employment)
* an equation associated to each of the field, determining its value over time, and how each fields are related to each others

there are three categories of possible equations : 
* **parameter :** the value is a constant (example, the gravitational constant, or the size of Mount Everest in a short-run simulation)
* **state variable :** the value is fully determined by every other fields ( the employment is determined by the quantity of workers and the population able to work, two other fields)
* **differential variables :** the variation of the value is a state variable : think about stock and flows : the variation of the stock is computed through the sum of the flow

It is possible that a same field is a parameter in some model (exogenous, constant), a state variable in other (instant adaptation), or a differential in others 

Here parameters are in blue, state variable yellow, differential variable in red. 
An simple criteria to know if it is an interesting model is "a model with loop in it, both positive and negative". 
On the left, the system is a Goodwin will its "extensive" equations, and on the right the dynamics on the phase-space. Both will solve the same overall thing


#### <a id='toc1_4_4_1_'></a>[Technical point : the data shape](#toc0_)

`chimes` core is made to take into account complex problem, the maximum level for the moment is : 
* multiple system in parrallel with different parameters (not interacting but simulated in parrallel) : it allows statistical treatment on a high number of run, stochasticity, sensibility....
* multiple regions with the same description, interacting differently
* fields to be a vector (N sectors who has a different price)
* fields to be a matrix (coupling between sectors for example)

`chimes` is mostly based on a numpy implementation, dealing well with complex problem of dimensions. By default, all the fields will have values as a 5-dimensional tensor as follow : 
* **a** 'nt' number of timesteps (parameters do not have this one)
* **b** 'nx' number of parrallel system
* **c** 'nr' number of regions
* **d** number of sectors or `__ONE__`
* **e** number of sectors or `__ONE__` 

In consequence, if you want the field `field` value at time iteration **a**, on parrallel system **b**, on region **c**, between sector **d** and **e**, you want 
`R[field]['value'][a,b,c,d,e]`
If you have a monosectoral system with only one region, one parrallel system, and you want all the time values :
`R[field]['value'][:,0,0,0,0]`

#### <a id='toc1_4_9_'></a>[Multiple regions Dynamics](#toc0_)

$\dfrac{\partial C}{\partial t} = -D \dfrac{\partial^2 C}{\partial x^2}$ 

Becomes : 

$\dfrac{\partial C}{\partial t} = -D [\nabla ( \nabla (C))]$ 

With : 

$C= \begin{pmatrix} C_1 \\ C_2 \\ ... \\ C_N \end{pmatrix}$

$\nabla= \begin{pmatrix}
 0 & (2dx)^{-1} & 0     & ... & 0\\ 
-(2dx)^{-1}     & \ddots& \ddots & 0 & ... \\ 
0         & \ddots& \ddots & \ddots & 0 \\
...         & ...& \ddots & \ddots & \ddots  \end{pmatrix}$

Modulation of $\nabla$ for network dynamics ( tweaked finite differences methods) 







########################### PART FOR MULTIRUN ##########################

hub=chm.Hub('GK')
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='business as usual')


### Shock on capital
hub=chm.Hub('GK')
hub.run(steps=500,verb=False)
R=hub.get_dfields()
K0=R['K']['value'][500,0,0,0,0]
hub.set_dfields(**{'K':K0/2},noreset=True)
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='capital shock')

### Change depreciation
hub=chm.Hub('GK')
hub.run(steps=500,verb=False)
R=hub.get_dfields()
delta=R['delta']['value'][0,0,0,0]
hub.set_dfields(**{'delta':delta*10},noreset=True)
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='depreciation shock')

### Ramp of depreciation
hub=chm.Hub('GK')
for i in range(20):
    hub.run(steps=50,verb=False)
    R=hub.get_dfields()
    delta=R['delta']['value'][0,0,0,0]
    hub.set_dfields(**{'delta':delta*1.2},noreset=True,verb=False)
hub.run()
hub.plot(filters_units=['','Units','y'],separate_variables={'':['pi','kappa']},title='Exponential damages')

################### PART FOR SENSITIVITY ################## 
# Exploring Sensitivity Analysis with CHIMES 

How to know which parameter is the one that requires best attention in the calibration ? 
We show how here how CHIMES can answer such issues, using Monte-Carlo-like simulations 

The protocol is the following:
* You decide a model you want to study
* You find an "as good as possible calibration" of the model
* You determine which output variables you consider relevant 
* You determine the timescale it should be relevant
* You run CHIMES
* You write your article!
## Replacing a parameter by a distribution of parameters

let assume we have a parameter $x$. Instead of running one simulation with one value of $x$, we select an ensemble of $N$ possible values for $x$ in a distribution $f(\mu,\sigma)$. 
Typically :
* $\mu$ is the mean value of the distribution
* $\sigma$ is the standard deviation of the value 
* $f()$ is a distribution. It can be a Gaussian, a log-normal, uniform... 

In order to know which type of distribution one should consider, here are a few rules of thumb:
* If your parameter is the consequence of the product of many phenomenon, it should be a log-normal. 
* If your parameter sign is well defined, chances are a log-normal should be better
* If your parameter is the consequence of a sum of many phenomenon, it should be normal

It's sometimes practical to think in term of value and margin of error 

hub=chm.Hub('GK')
hub.set_dfields('Delta',0.01)
hub.set_dfields('Tsim',5)
hub.set_dfields('dt',0.1)
OUT=hub.run_sensitivity(verb=False,std=0.05)
FIGURES=chm.Plots.Showsensitivity(OUT,['employment','omega','d'],0.05)

presetCoupled = chm.generate_dic_distribution({'alpha': {'mu': 0.02,
               'sigma': 0.5*0.02,
               'type': 'log'}, },
                                              N=100)


plt.figure('')
plt.hist(presetCoupled['alpha'])
plt.xlabel(r'Values of $\alpha$')
plt.ylabel('Number of runs with it')

hub=chm.Hub('GK',verb=False)
hub.set_dfields(**presetCoupled)
hub.set_dfields('Tsim',20)
hub.run()
hub.calculate_StatSensitivity()

for var in ['employment','omega','d']:
    chm.Plots.Var(hub,var,mode='sensitivity')


    
Tests = {'log':{    'mu': 1,
                    'sigma': .12,
                    'type':'log' },
            'lognormal':{'mu': .02,
                    'sigma': .3,
                    'type':  'lognormal'},
            'log-normal':{'mu': .02,
                    'sigma': .4,
                    'type':'log-normal'},
            'normal':{'mu': .02,
                    'sigma': .12,
                    'type': 'normal'},
            'gaussian':{'mu': .02,
                    'sigma': .12,
                    'type': 'gaussian'},
            'uniform':{'mu': .02,
                    'sigma': .12,
                    'type':'uniform'},
            'uniform-bounds':{'mu': .02,
                    'sigma': .12,
                    'type':'uniform-bounds'},
            }
TestDistrib = chm.generate_dic_distribution(Tests,
                                            N=1000)

import numpy as np

for k in Tests.keys():
    print(f'########{k}#########')
    print(f'Sent dic: {Tests[k]}' )
    print(f'mean :{np.mean(TestDistrib[k])}')
    print(f'std  :{np.std( TestDistrib[k])}')
    plt.figure(k)
    plt.hist(TestDistrib[k],bins=50)
    plt.show()