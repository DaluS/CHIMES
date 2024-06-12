# Model: Lotka_Goodwin


* **Creation** : 2024/06/11
* **Coder**    : Paul Valcke
* **Article**  : 
* **Keywords** : ['Stability', 'Predatory-Prey', 'Lotka-Volterra', 'Goodwin']


## What is this model ?

This model is a minimal dynamical core, similar to a Goodwin phase-space dynamics, but even simpler. 
The equation system is thus: 

$$\dot{x} = x (A-B f(y))$$
$$\dot{y} = y (C-D g(x))$$

Where $f(x)$ and $g(y)$ are increasing functions. 
The advantage is that the equilibrium is easy to calculate

$$y_{eq} = f^{-1}(A/B)$$
$$x_{eq} = g^{-1}(C/D)$$

The system has closed cycles, and the equilibrium is not stable nor unstable. 
To simplify, we use $f(y)=y$, and $g(x)=x$. 

One of the interest of such practice is to replace the parameters with subparameters and linear dependency

$$A 	o A_0 + A_x (x-x_{eq}) + A_y (y-y_{eq})$$
$$B 	o B_0 + B_x (x-x_{eq}) + B_y (y-y_{eq})$$
$$C 	o C_0 + C_x (x-x_{eq}) + C_y (y-y_{eq})$$
$$D 	o D_0 + D_x (x-x_{eq}) + D_y (y-y_{eq})$$

Changing the parameters will not change the equilibrium point, but it will change the stability. 
This can be typically captured by the calculation of the Jacobian, its trace and determinant

## Expected behavior
* When $A_x,B_x,C_x,D_x,A_y,B_y,C_y,D_y$ are zero, the system is doing closed cycles.
* Increasing $B_x,D_y$ stabilize the system (and slow down the cycles locally)
* Increasing $A_x,C_y$ destabilize the system (and accelerate the cycles locally)
* Increasing $A_y,C_x$ accelerate the cycles
* Increasing $B_y,D_x$ slow down the cycles

## Oscillating equilibrium 






## Presets

## Supplements

## Todo
* Presets and plots

## Equations
|      | eqtype       | definition                          | source_exp                          | com                        |
|:-----|:-------------|:------------------------------------|:------------------------------------|:---------------------------|
| y    | differential |                                     | dy/dt=y * (C-D*x),                  |                            |
| x    | differential |                                     | dx/dt=x * (A-B*y),                  |                            |
| y0   | differential |                                     | dy0/dt=y0 * (C0-D0*x0),             |                            |
| x0   | differential |                                     | dx0/dt=x0 * (A0-B0*y0),             |                            |
| xeqM | statevar     |                                     | xeqM=lambda C, D                    |                            |
| yeqM | statevar     |                                     | yeqM=lambda A, B                    |                            |
| xeq  | statevar     |                                     | xeq=lambda C0, D0                   |                            |
| yeq  | statevar     |                                     | yeq=lambda A0, B0                   |                            |
| A    | statevar     | Efficiency in CES prod              | A=lambda A0, Ax, Ay, x, y, xeq, yeq |                            |
| B    | statevar     |                                     | B=lambda B0, Bx, By, x, y, xeq, yeq |                            |
| C    | statevar     | flux of goods for household         | C=lambda C0, Cx, Cy, x, y, xeq, yeq | Consumption as full salary |
| D    | statevar     | Debt of private sector              | D=lambda D0, Dx, Dy, x, y, xeq, yeq |                            |
| A0   |              |                                     |                                     |                            |
| B0   |              |                                     |                                     |                            |
| C0   |              |                                     |                                     |                            |
| D0   |              |                                     |                                     |                            |
| Ax   |              |                                     |                                     |                            |
| Bx   |              |                                     |                                     |                            |
| Cx   |              |                                     |                                     |                            |
| Dx   |              |                                     |                                     |                            |
| Ay   |              | production efficiency general level |                                     |                            |
| By   |              |                                     |                                     |                            |
| Cy   |              |                                     |                                     |                            |
| Dy   |              | Damage on production                |                                     |                            |