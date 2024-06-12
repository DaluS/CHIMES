If you made it here, congrats! You're ready to create your own models with CHIMES. 

# What is a model file ?

Model files are:
* python files
* are located in a folder of `models` 
* with a name like `_model_NAMEOFYOURMODEL.py` 
* They need to contain a dictonnary called `_LOGICS` 

Once those ingredients are here, CHIMES will do as best as it can to transform it into a model. 

**The best method is to look at model files** Typically in `models/EXAMPLES`, they are voluntarily written with multiple approaches. Typically, copy-paste `_model___TEMPLATE_.py` to write your own ! You'll have everything there.

*Why using python file to declare a model ?* That way, it is easy to interact with the model, loading other models, data, write weird functions...

As long as `_LOGICS` is there, you can do your own things inside! In consequence, your model your style. 

Note that there are two method to declare dictionnary in python :
*  d = dict( key1 = value1,...)
*  d = {'key1':'value1',...}
Both are equivalent, choose the one you prefer but be consistent


## _LOGICS

_LOGICS is the core of the model file, and what CHIMES Will interpret deeply. You do not need to detail everything inside (initial values, definition, units, symbol) if it's done somewhere else and accessible !

### Categories
`_LOGICS` is a dictionnary, that will contains all the logics (equations) of the model. Reading it will allow CHIMES to know what quantities (fields) are needed, as well as their characteristics. It will link a field (key) to a logic or a value
`_LOGICS` is divided into categories, typically :
* **differential** : the time variation of the field is defined by a logic (the variation of a stock is defined by its flows)
* **statevar** : the value of the field is defined by a logic ( what you possess is the sum of your different stock values)
* **parameters** : the value of the field has no logics, is exogenous to the system
* **size** : special quantities that defines certain dimensions (advanced use only)
Any other key will be overlooked (or if mispelled, corrected)

```
_LOGICS = {
    'diferential : {[...]},
    'statevar' : {[...]},
    'parameter' : {[...]},
    'size' : {[...]},
}
```

### Filling the category

for each category [differential, statevar, parameter, size], you can now fill it with fields (Capital, Temperature, price, employment, speed...), and associate it with a function and more. For short functions, you can juste use `lambda` python functions (that are short to write !), or a function defined somewhere else ! 


For example, if you have $\dot{K}=I - \delta K$, you can do:

#### Only giving the equation
``` 
differential = dict( 
    [...]
    K = lambda K,delta,I : I - delta*K, 
    [...]
```

or 
```
def dotKeq( K,delta,I):
    Kplus = I
    Kmoins = deltaK
    return Kplus-Kmoins

[...]    
differential = dict( 
    [...]
    K = dotKeq, 
    [...]
'''

Same logic will apply for statevariable, and for parameters if you associate the value

```
_LOGICS = dict(
    differential = {'K': dotKeq},
    statevar = {'I': lambda time: np.exp(0.05*time)},
    parameter = {'delta':0.1}
)
'''

#### Adding more information

If you want to add more informations to the model, you can associate the field to a dictionnary, and add the following keys: 
* a logic (if it is a state variable or a differential variable) called `func`
* a comment on how it is calculated (if it is a state variable or a differential variable) called `com` : is it the application of a definition, the differential logic of the reduced system, the consequence of a stock-flow consistency ? Is it exogenous ? 
* an initial value per default `initial` if its a differential equation
* a value (it its a parameter) called `value`
* a definition called `definition` : what this field represent ? 
* a unit system called `units` : is it a time, the inverse of a time, a money quantity ? The existing units are : [ ]
* a symbol called `symbol` : a latex writing if you want something fancy for your plots 
* a size if your system is a multisectoral/agent based one (multiple entities with the same logic in the system, that can interact with each others), as `size`. 
* if your field is in `size` and you want the index to have labels, you can put them with `list` ( example : `_LOGICS = {'size': {'Nprod': {'list':['firstsector','secondsector'],[...]},[...]},[...]}`)

``` 
differential = dict( 
    [...]
    K = dict( func = lambda K,delta,I : I - delta*K, 
              com = 'sum of the investment and degradation,
              symbol = r'$\mathcal{K}$'
    [...]
```

### Priority management of information
 
A model does not have to give all informations as most of them might be redundant: the definition of capital should not change between models for a better compatibility. 
`
If you do not give an information in the model file, then the system is going to look what exist in the `_def_fields()` file that you can access by `chm.get_available_fields()`

## What else can be in a model file ? 

By default, the system will look for the following entries. If they do not exist, it will invent them. 
* a docstring on top of the file, typically a one-liner as a short description
* a long str called `_DESCRIPTION` that explains everything 
* a list of string `_TODO` that describe what should be done on this model  
* a string `_ARTICLE` with a link to an academic article (or a wikipedia page) about the model
* a string `_DATE` in YYYY/MM/DD of when the file has been created 
* a string `_CODER` with the names of people who coded the model
* a list of strings `_KEYWORDS` to classify models  

Two additional elemments will be explored: 
* `_SUPPLEMENTS` , a dictionnary { 'functioname', function } trhat you want the user to access
* `_PRESETS`, a dictionnary of dictionnary that contains sets of initial conditions/parameters as well as plot to demonstrate certain behaviors of the model

### How to write a preset ? 

First you give a name to the preset, that you can load by calling it. It opens a dictionnary, in which you gives :
* a short comment about what it does
* a dictionnary with all the values you want to change
* a dictionnary of plots you want to associate with it

It looks like this :
```
_PRESET = dict(
    nameofpreset1 = dict( 
        com = 'A short description of the behavior',
        fields = dict( 
            differential1 = value1, # You can assign values here
            [...]
            parameter1 = value3 
            [...] # If you do not put a value to a field, it keep the previous one
        ),
        plots = dict( 
            plotname1 = [{ plots arguments1}, # arguments are given by the plot description `chm.get_plot_documentation(plotname)`
                         { plots arguments2}], # You can do multiple plots of the same type by putting them in a list
            plotname2 = [...]
        )
    ),
    nameofpreset2 = [...]
)
```

## Models interactions 

You can load a model inside another model ! To do so, use : 
```
from chimes._models import importmodel      
_LOGICS, _PRESETS0, _SUPPLEMENTS_GK = importmodel('GK') # Get access to the different elements
```

From this, you can simply do changes on _LOGICS directly, or define another _LOGICS dictionnary with a different name, and merge both
```
 _LOGICS = merge_model(_LOGICS, logicsgoodwin, verb=False)     # Takes the equations of _LOGICS_GOODWIN and put them into _LOGICS
```

## Remarks 

* since CHIMES use tensors behind the hood, make sure to use broadcasted operators in your functions: replace np.min by np.minimum for example !
* you cannot define a field by a name that is a python keywork ( dict,list, lambda, def ) as you could not call it in a function

## Creating multisectoral models 

To extend the dimensionality of a variable (beyond parrallel and region): 
* You can add a 


