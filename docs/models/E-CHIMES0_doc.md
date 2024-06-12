# Model: E-CHIMES0


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []


# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY

* **Article :** https://www.overleaf.com/read/thbdnhbtrbfx
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke
* **Date    :** 14/09/23

## Description

E-CHIMES is an economic model with multiple productive sectors in co-dependency.
The model is fully stock-flow consistent on both the monetary and all physical plans.

It is a platform for endogenisation.


## Presets
|           | Description                               |
|:----------|:------------------------------------------|
| Goodwin   | Basic Goodwin dynamics on a monosectorial |
| 2Goodwin  |                                           |
| 5Goodwin  |                                           |
| SimpleBi  |                                           |
| SimpleTri |                                           |
## Supplements
|                  | documentation                                                                                 | signature                     |
|:-----------------|:----------------------------------------------------------------------------------------------|:------------------------------|
| generateNgoodwin | Generate a dfields to generate N Goodwin in parrallel                                         | (Nsect, gamma=0.1, xi=1)      |
| Kfor0dotV        | Given the value of parameters (Gamma,Xi,kappaC,delta,nu,p,a,w),                               | (params)                      |
|                  |     Find the vector of capital that ensure dotV=0 at the first iteration, only for a GOODWIN. |                               |
|                  |     You can then multiply it in order to have the right GDP or employment                     |                               |
| pForROC          | Find the price vector so that the natural return on capital is the growth rate of society     | (dic)                         |
|                  |     ROC = pi / (nu*xi^p)                                                                      |                               |
| LeontievInverse  | Give the equivalent of the Leontiev Matrix with intermediate consumption and capital weight   | (params, Eigenvalues=False)   |
| PiRepartition    | Plot the relative profit repartition for each sector                                          | (hub, tini=False, tend=False) |
| PhysicalFluxes   | Plot the physical fluxes for each sector                                                      | (hub, tini=False, tend=False) |
| MonetaryFluxes   | Plot monetary fluxes for each sectore                                                         | (hub, tini=False, tend=False) |
## Todo

## Equations
|               | eqtype       | definition                                           | source_exp                                              | com                        |
|:--------------|:-------------|:-----------------------------------------------------|:--------------------------------------------------------|:---------------------------|
| D             | differential | Debt of private sector                               | dD/dt=dotD                                              |                            |
| Dh            | differential | Debt of household                                    | dDh/dt=-W + O.sprod(p, C) - O.ssum(Shareholding)        |                            |
| V             | differential | Inventory of Goods                                   | dV/dt=dotV                                              |                            |
| K             | differential | Capital in real units                                | dK/dt=I - delta * K                                     |                            |
| p             | differential | price of goods                                       | dp/dt=p * inflation                                     |                            |
| w0            | differential | wage indicator                                       | dw0/dt=w0 * (Phillips + gammai * ibasket)               |                            |
| u0            | differential | voluntary use of productive capital                  | du0/dt=sigma * (1 - u0) * (1 - v),                      |                            |
| a0            | differential | Capital unit per worker                              | da0/dt=a0 * alpha,                                      | Productivity indicator     |
| N             | differential | Population of people able to work                    | dN/dt=N * n                                             |                            |
| w             | statevar     | Wage value                                           | w=w0 * zw                                               |                            |
| a             | statevar     | Productivity                                         | a=a0 * za                                               |                            |
| xi            | statevar     | relative capex weight                                | xi=(delta * nu) * O.ssum2(Mxi)                          |                            |
| omega         | statevar     | wage share                                           | omega=w * L / (p * Y)                                   |                            |
| gamma         | statevar     | share of intermediary consumption                    | gamma=O.ssum2(Mgamma)                                   |                            |
| rd            | statevar     | relative weight debt                                 | rd=r * D / (p * Y)                                      | explicit form              |
| pi            | statevar     | relative profit                                      | pi=1 - omega - gamma - xi - rd                          |                            |
| ROC           | statevar     | return on capital                                    | ROC=pi / (nu * O.matmul(Xi, p) / p)                     | raw definition             |
| c             | statevar     | production price                                     | c=p * (omega + gamma + xi)                              |                            |
| mu            | statevar     | Markup on prices                                     | mu=p / c,                                               |                            |
| u             | statevar     | Use intensity of capital                             | u=u0,                                                   | just u0                    |
| Mgamma        | statevar     | weight of intermediate consumption from j            | Mgamma=Gamma * O.transpose(p) / p                       | Matrix version             |
| Mxi           | statevar     | weight of capital destruction from j                 | Mxi=nu * delta * Xi * O.transpose(p) / p                | Matrix version             |
| basket        | statevar     | weight in consumption basket                         | basket=p * C / O.sprod(p, C)                            | cannot be non-auxilliary   |
| ibasket       | statevar     | basket of good inflation                             | ibasket=O.sprod(inflation, basket)                      | deduced from the basket    |
| L             | statevar     | Workers                                              | L=u * K / a                                             |                            |
| dotV          | statevar     | temporal variation of inventory                      | dotV=dotV                                               | stock-flow                 |
| Y             | statevar     | GDP in real units                                    | Y=u * K / nu,                                           |                            |
| I             | statevar     | Investment in nominal value                          | I=In / O.matmul(Xi, p),                                 |                            |
| C             | statevar     | flux of goods for household                          | C=kappaC * W / p,                                       | Consumption as full salary |
| v             | statevar     |                                                      | v=Y / V                                                 |                            |
| Kdelta        | statevar     | physical degraded of capital                         | Kdelta=delta * K,                                       |                            |
| GammaY        | statevar     | flux to intermediate consumption                     | GammaY=O.matmul(O.transpose(Gamma), Y),                 |                            |
| TakenforI     | statevar     |                                                      | TakenforI=O.matmul(O.transpose(Xi), I),                 |                            |
| Minter        | statevar     | Money from i to j through intermediary consumption   | Minter=O.transpose(Gamma * Y)                           | matrix expansion           |
| Minvest       | statevar     | Money from i to j through investment                 | Minvest=O.transpose(Xi * I)                             | matrix expansion           |
| MtransactY    | statevar     | Money from i to j through intermediary consumption   | MtransactY=Y * Gamma * O.transpose(p)                   | matrix expansion           |
| MtransactI    | statevar     | Money from i to j through investment                 | MtransactI=In * Xi * O.transpose(p) / (O.matmul(Xi, p)) | matrix expansion           |
| wL            | statevar     | wage bill per sector                                 | wL=w * L                                                | wage bill per sector       |
| Shareholding  | statevar     | flow of profits to households                        | Shareholding=Delta * p * Y * pi                         |                            |
| pC            | statevar     | monetary consumption                                 | pC=p * C                                                | explicit monetary flux     |
| Idelta        | statevar     |                                                      | Idelta=p * Y * xi                                       |                            |
| Ilever        | statevar     |                                                      | Ilever=Pi * kappaI                                      |                            |
| In            | statevar     |                                                      | In=Idelta + Ilever                                      |                            |
| rD            | statevar     | debt interests                                       | rD=r * D                                                | explicit monetary flux     |
| dotD          | statevar     | debt variation                                       | dotD=dotD                                               | explicit monetary flux     |
| Pi            | statevar     | Absolute profit                                      | Pi=p * Y * pi                                           |                            |
| W             | statevar     | Total income of household                            | W=O.sprod(w, L) - r * Dh + O.ssum(Shareholding)         |                            |
| rDh           | statevar     | bank interests for household                         | rDh=r * Dh,                                             |                            |
| employmentAGG | statevar     | Agregated employment                                 | employmentAGG=O.ssum(employment),                       |                            |
| Phillips      | statevar     | non-inflationary wage growth rate                    | Phillips=Phi0 + Phi1 / (1 - employmentAGG)**2,          | DIVERGING                  |
| g             | statevar     | Relative growth of GDP                               | g=I / K - delta                                         |                            |
| employment    | statevar     | employment rate                                      | employment=L / N                                        |                            |
| reldotv       | statevar     | relative budget weight of inventory change           | reldotv=(c - p) * dotV / (p * Y)                        |                            |
| reloverinvest | statevar     | relative overinstment of the budget                  | reloverinvest=pi - kappaI                               |                            |
| za            |              | sector-ponderation of labor efficiency               |                                                         |                            |
| zw            |              | sector ponderation of wage                           |                                                         |                            |
| Phi0          |              | Wage negociation base level (no employment)          |                                                         |                            |
| Phi1          |              | Linear sensibility to employment in wage negociation |                                                         |                            |
| kappaI        |              |                                                      |                                                         |                            |
| kappaC        |              | Share of income spent in consumption                 |                                                         |                            |
| phinull       |              | Unemployment rate with no salary increase            |                                                         |                            |
| r             |              | Interest on debt                                     |                                                         |                            |
| n             |              | Rate of population growth                            |                                                         |                            |
| alpha         |              | Rate of productivity increase                        |                                                         |                            |
| gammai        |              | inflation awareness                                  |                                                         |                            |
| Gamma         |              | intermediate consumption coefficients                |                                                         |                            |
| Xi            |              | capital recipe creation                              |                                                         |                            |
| delta         |              | Rate of capital depletion                            |                                                         |                            |
| inflation     |              | inflation rate                                       |                                                         |                            |
| sigma         |              | rate of use adjustment                               |                                                         |                            |
| nu            |              | Capital to output ratio                              |                                                         |                            |
| Delta         |              | proportion of profits as shareholding                |                                                         |                            |