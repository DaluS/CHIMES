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


_LOGICS_spatial = {
    'differential': {  # Differential variables are defined by their time derivative and not their value
        'N': lambda N, n, divPhiN: N*n+divPhiN,
    },
    'statevar': dict(  # State variables value are defined by their logic
        Ir=lambda Pi, p, divPhiI: (Pi+divPhiI)/p,

        divPhiI=lambda Nabla, PhiI, Dn, N, Laplacian: O.Rmatmul(PhiI, Nabla) + Dn * O.Rmatmul(N, Laplacian),
        divPhiN=lambda Nabla, PhiN, Di, Pi, Laplacian: O.Rmatmul(PhiN, Nabla) + Di * O.Rmatmul(Pi, Laplacian),

        PhiI=lambda PhipiI: PhipiI,
        PhiN=lambda PhiwN, PhilambdaN: PhiwN + PhilambdaN,

        PhiwN=lambda Nabla, muw, w, N: muw * (N/w) * O.Rmatmul(w, Nabla),
        PhilambdaN=lambda Nabla, mulambda, employment, N: mulambda * (N) * O.Rmatmul(employment, Nabla),
        PhipiI=lambda Nabla, mupi, pi, Y: mupi * (Y*pi) * O.Rmatmul(pi, Nabla),
    ),
    'parameter': dict(
        muw=0,
        mulambda=0,
        mupi=0,
        Di=0,
        Dn=0,
        Laplacian=dict(
            value=0,
            size=['nr']
            ),
        Nabla=dict(
            value=0,
            size=['nr']
            ),
        x=0,
    ),
}


def plot(hub):
    '''Plot time-slices of the concentration (horizontal time, vertical spatial).
    First concentration, second time variation, third gradient, fourth laplacian'''
    import matplotlib.pyplot as plt
    R = hub.get_dfields()
    employment = R['employment']['value'][:, 0, :, 0]
    omega = R['omega']['value'][:, 0, :, 0]
    Y = R['Y']['value'][:, 0, :, 0]
    # lapC = R['lapC']['value'][:, 0, :, 0]
    plt.figure()
    Tsim = -1
    plt.subplot(1, 3, 1)
    plt.pcolormesh(employment[:, :, 0])
    plt.colorbar()
    plt.xlabel(r'$\lambda$')
    plt.title(r'$\lambda$')
    plt.subplot(1, 3, 2)
    plt.pcolormesh(omega[:, :, 0])
    plt.colorbar()
    plt.xlabel(r'$\omega$')
    plt.title(r'$\omega$')
    plt.subplot(1, 3, 3)
    plt.pcolormesh(Y[:, :, 0])
    plt.colorbar()
    plt.xlabel(r'$Y$')
    plt.title(r'$Y$')
    plt.show()


def generate_Nabla(N):
    '''Generate a value for Nabla for N points'''
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
    return nabla, x


_SUPPLEMENTS = {
    'generate_Nabla': generate_Nabla,
    'plot': plot,
}

logicsgoodwin, presetgoodwin, supplementsgoodwin = importmodel('Goodwin_example')  # Will import locally the content of the model named 'Goodwin'
_LOGICS = merge_model(logicsgoodwin, _LOGICS_spatial, verb=False)     # Takes the equations of _LOGICS_GOODWIN and put them into _LOGICS
