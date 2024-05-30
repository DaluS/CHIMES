
"""
A simple 1D diffusion :

the system solves in 1D :
    $dC/dt = -D \nabla \nabla C$

It is more a proof of concept of what chimes can do in term of regions coupling.
A big part is still a bit sloppy.

I recommend :
```
hub=pgm.Hub('Diffusion',preset='Basic')
hub.run()
R=hub.get_dfields()
C=R['C']['value'][:,0,:,0,0]
for i in range(9):
    plt.plot(C[100*i,:],label=i)
plt.legend()
plt.show()
```
"""
import numpy as np
# ######################## OPERATORS ####################################
'''
Those are operators that can be used to do multisectoral operations :
coupling, transposition, sums...
'''


def matmul(M, V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M, V)


def Rmatmul(nabla, C):
    '''Matrix product but with the axis of Regions rather than multisectoral'''
    return matmul(np.swapaxes(nabla, -3, -1),
                  np.swapaxes(C, -3, -2))


# #######################################################################
# The loop to merge the two dictionnaries
def MERGE(Recipient, dictoadd, override=True, verb=True):
    '''
    If you mix two models or want to add new auxlliary logics,
    you can merge your two dictionnaries.

    override : true will replace previous fields with new one if conflict such as :
        * another definition with the same type of logic (ODE, statevar)
        * change of logic type (transform a statevar to an ODE)

    Recipient is _LOGICS that you want to fill
    dicttoadd contains the new elements you want
    '''
    # Category of the variable in a dict
    keyvars = {k: v.keys() for k, v in Recipient.items()}
    typ = {}
    for k, v in keyvars.items():
        for vv in v:
            typ[vv] = k
    # Merging dictionnaries
    for category, dic in dictoadd.items():  # LOOP ON [SECTOR SIZE,ODE,STATEVAR,PARAMETERS]
        for k, v in dic.items():  # LOOP ON THE FIELDS
            if k in typ.keys():  # IF FIELD ALREADY EXIST
                if override:
                    if verb:
                        print(f'Override {category} variable {k}. Previous :{Recipient[category][k]} \n by :{v}')
                    Recipient[category][k] = v
                if typ[k] != category:
                    if verb:
                        print(f'Category change for logic of {k} : from {typ[k]} to {category}')
                    del Recipient[typ[k]][k]
                elif verb:
                    print(f'Keeping old definition {category} variable {k}. Previous :{Recipient[category][k]} \n {v}')
            else:  # IF FIELD DOES NOT
                Recipient[category][k] = v
    return Recipient


# #######################################################################
# #######################################################################
# #######################################################################


# #### AUXILLIARY FIELDS THAT ARE NOT NECESSARY TO COMPUTE THE SYSTEM,
# ARE PRACTICAL TO EXPLORE IT
_LOGICS = {
    'size': {
    },
    'differential': {
        'C': {
            'func': lambda lapxC, lapyC, diffCoeff: diffCoeff * (lapxC + lapyC),
            'com': 'uniform diffcoeff',
            'definition': 'Concentration',
            'initial': 1,
        },
    },
    'statevar': {
        'gradCx': {
            'func': lambda C, nablax: Rmatmul(C, nablax),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'gradCy': {
            'func': lambda C, nablay: Rmatmul(C, nablay),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapxC': {
            'func': lambda C, lapx: Rmatmul(C, lapx),
        },
        'lapyC': {
            'func': lambda C, lapy: Rmatmul(C, lapy),
        },
    },
    'parameter': {
        'diffCoeff': {'value': 0.02, },
        'x': {'value': 0},
        'y': {'value': 0},
        'nablax': {'value': 0,
                   'definition': 'spatial operator',
                   'size': ['nr']},
        'nablay': {'value': 0,
                   'definition': 'spatial operator',
                   'size': ['nr']},
        'lapx': {'value': 0,
                 'definition': 'spatial operator',
                 'size': ['nr']},
        'lapy': {'value': 0,
                 'definition': 'spatial operator',
                 'size': ['nr']},
    },
}

# MATRIX PREPARATION
N = 50
NN = N * N
dx = 1 / N
X = np.linspace(0, 1, N, endpoint=False)
Y = np.linspace(0, 1, N, endpoint=False)
XX, YY = np.meshgrid(X, Y)

X2 = XX.reshape(-1)
Y2 = YY.reshape(-1)

# Spatial operator (should be normalized etc)


# THOSE TWO SEEMS TO BE NOT WORKING
diffmatX = np.zeros((NN, NN))
diffmatX[np.arange(NN) % NN, (np.arange(NN) + 1) % NN] = 1 / (2 * dx)
diffmatX[(np.arange(NN) + 1) % NN, np.arange(NN) % NN] = -1 / (2 * dx)
diffmatY = np.zeros((NN, NN))
diffmatY[(np.arange(NN)) % NN, (N + np.arange(NN)) % NN] = 1 / (2 * dx)
diffmatY[(N + np.arange(NN)) % NN, (np.arange(NN)) % NN] = -1 / (2 * dx)
nablax = np.zeros((1, NN, NN, 1))
nablax[0, :, :, 0] = diffmatX
nablay = np.zeros((1, NN, NN, 1))
nablay[0, :, :, 0] = diffmatY * 0

# LAPLACIAN IS WORKING
lapX = np.zeros((NN, NN))
lapX[np.arange(NN) % NN, np.arange(NN) % NN] = -2
lapX[(np.arange(NN) + 1) % NN, np.arange(NN) % NN] = 1
lapX[(np.arange(NN)) % NN, (np.arange(NN) + 1) % NN] = 1

lapY = np.zeros((NN, NN))
lapY[np.arange(NN) % NN, np.arange(NN) % NN] = -2
lapY[(np.arange(NN) + N) % NN, np.arange(NN) % NN] = 1
lapY[(np.arange(NN)) % NN, (np.arange(NN) + N) % NN] = 1
Lapx = np.zeros((1, NN, NN, 1))
Lapx[0, :, :, 0] = lapX
Lapy = np.zeros((1, NN, NN, 1))
Lapy[0, :, :, 0] = lapY

ZZ = np.exp(- 50 * (np.sqrt((XX - 0.5)**2 + (YY - 0.5)**2)))
C = np.zeros((1, NN, 1, 1))
C[0, :, 0, 0] = ZZ.reshape(-1)
Y = np.zeros((1, NN, 1, 1))
Y[0, :, 0, 0] = Y2
X = np.zeros((1, NN, 1, 1))
X[0, :, 0, 0] = X2

preset_basis = {
    'nr': NN,
    'dt': 0.1,
    'Tsim': 10,
    'nx': 1,
    'x': X,
    'y': Y,
    'diffCoeff': 0.1,
    'C': C,
    'nablax': nablax,
    'nablay': nablay,
    'lapx': Lapx,
    'lapy': Lapy,
}
_PRESETS = {
    'Basic': {
        'fields': preset_basis,
        'com': ('A diffusion on 100 elements of a gaussian'),
        'plots': {},
    },
}
