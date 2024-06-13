# Model: Spring_Network


    * **Creation** : 2024/06/04
    * **Coder**    : Paul Valcke
    * **Article**  : https://en.wikipedia.org/wiki/Spring_system
    * **Keywords** : ['Network', 'springs', 'mesh']
    

## What is this model?

A Spring Network is an ensemble of nodes that are linked by springs. Springs, depending on their compression, will apply forces on the nodes they connect. These forces will then move the nodes, which changes the spring tensions. This model is a classic example of local wave propagation on a network structure.

## How can it be represented with vectors and matrices?

In this model:
* Each node \(i \in N_{nodes}\) has a position \((x_i, y_i)\), and a speed \((v^x_i, v^y_i)\).
* The dynamics follow a classic equation: 
\[ \dot{v}^x_i = rac{F^x_i - 	ext{damp} \cdot v^y_i}{m_i} \]
where damp is fluid friction, and F is the force resulting from the spring network.

Springs are represented by tensors, not as individuals. We consider \(N_{springs}\) springs with four characteristics:
1. The index of their first node extremity \(I^1_j\)
2. The index of their second node extremity \(I^2_j\)
3. A stiffness \(k_j\)
4. An unstretched length \(L^0_j\)

Instead of calculating each spring individually using loops, we use matrices. Each node is considered to be linked to every other node, but with a default stiffness of 0.

Consequently, we define \(k_{ij}\) as the stiffness matrix of the network.

The dynamics are described by:
\[ \dot{v}_i = - \sum_j k_{ij} \left( 	ext{dist}(x_i, x_j) - L0_{ij} ight) \cos(	heta_i) - \eta v_i \]

with:
\[ 	ext{dist}(x_i, x_j) = \sqrt{(x_i - x_j )^2 + (y_i - y_j )^2} \]
\[ 	heta_i = 	ext{atan}\left( rac{(y_i - y_j)}{(x_i - x_j)} ight) \]

Matrices \(k\) and \(L^0\) represent the stiffness and unstretched lengths of the springs, respectively.

## Why is it a great archetypal model?

The Spring Network model is a great archetypal model for studying local wave propagation on a network structure. 
It provides a simplified yet powerful way to understand the dynamics of interconnected systems. 
This model is useful for various applications, including physics, engineering, and network theory.

## What are the different functions in supplements?

### Springlist_to_K_L0(Node1, Node2, Nnodes, k, L0, damp )
Converts a list representation of a spring network into weighted matrices representing the stiffness and unstretched lengths of the springs.

### NodesKLfromMatKL(K, L0)
Reconstructs the list of springs that compose the network from the stiffness and unstretched length matrices.

### plot_spring_network(hub, sizemass=True, idx=0, region=0, tini=0, tend=-1, returnFig=False)
Displays the spring network using Plotly, with options to animate the dynamics over time.

### plot_invariants(hub, returnFig=False)
Plots the invariant quantities of the spring network (e.g., kinetic energy, potential energy, momentum, barycenter) over time using Matplotlib.

### dictNodeSpring2(dic)
Converts a dictionary containing node and spring information into matrices for stiffness and unstretched lengths.

These functions allow you to create, analyze, and visualize the dynamics of a spring network efficiently and effectively.


## Presets

## Supplements
|                     | documentation                                                                                                | signature                                                               |
|:--------------------|:-------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| Springlist_to_K_L0  | Give a weighted matrix representation of a network from a list approach.                                     | (Node1, Node2, Nnodes, k=0, L0=0, damp=0, **kwargs)                     |
| plot_spring_network | Display the spring network dynamics using an animated plot.                                                  | (hub, sizemass=True, idx=0, region=0, tini=0, tend=-1, returnFig=False) |
| dictNode2SpringMat  | Convert a dictionary with node-spring information to include matrix representations that can feed the model. | (dic0)                                                                  |
| NodesKLfromMatKL    | Reconstruct the list of springs that composes the network represented in K and L0 matrices.                  | (K, L0)                                                                 |
| plot_invariants     | Plot the invariants of the spring network system over time.                                                  | (hub, returnFig=False)                                                  |
## Todo
* Nothing is done
* that should be done

## Equations
|             | eqtype       | definition                     | source_exp                                                                  | com   |
|:------------|:-------------|:-------------------------------|:----------------------------------------------------------------------------|:------|
| Nnodes      | size         | Number of nodes in the network |                                                                             |       |
| vx          | differential | horizontal velocity            | dvx/dt=Fx/m + Fdampx/m,                                                     |       |
| vy          | differential | vertical velocity              | dvy/dt=Fy/m + Fdampy/m,                                                     |       |
| x           | differential | horizontal position            | dx/dt=vx,                                                                   |       |
| y           | differential | vertical position              | dy/dt=vy,                                                                   |       |
| dx          | statevar     |                                | dx=x - np.moveaxis(x, -1, -2)),                                             |       |
| dy          | statevar     |                                | dy=y - np.moveaxis(y, -1, -2)),                                             |       |
| distance    | statevar     |                                | distance=(dx**2 + dy**2)**(1/2)),                                           |       |
| angle       | statevar     |                                | angle=np.arctan2(dy, dx)),                                                  |       |
| dvx         | statevar     |                                | dvx=vx - np.moveaxis(vx, -1, -2)),                                          |       |
| dvy         | statevar     |                                | dvy=vy - np.moveaxis(vy, -1, -2)),                                          |       |
| matspeed    | statevar     |                                | matspeed=(dvx**2 + dvy**2)**(1/2)),                                         |       |
| Fx          | statevar     |                                | Fx=O.ssum2(-Kmat*(distance-L0Mat)*np.cos(angle))),                          |       |
| Fy          | statevar     |                                | Fy=O.ssum2(-Kmat*(distance-L0Mat)*np.sin(angle))),                          |       |
| Fdampx      | statevar     |                                | Fdampx=O.ssum2(-dampMat*matspeed*np.cos(angle))),                           |       |
| Fdampy      | statevar     |                                | Fdampy=O.ssum2(-dampMat*matspeed*np.cos(angle))),                           |       |
| Kinetic     | statevar     |                                | Kinetic=0.5*np.sum(O.ssum(m*(vx**2 + vy**2))), axis=-2),                    |       |
| Potential   | statevar     |                                | Potential=0.25*np.sum(np.sum(Kmat*(distance-L0Mat)**2), axis=-1), axis=-2), |       |
| Baricenterx | statevar     |                                | Baricenterx=np.sum(x*m, axis=-2)/np.sum(m, axis=-2)),                       |       |
| Baricentery | statevar     |                                | Baricentery=np.sum(y*m, axis=-2)/np.sum(m, axis=-2)),                       |       |
| momentumx   | statevar     |                                | momentumx=np.sum(vx*m, axis=-2)),                                           |       |
| momentumy   | statevar     |                                | momentumy=np.sum(vy*m, axis=-2)),                                           |       |
| L0Mat       |              |                                |                                                                             |       |
| Kmat        |              |                                |                                                                             |       |
| m           |              |                                |                                                                             |       |
| dampMat     |              |                                |                                                                             |       |