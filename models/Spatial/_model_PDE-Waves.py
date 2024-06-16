"""Wave propagation with convection and diffusion"""
# ################ IMPORTS ##################################################
from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O

_DESCRIPTION = r"""## What is this model?

A 2D Periodic Convection-Diffusion model describes the transport and diffusion of a scalar field (e.g., temperature, concentration) in a 2D plane with periodic boundary conditions. This model combines the effects of convection (transport by fluid flow) and diffusion (spreading due to concentration gradients), and is widely used to simulate processes in fluid dynamics, meteorology, and environmental science.

## How can it be represented with vectors and matrices?

In this model:
* The scalar field $C(x, y, t)$ evolves over time according to the convection-diffusion equation.
* The velocity field $ \mathbf{u}(x, y) = (u_x(x, y), u_y(x, y)) $ represents the fluid flow.
* The dynamics follow the convection-diffusion equation: 
$$
\frac{\partial C}{\partial t} + \mathbf{u} \cdot \nabla C = D \nabla^2 C
$$
where $D$ is the diffusion coefficient.

The finite difference method is used to discretize the spatial domain into a grid of points:
* $X$ and $Y$ are 1D arrays representing the non-uniform grid points in the $x$ and $y$ directions.
* The gradient and Laplacian operators are represented by sparse matrices, allowing efficient computation of spatial derivatives.

### Gradient Operators:
The gradient operators $ \nabla_x $ and $ \nabla_y $ are constructed to compute the spatial derivatives:
$$
\nabla_x C \approx \frac{C(x + \Delta x, y) - C(x, y)}{\Delta x}
$$
$$
\nabla_y C \approx \frac{C(x, y + \Delta y) - C(x, y)}{\Delta y}
$$

### Laplacian Operator:
The Laplacian operator $ \nabla^2 $ is constructed as:
$$
\nabla^2 C \approx \frac{C(x + \Delta x, y) - 2C(x, y) + C(x - \Delta x, y)}{\Delta x^2} + \frac{C(x, y + \Delta y) - 2C(x, y) + C(x, y - \Delta y)}{\Delta y^2}
$$

## Why is it a great archetypal model?

The 2D Periodic Convection-Diffusion model is an excellent archetype for studying transport phenomena in fluid dynamics. It captures the essential physics of convection and diffusion, making it a versatile tool for understanding complex processes in natural and engineered systems. 
The periodic boundary conditions simplify the computational domain while preserving key dynamic behaviors.

"""


# ######################## LOGICS #######################################
_LOGICS = {
    'size': {
    },
    'differential': {
        'dC': {
            'func': lambda d2C: d2C,
            'com': 'wave EQ',
            'definition': 'time derivative of C',
            'initial': 0.0,
        },
        'C': {
            'func': lambda dC, diffCoeff, lapC, v, gradCx: dC + diffCoeff * lapC + v * gradCx,
            'com': 'deduced from dt + diffusion',
            'definition': 'Concentration',
            'initial': 0,
        },
    },
    'statevar': {
        'd2C': {
            'func': lambda lapC, c: c**2 * lapC,
            'com': 'wave EQ',
            'definition': 'time derivative of C',
        },
        'gradCx': {
            'func': lambda C, nabla: O.Rmatmul(C, nabla),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapC': {
            'func': lambda gradCx, nabla: O.Rmatmul(gradCx, nabla),
        },
    },
    'parameter': {
        'c': {'value': 3, },
        'x': {'value': 0},
        'diffCoeff': {'value': 0.02},
        'v': {'value': 1},
        'nabla': {'value': 0,
                  'definition': 'spatial operator',
                  'size': ['nr']}
    },
}


def plot(hub):
    '''Plot time-slices of the concentration (horizontal time, vertical spatial).
    First concentration, second time variation, third gradient, fourth laplacian'''
    import matplotlib.pyplot as plt
    R = hub.get_dfields()
    C = R['C']['value'][:, 0, :, 0]
    dC = R['dC']['value'][:, 0, :, 0]
    gradC = R['gradCx']['value'][:, 0, :, 0]
    lapC = R['lapC']['value'][:, 0, :, 0]
    plt.figure()
    Tsim = -1
    plt.subplot(4, 1, 1)
    plt.pcolormesh(np.transpose(C)[0, :, :Tsim])
    plt.colorbar()
    plt.ylabel('C')
    plt.subplot(4, 1, 2)
    plt.pcolormesh(np.transpose(dC)[0, :, :Tsim])
    plt.colorbar()
    plt.ylabel(r'$\dfrac{\partial C}{\partial t}$')
    plt.subplot(4, 1, 3)
    plt.pcolormesh(np.transpose(gradC)[0, :, :Tsim])
    plt.colorbar()
    plt.ylabel(r'$\nabla C$')
    plt.subplot(4, 1, 4)
    plt.pcolormesh(np.transpose(lapC)[0, :, :Tsim])
    plt.colorbar()
    plt.ylabel(r'$\nabla \nabla C$')
    plt.xlabel('time')
    plt.show()


def generate(diffcoeff, c, v, N):
    '''Generate all parameters for the simulation'''
    N = 100
    # Spatial operator (should be normalized etc)
    nabla0 = np.zeros((N, N))
    nabla0[np.arange(N - 1), np.arange(N - 1) + 1] = 1 / 2
    nabla0[np.arange(N - 1) + 1, np.arange(N - 1)] = -1 / 2
    nabla0[-1, 0] = 1 / 2
    nabla0[0, -1] = -1 / 2
    nabla = np.zeros((1, N, N, 1))
    nabla[0, :, :, 0] = nabla0 / 5

    x = np.linspace(0, 1, N, endpoint=False)
    # Concentration
    C0 = np.exp(-50 * (x - 0.3)**2)
    C = np.zeros((1, N, 1, 1))
    C[0, :, 0, 0] = C0
    # C0=np.sin(2*np.pi*x)

    preset = {
        'nr': N,
        'dt': 0.1,
        'Tsim': 1000,
        'nx': 1,
        'diffCoeff': diffcoeff,
        'C': C,
        'nabla': nabla,
        'c': c,
        'v': v
    }
    return preset


_SUPPLEMENTS = {
    'Plot': plot,
    'Generate': generate
}

# ####################### PRESETS #######################################
_PRESETS = {
    'Basic': {
        'fields': generate(2, 3, 2, 100),
        'com': ('A diffusion on 100 elements of a gaussian'),
        'plots': {},
    },
}
