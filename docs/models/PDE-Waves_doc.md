# Model: PDE-Waves


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []


Wave propagation with :
    * propagation speed 'c'
    * Convection 'v'
    * diffusion 'D'

the system solves in 1D (if v=D=0) :
    $d^2C/dt^2 - c**2 
abla 
abla C = 0 $

It is more a proof of concept of what chimes can do in term of regions coupling.
A big part is still a bit sloppy.


## Presets
|       | Description                               |
|:------|:------------------------------------------|
| Basic | A diffusion on 100 elements of a gaussian |
## Supplements
|          | documentation                                                                    | signature            |
|:---------|:---------------------------------------------------------------------------------|:---------------------|
| Plot     | Plot time-slices of the concentration (horizontal time, vertical spatial).       | (hub)                |
|          |     First concentration, second time variation, third gradient, fourth laplacian |                      |
| Generate | Generate all parameters for the simulation                                       | (diffcoeff, c, v, N) |
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