# Model: convection_diffusion_V2


* **Creation** : 2024/06/04
* **Coder**    : Paul Valcke
* **Article**  : https://en.wikipedia.org/wiki/Spring_system
* **Keywords** : ['Network', 'springs', 'mesh']
    
## What is this model?

A 2D Periodic Convection-Diffusion model describes the transport and diffusion of a scalar field (e.g., temperature, concentration) in a 2D plane with periodic boundary conditions. This model combines the effects of convection (transport by fluid flow) and diffusion (spreading due to concentration gradients), and is widely used to simulate processes in fluid dynamics, meteorology, and environmental science.

## How can it be represented with vectors and matrices?

In this model:
* The scalar field $C(x, y, t)$ evolves over time according to the convection-diffusion equation.
* The velocity field $ \mathbf{u}(x, y) = (u_x(x, y), u_y(x, y)) $ represents the fluid flow.
* The dynamics follow the convection-diffusion equation: 
$$
rac{\partial C}{\partial t} + \mathbf{u} \cdot 
abla C = D 
abla^2 C
$$
where $D$ is the diffusion coefficient.

The finite difference method is used to discretize the spatial domain into a grid of points:
* $X$ and $Y$ are 1D arrays representing the non-uniform grid points in the $x$ and $y$ directions.
* The gradient and Laplacian operators are represented by sparse matrices, allowing efficient computation of spatial derivatives.

### Gradient Operators:
The gradient operators $ 
abla_x $ and $ 
abla_y $ are constructed to compute the spatial derivatives:
$$

abla_x C pprox rac{C(x + \Delta x, y) - C(x, y)}{\Delta x}
$$
$$

abla_y C pprox rac{C(x, y + \Delta y) - C(x, y)}{\Delta y}
$$

### Laplacian Operator:
The Laplacian operator $ 
abla^2 $ is constructed as:
$$

abla^2 C pprox rac{C(x + \Delta x, y) - 2C(x, y) + C(x - \Delta x, y)}{\Delta x^2} + rac{C(x, y + \Delta y) - 2C(x, y) + C(x, y - \Delta y)}{\Delta y^2}
$$

## Why is it a great archetypal model?

The 2D Periodic Convection-Diffusion model is an excellent archetype for studying transport phenomena in fluid dynamics. It captures the essential physics of convection and diffusion, making it a versatile tool for understanding complex processes in natural and engineered systems. The periodic boundary conditions simplify the computational domain while preserving key dynamic behaviors.

## What are the different functions in supplements?

### generate_grid(X, Y, Nx, Ny)
Generates a non-uniform grid with periodic boundary conditions for the specified number of points in the $x$ and $y$ directions.

### compute_gradient(C, nabla_x, nabla_y)
Computes the gradient of the scalar field $C$ using the gradient operators $ 
abla_x $ and $ 
abla_y $.

### compute_laplacian(C, laplacian)
Computes the Laplacian of the scalar field $C$ using the Laplacian operator.

### plot_scalar_field(hub, field='C', time_step=0, returnFig=False)
Visualizes the scalar field $C$ at a given time step using Plotly, with options for animation over time.

### plot_velocity_field(hub, returnFig=False)
Plots the velocity field $ \mathbf{u}(x, y) $ using Matplotlib, showing the direction and magnitude of the fluid flow.

These functions allow you to create, analyze, and visualize the dynamics of a 2D periodic convection-diffusion system efficiently and effectively.


## Presets
|                | Description                                |
|:---------------|:-------------------------------------------|
| OneOscillation | One moving mass on a spring, one direction |
## Supplements
|                     | documentation                                                                                                | signature                                                               |
|:--------------------|:-------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| Springlist_to_K_L0  | Give a weighted matrix representation of a network from a list approach.                                     | (Node1, Node2, Nnodes, k=0, L0=0, damp=0, **kwargs)                     |
| plot_spring_network | Display the spring network dynamics using an animated plot.                                                  | (hub, sizemass=True, idx=0, region=0, tini=0, tend=-1, returnFig=False) |
| dictNode2SpringMat  | Convert a dictionary with node-spring information to include matrix representations that can feed the model. | (dic0)                                                                  |
| NodesKLfromMatKL    | Reconstruct the list of springs that composes the network represented in K and L0 matrices.                  | (K, L0)                                                                 |
| plot_invariants     | Plot the invariants of the spring network system over time.                                                  | (hub, returnFig=False)                                                  |
## Todo

## Equations
|             | eqtype       | definition                     | source_exp                                                                  | com   |
|:------------|:-------------|:-------------------------------|:----------------------------------------------------------------------------|:------|
| Nnodes      | size         | Number of nodes in the network |                                                                             |       |
| vx          | differential | horizontal velocity            | dvx/dt=Fx/m + Fdampx/m,                                                     |       |
| vy          | differential | vertical velocity              | dvy/dt=Fy/m + Fdampy/m,                                                     |       |
| x           | differential | horizontal position            | dx/dt=vx,                                                                   |       |
| y           | differential | vertical position              | dy/dt=vy,                                                                   |       |
| dx          | statevar     |                                | dx=x - np.moveaxis(x, -1, -2)),                                             |       |
| dy          | statevar     |                                | dy=y - np.moveaxis(y, -1, -2)),                                             |       |
| distance    | statevar     |                                | distance=(dx**2 + dy**2)**(1/2)),                                           |       |
| angle       | statevar     |                                | angle=np.arctan2(dy, dx)),                                                  |       |
| dvx         | statevar     |                                | dvx=vx - np.moveaxis(vx, -1, -2)),                                          |       |
| dvy         | statevar     |                                | dvy=vy - np.moveaxis(vy, -1, -2)),                                          |       |
| matspeed    | statevar     |                                | matspeed=(dvx**2 + dvy**2)**(1/2)),                                         |       |
| anglespeed  | statevar     |                                | anglespeed=np.arctan2(dvy, dvx)),                                           |       |
| Fx          | statevar     |                                | Fx=O.ssum2(-Kmat*(distance-L0Mat)*np.cos(angle))),                          |       |
| Fy          | statevar     |                                | Fy=O.ssum2(-Kmat*(distance-L0Mat)*np.sin(angle))),                          |       |
| Fdampx      | statevar     |                                | Fdampx=O.ssum2(-dampMat*matspeed*np.cos(anglespeed))),                      |       |
| Fdampy      | statevar     |                                | Fdampy=O.ssum2(-dampMat*matspeed*np.sin(anglespeed))),                      |       |
| Kinetic     | statevar     |                                | Kinetic=0.5*np.sum(O.ssum(m*(vx**2 + vy**2))), axis=-2),                    |       |
| Potential   | statevar     |                                | Potential=0.25*np.sum(np.sum(Kmat*(distance-L0Mat)**2), axis=-1), axis=-2), |       |
| Baricenterx | statevar     |                                | Baricenterx=np.sum(x*m, axis=-2)/np.sum(m, axis=-2)),                       |       |
| Baricentery | statevar     |                                | Baricentery=np.sum(y*m, axis=-2)/np.sum(m, axis=-2)),                       |       |
| momentumx   | statevar     |                                | momentumx=np.sum(vx*m, axis=-2)),                                           |       |
| momentumy   | statevar     |                                | momentumy=np.sum(vy*m, axis=-2)),                                           |       |
| L0Mat       |              |                                |                                                                             |       |
| Kmat        |              |                                |                                                                             |       |
| m           |              |                                |                                                                             |       |
| dampMat     |              |                                |                                                                             |       |