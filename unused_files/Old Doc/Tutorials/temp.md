
## CHM get 

CHIMES can gather many elements and make them interact. Some are composed of others types! For example, a model is composed of fields, and a run can be saved as a file that you can reuse, and plot its results. 
By default, CHIMES give you the following objects: 
* **fields** Any quantity that can exist in the system: temperature, debt, size, efficiency... With all its attributes. You can use those (recommended) and add your own when relevant
* **functions** Logics that are often found in models to link some fields to others in term of values
* **models** The most important one ! Models are linking fields with logics (functions), explain why one would do so and the typical plots and values you should use with it. CHIMES is made for models. You can use the existing one, create your own and couple models. Once they are loaded in the Hub, you can modify all their values
* **model_documentation** As many information as you can need to understand a model
* **saves** files of saved run using a models, in which you changed values, made simulations...
* **config** an ensemble of parameters that change the behavior of the library itself (for advanced users only)
* **plots** homebrewed plots to display your simulations 
* **operators** pieces of functions useful when you create a multisectoral or multiregional models 

Depending on your level, we recommend you know how to use the following:

* **users** should know `get_available_models()`, `get_model_documentation(modelname)`
* **advanced user** should know `get_available_plot()`, `get_available_save()`
* **modeler** should know `get_available_functions()`, `get_available_fields()`
* **advanced modeler** should know `get_available_operators()`
* **power-user** should know `get_available_config()`

### Models

Models are the core of CHIMES. They are the dynamical systems that are simulated.
A model is a set of equations written in a Python file and read by the library. 
As a use, you do not have to write your model; you can load the existing one. 

At first glance, you can check `chm.get_available_models()` to see which models are available. This function gives you the data frame of a model with a short description you can put in the hub. 

You can also get the full description of the model with `chm.get_model_documentation(modelname)`

Once you know which model you want to explore, do `hub=chm.Hub(modelname)` to create a hub with this model, and continue the exploration.

If you want to include your own model files, you have to change the model private folder in `chm.config` (see below)

```python
chm.get_available_models() #You have a filter on the top-right to check keywords you like!
```

```python
chm.get_model_documentation('Goodwin_example') # more documentation
```

### Fields

Fields, such as temperature or price, can be used in models. 
Most are defined in the library, but some are defined in models: 
    You can use those in the library without adding details, and they will be automatically loaded (units, symbols, default values, etc.).
    If you use your own fields, you need to add their property in the model file (see the template)

Retrieves all fields in CHIMES along with their units, default values, and additional information.
This function loads the library of fields, and if exploreModels is True, all fields are defined inside each available model. 

```python
chm.get_available_fields(exploreModels=True) 
```

### Config

The config element contains customization elements for the library, allowing you to change its global behaviour, folders, verbosity, warnings, accepted entries, etc. It is not something you should modify first, but it should remain accessible.  
* To know more about the config variables, their current values, and their possible values, use `chm.get_available_config()` or `config.get()`
* To get one variable current value `chm.config.get_current(valuename)`
* To change a value, use `chm.config.set_value(key,value)` or  `chm.config.set_value(**{key:value, [...] })`
* To see what customization values are currently taken into account, use `chm.config.read_local_config()` 
* To reset customized values, use `chm.config.reset(key)` or  `chm.config.reset([list of keys, ...])` or `chm.config.reset('all')`

```python
chm.get_available_config()
```

### Plots

CHIMES contains an ensemble of plots based on matplotlib or plotly, made for local formalism. 
Each has been developed to show specific aspects of your runs, some model properties, or to represent additional toolbox calculations. 

To know which plot is available, use `chm.get_available_plots()`

Once you know which plot you want to consider, use `chm.Plots.PLOTNAME(hub, **ARGUMENTS )` with the ARGUMENTS from the plot docstring. 

The structure of the arguments will always be : 
* Variables, keys, and filters that are considered
* indexes about region, parallel system, time 
* special properties of the plot activated through flags
* titles and decorators 

You can always do `chm.Plots.PLOTNAME?` to see more information, check the tutorial file on plots, or use `chm.get_plot_documentation(plotname)`

```python
chm.get_available_plots()
```
```python
chm.get_plot_documentation('Sankey')
```

### Functions

The function library contains a set of functions that can be used in the logic of the models. 
Models can contain other functions than those in the library, but they are not listed here.
To use one of those functions in your model, do `from chimes._models import Funcs` and then `key : Funcs.category.functionname`

```python
chm.get_available_functions()
```

### Operators

Operators are special operations that can be introduced in model creations that use the tensorial dimensions on the resolution. 
They are useful for multi-regional (PDE, Network) and multi-agent/multi-sectoral models. You can create your own or use those. 

```python
chm.get_available_operators()
```

## Hub 

The `Hub` class is a central object for the user, providing an interface to interact with a given model.
Given a model name, the `Hub` class loads the model file and retrieves its logics, presets, and associated values. 
It performs tasks such as :
* executing local models coupling operation in the `_model_MODELNAME.py` file, 
* identifying parameters, state variables, and differential variables, 
* finding their associated properties (definitions, units, values...), 
* determining an order of calculation.

Users can: 
* access fields for value modification, 
* the structure and properties in the model, 
* perform simulations, 
* Create plots
* conduct deeper analysis
* save the model


A `hub` has many introspection methods that return formatted data that can be called as `hub.get_[...]`


Here is the resume of everything in this tutorial

In most situations, the `get_summary()` method should cover your needs. 
It covers the flags of the system, their preset names, and fields by category with their attributes. As we will see after, get_summary displays the last value of the simulation when a run has been done.
```
hub=chm.Hub('modelname')      # CHIMES object that you can use to interact with a model
hub.get_summary()             # Basic General informations
hub.get_fieldsproperties()    # dataframe description of fields
hub.get_Network()             # network visualisation of the model
hub.get_presets()             # display a table of the presets
hub.get_supplements()         # display a table of the supplements
hub.get_dfields()             # dictionnary of all fields properties
hub.dfields_as_reverse_dict() # classified by eqtypes
hub.get_dvalues()             # dictionnary of time evolving values after a run
hub.dataframe()               # fields values as multi-index dataframe
hub.get_dimensions()          # return the fields that change tensor dimensions  
hub.get_multisectoral()       # return fields classed by their tensor dimensions 
hub.dflags                    # status of the model
hub.dfunc_order               # order of the functions resolution
hub.dmisc                     # miscelaneous information
hub.dmodel                    # What is read from the model file
```


Depending on your level, we recommend the following: 

* **users** should know `hub=chm.Hub('modelname')`, `hub.get_summary()`, `hub.plot()`, `hub.set_fields()` (basic use), `hub.dvalues()`
* **advanced user** should know `hub.get_Network() `, `hub.get_fieldsproperties()`, `hub.get_preset()`, `hub.set_fields()` (advanced use), `hub.dfields()`
* **modeller** should know `hub.get_supplements`, `hub.dflags`, `hub.dfunc_order`, 
* **power-user** should know `hub.dmodel`

#### Summary

```python
hub.get_summary()
```

Gives you a text version of everything in the model. Here is an example of the model ["Lorenz Attractor"](https://github.com/DaluS/CHIMES/blob/devel/models/EXAMPLES/_model_Lorenz_Attractor.py)

```
############################################################
####################      SUMMARY       ####################
############################################################
Model       : Lorenz_Attractor
Lorenz Chaotic Attractor: Butterfly effect!
File        : c:\Users\Paul Valcke\Documents\GitHub\CHIMES\tests\..\models\EXAMPLES\_model_Lorenz_Attractor.py
#################### Fields ####################
statevar        002 ['distance1', 'distance2']
differential    004 ['x', 'y', 'z', 'time']
parameters      004 ['lor_sigma', 'lor_rho', 'lor_beta', 'Nprod']
#################### Presets ####################
     Canonical example  : Chaotic attractor around two equilibrium, for those parameter values
          BeginEQ1      : Begins at the first equilibrium
#################### Flags ####################
run            : [0, 0]
cycles         : False
sensitivity    : False
derivative     : False
convergence    : False
multisectoral  : False
multiregional  : False
Parrallel      : False
reinterpolated : False
#################### Time vector ####################
Tsim                100                 Total simulated time
Tini                0                   Initial time for simulations
dt                  0.1                 solver timestep
nt                  1000                Number of timestep
#################### Dimensions ####################
nx                  1                   Number of system in parrallel
nr                  1                   Number of regions interconnected
Nprod               1                   Name of productive sectors


############################################################
####################       fields       ####################
############################################################
 
Model param.   sector         value          units          group          definition     
-------------  -------------  -------------  -------------  -------------  -------------  
lor_sigma                     10.000                                       Prandtl number 
lor_rho                       28.000                                       Rayleigh number
lor_beta                      2.667                                        Geometric factor

differential  sector  source                  initial    units  definition                        comment                Auxilliary
------------  ------  ----------------------  -------    -----  --------------------------------  ---------------------  ----------
x                     lor_sigma * (y - x),    0.200             rate of convection                reduced-form dynamics  False     
y                     x * (lor_rho - z) - y,  0.130             horizontal temperature variation  reduced-form dynamics  False     
z                     x * y - lor_beta * z,   0.210             vertical temperature variation    reduced-form dynamics  False     
time                  1.,                     0.000      y      Time vector                       dt/dt=1, time as ODE   True      

statevar   sector  source                                                                                                      initial    units      definition  comment                        Auxilliary
---------  ------  ----------------------------------------------------------------------------------------------------------  -------    ---------  ----------  -----------------------------  ----------
distance1          np.sqrt((x-np.sqrt(lor_beta*(lor_rho-1)))**2 + (y-np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2),  29.260     undefined              distance to the equilibrium 1  True      
distance2          np.sqrt((x+np.sqrt(lor_beta*(lor_rho-1)))**2 + (y+np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2),  29.451     undefined              distance to the equilibrium 2  True      
==============================
```

#### Field properties

`hub.get_fieldproperties` also allows you to create a data frame version and search the system when using tables. 

```python
hub.get_fieldsproperties()
```

#### Field properties, as a network

As we said, a model is a web of fields linked by equations. We can thus represent it as such and interact with it. 
The `get_Network()` method allows the customization of the representation.

You can hover over each nodes to get more information about its properties and dependencies. 

```python
hub.get_Network(auxilliary=True)
```

Will for example, give: 
![image](https://github.com/DaluS/CHIMES/assets/11523050/ee749fd6-86ad-4225-afe0-f1e308532c4a)

#### See the presets and supplements

Presets are a set of values for the system given by the model author that allows one specific run and the display of a specific system behaviour (quantitative or qualitative). They are often associated with one series of plots that show it. They can be loaded into the hub using `set_preset(presetname)`. To see the presets, use `hub.get_preset`, or read `hub.get_summary()` or even `chm.get_model_documentation`

Supplements are functions that ease the use of a specific model and thus are associated with it, either for the analyses, setting fields, or plots. They can be accessed using `hub.get_supplements` or `get_model_documentation`. They can be then used with `hub.supplements[supplementname](arguments_of_the_function)`

```python
presets = hub.get_presets('list') # Return a list of the presets
print('preset list',presets)
dpresets = hub.get_presets('dict') # Return a dictionary of the presets with theirdescription
print('preset_dict',dpresets)
hub.get_presets() # display a table of the presets
```

```python
lsupp = hub.get_supplements('list') # Return a list of the supplements
print('preset list',presets)
dsupp = hub.get_supplements('dict') # Return a dictionary of the supplements
print('preset dictionnary',presets)
hub.get_supplements() # display a table of the supplements
```

### dfields

dfields is where all the fields properties of the model, digested by the hub, are located. It is a dictionnary of a dictionnary architecture: the first level of dfields is fields names, then their attributes, such as their value, definition and so on. 

the keys are: 
* `eqtype` type of equation ['differential', 'statevar', 'None']
* `func` the python logic that is used to calculate the value
* `source_exp` A string version of the solved equation
* `com` a comment explaining the python function
* `definition` the definition of the field
* `units` the unit of the field ( years, humans, meters...) in latex formalism
* `symbol` a latex symbol that represent the field
* `group` a classification that helps looking
* `value` a numpy tensor that keep all values (see the corresponding section) 
* `isneeded` Is the field required to calculate the dynamics
* `size` a list of two field that are used to know the multisectoral size of this one
* `multisect` a flag that tell if the field need all its dimensions
* `kargs`  
* `args`  
* `minmax` 

When a new analysis is done with the hub, a new category will appear for each fields in `dfields`. 
We recommend building your own tools (plot, analyses, etc) with dfields as the input, you'll have everything you need !

```python
R = hub.get_dfields()
print('the available fields are :',R.keys())
x = R['x']
print('the keys of the field x are :',x.keys())
```
```
the available fields are : dict_keys(['x', 'y', 'z', 'distance1', 'distance2', 'lor_sigma', 'lor_rho', 'lor_beta', 'Tsim', 'Tini', 'dt', 'nx', 'nr', 'Nprod', '__ONE__', 'time', 'nt'])
the keys of the field x are : dict_keys(['func', 'com', 'definition', 'units', 'initial', 'eqtype', 'size', 'value', 'minmax', 'symbol', 'group', 'multisect', 'kargs', 'args', 'source_exp', 'isneeded'])
```

you can filter `get_dfields` to get only the fields corresponding to your criteria. 

```python
Rdiff = hub.get_dfields(eqtype=['differential']) # You only get differential equations
print('Eqtype differential',Rdiff.keys())
Rdiff2 = hub.get_dfields(eqtype='statevar') # You get state variables
print('Eqtype differential',Rdiff2.keys())
```
```
Eqtype differential dict_keys(['x', 'y', 'z', 'time'])
Eqtype differential dict_keys(['distance1', 'distance2'])
```

#### Getting fields according to criteria

It can be useful to have directly a field classification: `get_dfields_as_reverse_dict` is doing so. use `crit` to choose the classification type, and you can add criteria after
```python
Rclas =hub.get_dfields_as_reverse_dict(   # Return a dictionnary with the list of outputs for each input
                                   crit='units', # classified by units
                                   eqtype=['differential', 'statevar'] # only eqtype differential and statevar are kept
                                    ) # only eqtype differential and statevar are kept
for k in Rclas.keys():
    print(k,Rclas[k].keys())
```
```
 dict_keys(['x', 'y', 'z'])
y dict_keys(['time'])
undefined dict_keys(['distance1', 'distance2'])
```

another example
```python
Rclas = hub.get_dfields_as_reverse_dict(crit='eqtype') # classified by eqtypes
for k in Rclas.keys():
    print(k,Rclas[k].keys())
```
```
differential dict_keys(['x', 'y', 'z', 'time'])
size dict_keys(['nx', 'nr', 'Nprod'])
None dict_keys(['lor_sigma', 'lor_rho', 'lor_beta', 'Tsim', 'Tini', 'dt', '__ONE__'])
statevar dict_keys(['distance1', 'distance2'])
parameter dict_keys(['nt'])
```

#### Multi-region, Multi-agent, Multi-sector dimensions 

When you deal with multiple regions, coupling between dimensions, and multiple agents, you need to see which fields have different tensorial dimensions:
* `hub.get_dimensions()`  Give the different dimensions used in the model 
* `hub.get_multisectoral()` Give the dimensions of each field

```python
hub.get_dimensions()
```
|       | definition                       |   size | named list   | Impact in the model                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:------|:---------------------------------|-------:|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Nprod | Name of productive sectors       |      1 | ['MONO']     | ['D', 'V', 'K', 'p', [...], 'Cpond'] |
| nx    | Number of system in parrallel    |      1 | ['']         | All fields                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| nr    | Number of regions interconnected |      1 | ['']         | All fields                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

```
hub.get_multisectoral()
```

#### Getting values in most cases

You can get a dictionary of values with `dvalue` if you do not need the multisectoral properties. 
If you have multiple regions of a parallel system you can slice only the one you want with `nx = index, region = index`

```python
values = hub.get_dvalues(idx=0,         # By default idx=0
                         Region=0,      # By default region=0
                         params=False   # If True, return parameters too, otherwise only time evolving quantities
                         )
print('type',type(values))
for k,v in values.items():
    print(k,np.shape(v))
```

##### Dataframe approach

You can also access the values as a dataframe, that reshapes the dfields structure.
```python
hub.get_dataframe().transpose()
```

#### Decorators

Those variables are not shaped for user readability but can still be accessed. Those are protected and thus cannot be modified directly. 
You can modify the element by adding _ before its name if you know what you're doing

```python
hub.dflags # status of the model
```
Will typically have as output 
```
{'run': [0, 0],
 'cycles': False,
 'sensitivity': False,
 'derivative': False,
 'convergence': False,
 'multisectoral': True,
 'multiregional': False,
 'Parrallel': False,
 'reinterpolated': False}
```

other to consider are
```python
hub.dfunc_order # all the order of variable resolutions
hub.dmisc # miscelaneous information
hub.dmodel # What is read from the model file
```

