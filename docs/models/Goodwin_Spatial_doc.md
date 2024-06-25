# Model: Goodwin_Spatial


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

## Supplements
|                | documentation                                                                | signature    |
|:---------------|:-----------------------------------------------------------------------------|:-------------|
| generate_Nabla | <class 'function'>                                                           | no signature |
| plot           | First concentration, second time variation, third gradient, fourth laplacian | (hub)        |
## Todo

## Equations
|            | eqtype       | definition                                  | source_exp                                                      | com                               |
|:-----------|:-------------|:--------------------------------------------|:----------------------------------------------------------------|:----------------------------------|
| p          | differential | nominal value per physical unit produced    | dp/dt=p*inflation,                                              | Consequence of causal inflation   |
| a          | differential | Automatisation level                        | da/dt=a*alpha,                                                  | exogenous                         |
| K          | differential | Capital in real units                       | dK/dt=Ir-delta*K,                                               | Investment - dpreciation dynamics |
| w          | differential | individual wage value                       | dw/dt=w*phillips,                                               | short-run Phillips dynamics       |
| N          | differential | Population of people able to work           | dN/dt=lambda N, n, divPhiN                                      |                                   |
| pi         | statevar     | relative profit                             | pi=Pi / (p*Y),                                                  | its definition                    |
| omega      | statevar     | wage share                                  | omega=w*L/(p*Y),                                                | its definition                    |
| employment | statevar     | employment rate                             | employment=L/N,                                                 | its definition                    |
| g          | statevar     | Relative growth of GDP                      | g=Ir/K-delta,                                                   | manually calculated               |
| Y          | statevar     | GDP in real units                           | Y=K/nu,                                                         | Leontiev optimized on labor       |
| Pi         | statevar     | Absolute profit                             | Pi=p*Y-w*L,                                                     | definition without depreciation   |
| C          | statevar     | flux of goods for household                 | C=Y-Ir,                                                         | Consumption as full salary        |
| L          | statevar     | Workers                                     | L=K/a,                                                          | from automatisation definition    |
| phillips   | statevar     | Wage inflation rate                         | phillips=Phi0+Phi1/(1-employment)**2,                           | DIVERGING PHILLIPS CURVE          |
| Ir         | statevar     | Number of real unit from investment         | Ir=(Pi+divPhiI)/p,                                              |                                   |
| divPhiI    | statevar     |                                             | divPhiI=O.Rmatmul(PhiI, Nabla) + Dn * O.Rmatmul(N, Laplacian),  |                                   |
| divPhiN    | statevar     |                                             | divPhiN=O.Rmatmul(PhiN, Nabla) + Di * O.Rmatmul(Pi, Laplacian), |                                   |
| PhiI       | statevar     |                                             | PhiI=PhipiI,                                                    |                                   |
| PhiN       | statevar     |                                             | PhiN=PhiwN + PhilambdaN,                                        |                                   |
| PhiwN      | statevar     |                                             | PhiwN=muw * (N/w) * O.Rmatmul(w, Nabla),                        |                                   |
| PhilambdaN | statevar     |                                             | PhilambdaN=mulambda * (N) * O.Rmatmul(employment, Nabla),       |                                   |
| PhipiI     | statevar     |                                             | PhipiI=mupi * (Y*pi) * O.Rmatmul(pi, Nabla),                    |                                   |
| inflation  |              | inflation rate                              |                                                                 |                                   |
| alpha      |              | Rate of productivity increase               |                                                                 |                                   |
| n          |              | Rate of population growth                   |                                                                 |                                   |
| delta      |              | Rate of capital depletion                   |                                                                 |                                   |
| nu         |              | Capital to output ratio                     |                                                                 |                                   |
| Phi0       |              | wage reduction rate when full unemployement |                                                                 |                                   |
| Phi1       |              | wage rate dependance to unemployement       |                                                                 |                                   |
| muw        |              |                                             |                                                                 |                                   |
| mulambda   |              |                                             |                                                                 |                                   |
| mupi       |              |                                             |                                                                 |                                   |
| Di         |              |                                             |                                                                 |                                   |
| Dn         |              |                                             |                                                                 |                                   |
| Laplacian  |              |                                             |                                                                 |                                   |
| Nabla      |              |                                             |                                                                 |                                   |
| x          |              |                                             |                                                                 |                                   |