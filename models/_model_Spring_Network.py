"""Network of springs dynamics"""

from chimes.libraries import importmodel      # Import another model _LOGICS, _PRESETS
from chimes.libraries import Operators as O   # Prewritten operators for multisectoral and multiregional coupling. `chm.get_available_Operators()`
from chimes.libraries import fill_dimensions   # When using multisectoral dynamics, fill automatically the sizes of fields
from chimes.libraries import merge_model       # Merge two model logics into each others
from chimes.libraries import Funcs            # Prewritten functions from CHIMES use `chm.get_available_Functions()`
import numpy as np                          # if you need exponential, pi, log

_DESCRIPTION = _DESCRIPTION = """
## What is this model?

A Spring Network is an ensemble of nodes that are linked by springs. Springs, depending on their compression, will apply forces on the nodes they connect. These forces will then move the nodes, which changes the spring tensions. This model is a classic example of local wave propagation on a network structure.

## How can it be represented with vectors and matrices?

In this model:
* Each node \(i \in N_{nodes}\) has a position \((x_i, y_i)\), and a speed \((v^x_i, v^y_i)\).
* The dynamics follow a classic equation: 
\[ \dot{v}^x_i = \frac{F^x_i - \text{damp} \cdot v^y_i}{m_i} \]
where damp is fluid friction, and F is the force resulting from the spring network.

Springs are represented by tensors, not as individuals. We consider \(N_{springs}\) springs with four characteristics:
1. The index of their first node extremity \(I^1_j\)
2. The index of their second node extremity \(I^2_j\)
3. A stiffness \(k_j\)
4. An unstretched length \(L^0_j\)

Instead of calculating each spring individually using loops, we use matrices. Each node is considered to be linked to every other node, but with a default stiffness of 0.

Consequently, we define \(k_{ij}\) as the stiffness matrix of the network.

The dynamics are described by:
\[ \dot{v}_i = - \sum_j k_{ij} \left( \text{dist}(x_i, x_j) - L0_{ij} \right) \cos(\theta_i) - \eta v_i \]

with:
\[ \text{dist}(x_i, x_j) = \sqrt{(x_i - x_j )^2 + (y_i - y_j )^2} \]
\[ \theta_i = \text{atan}\left( \frac{(y_i - y_j)}{(x_i - x_j)} \right) \]

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
"""

_TODO = ['Nothing is done', 'that should be done']
_ARTICLE = "https://en.wikipedia.org/wiki/Spring_system"
_DATE = "2024/06/04"
_CODER = "Paul Valcke"
_KEYWORDS = ['Network', 'springs', 'mesh']

_LOGICS = dict(
    size=dict(
        Nnodes=dict(value=1,
                    definition='Number of nodes in the network'),
    ),
    differential=dict(
        vx=dict(
            func=lambda Fx, m, Fdampx: Fx/m + Fdampx/m,
            definition='horizontal velocity',
            initial=0),
        vy=dict(
            func=lambda Fy, m, Fdampy: Fy/m + Fdampy/m,
            definition='vertical velocity',
            initial=0),
        x=dict(
            func=lambda vx: vx,
            definition='horizontal position',
            initial=0),
        y=dict(
            func=lambda vy: vy,
            definition='vertical position',
            initial=0),
    ),
    statevar=dict(

        # Matrices of relationship between points
        dx=dict(func=lambda x: x - np.moveaxis(x, -1, -2)),
        dy=dict(func=lambda y: y - np.moveaxis(y, -1, -2)),
        distance=dict(func=lambda dx, dy: (dx**2 + dy**2)**(1/2)),

        angle=dict(func=lambda dx, dy: np.arctan2(dy, dx)),

        dvx=dict(func=lambda vx: vx - np.moveaxis(vx, -1, -2)),
        dvy=dict(func=lambda vy: vy - np.moveaxis(vy, -1, -2)),
        matspeed=dict(func=lambda dvx, dvy: (dvx**2 + dvy**2)**(1/2)),
        anglespeed=dict(func=lambda dvx, dvy: np.arctan2(dvy, dvx)),

        # Forces in the system
        Fx=dict(func=lambda Kmat, distance, L0Mat, angle: O.ssum2(-Kmat*(distance-L0Mat)*np.cos(angle))),
        Fy=dict(func=lambda Kmat, distance, L0Mat, angle: O.ssum2(-Kmat*(distance-L0Mat)*np.sin(angle))),
        # Fmx=dict(func=lambda Kmat, distance, L0Mat, angle: -Kmat*(distance-L0Mat)*np.cos(angle)),
        # Fmy=dict(func=lambda Kmat, distance, L0Mat, angle: -Kmat*(distance-L0Mat)*np.cos(angle)),
        Fdampx=dict(func=lambda dampMat, matspeed, anglespeed: O.ssum2(-dampMat*matspeed*np.cos(anglespeed))),
        Fdampy=dict(func=lambda dampMat, matspeed, anglespeed: O.ssum2(-dampMat*matspeed*np.sin(anglespeed))),

        # Scalar Invariants and quantities related to invariants
        Kinetic=dict(func=lambda m, vx, vy: 0.5*np.sum(O.ssum(m*(vx**2 + vy**2))), axis=-2),
        Potential=dict(func=lambda Kmat, distance, L0Mat: 0.25*np.sum(np.sum(Kmat*(distance-L0Mat)**2), axis=-1), axis=-2),
        Baricenterx=dict(func=lambda x, m: np.sum(x*m, axis=-2)/np.sum(m, axis=-2)),
        Baricentery=dict(func=lambda y, m: np.sum(y*m, axis=-2)/np.sum(m, axis=-2)),
        momentumx=dict(func=lambda vx, m: np.sum(vx*m, axis=-2)),
        momentumy=dict(func=lambda vy, m: np.sum(vy*m, axis=-2)),
    ),
    parameter=dict(
        L0Mat=1,
        Kmat=1,
        m=1,
        dampMat=0,
    )
)

Dimensions = {
    'scalar': ['Kinetic',
               'Potential',
               'momentumx',
               'momentumy',
               'Baricenterx',
               'Baricentery'],
    # 'vector': [],
    'matrix': ['L0Mat',
               'Kmat',
               'dampMat',

               'dx',
               'dy',
               'angle',
               'distance',

               'dvx',
               'dvy',
               'matspeed',
               'anglespeed'],
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nnodes'],
       'matrix': ['Nnodes', 'Nnodes']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)

# %% Supplements functions


def Springlist_to_K_L0(Node1, Node2, Nnodes, k=0, L0=0, damp=0, **kwargs):
    """
    Give a weighted matrix representation of a network from a list approach.

    Node1 and Node2 are the list of nodes at both extremity of the spring.
    k is the stiffness of the spring as a list.
    L0 is the length at which there is no force in the spring as a list.
    Nnodes is the number of nodes in the Network.

    Parameters
    ----------
    Node1 : array-like
        The indices of the first node of each spring.
    Node2 : array-like
        The indices of the second node of each spring.
    k : array-like
        The stiffness of each spring.
    L0 : array-like
        The unstretched length of each spring.
    Nnodes : int
        The number of nodes in the network.

    Returns
    -------
    tuple of np.ndarray
        A tuple containing:
        - k_matrix (np.ndarray): The stiffness matrix of the network.
        - L0_matrix (np.ndarray): The unstretched length matrix of the network.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-06-13
    """

    k_matrix = np.zeros((Nnodes, Nnodes))
    L0_matrix = np.zeros((Nnodes, Nnodes))
    Damp_matrix = np.zeros((Nnodes, Nnodes))

    k_matrix[Node1, Node2] = k
    k_matrix[Node2, Node1] = k

    L0_matrix[Node2, Node1] = L0
    L0_matrix[Node1, Node2] = L0

    Damp_matrix[Node1, Node2] = damp
    Damp_matrix[Node2, Node1] = damp

    return k_matrix, L0_matrix, Damp_matrix


def NodesKLfromMatKL(K, L0):
    """
    Reconstruct the list of springs that composes the network represented in K and L0 matrices.

    Parameters
    ----------
    K : np.ndarray
        The stiffness matrix of the network.
    L0 : np.ndarray
        The unstretched length matrix of the network.

    Returns
    -------
    tuple of list
        A tuple containing:
        - Node1 (list): Indices of the first node of each spring.
        - Node2 (list): Indices of the second node of each spring.
        - k (list): Stiffness of each spring.
        - L0 (list): Unstretched length of each spring.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-06-13
    """

    # Get the indices of the upper triangular part of the matrix, excluding the diagonal
    triu_indices = np.triu_indices_from(K, k=1)

    # Extract the values from the upper triangular part
    valuesK = K[triu_indices]
    valuesL = L0[triu_indices]
    # Filter out the zero values
    non_zero_mask = valuesK != 0
    Node1 = triu_indices[0][non_zero_mask]
    Node2 = triu_indices[1][non_zero_mask]
    k = valuesK[non_zero_mask]
    l0 = valuesL[non_zero_mask]
    return Node1, Node2, k, l0


def plot_spring_network(hub,
                        sizemass=True,
                        idx=0,
                        region=0,
                        tini=0,
                        tend=-1, returnFig=False):
    """
    Display the spring network dynamics using an animated plot.

    Parameters
    ----------
    hub : object
        The data hub containing the dynamic fields.
    sizemass : bool, optional
        If True, the size of the nodes in the plot will be proportional to their mass. Default is True.
    idx : int, optional
        Index for selecting a specific instance of the data. Default is 0.
    region : int, optional
        Index for selecting a specific region of the data. Default is 0.
    tini : int, optional
        Initial time index for the plot. Default is 0.
    tend : int, optional
        End time index for the plot. Default is -1.
    returnFig : bool, optional
        If True, the function returns the plotly figure object. If False, the plot is displayed. Default is False.

    Returns
    -------
    plotly.graph_objects.Figure or None
        The plotly figure object if returnFig is True, otherwise None.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-06-13
    """

    import plotly.graph_objects as go
    import numpy as np

    R = hub.get_dfields()
    nt = len(R['time']['value'][tini:tend, idx, region, 0, 0])
    x = R['x']['value'][tini:tend, idx, region, :, 0]
    y = R['y']['value'][tini:tend, idx, region, :, 0]
    fx = R['Fx']['value'][tini:tend, idx, region, :, 0]
    fy = R['Fy']['value'][tini:tend, idx, region, :, 0]
    m = R['m']['value'][idx, region, :, 0]
    K = R['Kmat']['value'][idx, region, :, :]
    L0 = R['L0Mat']['value'][idx, region, :, :]

    Node1, Node2, k, L0 = NodesKLfromMatKL(K, L0)
    Nspring = len(Node1)
    Springreldist = np.zeros((nt, Nspring))
    for k in range(Nspring):
        Springreldist[:, k] = ((x[:, Node1[k]]-x[:, Node2[k]])**2 +
                               (y[:, Node1[k]]-y[:, Node2[k]])**2)**(1/2)
        Springreldist[:, k] /= L0[k]

    # Function to create quiver plot
    def create_quiver(x, y, u, v, scale=0.2, color='black'):
        quivers = []
        for xi, yi, ui, vi in zip(x, y, u, v):
            quivers.append(go.Scatter(
                x=[xi, xi + ui*scale],
                y=[yi, yi + vi*scale],
                mode='lines',
                line=dict(color=color),
                showlegend=False
            ))
            # Add larger arrow head
            quivers.append(go.Scatter(
                x=[xi + ui*scale],
                y=[yi + vi*scale],
                mode='markers',
                marker=dict(size=10, color=color, symbol='star-triangle-up'),
                showlegend=False
            ))
        return quivers

    # Function to get color based on Springreldist value
    def get_color(value):
        value = 0.5*(1+np.tanh(100*(value-1)))
        # value = max(0, min(value, 3))  # Clamp the value between 0 and 3
        red = int(255 * value)
        blue = 255 - red
        return f'rgb({red}, 0, {blue})'

    def scatt(x, y, t, m, sizemass):
        return go.Scatter(
            x=x[t],
            y=y[t],
            mode='markers',
            marker=dict(size=10*m**(1/3), color='black') if sizemass else dict(size=10, color='black'),
            name='Nodes'
        )

    def springline(x, y, Node1, Node2, Springreldist, t):
        color = get_color(Springreldist[t, i])
        return go.Scatter(
            x=[x[t, Node1[i]], x[t, Node2[i]]],
            y=[y[t, Node1[i]], y[t, Node2[i]]],
            mode='lines',
            line=dict(width=1, color=color),
            showlegend=False
        )
    # Create initial scatter plot and quiver plot
    fig = go.Figure()

    fig.add_trace(scatt(x, y, 0, m, sizemass))                    # Add scatter plot for nodes
    quivers = create_quiver(x[0], y[0], fx[0], fy[0])   # Add quiver plot for forces
    for q in quivers:
        fig.add_trace(q)
    for i in range(Nspring):
        fig.add_trace(springline(x, y, Node1, Node2, Springreldist, 0))

    # Create frames for animation
    frames = []
    for t in range(nt):
        frame_data = [scatt(x, y, t, m, sizemass)]
        quivers = create_quiver(x[t], y[t], fx[t], fy[t])
        frame_data.extend(quivers)
        for i in range(Nspring):
            frame_data.append(springline(x, y, Node1, Node2, Springreldist, t))
        frames.append(go.Frame(data=frame_data, name=str(t)))

    # Update layout with fixed axis limits
    fig.update_layout(
        xaxis=dict(range=[np.min(x)-1, np.max(x)+1], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[np.min(y)-1, np.max(y)+1]),
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }],
        sliders=[{
            'steps': [{'args': [[f.name], {'frame': {'duration': 50, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                       'label': str(k),
                       'method': 'animate'} for k, f in enumerate(frames)],
            'active': 0,
            'transition': {'duration': 0},
            'x': 0.1,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'top'
        }]
    )

    fig.frames = frames

    if returnFig:
        return fig
    else:
        fig.show()


def plot_invariants(hub, returnFig=False):
    """
    Plot the invariants of the spring network system over time.
    Typically : 
    * Kinetic and Potential energy 
    * Baricenter position
    * momentum

    Parameters
    ----------
    hub : object
        The data hub containing the dynamic fields.
    returnFig : bool, optional
        If True, the function returns the matplotlib figure object. If False, the plots are displayed. Default is False.

    Returns
    -------
    matplotlib.figure.Figure or None
        The matplotlib figure object if returnFig is True, otherwise None.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-06-13
    """

    import matplotlib.pyplot as plt
    R = hub.get_dfields()
    t = R['time']['value'][:, 0, 0, 0, 0]
    Kinetic = R['Kinetic']['value'][:, 0, 0, 0, 0]
    Potential = R['Potential']['value'][:, 0, 0, 0, 0]
    Baricenterx = R['Baricenterx']['value'][:, 0, 0, 0, 0]
    Baricentery = R['Baricentery']['value'][:, 0, 0, 0, 0]
    momentumy = R['momentumy']['value'][:, 0, 0, 0, 0]
    momentumx = R['momentumx']['value'][:, 0, 0, 0, 0]

    plt.close('all')
    fig = plt.figure('Invariants', figsize=(10, 8))

    # Plot for energies
    plt.subplot(311)
    plt.plot(t, Kinetic, label='Kinetic Energy')
    plt.plot(t, Potential, label='Potential Energy')
    plt.plot(t, Kinetic + Potential, label='Total Energy')
    plt.legend()
    plt.ylabel('Energy')
    plt.title('Invariants of the Spring Network System')
    plt.tick_params(labelbottom=False)  # Remove x-ticks

    # Plot for barycenter
    plt.subplot(312)
    plt.plot(t, Baricenterx, label='x Barycenter')
    plt.plot(t, Baricentery, label='y Barycenter')
    plt.legend()
    plt.ylabel('Barycenter Position')
    plt.tick_params(labelbottom=False)  # Remove x-ticks

    # Plot for momentum
    plt.subplot(313)
    plt.plot(t, momentumx, label='x Momentum')
    plt.plot(t, momentumy, label='y Momentum')
    plt.legend()
    plt.ylabel('Momentum')
    plt.xlabel('Time')

    plt.tight_layout()  # Adjust subplots to fit in the figure area.

    if returnFig:
        return fig
    else:
        plt.show()
        return


def dictNode2SpringMat(dic0):
    """
    Convert a dictionary with node-spring information to include matrix representations that can feed the model.

    Parameters
    ----------
    dic : dict
        Dictionary containing keys 'Node1', 'Node2', 'k', 'L0', and 'Nnodes'.

    Returns
    -------
    dict
        The updated dictionary with keys 'Kmat' and 'Lmat', and without 'Node1', 'Node2', 'k', 'L0'.

    Author
    ------
    Paul Valcke

    Date
    ----
    2024-06-13
    """
    import copy
    dic = copy.deepcopy(dic0)  # avoid modyfication of the original dictionary

    dic['Kmat'], dic['L0Mat'], dic['dampMat'] = Springlist_to_K_L0(dic['Node1'], dic['Node2'], dic['Nnodes'], dic['k'], dic['L0'], dic['damp'])
    del dic['Node1'], dic['Node2'], dic['k'], dic['L0']
    return dic


_SUPPLEMENTS = {'Springlist_to_K_L0': Springlist_to_K_L0,
                'plot_spring_network': plot_spring_network,
                'dictNode2SpringMat': dictNode2SpringMat,
                'NodesKLfromMatKL': NodesKLfromMatKL,
                'plot_invariants': plot_invariants}

# %% Presets
_PRESETS = {
    'OneOscillation': {
        'com': 'One moving mass on a spring, one direction',
        'fields': dictNode2SpringMat(dict(
            Nnodes=2,
            x=np.array([0., 1.]),  # initial positions
            y=np.array([0., 0.]),
            vx=np.array([0., 0.]),  # initial velocities
            vy=np.array([0., 0.]),
            m=np.array([10000., 1.]),  # masses

            # Springs
            Nsprings=1,  # number of springs
            Node1=np.array([0]),  # first node index of the spring
            Node2=np.array([1]),  # second node index of the spring
            k=np.array([10.0]),  # stiffness
            L0=np.array([1.4]),  # rest length
            damp=np.array([0.0]),

            dt=0.1,
            Tsim=30
        )) ,
        'plots': {'plot_invariants': [{}],
                  'plot_spring_network': [{'idx':0}]}
    }
}
