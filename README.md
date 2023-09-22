# CHIMES: Core of Holistic Intertwined Models for Ecological Sustainability


# CHIMES overview

* You want to explore, couple, analyze existing models, or create your own ? CHIMES is the library made for you! 
* You work with Agent-Based models (collective behavior, economic agents, birds movements), chaotic systems, spatial properties, multiple circuits of ressources (Money, CHNOPS...), CHIMES is the library for you! 
* You want to do a lot of runs in parrallel to test the sensitivity of a parameter or initial condition? Same!
* You want a user-friendly interface so that you do not code too much, while keeping the full flexibility of python at every step ? Same! 
* You like python for its practicality but it's slow to solve equations ? CHIMES is the library for you !

![image](https://github.com/georgetown-ejp/CHIMES/assets/11523050/00cd06e1-0a8d-4f38-a74a-f1ee006f83af)
*Some illustrations of CHIMES content*


# What is CHIMES?

CHIMES is a numerical core, with a huge toolbox and interface around it. It goals are the following:
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

![image](https://github.com/georgetown-ejp/CHIMES/assets/11523050/22286361-1d5e-48c3-9d6c-d3179eb27515)
* The flow inside the library*

In consequence, it is possible to do multisectoral, multiregional, resources-inequalities-climate-international socio-economic system. 

## What is a model? 

A model is a intertwined map of fields. Fields are quantities (Population size, temperature anomaly, price, inflation) relevant for the system. Creating a model is building the web of dependency, how each field relate to each other, through logic equations. 
Those equation can be purely algebraic expressions. 

To each field can be associated a logic. The logical can be differential "the variation of the field is given by this mathematical relationship", or a state variable "the value of this field is given by this mathematical relationship". 
If a field has no logic, it is a parameter. 

A model is a map, not the values themselves. Putting values allows one to do go from one model to specific uses of the model as examples (presets). Coupling a model with a database allow it to animate its elements and do prospective! 

![image](https://github.com/georgetown-ejp/CHIMES/assets/11523050/33a7e520-3a0a-4489-b99f-f167c51c9e4f)
*Causal map of a Goodwin-Keen model*

## How to use the library (importation)

### Importing the library
Since the library is not on a pip wheel, you need to add it to your path 

To do so I recommend 
```
path = "C:\\Users\\Username\\Documents\\GitHub\\CHIMES" 
import sys
sys.path.insert(0, path)

import chimes as chm
```

Where path is where you installed the library

### Installing the requirements
The requirements can be found in `requirement.txt`, you need to install all of them. 
It can be done by executing: 
```
import os 
import importlib.util
with open(os.path.join(path,'requirements.txt'),'rb') as f :
    out=str(f.read())
    libraries = out.split('\\r\\n')[1:]
    for l in libraries:
        if importli
        b.util.find_spec(l) is None:
            !{sys.executable} -m pip install {l}
        else: 
            print(l,'already installed')
```

### Exploring the library 
Always use `?` and `tab` (help and autocompletion) to know what are in each element. 

To know the content I recommend: 
```
chm.get_available_models()
chm.get_available_fields()
chm.get_available_functions()
chm.get_available_operators()
chm.get_available_plots()
chm.get_available_saves()
```

To explore one model in particular:
```
chm.get_model_documentation('modelname')
```

To load a model 
```
hub=chm.Hub('modelname')
```

To load the save of a model 
```
hub=chm.load('nameofthefile')
```

To explore it 
```
hub.get_summary()
```

To explore it further
```
hub.get_Network()
hub.get_dataframe()
hub.get_dparam()
hub.get_dparam_as_reverse_dict()
hub.get_dvalues()
hub.get_equations_description()
hub.get_fieldsproperties()
hub.get_new_summary()
hub.get_presets()
hub.get_summary()
hub.get_supplements()
hub.reverse_cycles_dic()
hub.Extract_preset()
```

To load a preset 
```
hub.set_preset('presetname')
```

To run the model 
```
hub.run()
```

To access values 
```
dval = hub.get_dvalues() # Minimal values output
dparam = hub.get_dparam() # Contains all the model fields and properties
```

# Contributing

There are three layers of contributions possible
* User (just have fun with the library and use it for your work)
* Modeler (add new model in the system)
* Developer (add new functionalities)

## Contributing as a User
1. Explore the interface using `chm.Interface()`
1. Do the tutorial in `doc\tutorial.ipynb`
2. Try different models and preset, with their plots
3. Changing values and see the impact
4. Save your runs
3. Emit `issues` on the github page

## Contributing as a Modeller
The goal of a modeller is to implement models given the framework of `CHIMES`. 
1. Look at model files (typically `models/_model__TEMPLATE_.py`)
2. Explore the `Tutorial-model.md` tutorial on how to create a model
3. Explore `get_available_fields()` to see what fields are already developed
4. Create your own model, either loading a previous model (extension), connecting two models (bridging)
5. Create your preset to insert relevant run of the model 
6. Add supplements that can be used with the model in its section
7. Share the model through a github pull request

## Contributing as developer
The goal of a developer is to ensure the consistency of models and the toolboxes
1. If a model is in the pull request, verify that it works, and is not duplicating fields
2. If there is no duplicate, integrate new fields in `_def_fields`
3. Check the supplements, and if relevant add them in `_plots` or `_core` depending of their use
4. Help on the issues 


## Code path at initialization (for developper)

1) __config 
2) __init__
3) _core hub __init__
    4) _class_set.load_model 
        * Check model name
        * Load "model" as a dictionnary
        * prepare CHIMES knowledge of fields to be compatible
        * Check completude 
        * Translation from dmodel to dparam 
        * Add CHIMES knowledge 
        * Identification for categories/solving
        * Initial shapes
        * Big dictionnary of pointers
    5) _set_preset
        * set dparam
            * set dimensions
            * set fields 
    6) reset 
7) set dparam
    * set dimensions            
    * set fields 
8) run
    9) _solvers.solve
        10) get_func_dydt
            * Create all buffers and arrays
            * create the function y'=F(y) with F coupling functions

## Files and folder description

* **doc** Contains practical files for user that do not touch the code
* **model** Contains all models loaded by CHIMES with categories subfolder
* **pygemmes** Contains the code library
    * `_config.py` All flags and general properties of the library
    * `_core.py` Main methods for the Hub
    * `_toolbox.py` Miscellaneous functions for CHIMES
    * `__init__.py` Welcome message if activated
    * **_models** Basic shared properties of models and introspection methods 
        * `__init__.py` Introspection, completion methods, integrity checks (should be moved away)
        * `_def_fields.py` Fields library 
        * `_def_functions.py` Functions library used in model file
        * `_def_Operators.py` Operators library used in model files (scalar product, transpose etc)
    * **_plots** Plot functions for the hub
    * **_utilities** Additional functions for the hub, complement of `_core`
        * `_class_check` Verify the model integrity
        * `_class_set` Transform the model file into practical hub version
        * `_class_utility` Miscellaneous functions
        * `_Network` Representation of models in nodes
        * `_solvers` Solving time iterations
        * `_utils` Should be fused with `_class_utility`
    * **test** Unit tests 

# The Developpers (that have done at least one PR)

* Paul Valcke
* Didier Vezinet
