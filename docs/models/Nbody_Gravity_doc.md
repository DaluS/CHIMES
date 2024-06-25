# Model: Nbody_Gravity


* **Creation** : 2024/06/13
* **Coder**    : Paul Valcke
* **Article**  : https://en.wikipedia.org/wiki/N-body_problem
* **Keywords** : ['Nbody', 'physics', 'chaos']
    

## What is this model?

A Spring Network is an ensemble of nodes that are linked by springs. Springs, depending on their compression, will apply forces on the nodes they connect. 
These forces will then move the nodes, which changes the spring tensions. This model is a classic example of local wave propagation on a network structure.

## How can it be represented with vectors and matrices?

Each element $i$ is a node of mass $m_i$ at position $(x_i, y_i)$ and velocity $(v^x_i, v^y_i)$.

They are in a gravity field $G$

In consequence, the forces are:

$$a^x_i = \sum_j G  m_j r_{ij}^{-2} \cos(\theta_{ij}) - \eta_i v^x_i$$
$$a^y_i = \sum_j G  m_j r_{ij}^{-2} \sin(\theta_{ij}) - \eta_i v^y_i $$
$$\dot{v}^x_i = a^x_i$$
$$\dot{v}^y_i = a^y_i$$
$$\dot{x}^x_i = v^x_i$$
$$\dot{x}^y_i = v^y_i$$

with :

$$r_{ij}^{-2} = ((x_i - x_j )^2 + (y_i - y_j ))^{-1}$$

We suppose that $G=1$ in this calculation

## Why is it a great archetypal model?

The N-body gravity dynamics model is essential for simulating the behavior of celestial bodies under gravitational influence. 
It provides insights into complex systems such as planetary orbits, galaxy formations, and stellar interactions. 
This model serves as a foundational tool in astrophysics, cosmology, and computational physics for understanding the dynamics of gravitational interactions at various scales.


## Presets
|                | Description   |
|:---------------|:--------------|
| OneOscillation |               |
## Supplements
|                 | documentation                                               | signature              |
|:----------------|:------------------------------------------------------------|:-----------------------|
| plot_invariants | Plot the invariants of the spring network system over time. | (hub, returnFig=False) |
## Todo
*  

## Equations
|           | eqtype       | definition                   | source_exp                                                                   | com   |
|:----------|:-------------|:-----------------------------|:-----------------------------------------------------------------------------|:------|
| Nbody     | size         | Number of interacting bodies |                                                                              |       |
| vx        | differential | horizontal velocity          | dvx/dt=Fx/m,                                                                 |       |
| vy        | differential | vertical velocity            | dvy/dt=Fy/m,                                                                 |       |
| x         | differential | horizontal position          | dx/dt=vx,                                                                    |       |
| y         | differential | vertical position            | dy/dt=vy,                                                                    |       |
| dx        | statevar     |                              | dx=x - np.moveaxis(x, -1, -2)),                                              |       |
| dy        | statevar     |                              | dy=y - np.moveaxis(y, -1, -2)),                                              |       |
| heavi     | statevar     |                              | heavi=np.heaviside(distance-0.01, 0),                                        |       |
| distance  | statevar     |                              | distance=(dx**2 + 0.000001 + dy**2)**(1/2)),                                 |       |
| rm2       | statevar     |                              | rm2=np.heaviside(distance-0.01, 0) * distance**(-2)),                        |       |
| angle     | statevar     |                              | angle=np.arctan2(dy, dx)),                                                   |       |
| Fx        | statevar     |                              | Fx=O.ssum2(-m*np.moveaxis(m, -1, -2)*rm2*np.cos(angle))),                    |       |
| Fy        | statevar     |                              | Fy=O.ssum2(-m*np.moveaxis(m, -1, -2)*rm2*np.sin(angle))),                    |       |
| Kinetic   | statevar     |                              | Kinetic=0.5*np.sum(O.ssum(m*(vx**2 + vy**2))), axis=-2),                     |       |
| Potential | statevar     |                              | Potential=0.25*np.sum(np.sum(-m*np.moveaxis(m, -1, -2)), axis=-1), axis=-2), |       |
| m         |              |                              |                                                                              |       |