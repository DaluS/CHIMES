# README HAS TO BE WRITTEN, THIS IS AN OLD VERSION. Look At The Ipython Notebook in doc/Tutorial.ipynb

# Contributing

There are three layers of contributions possible
* User (just have fun with the library and use it for your work)
* Modeller (add new model in the system)
* Developper (add new functionalities)

## Contributing as a User
1. Do the tutorial in `doc\tutorial.py`
2. Try different models and preset
3. Emit `issues` when something looks wrong `https://github.com/DaluS/GEMMES/issues/new`


## Contributing as a Modeller
The goal of a modeller is to implement models given the framework of `pygemmes`


### Try being a user !
1. Do everything in "contributing as a user" section just above
2. Look at the list of proposed model to implement in `https://github.com/DaluS/GEMMES/projects/1`, or choose your own


### Get to know what exist
1. Look at models using ` `
2. Look at the fields available ` `
3. Look at the functions available ` `
4. Look at the plot available ` `


### Get to know what to put in your economic model (on paper)
1. Choose what sectors you want to put in your model
2. Choose the stocks they have (money, physical units)
3. Choose the flux that links them
4. Write stock-flow consistency (evolution of stock depending of flux)
5. Detail the quantitative values of flux (Metabolix hypothesis, Behavior)
6. You might have some circular dependency in your variable : a first round of simplification might be needed


### Implement everything : in the model file
1. Copy a file model that you think is inspiring and write it with a new name
2. Use all the fields alaready existing in `_def_fields` that exist in your model
3. Use all the function existing in `_def_functions` that correspond to your model
4. Write your presets
5. Define new fields and parameters if needed
6. Define new functions if needed
7. Define in your preset plot new functions if needed


### Sharing with the community : first pull request
1. Create a branch on your git
2. Put your model file in the `pygemmes` folder
3. Push your branch
4. Do a pull request explaining what you've put inside your model (you can do generalisation directly if you want and avoid the multiple pull request)


### Generalisation : from the model file to the library
This step is optional but appreciated !

0. Create a new branch
1. put all your new fields inside `def_fields` either by creating a new group or adding elements in an existing one
2. put your new functions inside `def_functions`
3. put your new plots inside `def_plots`
4. Re-edit your models calling the functions of these files instead
5. Do a new pull request


## Contributing as a Developper <3
1. First add a model in the system
2. Look at the issues
3. Choose which issue you want to work on and say it on the issue (or raise a new issue)
4. Bring a PR with your new code !








# GEMMES NUMERICAL MODELS FOR MACROECONOMIC AND ECOLOGIC STUDIES

## WHAT, AND WHY THESE MODELS ?

### WHAT GEMMES STANDS FOR ?

GEMMES Stands for :

**G**eneral

**M**onetary and

**M**ultisectoral

**M**acrodynamics for the

**E**cological

**S**hift

**The goal** is to give user some insight about the dynamics society could go into with problematic such as :
* Economic instability (Debt, unemployement, endogeneous cycles)
* Ressource scarcity
* Climate impact
* Biodiversity impact

### IS IT AN IAM AS MANY OTHERS ?

It is an IAM (Integrated assessment model) but not in the standard way : it is based on dynamical systems rather than intertemporal optimisation.

As a consequence, the model is much more suited to take into account economy as a part of the world (ecology) rather than seeing the ecology as a part of the economy.
It is much more convenient that way to couple different disciplines that way. This formulation is also stock-flow consistent : nothing appear or disappear out of nowhere by construction. This is a great help to get closer to a thermodynamic consistent model.

The economic part is handled through Post-Keynesian approach, particularly efficient on rapidly-evolving, out of equilibrium dynamics with endogeneous crysis.

In the general methodology, one could see similitudes with 'Limits to growth' but with 50 years of update in term of dynamical systems and interdisciplinary research, and more policy oriented.
The model are based on descriptivity and allow the user to develop normativity.

### WHAT ARE OUR GOALS WITH THE MODELISATION PROGRAM ?

We aim a three goals :
* Create a common background that is practical for all disciplines to communicate through one platform and language in coupled models
* Show through simplified models emerging properties in economy, and the potent of post-keynesian models for the economy in the XXI century
* Propose coupled modelisation to show interdisciplinary results with a true strong coupling of disciplines

## WHAT CAN YOU FIND IN THIS CODE ?

### A galaxy of related models from previous articles

### Toy-models to show some emerging properties in economic systems

# HOW TO USE THE CODE

## Installation : Dependencies



## Installation : The files

* **main**
* **Miscfunc**
* **ClassesGoodwin**
* **parameters**

* **VariableDictionnary**
* **plots**

## HOW TO USE THE CODE

## HOW TO WRITE YOUR OWN MODULE

### Check the state of the library of models
Check the ensemble of models to find good inspiration.
To do so, execute.

```
import _core
_core._class_checks.models.describe_available_models()
```

Maybe one of them is a good basis that you can fork (copy then modify).

### Check the state of the library of fields
Check the library to know what field are defined or not. To do so, execute in the cockpit
```
import models._def_fields_NEWFORMALISM as dfields
dfields.print_fields(value=False,com=True,unit=False,group=False)
```

In some fields you are interested on don't exist, do not edit the library yet. You will add them in your model

DO NOT OVERLOAD A FIELD IF YOU WANT TO CHANGE WHAT IT IS RELATED TO.
For example don't use `lambda` for thermic conductivity as it is defined as the employement rate (as written in the comment), use rather `lambda_therm`

### Write your model

#### Write a description
Write a description of the model in `_DESCRIPTION`, with the typical behavior, and a link to an article/working paper

#### Write the logic of the model
 Write in `_LOGICS`:
    1. in 'ode' all the differential equation
    2. in 'func' all the intermediary functions, that makes the model easier to understand !
    3. if 'PDE' and 'DDE' are developped, same logic

The user define in each a key 'nameofthevariable' a dict with at least 'logic' (a function or a lambda function)
and a comment in 'com'. when writing the lambda function, use the following principle :
* The name of variables will have to be related either to a name in the library (it will be loaded) or in _LOGICS
* When writing a differential equation, instead of naming the variable in its definition, use `itself`

For example `da/dt= alpha a` will be :
```
'a': {
            'logic': lambda alpha=0, itself=0: alpha * itself,
            'com': 'Exogenous technical progress as an exponential',
        },
```

if you want to write a more complex function, you can define it on the side an call it in logic !

#### Write presets
Write preset in _PRESETS which contains each as a dictionarry of dictionnary.
Each preset contains :
* `fields` that is a dictionnary with all the values you want to specify when running to model (both ODE and parameters). Don't put  intermediary functions in it :)
* `com` a short description
* `plot` a list of plots from the plot file

If an initial condition/parameter is not specified, the value will be taken in `_def_fields` (the library)

It is good practice to put a `default` as one of the model with all field defined

#### Add Precision

You can fill `_FUNC_ORDER` and `_FUNC_PARAMS` with a list in each, that contains :
* `_FUNC_ORDER` : the order of 'func' (for example `['Y','GDP','L']`... that must have the same size as `func`
* `_FUNC_PARAMS` : all the parameters that are in the model

If you put `None` the system will fill it automatically the best he can

### I want my model to be fully compatible

Add your fields in the `_library` located in `model/_def_fields.py`.
1. Create a dictionnary that will be your group in the dic `_library` [IMAGE]
2. Add the parameters following this formalism [IMAGE]
3. You can add parameters which depends only of parameters using [IMAGE]
4. To put function related fields use the formalism as [IMAGE]
5. To add ode related fields use the formalism as [IMAGE]




# The Developpers

* Paul Valcke
* Didier Vezinet
* Camille Guittoneau
