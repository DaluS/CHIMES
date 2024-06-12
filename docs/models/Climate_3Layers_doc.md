# Model: Climate_3Layers


* **Creation** : 2021
* **Coder**    : Paul Valcke
* **Article**  :  
* **Keywords** : ['Climate', 'Module', 'Emission', 'Temperature']


## Description

A 3-Layer climate model, with a simple atmosphere, an upper ocean and a lower ocean.
There are two temperature variables, one for the atmosphere and one for the ocean.
The model is not spatial, and the temperature is given as an anomaly, not an absolute value.

From the concentration in the atmosphere is deduced radiative forcing, which is the difference between the incoming and outgoing radiation.
From the forcing is deduced the temperature variation

Emission should be given in GtC/year, when not plugged to anything the emissions are in an exponential decay.

## Why is it interesting? 

This is too rough of a model to be used for anything quantititative, but it is a nice illustration of the carbon cycle. 
It shows that carbon is causing temperature variation, and that carbon is slowly moving from the atmosphere to the ocean. 
This phenomena has however some delays, and the temperature is not following the concentration in the atmosphere.

Importantly, if one stops the emissions (apart from specific scenarios), the temperature will quickly stabilize. 
The concentration however will slowly moves toward the ocean until the chemical potential of the ocean is equal to the one of the atmosphere.

## Expected behavior

Emissions are first entering in the atmosphere, then upper ocean and eventually lower ocean.
When a dirac of emission is sent to the system, it will take time for temperature to reach its equilibrium, same for the concentration in the atmosphere.

## What is important to remember

This model is not spatial. 
The output is the temperature anomaly, not the temperature itself.


## Presets
|         | Description                                                                                     |
|:--------|:------------------------------------------------------------------------------------------------|
| default | Default run                                                                                     |
| dirac   | A very intense emission at t=0 (x10 the default run), rapidly diminshing (10x the default run). |
## Supplements
|                | documentation                                                                                        | signature     |
|:---------------|:-----------------------------------------------------------------------------------------------------|:--------------|
| prepare_sankey | Prepare the Sankey Diagram for carbon flows. Return as a dict that you can send directly into Sankey | (hub) -> dict |
## Todo
* Better models !

## Equations
|               | eqtype       | definition                           | source_exp                                                                                 | com                            |
|:--------------|:-------------|:-------------------------------------|:-------------------------------------------------------------------------------------------|:-------------------------------|
| CO2AT         | differential | CO2 in atmosphere                    | dCO2AT/dt=(1. / 3.666) * Emission - phi12 * CO2AT + phi12 * CAT / CUP * CO2UP,             | 3-Layer dynamics (Atmosphere)  |
| CO2UP         | differential | CO2 in upper ocean                   | dCO2UP/dt=phi12 * CO2AT - CO2UP * (phi12 * CAT / CUP - phi23) + phi23 * CUP / CLO * CO2LO, | 3-Layer dynamics (Upper ocean) |
| CO2LO         | differential | CO2 in lower ocean                   | dCO2LO/dt=phi23 * CO2UP - phi23 * CUP / CLO * CO2LO,                                       | 3-Layer dynamics (lower ocean) |
| T             | differential | temperature anomaly of atmosphere    | dT/dt=(F - rhoAtmo * T - gammaAtmo * (T - T0)) / Capacity,                                 | Forcing and ocean dynamics     |
| T0            | differential | temperature anomaly of ocean         | dT0/dt=(gammaAtmo * (T - T0)) / Capacity0,                                                 | Accumulation from atmosphere   |
| F             | statevar     | Radiative Forcing                    | F=F2CO2 / np.log(2) * np.log(CO2AT / CAT),                                                 | Forcing as sensitivity         |
| Emission      | statevar     | CO2 Emission per year (Gt)           | Emission=Emission0 * np.exp(-time * deltaEmission),                                        | CO2 Emission rate              |
| phi12         |              | Transfer rate atmosphere-ocean       |                                                                                            |                                |
| CUP           |              | Historical CO2 in upper ocean        |                                                                                            |                                |
| CAT           |              | Historical CO2 in atmosphere         |                                                                                            |                                |
| phi23         |              | Transfer rate upper-lower ocean      |                                                                                            |                                |
| CLO           |              | Historical CO2 in lower ocean        |                                                                                            |                                |
| rhoAtmo       |              | radiative feedback parameter         |                                                                                            |                                |
| gammaAtmo     |              | Heat exchange between layers         |                                                                                            |                                |
| Capacity      |              | Heat capacity atmosphere+upper ocean |                                                                                            |                                |
| Capacity0     |              | Heat capacity lower ocean            |                                                                                            |                                |
| F2CO2         |              | Forcing when doubling CO2            |                                                                                            |                                |
| Emission0     |              | CO2 Emission per year (Gt) at t=0    |                                                                                            |                                |
| deltaEmission |              | Diminution rate of carbon emission   |                                                                                            |                                |