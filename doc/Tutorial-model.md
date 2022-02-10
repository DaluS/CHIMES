# Welcome in this tutorial on how to create a model !

There are many ways to write a model in **pygemmes**, and one might fit your project better than other ones.
As there are already some stuff coded, you should always have an eye on :
    * Existing models ( list can be obtained using `pgm.get_available_models` or in `_models\model_*.py`
    * Existing fields ( list can be obtained using `pgm.get_available_fields` or in `_models\_def_fields.py`
    * Existing functions ( list can be obtained using `pgm.get_available_functions` or in `_models\_def_functions.py`
That way you do not have to reinvent something that's already been added !

To explore the different approaches one can explore :
     1. `LorenzSystem` which contains all the basis (not using any external source)
     2. `G` as a Goodwin model using both the fields and functions library
     3. `G-CES` as an extension of `G` model

## How to read a model file
A model file is two big dictionnary :
    * `_LOGICS` that contains all the logics that links fields together
    * `_PRESETS` that contains typical values and plots for simulations. it
is a help for new users who wants to understand the typical properties of the model.

### `_LOGICS` Dictionnary
_LOGICS contains in itself 3 dictionnary :
    * ODE which contains all the fields which are defined by a differential equation
    * Statevar which contains all the fields which are defined by a state variables
    * param which contains all the fields which are not changing through time but are
 not defined in pygemmes's library (read `pgm.get_available_fields()` to check)

#### How to write a logic from scratch ?

for example, let's define an exogenous equation for productivity :

```
da/dt = a * (alpha + zouplala/proutprout)
```
1. we check if the fields do exist :
    * a exist
    * alpha exist
    * zouplala do not exist : I will have to add it
    * Proutprout do not exist either : We will have to add it also
2. It is a differential equation, so it goes inside ODE section.
    we write in ode a new key named 'a' , with a dictionnary as value
3. the dictionnary contains itself two fields :
    * 'func': the logics that link fields (see point 4 on how to write it)
    * 'com': a string to help user understanding the logic of equation
4. How to write a function ?
    * the recommended approach is a lambda function : It allow a better visualisation in get_summary and in the network.  If you do not want the function to be easily read (or your function is way too long), you can use a def: function outside
    * all the dependencies are explicit, and given a value that will not return an error (those value are just to check the integrity of the equation).
    * It looks like this : `lambda GDP=0, w=0, L=0: GDP - w * L`
    * If it is an ODE using its own value, please call it using "itself" instead
5. In consequence of last point of 4), 'a' will be written :
    * as a lambda :
       ```
       'ode': {
           [...]
           'a': { 'func': lambda itself=0, alpha=0, zouplala=0, proutprout=1 : itself*(alpha + zouplala/proutprout),
                       'com': 'exogenous productivity + two weird terms for pleasure'},
            [...]
            },
        ```
    * as a function :
        * define it above `_LOGICS`
        * for example you can do
        ``` def MyFunc_forA(itself=0, alpha=0, zouplala=0, proutprout=1 ):
                term1 = itself*alpha
                term2 = zouplala/proutprout
            return term1 + term2
        ```
        * And you use it as  :
        ```
        ode': {
           [...]
           'a': { 'func': MyFunc_forA,
                 'com': 'exogenous productivity + two weird terms for pleasure written as a big function'},
            [...]
            },
        ```
6. Now wou will have to define zouplala and proutprout our two new fields.
    We will say for the sake of it that `zouplala` is a parameter, `proutprout` a state variable
    * to write zouplala : we have to give him a value by default, and it's good practice to give
him a definition and an unit, for readability.
        ```
        'param': {
            [...]
            'zouplala': { 'value': 0.25 ,
                          'definition': 'a weird thing I introduced',
                          'units': '$',
                         },
            [...]
        },
        ```
    * we say for the sake of it that proutprout = w/a. we write it as :
        ```
        'statevar': {
            [...]
            'proutprout': {'func': lambda w=0,a=1: w/a,
                           'com': 'madeup expression',
                           'definition': 'a madeup term',
                           'units': '$^{-1}'},
            [...]
        },
        ```
   * if the field you introduce is dimensionless, then the unit is '',

    # DO IT AN EASIER WAY :
        If the logic already exist with the same dependency in `def_functions` do :
            `'a': Funcs.Productivity.exogenous,`

    # DO IT A VERY LAZY WAY :
        If you construct on top of a previous model, you can import all his logics.

        For example, we want to add a CES production function on a Goodwin Keen model.
        We first load the previous model

        ```
        from pygemmes._models._model_G import _LOGICS as _LOGICS0
        _LOGICS = deepcopy(_LOGICS0)
        ```

        Then we write a dictionnary only containing the different and new fields

        ```
        _CES_LOGICS = {
            'statevar': {
                # Characteristics of a CES
                'cesLcarac': Funcs.ProductionWorkers.cesLcarac,
                'cesYcarac': Funcs.ProductionWorkers.cesYcarac,
                'omegacarac': Funcs.ProductionWorkers.omegacarac,

                # From it are deduced optimised quantities
                'nu': Funcs.ProductionWorkers.CES_Optimised.nu,
                'l': Funcs.ProductionWorkers.CES_Optimised.l,

                # From it are deduced Labor and Output
                'Y': Funcs.ProductionWorkers.CES_Optimised.Y,
                'L': Funcs.ProductionWorkers.CES_Optimised.L,
            },
        }
        ```

        Then we overload the previous model with our new definitions

        ```
        # We add them explicitely
        for category, dic in _CES_LOGICS.items():
            for k, v in dic.items():
                _LOGICS[category][k] = v
        ```

    * If you change the category of hypothesis (from a statevar to an ODE for example),
    be sure you delete it in the previous section.
    * If you want to use the field lambda in a logic, call it `lamb` the system will understand !
