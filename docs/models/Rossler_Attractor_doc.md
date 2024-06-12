# Model: Rossler_Attractor


    * **Creation** :  2024/04/23
    * **Coder**    : Paul Valcke
    * **Article**  : https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor
    * **Keywords** : ['stochastic', 'Documentation', 'chaos', 'attractor']
    

3 Differential attractor. One equilibrium point

$$\dfrac{\partial x}{\partial t} = -y - z$$
$$\dfrac{\partial y}{\partial t} = x+ay$$
$$\dfrac{\partial z}{\partial t} = b + z(x-c) $$


## What is this model ?

A 3 Dimensional attractor, that can exhibit chaotic behavior. 
It is mostly a 2D unstable oscillator on the XY plane, that extend to 3D at large scale, then go back to the equilibrium point

## Why is it interesting ?

## what is the purpose of your model

It is a good illustration of a complex system, unexpected behavior and emergent properties.


## Presets
|       | Description    |
|:------|:---------------|
| plots | Just the plots |
## Supplements

## Todo

## Equations
|       | eqtype       | definition             | source_exp               | com   |
|:------|:-------------|:-----------------------|:-------------------------|:------|
| x     | differential |                        | dx/dt=-y-z,              |       |
| y     | differential |                        | dy/dt=x+ros_a*y,         |       |
| z     | differential | local wage ponderation | dz/dt=ros_b+z*(x-ros_c), |       |
| ros_a |              |                        |                          |       |
| ros_b |              |                        |                          |       |
| ros_c |              |                        |                          |       |