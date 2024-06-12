# Model: ICED


    * **Creation** : 2023/12/07 model file creation
    * **Coder**    : Paul Valcke
    * **Article**  : https://www.overleaf.com/read/fxppgztffzph#6fa1cb
    * **Keywords** : ['module', 'capital', 'investment', 'decarbonation']
    

## Parameters added 

* sigmay :
* pc :
* deltaC : 
* zi : market sensibility
* zg : market preference
* Ag : Green efficiency 
* CESexp : Energy - (Labor-Capital) non-substitution
* Eeff : Energy efficiency 

## What is this model ?


## Why is it interesting ?




## what is the purpose of your model


## Expected behavior




## Presets
|         | Description                        |
|:--------|:-----------------------------------|
| default | Changes nothing, just plot holders |
## Supplements
|        | documentation                                                  | signature   |
|:-------|:---------------------------------------------------------------|:------------|
| Sankey | Display the Physical and nominal Sankey for the run of the hub | (hub)       |
## Todo
* Completing the model
* that should be done

## Equations
|            | eqtype       | definition                                                | source_exp                                                       | com                                                                             |
|:-----------|:-------------|:----------------------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------------------------|
| Ky         | differential |                                                           | dKy/dt=Iy - deltay * Ky,                                         | Basic investment-depreciation                                                   |
| Kg         | differential |                                                           | dKg/dt=Ig - deltag * Kg,                                         | Basic investment-depreciation                                                   |
| Kb         | differential |                                                           | dKb/dt=Ib - deltab * Kb,                                         | Basic investment-depreciation                                                   |
| ay         | differential |                                                           | day/dt=ay * alphay,                                              | Basic exogenous technological change                                            |
| ag         | differential |                                                           | dag/dt=ag * alphag,                                              | Basic exogenous technological change                                            |
| ab         | differential |                                                           | dab/dt=ab * alphab,                                              | Basic exogenous technological change                                            |
| epsilony   | differential | share of investment into energy capital                   | depsilony/dt=sigmay * epsilony * (1 - epsilony) * (1 - uE),      | lazy way to ensure that enough energy is available. Unstable mechanism in a CHI |
| D          | differential | Debt of private sector                                    | dD/dt=r * D + w * L + Delta * Pi - C * p,                        |                                                                                 |
| p          | differential | price of goods                                            | dp/dt=p * inflation,                                             |                                                                                 |
| N          | differential | Population of people able to work                         | dN/dt=N * n,                                                     |                                                                                 |
| w          | differential | Wage value                                                | dw/dt=w * phillips,                                              |                                                                                 |
| Hc         | differential |                                                           | dHc/dt=dict(func=lambda Hc, deltaHc, Cc                          |                                                                                 |
| Hw         | differential |                                                           | dHw/dt=dict(func=lambda Hw, deltaHw, Cw                          |                                                                                 |
| pc         | differential | carbon price                                              | dpc/dt=dict(func=lambda pc, inflation, omega                     |                                                                                 |
| Y          | statevar     | GDP in real units                                         | Y=Ay*Ky                                                          |                                                                                 |
| I          | statevar     | Investment in nominal value                               | I=Y - C,                                                         |                                                                                 |
| Iy         | statevar     |                                                           | Iy=I * epsilony,                                                 |                                                                                 |
| Ig         | statevar     |                                                           | Ig=I * (1 - epsilony) * epsilong,                                |                                                                                 |
| Ib         | statevar     |                                                           | Ib=I * (1 - epsilony) * (1 - epsilong),                          |                                                                                 |
| uE         | statevar     | use of energy capital                                     | uE=Ky / (Eeff*E),                                                |                                                                                 |
| E          | statevar     | Energy flux                                               | E=Ab * Kb + Ag * Kg,                                             |                                                                                 |
| Color      | statevar     | 1 energy is fully green, 0 fully brown                    | Color=Ag*Kg/E,                                                   |                                                                                 |
| Emission   | statevar     | Carbon emissions                                          | Emission=Ab*Kb,                                                  |                                                                                 |
| rocb       | statevar     | Return of capital for brown technology                    | rocb=Ab - omega * ay / ab - deltab - pc/p*pollb*Ab,              | no carbon tax                                                                   |
| rocg       | statevar     | Return of capital for green technology                    | rocg=Ag - omega * ay / ag - deltag+(Kb/Kg) * pc/p*pollb*Ab,      | no carbon tax                                                                   |
| epsilong   | statevar     | share of energy investment in green                       | epsilong=.5 * (1 + np.tanh(zi * (rocg - rocb - 1 + zg))),        | market allocation through ROC                                                   |
| g          | statevar     | growth rate usefull output                                | g=Iy/K - deltay,                                                 | its definition                                                                  |
| L          | statevar     | Workers                                                   | L=Ky / ay + Kb / ab + Kg / ag                                    |                                                                                 |
| a          | statevar     | Productivity                                              | a=K / L                                                          |                                                                                 |
| nu         | statevar     | Capital to output ratio                                   | nu=K / Y                                                         |                                                                                 |
| delta      | statevar     | Rate of capital depletion                                 | delta=(Kb*deltab+Kg*deltag+Ky*deltay)/K                          |                                                                                 |
| prod       | statevar     | productivity per worker                                   | prod=Y / L,                                                      |                                                                                 |
| K          | statevar     | Capital in real units                                     | K=Ky + Kb + Kg                                                   |                                                                                 |
| deltab     | statevar     | effective depreciation rate of useful capital             | deltab=deltab0 + deltaC,                                         |                                                                                 |
| C          | statevar     | flux of goods for household                               | C=(Ww+kappaC*Wc)/p,                                              | Consumption as full salary                                                      |
| Ww         | statevar     | workers total disposable income                           | Ww=w*L,                                                          |                                                                                 |
| Wc         | statevar     | capitalists total disposable income                       | Wc=r * D + Delta * Pi,                                           |                                                                                 |
| employment | statevar     | employment rate                                           | employment=L / N,                                                |                                                                                 |
| phillips   | statevar     | Wage inflation rate                                       | phillips=Phi0 + Phi1 * flambda,                                  |                                                                                 |
| flambda    | statevar     | non-linear function of employment in wage                 | flambda=((np.maximum(pi, 0.01)/0.1)**zpi) / (1 - employment)**2, |                                                                                 |
| omega      | statevar     | wage share                                                | omega=w * L / (p * Y),                                           |                                                                                 |
| d          | statevar     | relative debt                                             | d=D / (p * Y),                                                   |                                                                                 |
| Pi         | statevar     | Absolute profit                                           | Pi=p*Y-w*L-r*D-delta*p*K,                                        |                                                                                 |
| pi         | statevar     | relative profit                                           | pi=Pi/(p*Y),                                                     |                                                                                 |
| Cc         | statevar     |                                                           | Cc=kappaC*Wc/p,                                                  |                                                                                 |
| Cw         | statevar     |                                                           | Cw=Ww/p,                                                         |                                                                                 |
| Ag         | statevar     | Efficiency of green capital                               | Ag=Ag0 * (Kg / 0.1)**(0.1),                                      | Increasing output on capital                                                    |
| pollb      |              | Carbon intensity of producing 1 unit of energy through Kb |                                                                  |                                                                                 |
| Eeff       |              | Energy consumption efficiency                             |                                                                  |                                                                                 |
| alphab     |              | Automatisation rate for brown capital                     |                                                                  |                                                                                 |
| alphag     |              | Automatisation rate for grown capital                     |                                                                  |                                                                                 |
| alphay     |              | Automatisation rate for output capital                    |                                                                  |                                                                                 |
| deltay     |              | depreciation rate of useful capital                       |                                                                  |                                                                                 |
| deltab0    |              | exogenous depreciation rate of brown capital              |                                                                  |                                                                                 |
| deltag     |              | depreciation rate of green capital                        |                                                                  |                                                                                 |
| deltaC     |              | Voluntary destruction of brown capital                    |                                                                  |                                                                                 |
| Ab         |              | production efficiency for browm technology                |                                                                  |                                                                                 |
| Ay         |              | production efficiency general level                       |                                                                  |                                                                                 |
| sigmay     |              | rate of allocation change for energy                      |                                                                  |                                                                                 |
| zi         |              | Market profit sensibility in arbitrage                    |                                                                  |                                                                                 |
| zg         |              | Market green willingness                                  |                                                                  |                                                                                 |
| kappaC     |              | Share of income spent in consumption                      |                                                                  |                                                                                 |
| Delta      |              | proportion of profits as shareholding                     |                                                                  |                                                                                 |
| Phi0       |              | Wage negociation base level (no employment)               |                                                                  |                                                                                 |
| Phi1       |              | Linear sensibility to employment in wage negociation      |                                                                  |                                                                                 |
| inflation  |              | inflation rate                                            |                                                                  |                                                                                 |
| zpi        |              | profit sensibility in wage negotiation                    |                                                                  |                                                                                 |
| deltaHc    |              |                                                           |                                                                  |                                                                                 |
| deltaHw    |              |                                                           |                                                                  |                                                                                 |
| Ag0        |              | Base level of production efficiency for green technology  |                                                                  |                                                                                 |
| r          |              | Interest on debt                                          |                                                                  |                                                                                 |
| n          |              | Rate of population growth                                 |                                                                  |                                                                                 |