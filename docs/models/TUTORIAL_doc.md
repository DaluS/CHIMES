# Model: TUTORIAL


* **Creation** :  YYYY/MM/DD model file creation
* **Coder**    :  Name of the coder
* **Article**  :  a link to the published article if existing
* **Keywords** : ['a list of relevant elements for classification', 'Documentation', 'Tutorial']

A longer description in markdown format that explains: 
## What is this model ?
## Why is it interesting ? 
## what is the purpose of your model,
## Expected behavior
how it is constructed, and its expected behavior.


## Presets
|         | Description        |
|:--------|:-------------------|
| preset0 | change p and delta |
## Supplements
|                      | documentation                                         | signature          |
|:---------------------|:------------------------------------------------------|:-------------------|
| MethodForSupplements | This method can be accessible through hub.supplements | (var)              |
| plogics              |                                                       | (p=0, inflation=0) |
## Todo
* a list of tasks
* that should be done

## Equations
|           | eqtype       | definition                               | source_exp             | com              |
|:----------|:-------------|:-----------------------------------------|:-----------------------|:-----------------|
| p         | differential | nominal value per physical unit produced | dp/dt=p*inflation,     | inflation driven |
| K         | differential | Capital in real units                    | dK/dt=0.1*K - delta*K, |                  |
| N         | differential | Population of people able to work        | dN/dt=pop              |                  |
| a         | differential | Productivity                             | da/dt=progress         |                  |
| w0        | statevar     | wage indicator                           | w0=np.exp(p/a)*para,   |                  |
| delta     |              | Rate of capital depletion                |                        |                  |
| para      |              |                                          |                        |                  |
| inflation |              | inflation rate                           |                        |                  |
| n         |              | Rate of population growth                |                        |                  |
| alpha     |              | Rate of productivity increase            |                        |                  |