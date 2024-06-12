# Model: Goodwin_example_short


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []

Goodwin model with minimal formalism

## Presets

## Supplements

## Todo

## Equations
|            | eqtype       | definition                                           | source_exp                             | com                        |
|:-----------|:-------------|:-----------------------------------------------------|:---------------------------------------|:---------------------------|
| p          | differential | price of goods                                       | dp/dt=p*inflation,                     |                            |
| a          | differential | Productivity                                         | da/dt=a*alpha,                         |                            |
| N          | differential | Population of people able to work                    | dN/dt=N*n,                             |                            |
| K          | differential | Capital in real units                                | dK/dt=Ir-delta*K,                      |                            |
| w          | differential | Wage value                                           | dw/dt=w*phillips),                     |                            |
| pi         | statevar     | relative profit                                      | pi=Pi / (p*Y),                         |                            |
| omega      | statevar     | wage share                                           | omega=w*L/(p*Y),                       |                            |
| employment | statevar     | employment rate                                      | employment=L/N,                        |                            |
| g          | statevar     | Relative growth of GDP                               | g=Ir/K-delta,                          |                            |
| Y          | statevar     | GDP in real units                                    | Y=K/nu,                                |                            |
| Pi         | statevar     | Absolute profit                                      | Pi=p*Y-w*L,                            |                            |
| C          | statevar     | flux of goods for household                          | C=Y-Ir,                                | Consumption as full salary |
| Ir         | statevar     | Number of real unit from investment                  | Ir=Pi/p,                               |                            |
| L          | statevar     | Workers                                              | L=K/a,                                 |                            |
| phillips   | statevar     | Wage inflation rate                                  | phillips=Phi0+Phi1/(1-employment)**2), |                            |
| inflation  |              | inflation rate                                       |                                        |                            |
| alpha      |              | Rate of productivity increase                        |                                        |                            |
| n          |              | Rate of population growth                            |                                        |                            |
| delta      |              | Rate of capital depletion                            |                                        |                            |
| nu         |              | Capital to output ratio                              |                                        |                            |
| Phi0       |              | Wage negociation base level (no employment)          |                                        |                            |
| Phi1       |              | Linear sensibility to employment in wage negociation |                                        |                            |