"""Shallow Water equations"""
# ################ IMPORTS ##################################################
from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O
_DESCRIPTION = """
https://en.m.wikipedia.org/wiki/Shallow_water_equations

$$\frac{\partial h}{\partial t} &+ \frac{\partial}{\partial x} \Bigl( (H+h) u \Bigr) + \frac{\partial}{\partial y} \Bigl( (H+h) v \Bigr) = 0$$
$$\frac{\partial u}{\partial t} &+ u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y}  = -g \frac{\partial h}{\partial x} - u + \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$
$$\frac{\partial v}{\partial t} &+ u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} u = -g \frac{\partial h}{\partial y} - k v + \nu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right)$$
"""


# ######################## LOGICS #######################################
_LOGICS = {
    'size': {
    },
    'differential': {
        'h': dict(func=lambda nablax, nablay, H, h, u, v: -O.Rmatmul((H+h)*u, nablax)-O.Rmatmul((H+h)*v, nablay),
                  definition='wave height',
                  initial=0.0,
                  ),

        'u': dict(fun=lambda hx, u, v, ux, uy, uxx, uyy, g, k, nu: -g*hx-k*u+nu*(uxx+uyy)-u*ux-v*uy,
                  ),
        'v': dict(fun=lambda hy, u, v, vx, vy, vxx, vyy, g, k, nu: -g*hy-k*u+nu*(vxx+vyy)-u*vx-v*vy,
                  ),

    },
    'statevar': {
        'ux': dict(lambda u, nablax: O.Rmatmul(u, nablax)),
        'uy': dict(lambda u, nablay: O.Rmatmul(u, nablay)),
        'vx': dict(lambda v, nablax: O.Rmatmul(v, nablax)),
        'vy': dict(lambda v, nablay: O.Rmatmul(v, nablay)),
        'hx': dict(lambda h, nablax: O.Rmatmul(h, nablax)),
        'hy': dict(lambda h, nablay: O.Rmatmul(h, nablay)),

        'uxx': dict(lambda ux, nablax: O.Rmatmul(ux, nablax)),
        'uyy': dict(lambda uy, nablay: O.Rmatmul(uy, nablay)),
        'vxx': dict(lambda vx, nablax: O.Rmatmul(vx, nablax)),
        'vyy': dict(lambda vy, nablay: O.Rmatmul(vy, nablay)),
    },
    'parameter': {
        'H': dict(value=3),
        'g': dict(value=10),
        'nu': dict(value=1),
        'nablax': {'value': 0,
                   'definition': 'spatial operator',
                   'size': ['nr']},
        'nablay': {'value': 0,
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
