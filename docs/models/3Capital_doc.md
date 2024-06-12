# Model: 3Capital


* **Creation** : 2023/12/07 model file creation
* **Coder**    : Paul Valcke
* **Article**  : https://www.overleaf.com/read/fxppgztffzph#6fa1cb
* **Keywords** : ['module', 'capital', 'investment', 'decarbonation']


## What is this model ?

This model is the capital core properties for ICED (Inequality-Climate-Economy-Decarbonation).
It cover the output and investment dynamics in three types of capitals and its consequences

## Why is it interesting ?

It allows to see how -social consequences and climate feedback aside- technology coefficient and climate policies will impact decoupling. 



## what is the purpose of your model

The less efficient energy production is, the more investment is allocated to it.
The technology with the higher capital-to-output ratio will have the bigger investment.
The investment is causal of the capital amount, and the emissions are consequence of the amount of capital.
In consequence, the model capture the inertia of decarbonation.

Beyond the natural evolution of the market, we add the following mechanisms:
* Voluntary destruction of brown capital at a rate $\delta^C$
* Carbon tax taken from brown sector to green sector

## Expected behavior

* The system start with high investment into brown as its rentability is higher
* A bigger carbon tax makes a rapid boost early stage for green that then slow down as the relative effects dampens
* Without voluntary destruction of brown capital, the emissions will at best slow down as fast as the natural depreciation rate of brown assets



## Presets
|         | Description                        |
|:--------|:-----------------------------------|
| default | Changes nothing, just plot holders |
## Supplements

## Todo
* Completing the model
* that should be done

## Equations
|          | eqtype       | definition                                                | source_exp                                                  | com                                                                             |
|:---------|:-------------|:----------------------------------------------------------|:------------------------------------------------------------|:--------------------------------------------------------------------------------|
| Ky       | differential |                                                           | dKy/dt=Iy - deltay * Ky,                                    | Basic investment-depreciation                                                   |
| Kg       | differential |                                                           | dKg/dt=Ig - deltag * Kg,                                    | Basic investment-depreciation                                                   |
| Kb       | differential |                                                           | dKb/dt=Ib - deltab * Kb,                                    | Basic investment-depreciation                                                   |
| ay       | differential |                                                           | day/dt=ay * alphay,                                         | Basic exogenous technological change                                            |
| ag       | differential |                                                           | dag/dt=ag * alphag,                                         | Basic exogenous technological change                                            |
| ab       | differential |                                                           | dab/dt=ab * alphab,                                         | Basic exogenous technological change                                            |
| epsilony | differential | share of investment into energy capital                   | depsilony/dt=sigmay * epsilony * (1 - epsilony) * (1 - uE), | lazy way to ensure that enough energy is available. Unstable mechanism in a CHI |
| Y        | statevar     | GDP in real units                                         | Y=Ay*Ky                                                     |                                                                                 |
| C        | statevar     | flux of goods for household                               | C=Y*omega,                                                  | Consumption as full salary                                                      |
| I        | statevar     | Investment in nominal value                               | I=Y - C,                                                    |                                                                                 |
| Iy       | statevar     |                                                           | Iy=I * epsilony,                                            |                                                                                 |
| Ig       | statevar     |                                                           | Ig=I * (1 - epsilony) * epsilong,                           |                                                                                 |
| Ib       | statevar     |                                                           | Ib=I * (1 - epsilony) * (1 - epsilong),                     |                                                                                 |
| uE       | statevar     | use of energy capital                                     | uE=Ky / (Eeff*E),                                           |                                                                                 |
| E        | statevar     | Energy flux                                               | E=Ab * Kb + Ag * Kg,                                        |                                                                                 |
| Color    | statevar     | 1 energy is fully green, 0 fully brown                    | Color=Ag*Kg/E,                                              |                                                                                 |
| Emission | statevar     | Carbon emissions                                          | Emission=Ab*Kb,                                             |                                                                                 |
| rocb     | statevar     | Return of capital for brown technology                    | rocb=Ab - omega * ay / ab - deltab - pc/p*pollb*Ab,         | no carbon tax                                                                   |
| rocg     | statevar     | Return of capital for green technology                    | rocg=Ag - omega * ay / ag - deltag+(Kb/Kg) * pc/p*pollb*Ab, | no carbon tax                                                                   |
| epsilong | statevar     | share of energy investment in green                       | epsilong=.5 * (1 + np.tanh(zi * (rocg - rocb - 1 + zg))),   | market allocation through ROC                                                   |
| g        | statevar     | growth rate usefull output                                | g=Iy/K - deltay,                                            | its definition                                                                  |
| L        | statevar     | Workers                                                   | L=Ky / ay + Kb / ab + Kg / ag                               |                                                                                 |
| a        | statevar     | Productivity                                              | a=K / L                                                     |                                                                                 |
| nu       | statevar     | Capital to output ratio                                   | nu=K / Y                                                    |                                                                                 |
| delta    | statevar     | Rate of capital depletion                                 | delta=(Kb*deltab+Kg*deltag+Ky*deltay)/K                     |                                                                                 |
| prod     | statevar     | productivity per worker                                   | prod=Y / L,                                                 |                                                                                 |
| K        | statevar     | Capital in real units                                     | K=Ky + Kb + Kg                                              |                                                                                 |
| deltab   | statevar     | effective depreciation rate of useful capital             | deltab=deltab0 + deltaC,                                    |                                                                                 |
| pc       |              | carbon price                                              |                                                             |                                                                                 |
| pollb    |              | Carbon intensity of producing 1 unit of energy through Kb |                                                             |                                                                                 |
| Eeff     |              | Energy consumption efficiency                             |                                                             |                                                                                 |
| alphab   |              | Automatisation rate for brown capital                     |                                                             |                                                                                 |
| alphag   |              | Automatisation rate for grown capital                     |                                                             |                                                                                 |
| alphay   |              | Automatisation rate for output capital                    |                                                             |                                                                                 |
| deltay   |              | depreciation rate of useful capital                       |                                                             |                                                                                 |
| deltab0  |              | exogenous depreciation rate of brown capital              |                                                             |                                                                                 |
| deltag   |              | depreciation rate of green capital                        |                                                             |                                                                                 |
| deltaC   |              | Voluntary destruction of brown capital                    |                                                             |                                                                                 |
| Ab       |              | production efficiency for browm technology                |                                                             |                                                                                 |
| Ay       |              | production efficiency general level                       |                                                             |                                                                                 |
| Ag       |              | Effective production efficiency for green technology      |                                                             |                                                                                 |
| sigmay   |              | rate of allocation change for energy                      |                                                             |                                                                                 |
| zi       |              | Market profit sensibility in arbitrage                    |                                                             |                                                                                 |
| zg       |              | Market green willingness                                  |                                                             |                                                                                 |
| omega    |              | wage share                                                |                                                             |                                                                                 |
| p        |              | price of goods                                            |                                                             |                                                                                 |