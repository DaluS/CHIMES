# Model: Agents_Vicsek


    * **Creation** : 
    * **Coder**    : 
    * **Article**  : 
    * **Keywords** : []
    


* **Name :** Vicsek Agent-Based dynamics
* **Article :** https://en.wikipedia.org/wiki/Vicsek_model
* **Author  :**
* **Coder   :** Paul Valcke


## Presets
|                 | Description                                      |
|:----------------|:-------------------------------------------------|
| synchronisation | Agents are going to synchronize in one direction |
| TooNoisy        | Agents cannot synchronize                        |
| LowSync         | Agents cannot synchronize                        |
## Supplements
|                  | documentation            | signature   |
|:-----------------|:-------------------------|:------------|
| PlotTrajectories | Plot of all trajectories | (hub)       |
## Todo

## Equations
|               | eqtype       | definition   | source_exp                                                                         | com               |
|:--------------|:-------------|:-------------|:-----------------------------------------------------------------------------------|:------------------|
| Nagents       | size         |              |                                                                                    |                   |
| x             | differential |              | dx/dt=vx,                                                                          |                   |
| y             | differential |              | dy/dt=vy,                                                                          |                   |
| theta         | differential |              | dtheta/dt=-weightmeangle + noise * np.random.normal(0, size=(nx, nr, Nagents, 1)), |                   |
| vx            | statevar     |              | vx=v * np.cos(theta),                                                              |                   |
| vy            | statevar     |              | vy=v * np.sin(theta),                                                              |                   |
| distances     | statevar     |              | distances=np.sqrt((x - O.transpose(x)) ** 2 + (y - O.transpose(y)) ** 2),          | vector norm       |
| anglediff     | statevar     |              | anglediff=theta - O.transpose(theta),                                              |                   |
| closeenough   | statevar     |              | closeenough=np.heaviside(distscreen - distances, 0),                               |                   |
| weightmeangle | statevar     |              | weightmeangle=localmeantheta                                                       | with an heaviside |
| meanX         | statevar     |              | meanX=O.ssum(x) / O.ssum(x * 0 + 1),                                               | mean position     |
| meanY         | statevar     |              | meanY=O.ssum(y) / O.ssum(y * 0 + 1),                                               | mean position     |
| speed         | statevar     |              | speed=np.sqrt(vx**2 + vy**2),                                                      | vector norm       |
| noise         |              |              |                                                                                    |                   |
| distscreen    |              |              |                                                                                    |                   |
| v             |              |              |                                                                                    |                   |