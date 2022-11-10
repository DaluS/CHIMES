# -*- coding: utf-8 -*-
"""
Wave propagation with :
    * propagation speed 'c'
    * Convection 'v'
    * diffusion 'D'

the system solves in 1D (if v=D=0) :
    $d^2C/dt^2 - c**2 \nabla \nabla C = 0 $

It is more a proof of concept of what pygemmes can do in term of regions coupling.
A big part is still a bit sloppy.

I recommend :
```
hub=pgm.Hub('PDE-Waves',preset='Basic')
hub.run()
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
```
"""

# ######################## PRELIMINARY ELEMENTS #########################
import numpy as np
from pygemmes._models import Funcs, importmodel,mergemodel

# ######################## OPERATORS ####################################
'''
Those are operators that can be used to do multisectoral operations : 
coupling, transposition, sums... 
'''
def matmul(M,V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M,V)
def Rmatmul(nabla,C):
    '''Matrix product but with the axis of Regions rather than multisectoral'''
    return matmul(np.swapaxes(nabla, -3, -1),
                  np.swapaxes(C, -3, -2))


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
            'func': lambda C,nabla : Rmatmul(C,nabla),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapC': {
            'func': lambda gradCx,nabla : Rmatmul(gradCx,nabla),
        },
    },
    'parameter': {
        'c'  :{'value': 3,},
        'x'          :{'value': 0},
        'diffCoeff': {'value':0.02},
        'v' : {'value':0.1},
        'nabla': {'value':0,
                  'definition': 'spatial operator',
                  'size':['nr']}
    },
}

# ####################### PRESETS #######################################
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

preset_basis = {
    'nr':N,
    'dt':0.1,
    'Tmax':1000,
    'nx':1,
    'diffCoeff':10,
    'C':C,
    'nabla':nabla,
    }
_PRESETS = {
    'Basic': {
        'fields': preset_basis,
        'com': ('A diffusion on 100 elements of a gaussian'),
        'plots': {},
    },
}