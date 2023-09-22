# What is a model file ?

There are many ways to write a model in **CHIMES**, and one might fit your project better than other ones. You can explore different existing models (in the `models` folder of CHIMES) to take a look at your favorite. 

All files have the same common properties:
* models are in the folder `models`, in any subfolder
* model files are python files: you can do anything python authorize inside!
* models names have the nomenclature `_model_{modelname}.py`. They will not be read otherwise *example: `_model_mymodel.py`

The model file NEED to contains : 
* A docstring at the beginning (containing the short description of your model)
* A long docstring `_DESCRIPTION` that can be written in Markdown 
* A dictionary called `_LOGICS` with a specific shape (see next part)
* A dictionnary called `_PRESETS` with a specific shape 

The model file CAN contains : 
* An ensemble of supplementary tools to transmit with `_SUPPLEMENTS`, in a dictionnary. Typically an ensemble of functions one might want to call to study the model (plots, initialisations methods, advanced analyses... )
* New units specific to your model in `_UNITS` 

We recommend the exploration of `models/_model__TEMPLATE__.py` for more informations. Do not modify it! But you can copy it (or `__MINITEMPLATE__`) then modify the copy to create your own


## The shape of `_LOGICS`

The model can contains : 
* differential variables
* state variables
* parameters 
* size of multisectoral shapes

The structure of `_LOGICS` will be : 
```
_LOGICS = {
    'diferential : {[...]},
    'statevar' : {[...]},
    'parameter' : {[...]},
    'size' : {[...]},
} # check there is not ',' at the end !
```
If you do not need one section, you can remove it ! a model with only differential will have : 
```
_LOGICS = {'diferential : {[...]},}
```

### How to define a field in a dictionnary 

To each "field" ( Capital, temperature, price, employment ) we can associate through a dictionnary : 
* a logic (if it is a state variable or a differential variable) called `func`
* a comment on how it is calculated (if it is a state variable or a differential variable) called `com` : is it the application of a definition, the differential logic of the reduced system, the consequence of a stock-flow consistency ? Is it exogenous ? 
* an initial value per default `initial` if its a differential equation
* a value (it its a parameter) called `value`
* a definition called `definition` : what this field represent ? 
* a unit system called `units` : is it a time, the inverse of a time, a money quantity ? The existing units are : [ ]
* a symbol called `symbol` : a latex writing if you want something fancy for your plots 
* a size if your system is a multisectoral/agent based one (multiple entities with the same logic in the system, that can interact with each others), as `size`. 
* if your field is in `size` and you want the index to have labels, you can put them with `list` ( example : `_LOGICS = {'size': {'Nprod': {'list':['firstsector','secondsector'],[...]},[...]},[...]}`)

That's a lot keys for each field, but you DO NOT need to write them every time ! The system will : 
* Try to find if the field is already defined somewhere, and if so will autofill with what he has found about it
* Fill the undefined keys with a default value (the symbol is the name, the comment is empty, the unit is `undefined`...) 

In consequence the field `K` defined as a differential variable $\dot{K} = I^r - \delta u K $ can be written as (I will explain the function later): 
```
'K': {
    'func': lambda Ir,delta,u,K: Ir-delta*u*K,
    'com': 'depreciation proportional to u',
    'definition': 'Productive capital in physical units',
    'units': 'units',
    'size': ['Nprod'],
    'initial': 2.7,
},
```
but also 
```
def dotK(Ir,delta,u,K):
    return Ir-delta*u*K

'K': {'func' : dotK},
```
And the system will do its best for the rest using informations in `pgm.get_available_fields()`. The more you give the better !
If some fields are needed but not specified, the system will try to find them on its own. For example in `delta` is never defined in any component of the `_LOGICS` of the model, he will look for it in the shared library `_def_fields`. 

### Priority management of information
 
A model does not have to give all informations as most of them might be redundant: the definition of capital should not change between models for a better compatibility. 

If you do not give an information in the model file, then the system is going to look what exist in the `_def_fields()` file that you can access by `chm.get_available_fields()`

### writing `func` the functions

Functions can be written two ways :
* classic functions defined somewhere else and called in `'func':`
* "lambda" (un-named function) 

`chimes` is going to READ the function and the names of what you call. So put the right names inside ! For example : `func': lambda Ir,delta,u,K: Ir-delta*u*K`, the system will look at the fields named `Ir`, `delta`, `u`, `K` to compute the value. 

* If your field is in `differential`, it is assumed that what you define is its time derivative (like in the previous example)
* If your field is in `statevar`, it is assumed that what you define is the value.

I recommend using mostly lambda functions, it is more compact, easier to read and the system has more ease with them. But if you want you can do : 

```
def dotK(Ir,delta,u,K): 
    Kplus = Ir
    Kminus = delta*u*K
    return Kplus-Kminus

_LOGICS = {
    [...]
    'differential' : {
         [...]
         'K' { 'func' : dotK,
               [...],
             },
         [...],
         },
    [...]
    }
```

This is practical if you need complex multiline functions, or to call an external model



### The presets

Presets are pre-defined set of fields values and plots that a user can load to explore the properties of the model. As often in chimes, it is a dictionnary of dictionnary : 
```
_PRESETS= {
    'presetname_1': {
        'fields': {[...]},
        'com' : '''description of the preset```
        'plots' : {[...]},
    'presetname_2' : {[...]},
    [...]
    },
```
you can put as many preset as you want

#### Fields in presets
writing the fields is straightforward : any value you want to be specified is given as the key with an associated value : 
```
    [...]
    'fields': {'k0':-1,
               'dt':0.01,
               'omega':0.75,
               [...]
               },
    [...]
```

There can be some numerical keys in the preset : 
* 'nx' number of system in parrallel
* 'nr' regions solved at the same time
* 'Tmax' time of the simulation
* 'dt' timestep 

`fields` work the same way as `hub.set_dparam` : you can put multiple value at once on parrallel systems and so on !


#### plots in preset 
 
for each preset you can define multiple plots easy to access by the user. To do so, check `pgm.get_available_plots` : they give you the list of plots name you can put in your `plots` as keys. 
The value is a list of dictionnary : 
    * a list because each element of the list will be a separate plot (you can use the same time of plots multiple time for a same preset
    * dictionnaries working as `kwargs` of the plot function : you put each time what you want to put in your plot function. 
    
Example : 
```
    [...]
    'fields': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'omega'],
                              ['d'],
                              ['kappa', 'pi'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':2},
                       {'x': 'time',
                        'y': [['K', 'Y', 'I', 'Pi'],
                              ['inflation', 'g'],
                              ],
                        'idx':0,
                        'log':[False,False],
                        'title':'',
                        'lw':1}],
            'XY': [{'x': 'employment',
                            'y': 'omega',
                            'color': 'd',
                            'idx': 0}],
            '3D': [{'x': 'employment',
                    'y': 'omega',
                    'z': 'd',
                    'color': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [{'title': '',
                         'lw': 2,       # optional
                         'idx': 0,      # optional
                         },  # optional
                        ],
        }
    [...]
```



### It's python language ! You can do wild things ! 

If your model is a fork (modification of) a previous model, you can import the logic of the previous model, and upgrade it. For example to go from a Goodwin to a Goodwin-Keen with inflation : 

More powerful functions are comming to do such thing (but can be found in `_model_CHIMES` as `Merge`
```
from chimes._models._model_Goodwin import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0) # security
_GK_LOGICS = {
    'differential': {
        # Stock-flow consistency
        'D': {
            'func': lambda I, Pi: I - Pi,
            'com': 'Debt as Investment-Profit difference', },

        # Price Dynamics
        'w': Funcs.Phillips.salaryfromPhillips,
        'p': {
            'func': lambda p,inflation : p*inflation,
            'initial':1,
            'units': '$.Units^{-1}',
            'com': 'inflation driven'
        }
    },

    # Intermediary relevant functions
    'statevar': {
        # Stock-flow consistency
        'Pi': {
            'func': lambda w, GDP, L, r, D: GDP - w * L - r * D,
            'com': 'Profit for production-Salary-debt func', },

        # Intermediary
        'kappa': Funcs.Kappa.exp,
        'inflation': Funcs.Inflation.markup,
        'I': Funcs.Kappa.ifromkappa,
        'd': Funcs.Definitions.d,

        # Growth manually coded
        'g': {
            'func': lambda Ir, K, delta: (Ir - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'parameter': {},
    'size': {},
}

# We add them explicitely
for category, dic in _GK_LOGICS.items():
    for k, v in dic.items():
        _LOGICS[category][k] = v
```

That way fields not modified from a Goodwin to a Goodwin-Keen do not have to be modified. Note that the consumption is not defined in the Goodwin file (nor here) so it does not have to be modified



### Calling an external module

Let's say you have a climate solver that gives you a temperature `T`, and that you can feed with emissions `E`, and you have a binding of your model `MODEL`

```
def TfromE(E,time): 
    ### Initialize your model
    if time==0:
        MODEL.start()
    ### If chimes is too much in advance in time, compute next iteration
    if time>MODEL['simulatedtime']:
        MODEL.run('Emissions'=E)
    T=MODEL.give('Temperature',time)
    return T   
```

Of course the binding needs to have `MODEL` correctly coded. 
As chimes use an RK-4 solver, `MODEL.give` must not necessary compute the iteration at each timestep (depends of your solver on the other side.