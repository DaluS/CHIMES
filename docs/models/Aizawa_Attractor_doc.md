# Model: Aizawa_Attractor


* **Creation** :  2024/04/23
* **Coder**    : Paul Valcke
* **Article**  : https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor
* **Keywords** : ['stochastic', 'Documentation', 'chaos', 'attractor']


3 Differential attractor. 


## What is this model ?

A 3 Dimensional attractor, with oscillations on a spheres and on its polar axis



## Presets
|       | Description    |
|:------|:---------------|
| plots | Just the plots |
## Supplements

## Todo

## Equations
|    | eqtype       | definition                        | source_exp                                           | com   |
|:---|:-------------|:----------------------------------|:-----------------------------------------------------|:------|
| x  | differential |                                   | dx/dt=(z-b)*x-d*y,                                   |       |
| y  | differential |                                   | dy/dt=d*x + (z-b)*y,                                 |       |
| z  | differential | local wage ponderation            | dz/dt=c+a*z-(z**3)/3-(x**2+y**2)*(1+e*z) + f*z*x**3, |       |
| a  |              | Productivity                      |                                                      |       |
| b  |              | part of capital in prod intensity |                                                      |       |
| c  |              | production price                  |                                                      |       |
| d  |              | relative debt                     |                                                      |       |
| e  |              |                                   |                                                      |       |
| f  |              |                                   |                                                      |       |