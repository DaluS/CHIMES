"""Wave propagation with convection and diffusion in 1D"""

_DESCRIPTION ="""
Wave propagation with :
    * propagation speed 'c'
    * Convection 'v'
    * diffusion 'D'

the system solves in 1D (if v=D=0) :
    $d^2C/dt^2 - c**2 \nabla \nabla C = 0 $

It is more a proof of concept of what chimes can do in term of regions coupling.
A big part is still a bit sloppy.
"""

################# IMPORTS ##################################################
import numpy as np #(if you need exponential, pi, log, of matrix products...)
from chimes._models import Funcs, importmodel,mergemodel,filldimensions
from chimes._models import Operators as O

# ######################## LOGICS #######################################
_LOGICS = {
    'size': {
    },
    'differential': {
        'dC': {
            'func': lambda d2C : d2C ,
            'com': 'wave EQ',
            'definition': 'time derivative of C',
            'initial':0.0,
        },
        'C': {
            'func': lambda dC,diffCoeff,lapC,v,gradCx : dC+ diffCoeff*lapC + v * gradCx,
            'com': 'deduced from dt + diffusion',
            'definition': 'Concentration',
            'initial':0,
        },
    },
    'statevar': {
        'd2C' : {
            'func': lambda lapC,c : c**2*lapC,
            'com': 'wave EQ',
            'definition': 'time derivative of C',
        },
        'gradCx': {
            'func': lambda C,nabla : O.Rmatmul(C,nabla),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapC': {
            'func': lambda gradCx,nabla : O.Rmatmul(gradCx,nabla),
        },
    },
    'parameter': {
        'c'  :{'value': 3,},
        'x'          :{'value': 0},
        'diffCoeff': {'value':0.02},
        'v' : {'value':1},
        'nabla': {'value':0,
                  'definition': 'spatial operator',
                  'size':['nr']}
    },
}



def plot(hub):
    '''Plot time-slices of the concentration (horizontal time, vertical spatial). 
    First concentration, second time variation, third gradient, fourth laplacian'''
    import matplotlib.pyplot as plt
    R=hub.get_dparam()
    C=R['C']['value'][:,0,:,0]
    dC=R['dC']['value'][:,0,:,0]
    gradC=R['gradCx']['value'][:,0,:,0]
    lapC=R['lapC']['value'][:,0,:,0]
    plt.figure()
    Tmax=-1
    plt.subplot(4,1,1); plt.pcolormesh(np.transpose(C)[0,:,:Tmax]); plt.colorbar();plt.ylabel('C')
    plt.subplot(4,1,2); plt.pcolormesh(np.transpose(dC)[0,:,:Tmax]); plt.colorbar(); plt.ylabel(r'$\dfrac{\partial C}{\partial t}$')
    plt.subplot(4,1,3); plt.pcolormesh(np.transpose(gradC)[0,:,:Tmax]); plt.colorbar(); plt.ylabel(r'$\nabla C$')
    plt.subplot(4,1,4); plt.pcolormesh(np.transpose(lapC)[0,:,:Tmax]); plt.colorbar();plt.ylabel(r'$\nabla \nabla C$');plt.xlabel('time')
    plt.show()

def generate(diffcoeff,c,v,N):
    '''Generate all parameters for the simulation'''
    N=100
    # Spatial operator (should be normalized etc)
    nabla0=np.zeros((N,N))
    nabla0[np.arange(N-1) ,np.arange(N-1)+1]=1/2
    nabla0[np.arange(N-1)+1,np.arange(N-1)]=-1/2
    nabla0[-1,0]=1/2
    nabla0[0,-1]=-1/2
    nabla=np.zeros((1,N,N,1))
    nabla[0,:,:,0]=nabla0/5

    x=np.linspace(0,1,N, endpoint=False)
    # Concentration
    C0=np.exp(-50*(x-0.3)**2)
    C=np.zeros((1,N,1,1))
    C[0,:,0,0]=C0
    #C0=np.sin(2*np.pi*x)

    preset = {
        'nr':N,
        'dt':0.1,
        'Tmax':1000,
        'nx':1,
        'diffCoeff':diffcoeff,
        'C':C,
        'nabla':nabla,
        'c':c,
        'v':v
        }
    return preset

_SUPPLEMENTS = { 
    'Plot': plot,
    'Generate': generate
}

# ####################### PRESETS #######################################
_PRESETS = {
    'Basic': {
        'fields': generate(2,3,2,100),
        'com': ('A diffusion on 100 elements of a gaussian'),
        'plots': {},
    },
}