# Model: Attractor1D


* **Creation** :  2023/12/14
* **Coder**    : Paul Valcke
* **Article**  : 
* **Keywords** : ['stochastic', 'Documentation', '']


# Tipping point in an independant landscape: 1D with no position feedback


## What is this model ?
A particle of position `x` in a potential `V(x)`.
Its acceleration is due to potential and a brownian motion.

The potential has to equilibrium position `x_1` and `x_2` with different potential values.
There is barrier between them which is the maximum of the potential between `x_1` an `x_2`.

## What is the expected behavior ?
The particle remain trapped around an equilibrium position.
If noise is too small, the particle remains in its local basin.
A fluctuation big enough will make it move from one side to the other.
At small temporal scale the system oscillate with noise around one attractor.
At large temporal scale the system oscillate from one equilibrium to the other.

## Why is it interesting ?

[Blablabla]


## Presets

## Supplements

## Todo
* implement presets
* implement equilibrium position
* add interest and theory
* implement visualisations

## Equations
|      | eqtype       | definition                        | source_exp                             | com   |
|:-----|:-------------|:----------------------------------|:---------------------------------------|:------|
| v    | differential |                                   | dv/dt=a,                               |       |
| x    | differential |                                   | dx/dt=v,                               |       |
| a    | statevar     | Productivity                      | a=lambda T, nx, x, v1, v2, v3, v, damp |       |
| T    |              | temperature anomaly of atmosphere |                                        |       |
| v1   |              |                                   |                                        |       |
| v2   |              |                                   |                                        |       |
| v3   |              |                                   |                                        |       |
| damp |              |                                   |                                        |       |