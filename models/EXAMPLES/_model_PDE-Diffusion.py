"""Spatial Diffusion Dynamics using Partial differential equations"""

import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O

_DESCRIPTION = """
CHIMES can Solve PDE, using regions as points on a grid similar to a finite difference method of resolution. 
https://en.wikipedia.org/wiki/Finite_difference_method, using explicit schemas. 

The equation solve is : 

    $$dC(x,t)/dt = -D [\nabla [\nabla C(x,t)]]$$
    
Nabla is a spatial operator represented by a matrix, and [] correspond to the matrix product. 
The type of schemas and the property of space are located here in the definition of nabla. 

When the model is initialized, there is no spatiality. It's only when applying a preset that the PDE aspect shines. 

The spatial coupling is done by CHIMES operators that begins with R (for regional)

"""

_TODO = ['Generalization of nabla', 'plotly plots']
_ARTICLE = "https://en.wikipedia.org/wiki/Heat_equation"
_DATE = "2024/01/22"
_CODER = "Paul Valcke"
_KEYWORDS = ['PDE', 'Phyics', 'Tutorial',]


# ######################## LOGICS #######################################
_LOGICS = dict(
    size=dict(),  # regional size is already deined by default in the system
    differential=dict(
        C=dict(
            func=lambda lapC, diffCoeff: diffCoeff * lapC,
            com='uniform diffcoeff',
            definition='Concentration',
            initial=1,
        ),
    ),
    statevar=dict(
        gradC=dict(
            func=lambda C, nabla: O.Rmatmul(C, nabla),
            definition='1d gradient of C',
            com='calculated with nabla matrix multiplication'),
        lapC=lambda gradC, nabla: O.Rmatmul(gradC, nabla),
    ),
    parameter=dict(
        diffCoeff=0.02,
        x=0,
        nabla={'value': 0,
               'definition': 'spatial operator',
               'size': ['nr']}
    ),
)


def generate(diffcoeff, N):
    '''
    Generate a minimal conditions'''

    N = 100
    # Spatial operator (should be normalized etc)
    nabla0 = np.zeros((N, N))
    nabla0[np.arange(N - 1), np.arange(N - 1) + 1] = 1 / 2
    nabla0[np.arange(N - 1) + 1, np.arange(N - 1)] = -1 / 2
    nabla0[-1, 0] = 1 / 2
    nabla0[0, -1] = -1 / 2
    nabla = np.zeros((1, N, N, 1))
    nabla[0, :, :, 0] = nabla0

    x = np.linspace(0, 1, N, endpoint=False)
    # Concentration
    C0 = np.exp(-50 * (x - 0.5)**2)
    C = np.zeros((1, N, 1, 1))
    C[0, :, 0, 0] = C0

    # C0=np.sin(2*np.pi*x)
    preset = {
        'nr': N,
        'dt': 0.1,
        'nx': 1,
        'diffCoeff': 10,
        'C': C,
        'nabla': nabla,
    }
    return preset


def plot(hub):
    '''
    Minimal plot of the Concentration evolution
    '''
    import matplotlib.pyplot as plt
    R = hub.get_dfields()
    C = R['C']['value'][:, 0, :, 0, 0]
    plt.pcolormesh(np.transpose(C))
    plt.colorbar()
    plt.ylabel('C(x)')
    plt.xlabel('time')
    plt.show()


_SUPPLEMENTS = {
    'Plot': plot,
    'Generate': generate
}

_PRESETS = {
    'Basic': {
        'fields': generate(10, 100),
        'com': ('A diffusion on 100 elements of a gaussian distribution'),
        'plots': {},
    },
}
