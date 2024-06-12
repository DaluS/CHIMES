# Model: PDE-Diffusion


    * **Creation** : 2024/01/22
    * **Coder**    : Paul Valcke
    * **Article**  : https://en.wikipedia.org/wiki/Heat_equation
    * **Keywords** : ['PDE', 'Phyics', 'Tutorial']
    

CHIMES can Solve PDE, using regions as points on a grid similar to a finite difference method of resolution. 
https://en.wikipedia.org/wiki/Finite_difference_method, using explicit schemas. 

The equation solve is : 

    $$dC(x,t)/dt = -D [
abla [
abla C(x,t)]]$$
    
Nabla is a spatial operator represented by a matrix, and [] correspond to the matrix product. 
The type of schemas and the property of space are located here in the definition of nabla. 

When the model is initialized, there is no spatiality. It's only when applying a preset that the PDE aspect shines. 

The spatial coupling is done by CHIMES operators that begins with R (for regional)



## Presets
|       | Description                                            |
|:------|:-------------------------------------------------------|
| Basic | A diffusion on 100 elements of a gaussian distribution |
## Supplements
|          | documentation                               | signature      |
|:---------|:--------------------------------------------|:---------------|
| Plot     | Minimal plot of the Concentration evolution | (hub)          |
| Generate | Generate a minimal conditions               | (diffcoeff, N) |
## Todo
* Generalization of nabla
* plotly plots

## Equations
|           | eqtype       | definition       | source_exp                    | com                                         |
|:----------|:-------------|:-----------------|:------------------------------|:--------------------------------------------|
| C         | differential | Concentration    | dC/dt=diffCoeff * lapC,       | uniform diffcoeff                           |
| gradC     | statevar     | 1d gradient of C | gradC=O.Rmatmul(C, nabla),    | calculated with nabla matrix multiplication |
| lapC      | statevar     |                  | lapC=O.Rmatmul(gradC, nabla), |                                             |
| diffCoeff |              |                  |                               |                                             |
| x         |              |                  |                               |                                             |
| nabla     |              | spatial operator |                               |                                             |