# Model: GK


    * **Creation** : 2021
    * **Coder**    : Paul Valcke
    * **Article**  :  
    * **Keywords** : ['Goodwin', 'Toy-model', 'Debt', 'Crises']
    

## What is this model ?

This is a Goodwin model with a few modifications. 
The bigger the profits rate $\pi$, the bigger the investment, which appears as debt-financed. 
Since the system is respecting Say's law $Y=C+I$, more investment at a constant production means less consumption.
In consequence, the system behaves as if households where loaning money to the firms, prefering not to consume at the instant.

In term of equations: 
* In a Goodwin model $I=\pi Y$
* In a Goodwin-Keen model $I = \kappa(\pi) Y$, kappa being a parametric function 

Since the debt equation is $\dot{D}= rD + wL - p*C$, it becomes $\dot{D} = pY * (\kappa(\pi)-\pi)$

## Why is it interesting ? 

Private debt is often overlooked and allow another angle of approach. 
A non-linear kappa curve will also break the closed cycles aspect of a Goodwin. 
In certains conditions there can be a debt crisis

## Expected behavior

The equilibrium is now stable in most cases, and another equilibrium (inifinite debt ratio) also appears. 
The "bad" solovian equilibrium is also stable, meaning that an economy can be driven toward it. 

## What is important to remember

It is a nice illustration of two-attractor dynamics in economy, however the investment mechanism without inflation correction is at best naive.
Debt-fundings is also not the only locally stabilizing mechanism to consider 


## Presets
|                   | Description                          |
|:------------------|:-------------------------------------|
| default           | Convergence to equilibrium           |
| debtcrisis        | Path toward infinite relative debt   |
| debtstabilisation | Stabilization through excess of debt |
## Supplements
|               | documentation                                                                           | signature   |
|:--------------|:----------------------------------------------------------------------------------------|:------------|
| ThreeDynamics | Draw three qualitatively different Dynamical phase-space associated with a Goodwin-Keen | (hub)       |
## Todo
* Better models !

## Equations
|            | eqtype       | definition                                | source_exp                                   | com                        |
|:-----------|:-------------|:------------------------------------------|:---------------------------------------------|:---------------------------|
| a          | differential | Productivity                              | da/dt=a * alpha),                            |                            |
| N          | differential | Population of people able to work         | dN/dt=N * n),                                |                            |
| K          | differential | Capital in real units                     | dK/dt=Ir - delta * K),                       |                            |
| w          | differential | Wage value                                | dw/dt=w * phillips),                         |                            |
| p          | differential | price of goods                            | dp/dt=p * inflation),                        |                            |
| D          | differential | Debt of private sector                    | dD/dt=r * D + w * L - p * C),                |                            |
| Dh         | differential | Debt of household                         | dDh/dt=-r * D - w * L + p * C),              |                            |
| pi         | statevar     | relative profit                           | pi=Pi / (p * Y)),                            |                            |
| d          | statevar     | relative debt                             | d=D / (p * Y)),                              |                            |
| omega      | statevar     | wage share                                | omega=w * L / (p * Y)),                      |                            |
| employment | statevar     | employment rate                           | employment=L / N),                           |                            |
| c          | statevar     | production price                          | c=p * omega),                                |                            |
| g          | statevar     | Relative growth of GDP                    | g=Ir / K - delta),                           |                            |
| Y          | statevar     | GDP in real units                         | Y=K / nu),                                   |                            |
| Pi         | statevar     | Absolute profit                           | Pi=p * Y - w * L - r * D),                   |                            |
| I          | statevar     | Investment in nominal value               | I=kappa * p * Y),                            |                            |
| C          | statevar     | flux of goods for household               | C=Y - Ir),                                   | Consumption as full salary |
| Ir         | statevar     | Number of real unit from investment       | Ir=I / p),                                   |                            |
| L          | statevar     | Workers                                   | L=Y / a),                                    |                            |
| GDP        | statevar     | nominal GDP                               | GDP=Y * p),                                  |                            |
| inflation  | statevar     | inflation rate                            | inflation=eta * (mu * c / p - 1)),           |                            |
| kappa      | statevar     | Part of GDP in investment                 | kappa=k0 + k1 * np.exp(k2 * pi),             | Exponential kappa function |
| phillips   | statevar     | Wage inflation rate                       | phillips=-phi0 + phi1 / (1 - employment)**2, | Divergent Phillips curve   |
| Delta      |              | proportion of profits as shareholding     |                                              |                            |
| alpha      |              | Rate of productivity increase             |                                              |                            |
| n          |              | Rate of population growth                 |                                              |                            |
| delta      |              | Rate of capital depletion                 |                                              |                            |
| r          |              | Interest on debt                          |                                              |                            |
| nu         |              | Capital to output ratio                   |                                              |                            |
| eta        |              | timerate of price adjustment              |                                              |                            |
| mu         |              | Markup on prices                          |                                              |                            |
| k0         |              | GDP share investedat zeroprofit (expo)    |                                              |                            |
| k1         |              | Investment slope (expo)                   |                                              |                            |
| k2         |              | Investment power in kappa (expo)          |                                              |                            |
| phinull    |              | Unemployment rate with no salary increase |                                              |                            |
| phi0       | parameter    | Parameter1 for diverving squared          | phinull / (1 - phinull**2),                  |                            |
| phi1       | parameter    | Parameter1 for diverving squared          | phinull**3 / (1 - phinull**2),               |                            |