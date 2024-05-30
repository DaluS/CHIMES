'''

Model of self-propagating inflation in the cast of a cost-pushed inflation


'''


import numpy as np


def Identity(X):
    '''generate an identity matrix of the same size a matrix X'''
    return np.eye(np.shape(X)[-1])


def matmul(M, V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M, V)


_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    'differential': {
        'mu': {
            'func': lambda mu, costpushi, vec, M, residue: (mu**2) * (matmul(M, (costpushi + residue) * vec)) / vec,
            'size': ['Nprod'],
            'com': '',
            'symbol': r'$\mu$',
            'initial': 1,
        },
    },
    'statevar': {
        'inverseM': {
            'func': lambda M: np.linalg.inv(M),
            'size': ['Nprod', 'Nprod'],
            'com': '',
        },
        'M': {
            'func': lambda mu, Xi, nu, delta, Gamma: matmul(Identity(Gamma), 1 / mu) - Gamma - nu * delta * Xi,
            'size': ['Nprod', 'Nprod'],
            'com': '',
        },
        'vec': {
            'func': lambda inverseM, z, b: matmul(inverseM, z / b),
            'size': ['Nprod'],
            'com': '',
        },
        'costpushi': {
            'func': lambda mu, mu0, eta: eta * (mu0 / mu - 1),
            # 'func': lambda mu,mu0,eta : eta*np.log(mu0/mu),
            'size': ['Nprod'],
            'com': '',
            'units': 'y^{-1}',
            'symbol': r'$i^{\mu}$',
        }
    },
    'parameter': {
        'residue': {
            'value': -0,
            'definition': 'Everything else'
        }
    },
}

for par in ['nu', 'mu0', 'z', 'b', 'delta']:
    _LOGICS['parameter'][par] = {'size': ['Nprod']}
for par in ['Xi', 'Gamma']:
    _LOGICS['parameter'][par] = {'size': ['Nprod', 'Nprod']}


Nsector = 5
Gamma = np.zeros((Nsector, Nsector))
vec = np.arange(0, Nsector - 2)
Gamma[vec, 1 + vec] = 0.1

base = {
    'Nprod': [str(i) for i in range(Nsector)],
    'nu': 3,
    'z': 1,
    'b': 1,
    'mu0': 1.5,
    'mu': [1.5, 1.5, 1.5, 1.5, 1.4],
    'delta': 0.05,
    'Xi': np.zeros((Nsector, Nsector)) + np.array([0 for i in range(Nsector - 1)] + [1]),
    'Gamma': np.eye(Nsector) * 0.1,
    'Tsim': 3,
    'dt': 0.01,
}

_PRESETS = {
    'Monosectoral': {
        'fields': {
            'Nprod': ['Mono'],
            'nu': 3,
            'z': 1,
            'b': 1,
            'mu0': 1.3,
            'mu': 1,
            'delta': 0.05,
            'Xi': 1,
            'Gamma': 0,
        },
        'com': '',
        'plots': {},
    },
    'Bisectoral': {
        'fields': {
            'Nprod': ['Consumption', 'Capital'],
            'nu': [3, 3],
            'z': [1, 1],
            'b': [1, 1],
            'mu0': [1.3, 1.3],
            'mu': [1, 1.1],
            'delta': [0.05, 0.05],
            'Xi': [[0, 1],
                   [0, 1]],
            'Gamma': [[0, 0],
                      [0, 0]],
            'eta': [1, 1]
        },
        'com': '',
        'plots': {},
    },
    'Manysectors': {
        'fields': base,
        'com': '',
        'plots': {}
    },
}
