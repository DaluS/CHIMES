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



