# Model: _CESprod


    * **Creation** : 
    * **Coder**    : 
    * **Article**  : 
    * **Keywords** : []
    

* **Name :** CES module
* **Article :** []
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

* **Supplements description :** Not developped to be used in standalone

$$Y=A (b K^{-\eta} + (1-b) (aL)^{-\eta} )^(-1/\eta)$$
$$Y=Yc (1 + (L/L_c)^{-\eta} )^(-1/\eta)= Yc (1 + (l)^{-\eta} )^(-1/\eta)$$

Solving $$\dfrac{\partial \Pi}{\partial L}= 0$$

It gives :
$$ \omega_c = (w/(A*a0*p*(1-gamma)))*((1-b)/b)^(1/\eta)$$
$$ l = (omegacarac^(-CESexp/(1+CESexp)) - 1)^(1/CESexp)$$

There is an hard-cap to ensure that it can work with $\omega_c\geq 1 $ (which gives $l=0$)

**TODO:**
* DO NOT EDIT THIS FILE ! COPY AND PASTE IT THEN MODIFY THE COPY TO WRITE YOUR MODEL


## Presets
|         | Description   |
|:--------|:--------------|
| preset0 |               |
## Supplements

## Todo

## Equations
|            | eqtype   | definition                                      | source_exp                                                                 | com                     |
|:-----------|:---------|:------------------------------------------------|:---------------------------------------------------------------------------|:------------------------|
| Yc         | statevar |                                                 | Yc=A * K * b**(-1 / CESexp),                                               |                         |
| cesLcarac  | statevar | Typical Labor from capital                      | cesLcarac=K / a0 * (b / (1 - b))**(-1 / CESexp),                           | Extracted from YCES     |
| omegacarac | statevar | Typical omega without substituability           | omegacarac=(w / (A * a0 * p * (1 - gamma))) * ((1 - b) / b)**(1 / CESexp), | Extracted from YCES     |
| l          | statevar | ratio btwn effective workers and typical worker | l=l                                                                        | Floor at 0.5            |
| Y          | statevar | GDP in real units                               | Y=Yc * (1 + l**(-CESexp))**(-1 / CESexp),                                  | CES PRODUCTION FUNCTION |
| L          | statevar | Workers                                         | L=l * cesLcarac                                                            |                         |
| nu         | statevar | Capital to output ratio                         | nu=K / Y                                                                   |                         |
| K          |          | Capital in real units                           |                                                                            |                         |
| b          |          | part of capital in prod intensity               |                                                                            |                         |
| CESexp     |          | exponent in CES function                        |                                                                            |                         |
| A          |          | Efficiency in CES prod                          |                                                                            |                         |
| a0         |          |                                                 |                                                                            | Productivity indicator  |
| w          |          | Wage value                                      |                                                                            |                         |
| p          |          | price of goods                                  |                                                                            |                         |
| gamma      |          | share of intermediary consumption               |                                                                            |                         |