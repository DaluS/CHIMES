# Model: CHI


    * **Creation** : 
    * **Coder**    : 
    * **Article**  : 
    * **Keywords** : []
    

* **Article :** https://www.overleaf.com/read/bczdyhfqrdgh
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

Model as presented in "H-C instability".

Two sector (production, consolidated households), with physical (V,K) and nominal (D,Dh) stock-flow (Y,C,I) consistency.

Behavior:
* consumption proportional to sum of income sources
* investment proportional to post-dividends profits
* Wage through employment Philipps curve

**TODO:**
* Presets, presets, presets
* Add endogenisation


## Presets
|         | Description           |
|:--------|:----------------------|
| default | Goodwin-like behavior |
## Supplements
|                 | documentation                                                       | signature                |
|:----------------|:--------------------------------------------------------------------|:-------------------------|
| get_equilibrium | Calculate the equilibrium properties for a diverging phillips curve | (hub, ftype='divergent') |
## Todo

## Equations
|              | eqtype       | definition                                           | source_exp                                                  | com                |
|:-------------|:-------------|:-----------------------------------------------------|:------------------------------------------------------------|:-------------------|
| K            | differential | Capital in real units                                | dK/dt=I - delta * K                                         |                    |
| D            | differential | Debt of private sector                               | dD/dt=r * D + w * L + Delta * Pi - C * p,                   |                    |
| Dh           | differential | Debt of household                                    | dDh/dt=-r * D - w * L - Delta * Pi + C * p                  |                    |
| p            | differential | price of goods                                       | dp/dt=p * inflation                                         |                    |
| a            | differential | Productivity                                         | da/dt=a * alpha,                                            |                    |
| N            | differential | Population of people able to work                    | dN/dt=N * n                                                 |                    |
| w            | differential | Wage value                                           | dw/dt=w * phillips                                          |                    |
| I            | statevar     | Investment in nominal value                          | I=In / (Xi * p)                                             |                    |
| C            | statevar     | flux of goods for household                          | C=Y * (1 - Gamma) - I,                                      | KEENLINKE OVERRIDE |
| Pi           | statevar     | Absolute profit                                      | Pi=p * Y * (1 - Gamma) - w * L - p * delta * Xi * K - r * D |                    |
| W            | statevar     | Total income of household                            | W=w * L + r * D + Delta * Pi                                |                    |
| Y            | statevar     | GDP in real units                                    | Y=A * K                                                     |                    |
| Yc           | statevar     |                                                      | Yc=A * K                                                    |                    |
| Lc           | statevar     |                                                      | Lc=K / a                                                    |                    |
| Leff         | statevar     |                                                      | Leff=L / Lc                                                 |                    |
| L            | statevar     | Workers                                              | L=Lc                                                        |                    |
| Cn           | statevar     |                                                      | Cn=C * p,                                                   | KEENLINKE OVERRIDE |
| In           | statevar     |                                                      | In=p * delta * Xi * K + kappaI * (1 - Delta) * Pi           |                    |
| employment   | statevar     | employment rate                                      | employment=L / N                                            |                    |
| phillips     | statevar     | Wage inflation rate                                  | phillips=Phi0 + Phi1 * flambda                              |                    |
| flambda      | statevar     | non-linear function of employment in wage            | flambda={'func'                                             |                    |
| nu           | statevar     | Capital to output ratio                              | nu=K / Y                                                    |                    |
| omega        | statevar     | wage share                                           | omega=w * L / (p * Y)                                       |                    |
| d            | statevar     | relative debt                                        | d=D / (p * Y)                                               |                    |
| pi           | statevar     | relative profit                                      | pi=Pi / (p * Y)                                             |                    |
| productivity | statevar     |                                                      | productivity=Y / L                                          |                    |
| g            | statevar     | Relative growth of GDP                               | g=I / K - delta                                             |                    |
| ROC          | statevar     | return on capital                                    | ROC=Pi / (p * Xi * K)                                       | raw definition     |
| Solvability  | statevar     |                                                      | Solvability=1 - D / (K * Xi * p)                            |                    |
| c            | statevar     | production price                                     | c=p * (omega + Gamma + nu * delta * Xi)                     |                    |
| mu           | statevar     | Markup on prices                                     | mu=p / c                                                    |                    |
| GDPn         | statevar     |                                                      | GDPn=p * Y * (1 - Gamma)                                    |                    |
| GDP          | statevar     | nominal GDP                                          | GDP=Y * (1 - Gamma)                                         |                    |
| kappaC       | statevar     | Share of income spent in consumption                 | kappaC=Cn / W,                                              | KEENLINKE OVERRIDE |
| alpha        |              | Rate of productivity increase                        |                                                             |                    |
| n            |              | Rate of population growth                            |                                                             |                    |
| r            |              | Interest on debt                                     |                                                             |                    |
| delta        |              | Rate of capital depletion                            |                                                             |                    |
| Delta        |              | proportion of profits as shareholding                |                                                             |                    |
| Phi0         |              | Wage negociation base level (no employment)          |                                                             |                    |
| Phi1         |              | Linear sensibility to employment in wage negociation |                                                             |                    |
| phialpha     |              |                                                      |                                                             |                    |
| phii         |              |                                                      |                                                             |                    |
| inflation    |              | inflation rate                                       |                                                             |                    |
| A            |              | Efficiency in CES prod                               |                                                             |                    |
| Gamma        |              | intermediate consumption coefficients                |                                                             |                    |
| Xi           |              | capital recipe creation                              |                                                             |                    |
| kappaI       |              |                                                      |                                                             |                    |
| V            |              | Inventory of Goods                                   |                                                             |                    |