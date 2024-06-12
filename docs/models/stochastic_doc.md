# Model: stochastic


    * **Creation** : 
    * **Coder**    : 
    * **Article**  : 
    * **Keywords** : []
    

solve $\dot{y} = y \sigma$, with sigma a guassian noise


## Presets
|        | Description               |
|:-------|:--------------------------|
| Onevar | One variable              |
| 10     | One hundred parrallel run |
## Supplements
|      | documentation   | signature   |
|:-----|:----------------|:------------|
| plot |                 | (hub)       |
## Todo

## Equations
|         | eqtype       | definition                     | source_exp                                                    | com                  |
|:--------|:-------------|:-------------------------------|:--------------------------------------------------------------|:---------------------|
| y       | differential |                                | dy/dt=y * noisamp,                                            | noise on growth rate |
| noisamp | statevar     |                                | noisamp=noise * np.random.normal(loc=0, size=(nx, nr, 1, 1)), |                      |
| noise   |              | noise amplitude on growth rate |                                                               |                      |