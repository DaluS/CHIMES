# Model: _EXTERNALCOUPLING


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []


CHIMES can be coupled with external structures and models, with a simple API. THis is an example

Here we create the API inside the model file, eventually they can be imported separately.
The class structure can be used for various models later.

The class has te following elements: 
1. Flags 
2. a `get_var` method that if required will do a timestep of the external model and give the output
3. a `set_var` that can send information to the external module
4. a `_TrueInit` that will initialize the external model and run it until it's ready for the rest of the system 
5. a `_simulate` that will do internal calculations to the module

To call the class in a CHIMES model, one add a function with the same structure as giveINPUT_getOUTPUT
The sizes nr,nt,nx do not have to be sent in each function, only in the first one that will be executed as they are required for the initialisation.


## Presets
|         | Description   |
|:--------|:--------------|
| preset0 |               |
## Supplements
|                 | documentation   | signature   |
|:----------------|:----------------|:------------|
| access_External |                 | (_EXTERNAL) |
## Todo

## Equations
|           | eqtype       | definition             | source_exp               | com   |
|:----------|:-------------|:-----------------------|:-------------------------|:------|
| Stock     | differential |                        | dStock/dt=Flow,          |       |
| LocalCalc | statevar     |                        | LocalCalc={'LocalCalc'   |       |
| Flow      | statevar     |                        | Flow=giveINPUT_getOUTPUT |       |
| g         |              | Relative growth of GDP |                          |       |