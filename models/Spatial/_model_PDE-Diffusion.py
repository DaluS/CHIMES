"""1D Diffusion in space"""

_DESCRIPTION ="""
A simple 1D diffusion :

the system solves in 1D :
    $dC/dt = -D \nabla \nabla C$

It is more a proof of concept of what pygemmes can do in term of regions coupling.
A big part is still a bit sloppy.
"""

################# IMPORTS ##################################################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from pygemmes._models import Funcs, importmodel,mergemodel,filldimensions
from pygemmes._models import Operators as O

# ######################## LOGICS #######################################
_LOGICS = {
    'size': {
    },
    'differential': {
        'C': {
            'func': lambda lapC,diffCoeff : diffCoeff*lapC ,
            'com': 'uniform diffcoeff',
            'definition': 'Concentration',
            'initial':1,
        },
    },
    'statevar': {
        'gradCx': {
            'func': lambda C,nabla : O.Rmatmul(C,nabla),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapC': {
            'func': lambda gradCx,nabla : O.Rmatmul(gradCx,nabla),
        },
    },
    'parameter': {
        'diffCoeff'  :{'value': 0.02,},
        'x'          :{'value': 0},
        'nabla': {'value':0,
                  'definition': 'spatial operator',
                  'size':['nr']}
    },
}



def generate(diffcoeff,N):
    N=100
    # Spatial operator (should be normalized etc)
    nabla0=np.zeros((N,N))
    nabla0[np.arange(N-1) ,np.arange(N-1)+1]=1/2
    nabla0[np.arange(N-1)+1,np.arange(N-1)]=-1/2
    nabla0[-1,0]=1/2
    nabla0[0,-1]=-1/2
    nabla=np.zeros((1,N,N,1))
    nabla[0,:,:,0]=nabla0

    x=np.linspace(0,1,N, endpoint=False)
    # Concentration
    C0=np.exp(-50*(x-0.5)**2)
    C=np.zeros((1,N,1,1))
    C[0,:,0,0]=C0

    #C0=np.sin(2*np.pi*x)
    preset = {
        'nr':N,
        'dt':0.1,
        'nx':1,
        'diffCoeff':10,
        'C':C,
        'nabla':nabla,
        }
    return preset

def plot(hub):
    '''
    Minimal plot of the Concentration evolution
    '''
    import matplotlib.pyplot as plt
    R=hub.get_dparam()
    C=R['C']['value'][:,0,:,0,0]
    plt.pcolormesh(np.transpose(C)); 
    plt.colorbar()
    plt.ylabel('C(x)')
    plt.xlabel('time')
    plt.show()

_SUPPLEMENTS = { 
    'Plot'    : plot,
    'Generate': generate
}

_PRESETS = {
    'Basic': {
        'fields': generate(10,100),
        'com': ('A diffusion on 100 elements of a gaussian distribution'),
        'plots': {},
    },
}