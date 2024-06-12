# Model: Goodwin_example


    * **Creation** : 2023/11/17
    * **Coder**    : Paul Valcke
    * **Article**  : https://link.springer.com/chapter/10.1007/978-1-349-05504-3_12
    * **Keywords** : ['Tutorial', 'Documentation', 'Goodwin', 'Economics', 'Oscillations', 'Monosectoral']
    

## What is this model ?
A Goodwin is a two-sector model of an economy : household and firms. 
The growth is endogenous, but eventually driven by technical automatization and population growth
It share many points with a Solow and and Ramsay model of growth. 
The main difference is that this model is able to explore out of equilibrium without exploding.
To do so, the wages (and thus consumption) is driven by a long causal chain: a short-run Phillips curve.
The higher the employment, the faster wages grows. 

## Expected behavior
* When looking at the causal variables (K,w) it looks like an exponential with oscillations.
* When looking at the dimensionless state variables (employment,wage share "omega"), it is just sustaining oscillations.
* The further from the equilibrium, the bigger and slower the oscillations
* The dimensionless oscillations should not grow or shrink

## Why is it interesting ? 
The Goodwin model has been over the years an excellent platform for more complex models, as it can be:
* Stock-flow consistent both physically and nominally
* Have inventory and debt fluctuations
* Naturally englobe business cycles
* Work out of equilibrium 
* Add sectors, be disaggregated... 
* Any endogenization effect can be easily read as it either stabilize, destabilize, change the cycles and equilibrium point
* None of the hypothesis is central and they can all be changed

## The predatory-prey aspect
One can study the "reduced" form of the system, rewriting the equations with the derivatives on employment and wage share is 
giving a system of 2 equations, similar to a Lotka-Volterra system in population dynamics, also called "predatory-prey".
In consequence, a part of the community assumed that some where the predators (capital) and prey (workers), giving the model 
a "class struggle" political coloration and making it overlooked by many. 
A Lotka-Volterra system is a non-linear oscillator that do not know what is his equilibrium. 

## What is different from the paper ?
We use a slightly different variable convention. There is a constant inflation, and productivity is here a/nu. 
a is used for labor efficiency (number of capital unit per worker)

## What is particular with this model file ? 
It has been written to have a full description inside the model file, and thus is not using the default library inside CHIMES. 
It is a good example to follow if you want to do something fully commented and fully independant.
You can check the file `_model_Goodwin.py` for the short version relying on the library




## Presets
|                    | Description                                                                                                    |
|:-------------------|:---------------------------------------------------------------------------------------------------------------|
| startatequilibrium | equilibrium is here when the employemnt and wage share are constant.                                           |
|                    |         On this case, we force the system to naturally start there. Only exponential growth should be observed |
| Farfromequilibrium | This run start far from the equilibrium point, and the will oscillate slowly                                   |
| Parrallel runs     | This run makes 10 system in parrallel, that do not interact.                                                   |
|                    |         The first is the "startatequilibrium and the last "Farfromequilibrium".                                |
|                    |         The one in the middle are linear combination of the two initial conditions.                            |
## Supplements
|                       | documentation                                                                                         | signature                |
|:----------------------|:------------------------------------------------------------------------------------------------------|:-------------------------|
| Equilibrium_fromparam | For a Goodwin model, will analytically find the equilibrium position                                  | (hub)                    |
| K_w_for_lambdaomega   | One might want to initiate its system at a certain value of employment(lambda) and wage share(omega). | (hub, employment, omega) |
|                       |     The system deduces the right value of K and w to ensure such characteristics                      |                          |
## Todo
* Write the equilibrium position in supplements

## Equations
|            | eqtype       | definition                                  | source_exp                            | com                               |
|:-----------|:-------------|:--------------------------------------------|:--------------------------------------|:----------------------------------|
| p          | differential | nominal value per physical unit produced    | dp/dt=p*inflation,                    | Consequence of causal inflation   |
| a          | differential | Automatisation level                        | da/dt=a*alpha,                        | exogenous                         |
| N          | differential | Worker pool                                 | dN/dt=N*n,                            | exogenous exponential             |
| K          | differential | Capital in real units                       | dK/dt=Ir-delta*K,                     | Investment - dpreciation dynamics |
| w          | differential | individual wage value                       | dw/dt=w*phillips,                     | short-run Phillips dynamics       |
| pi         | statevar     | relative profit                             | pi=Pi / (p*Y),                        | its definition                    |
| omega      | statevar     | wage share                                  | omega=w*L/(p*Y),                      | its definition                    |
| employment | statevar     | employment rate                             | employment=L/N,                       | its definition                    |
| g          | statevar     | Relative growth of GDP                      | g=Ir/K-delta,                         | manually calculated               |
| Y          | statevar     | GDP in real units                           | Y=K/nu,                               | Leontiev optimized on labor       |
| Pi         | statevar     | Absolute profit                             | Pi=p*Y-w*L,                           | definition without depreciation   |
| C          | statevar     | flux of goods for household                 | C=Y-Ir,                               | Consumption as full salary        |
| Ir         | statevar     | Number of real unit from investment         | Ir=Pi/p,                              | Profit reinvested                 |
| L          | statevar     | Workers                                     | L=K/a,                                | from automatisation definition    |
| phillips   | statevar     | Wage inflation rate                         | phillips=Phi0+Phi1/(1-employment)**2, | DIVERGING PHILLIPS CURVE          |
| inflation  |              | inflation rate                              |                                       |                                   |
| alpha      |              | Rate of productivity increase               |                                       |                                   |
| n          |              | Rate of population growth                   |                                       |                                   |
| delta      |              | Rate of capital depletion                   |                                       |                                   |
| nu         |              | Capital to output ratio                     |                                       |                                   |
| Phi0       |              | wage reduction rate when full unemployement |                                       |                                   |
| Phi1       |              | wage rate dependance to unemployement       |                                       |                                   |