"""Nbody-gravity dynamics model"""

from chimes.libraries import importmodel      # Import another model _LOGICS, _PRESETS
from chimes.libraries import Operators as O   # Prewritten operators for multisectoral and multiregional coupling. `chm.get_available_Operators()`
from chimes.libraries import fill_dimensions   # When using multisectoral dynamics, fill automatically the sizes of fields
from chimes.libraries import merge_model       # Merge two model logics into each others
from chimes.libraries import Funcs            # Prewritten functions from CHIMES use `chm.get_available_Functions()`
import numpy as np                          # if you need exponential, pi, log

_DESCRIPTION = r"""
## What is this model?

A Spring Network is an ensemble of nodes that are linked by springs. Springs, depending on their compression, will apply forces on the nodes they connect. 
These forces will then move the nodes, which changes the spring tensions. This model is a classic example of local wave propagation on a network structure.

## How can it be represented with vectors and matrices?

Each element $i$ is a node of mass $m_i$ at position $(x_i, y_i)$ and velocity $(v^x_i, v^y_i)$.

They are in a gravity field $G$

In consequence, the forces are:

$$a^x_i = \sum_j G  m_j r_{ij}^{-2} \cos(\theta_{ij}) - \eta_i v^x_i$$
$$a^y_i = \sum_j G  m_j r_{ij}^{-2} \sin(\theta_{ij}) - \eta_i v^y_i $$
$$\dot{v}^x_i = a^x_i$$
$$\dot{v}^y_i = a^y_i$$
$$\dot{x}^x_i = v^x_i$$
$$\dot{x}^y_i = v^y_i$$

with :

$$r_{ij}^{-2} = ((x_i - x_j )^2 + (y_i - y_j ))^{-1}$$

We suppose that $G=1$ in this calculation

## Why is it a great archetypal model?

The N-body gravity dynamics model is essential for simulating the behavior of celestial bodies under gravitational influence. 
It provides insights into complex systems such as planetary orbits, galaxy formations, and stellar interactions. 
This model serves as a foundational tool in astrophysics, cosmology, and computational physics for understanding the dynamics of gravitational interactions at various scales.
"""

_TODO = [' ']
_ARTICLE = "https://en.wikipedia.org/wiki/N-body_problem"
_DATE = "2024/06/13"
_CODER = "Paul Valcke"
_KEYWORDS = ['Nbody', 'physics', 'chaos']

_LOGICS = dict(
    size=dict(
        Nbody=dict(value=1,
                   definition='Number of interacting bodies'),
    ),
    differential=dict(
        vx=dict(
            func=lambda Fx, m: Fx/m,
            definition='horizontal velocity',
            initial=0.),
        vy=dict(
            func=lambda Fy, m: Fy/m,
            definition='vertical velocity',
            initial=0.),
        x=dict(
            func=lambda vx: vx,
            definition='horizontal position',
            initial=0.),
        y=dict(
            func=lambda vy: vy,
            definition='vertical position',
            initial=0),
    ),
    statevar=dict(

        # Matrices of relationship between points
        dx=dict(func=lambda x: x - np.moveaxis(x, -1, -2)),
        dy=dict(func=lambda y: y - np.moveaxis(y, -1, -2)),
        heavi=lambda distance: np.heaviside(distance-0.01, 0),
        distance=dict(func=lambda dx, dy:  (dx**2 + 0.000001 + dy**2)**(1/2)),
        rm2=dict(func=lambda distance: np.heaviside(distance-0.01, 0) * distance**(-2)),
        angle=dict(func=lambda dx, dy: np.arctan2(dy, dx)),

        # Forces in the system
        Fx=dict(func=lambda m, rm2, angle: O.ssum2(-m*np.moveaxis(m, -1, -2)*rm2*np.cos(angle))),
        Fy=dict(func=lambda m, rm2, angle: O.ssum2(-m*np.moveaxis(m, -1, -2)*rm2*np.sin(angle))),

        # Scalar Invariants and quantities related to invariants
        Kinetic=dict(func=lambda m, vx, vy: 0.5*np.sum(O.ssum(m*(vx**2 + vy**2))), axis=-2),
        Potential=dict(func=lambda m, distance: 0.25*np.sum(np.sum(-m*np.moveaxis(m, -1, -2)), axis=-1), axis=-2),
        #Baricenterx=dict(func=lambda x, m: np.sum(x*m, axis=-2)/np.sum(m, axis=-2)),
        #Baricentery=dict(func=lambda y, m: np.sum(y*m, axis=-2)/np.sum(m, axis=-2)),
        #momentumx=dict(func=lambda vx, m: np.sum(vx*m, axis=-2)),
        #momentumy=dict(func=lambda vy, m: np.sum(vy*m, axis=-2)),
    ),
    parameter=dict(
        m=1.,
    )
)

Dimensions = {
    'scalar': ['Kinetic',
               'Potential',
               #'momentumx',
               #'momentumy',
               #'Baricenterx',
               #'Baricentery'
               ],
    # 'vector': [],
    'matrix': ['dx',
               'dy',
               'angle',
               'distance',
               'rm2',
               'heavi'],
}
DIM = {'scalar': ['__ONE__'],
       'vector': ['Nbody'],
       'matrix': ['Nbody', 'Nbody']}
_LOGICS = fill_dimensions(_LOGICS, Dimensions, DIM)

# %% Supplements functions


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


_SUPPLEMENTS = {'plot_invariants': plot_invariants}

# %% Presets
_PRESETS = {
    'OneOscillation': {
        'com': '',
        'fields': dict(),
        'plots': {'plot_invariants': [{}],
                  }
    }
}
