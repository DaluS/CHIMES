# Model: PDE-Waves


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []
    
## What is this model?

A 2D Periodic Convection-Diffusion model describes the transport and diffusion of a scalar field (e.g., temperature, concentration) in a 2D plane with periodic boundary conditions. This model combines the effects of convection (transport by fluid flow) and diffusion (spreading due to concentration gradients), and is widely used to simulate processes in fluid dynamics, meteorology, and environmental science.

## How can it be represented with vectors and matrices?

In this model:
* The scalar field $C(x, y, t)$ evolves over time according to the convection-diffusion equation.
* The velocity field $ \mathbf{u}(x, y) = (u_x(x, y), u_y(x, y)) $ represents the fluid flow.
* The dynamics follow the convection-diffusion equation: 
$$
\frac{\partial C}{\partial t} + \mathbf{u} \cdot \nabla C = D \nabla^2 C
$$
where $D$ is the diffusion coefficient.

The finite difference method is used to discretize the spatial domain into a grid of points:
* $X$ and $Y$ are 1D arrays representing the non-uniform grid points in the $x$ and $y$ directions.
* The gradient and Laplacian operators are represented by sparse matrices, allowing efficient computation of spatial derivatives.

### Gradient Operators:
The gradient operators $ \nabla_x $ and $ \nabla_y $ are constructed to compute the spatial derivatives:
$$
\nabla_x C \approx \frac{C(x + \Delta x, y) - C(x, y)}{\Delta x}
$$
$$
\nabla_y C \approx \frac{C(x, y + \Delta y) - C(x, y)}{\Delta y}
$$

### Laplacian Operator:
The Laplacian operator $ \nabla^2 $ is constructed as:
$$
\nabla^2 C \approx \frac{C(x + \Delta x, y) - 2C(x, y) + C(x - \Delta x, y)}{\Delta x^2} + \frac{C(x, y + \Delta y) - 2C(x, y) + C(x, y - \Delta y)}{\Delta y^2}
$$

## Why is it a great archetypal model?

The 2D Periodic Convection-Diffusion model is an excellent archetype for studying transport phenomena in fluid dynamics. It captures the essential physics of convection and diffusion, making it a versatile tool for understanding complex processes in natural and engineered systems. 
The periodic boundary conditions simplify the computational domain while preserving key dynamic behaviors.



## Presets
|       | Description                               |
|:------|:------------------------------------------|
| Basic | A diffusion on 100 elements of a gaussian |
## Supplements
|          | documentation                                                                | signature    |
|:---------|:-----------------------------------------------------------------------------|:-------------|
| Plot     | First concentration, second time variation, third gradient, fourth laplacian | (hub)        |
| Generate | <class 'function'>                                                           | no signature |
## Todo

## Equations
|           | eqtype       | definition           | source_exp                                | com                                         |
|:----------|:-------------|:---------------------|:------------------------------------------|:--------------------------------------------|
| dC        | differential | time derivative of C | ddC/dt=d2C,                               | wave EQ                                     |
| C         | differential | Concentration        | dC/dt=dC + diffCoeff * lapC + v * gradCx, | deduced from dt + diffusion                 |
| d2C       | statevar     | time derivative of C | d2C=c**2 * lapC,                          | wave EQ                                     |
| gradCx    | statevar     | 1d gradient of C     | gradCx=O.Rmatmul(C, nabla),               | calculated with nabla matrix multiplication |
| lapC      | statevar     |                      | lapC=O.Rmatmul(gradCx, nabla),            |                                             |
| c         |              | production price     |                                           |                                             |
| x         |              |                      |                                           |                                             |
| diffCoeff |              |                      |                                           |                                             |
| v         |              |                      |                                           |                                             |
| nabla     |              | spatial operator     |                                           |                                             |