# Model: DoublePendulum


* **Creation** : 
* **Coder**    : 
* **Article**  : 
* **Keywords** : []


Two pendulums one on the other. This is creating a chaotic movement.
This set of equation assume m1=m2 and l1=l2

* **Name :** Double Uniform Pendulum Chaotic Dynamics
* **Article :** https://en.wikipedia.org/wiki/Double_pendulum
* **Author  :**
* **Coder   :** Paul Valcke

** TODO:**
* Create good plots
* Find equation for two different pendulum
* Explore more cases



## Presets
|         | Description   |
|:--------|:--------------|
| default | Default run   |
## Supplements

## Todo

## Equations
|     | eqtype       | definition                                      | source_exp                                                                                  | com                          |
|:----|:-------------|:------------------------------------------------|:--------------------------------------------------------------------------------------------|:-----------------------------|
| t1  | differential |                                                 | dt1/dt=dt1,                                                                                 | Upper pendulum angle         |
| t2  | differential |                                                 | dt2/dt=dt2,                                                                                 | lower pendulum angle         |
| pt1 | differential |                                                 | dpt1/dt=-m * l**2 / 2 * (dt1 * dt2 * np.sin(t1 - t2) + 3 * g / l * np.sin(t1)),             | Upper pendulum impulsion     |
| pt2 | differential |                                                 | dpt2/dt=-m * l**2 / 2 * (-dt1 * dt2 * np.sin(t1 - t2) + g / l * np.sin(t2)),                | Lower pendulum impulsion     |
| dt1 | statevar     |                                                 | dt1=(6 / m * l**2) * (2 * pt1 - 3 * np.cos(t1 - t2) * pt2) / (16 - 9 * np.cos(t1 - t2)**2), | Upper Angle variation        |
| dt2 | statevar     |                                                 | dt2=(6 / m * l**2) * (8 * pt1 - 3 * np.cos(t1 - t2) * pt1) / (16 - 9 * np.cos(t1 - t2)**2), | lower angle variation        |
| m   |              |                                                 |                                                                                             |                              |
| l   | param        | ratio btwn effective workers and typical worker |                                                                                             | deduced from Pi optimisation |
| g   |              | Relative growth of GDP                          |                                                                                             |                              |