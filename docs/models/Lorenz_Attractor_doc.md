# Model: Lorenz_Attractor


* **Creation** :  2023/08/21
* **Coder**    : Paul Valcke
* **Article**  : https://en.wikipedia.org/wiki/Lorenz_system
* **Keywords** : ['stochastic', 'Documentation', 'chaos', 'attractor']


Solving the famous 3-coupled ordinary differential system. Canonical case has the two equilibrium with the strange attraction

## What is this model ?

Developed to study properties of a simplified model of atmospheric convection.
The model is a system of three ordinary differential equations. Parameters are linked to hydrodynamics properties of the atmosphere.

## Why is it interesting ? 

Chaos ! The system when solved numerically around certain values is highly sensitive to initial conditions. 
This is the butterfly effect. The system is also a canonical example of a strange attractor: two equilibrium, both unstable. 
The system will oscillate around one, then switch to the other one, staying in a bounded area of the phase space.

The condition to jump from one to the other are very peculiar, in consequence each bifurcation is an event difficult to predict and that impacts deeplt
the system.

As written on the wikipedia page:
The Lorenz equations can arise in simplified models for:
* lasers
* dynamos
* thermosyphons
* brushless DC motors
* electric circuits
* chemical reactions
* forward osmosis
* The Lorenz equations also arise in simplified models for the behaviour of convection rolls

## what is the purpose of your model

It is a good illustration of a complex system, unexpected behavior and emergent properties.


## Presets
|                   | Description                                                          |
|:------------------|:---------------------------------------------------------------------|
| Canonical example | Chaotic attractor around two equilibrium, for those parameter values |
| BeginEQ1          | Begins at the first equilibrium                                      |
## Supplements
|                            | documentation                                                                                        | signature   |
|:---------------------------|:-----------------------------------------------------------------------------------------------------|:------------|
| OneTenthPercentUncertainty | Run the canonical example with 1% uncertainty on initial conditions and display it in an nyaxis plot | (hub)       |
## Todo

## Equations
|           | eqtype       | definition                       | source_exp                                                                                                           | com                           |
|:----------|:-------------|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------|:------------------------------|
| x         | differential | rate of convection               | dx/dt=lor_sigma * (y - x),                                                                                           | reduced-form dynamics         |
| y         | differential | horizontal temperature variation | dy/dt=x * (lor_rho - z) - y,                                                                                         | reduced-form dynamics         |
| z         | differential | vertical temperature variation   | dz/dt=x * y - lor_beta * z,                                                                                          | reduced-form dynamics         |
| distance1 | statevar     |                                  | distance1=np.sqrt((x-np.sqrt(lor_beta*(lor_rho-1)))**2 + (y-np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2), | distance to the equilibrium 1 |
| distance2 | statevar     |                                  | distance2=np.sqrt((x+np.sqrt(lor_beta*(lor_rho-1)))**2 + (y+np.sqrt(lor_beta*(lor_rho-1)))**2 + (z-(lor_rho-1))**2), | distance to the equilibrium 2 |
| lor_sigma |              | Prandtl number                   |                                                                                                                      |                               |
| lor_rho   |              | Rayleigh number                  |                                                                                                                      |                               |
| lor_beta  |              | Geometric factor                 |                                                                                                                      |                               |