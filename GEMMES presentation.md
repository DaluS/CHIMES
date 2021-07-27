# PYGEMMES : prototyping and analysis of models based on dynamical systems 

by Didier Vezinet and Paul Valcke 

Environmental Justice Program 

[logo labo]

[logo distribution]

Date : 

# Outline of this presentation 

* Creating models, analysing models, running simulations
* Quick recall on economic model with dynamical system formalism 
* Code specifications 
* The structure of the code
* How to run the code
* How to develop the code
* Future functionalities 

# What are models ? 

## Definition of models 

A **Model** is : 
* An ensemble of systems ( atmosphere, bank, mines...), with each an ensemble of characteristics (fields), either variables or constant (parameters)
* An ensemble of logical hypothesis that links the characteristic, that either links multiple fields of the system or fields from different systems. 
* There is a wide topology of links between these variables. Depending of the topology and the nature of the links, the model belong to certain types of model class 

## Level of hypotheses 

there are five levels of description for a field :

1. I exist, but I am unrelated (so not taken into account in the model)
2. I exist and I am related, but my value is constant (parameter) : I am defined by myself and not by the system
3. I exist and I am related, but my temporal evolution is given by external factors only (exogeneous) : I am defined by myself and not by the system
4. I exist, and I am related, but my temporal evolution is only a consequence of the other one and not of myself (endogeneous)
5. I exist, I am related, my temporal evolution is the consequence of the other ones and also of myself (endogeneous, differential)

_4 is a special case of 5, for example if 4 is $y=f(x)$, then five can be for example $dy/dt = \frac{f(x)-y}{\tau}$, which explicit the fact that there is a typical time in the model for y to react to its precise value ( for example, recruitment/firing in a goodwin extension) $\tau=0$ force $f(x)=y$_

## The work of a modeler

The work of a modeler is :
* **Model creation** : to determine the systems, the fields, and the links that "close" the system (make it consistent in his own universe, with no need of something exterior to exist)
* **Model analysis** : to determine, depending of the relationship of values, the broad behavior of the system (equilibrium, stability...), done through an ensemble of simulation (numerical approach) or analytically

There are two golden rules in modelling : 
* The model must be as simple as possible (but not simpler) to keep it understandable 
* The hypotheses done to create the model must always be modifiable without breaking the whole model to allow easy improvement 

_If logic A and logic B, then logic C emerges on these conditions_

## Doing simulation

The work of simulation is : 
* **parametrisation/calibration** : finding the most relevant values to initiate the system so that it corresponds to the real system you want to compare with. It is a projection of the model into one set of values
* **Trajectory analysis** : Let the system evolves through the conjonction of initial values + logics, analyse the properties of the trajectory, use it for descriptivity and normativity

_The simulation shows that in these condition we can expect X to increase of Y% during a time Z%_

## Models and simulation

It's hard to do a model simple enough that it is easy to understand, and strong enough that it allows good simulation. A good modeler creates structure that does both. 

A simple model that gives a lot of :
* Emerging properties depending of the parameter projection 
* An accurate-enough description when applied to reality 

Is an **Archetype**. That's the graal (perfect gas, harmonic oscillator...)

# Models in economy 

## The neoclassic core 

* Based on the notion of utility 
* Based on the notion of discount rate over time 
* Based on the optimisation of utility 

Based on one two fields that we cannot measure, and optimization as the process. Difficult to improve a lot of the core hypotheses 

$y(t) = \int_{t_0} u(y(t)) \dfrac{dt}{e^\rho t}$ 

"The trajectory taken by the system is the consequence of the complete exploration of all possible trajectories, with only the best one kept"

* Outcome centered, with the process as a way to get there, produce normativity without descriptivity
* Lot of processes cannot be written in this formalism
* Very far from the formalism of other sciences 

## Dynamical systems 

* The evolution of the state of the system is determined by the state of the system 
* Temporal evolution is the iteration of this logic on itself 

$\dfrac{\partial y}{\partial t}= f(y)$

* Process-centered, optimization can be an outcome of it
* Hypotheses easy to be improved
* Formalism close to other sciences 
* Produce descriptivity with possibility of normativity

# GEMMES modelisation 

## Principle of creation

* Written with differential equations (stock and flow) evolution
* Determined with two types of logic hypotheses : 
	1. Stock-Flow consistency (nothing appears or disappear out of nothing)
	2. Behavioral hypotheses (humans behavior)
	3. Metabolic hypotheses (one quantity of something can be transformed into another)
* Easy to modify the hypotheses
* Easy to couple with other disciplines 

_Allow us to put back economy as a part of the environnement, and not environment as a part of economy_

## A galaxy of models 

* Based on a goodwin Model []
* With Private Debt (Keen) []
* With price dynamics and inflation []
* Driven by demand []
* CES part []
* Climate retroaction []
* Inertia []
* Ressources []
* Minimal multisector []
* With stochastic terms []
* Minimal household multisectorialisation []

# PYGEMMES 

## Two step back... 

The typical principle in science is : 

Descriptivity -> normativity -> politics 

We can add more categories to understand where we are :  

Model creation -> Model analysis -> Simulation -> Descriptivity -> Normativity -> Politics 

The goal of this program is help modeller on both two first steps > 

* Easy model creation 
* Easy model analysis 

It also allow model comparison through a common background ! 

## How to run the code

1. Download the package (through github) https://github.com/DaluS/GEMMES
2. If you don't have python, download an IDE (for example anaconda is great https://www.anaconda.com/products/individual )
3. Set your path to the place you put the python files [image]
4. Execute line by line `tutorial.py` and read `readme.md`

## The structure of the code

### Controlling the system 
* `gemmes.py` 
* `cockpit.py`
* `tutorial.py` 

### Structure the system 
* `models/_model_NAMEOFTHEMODEL.py`
* `models/_def_field.py`
* `_plots.py`
* `_core.py`

### Files you should not modify 
* `__init__.py`
* everything not in the folder `output` or your own models 

## Step-by-step exploration 

## Step-by-step "Create your own model" ! 

1. Choose an inspiration model 
2. Do a copy with a new name 
3. Modify the description
4. Modify the equations 
5. Modify the presets
6. Check that it can run 
7. Make it run 
8. Compare it with other models
9. When satisfied, add your fields to `_def_fields.py`  

## Step-by-step "Create your own plot" ! 

1. Copy a function in `_def_plots.py`

## Becomes a developper ! 