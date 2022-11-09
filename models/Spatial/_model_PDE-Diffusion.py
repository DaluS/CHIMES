# -*- coding: utf-8 -*-
"""
A simple 1D diffusion :

the system solves in 1D :
    $dC/dt = -D \nabla \nabla C$

It is more a proof of concept of what pygemmes can do in term of regions coupling.
A big part is still a bit sloppy.

I recommend :
```
hub=pgm.Hub('Diffusion',preset='Basic')
hub.run()
R=hub.get_dparam()
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
def matmul(M,V):
    '''Matrix product Z=matmul(M,V) Z_i = \sum_j M_{ij} V_j'''
    return np.matmul(M,V)
def Rmatmul(nabla,C):
    '''Matrix product but with the axis of Regions rather than multisectoral'''
    return matmul(np.swapaxes(nabla, -3, -1),
                  np.swapaxes(C, -3, -2))


# #######################################################################
### The loop to merge the two dictionnaries
def MERGE(Recipient,dictoadd,override=True,verb=True):
    '''
    If you mix two models or want to add new auxlliary logics,
    you can merge your two dictionnaries.

    override : true will replace previous fields with new one if conflict such as :
        * another definition with the same type of logic (ODE, statevar)
        * change of logic type (transform a statevar to an ODE)

    Recipient is _LOGICS that you want to fill
    dicttoadd contains the new elements you want
    '''
    ### Category of the variable in a dict
    keyvars = { k:v.keys() for k,v in Recipient.items() }
    typ= {}
    for k,v in keyvars.items():
        for vv in v :
            typ[vv]=k
    ### Merging dictionnaries
    for category, dic in dictoadd.items(): ### LOOP ON [SECTOR SIZE,ODE,STATEVAR,PARAMETERS]
        for k, v in dic.items(): ### LOOP ON THE FIELDS
            if k in typ.keys(): ### IF FIELD ALREADY EXIST
                if override:
                    if verb : print(f'Override {category} variable {k}. Previous :{Recipient[category][k]} \n by :{v}')
                    Recipient[category][k] = v
                if typ[k]!=category :
                    if verb : print(f'Category change for logic of {k} : from {typ[k]} to {category}')
                    del Recipient[typ[k]][k]
                elif verb : print(f'Keeping old definition {category} variable {k}. Previous :{Recipient[category][k]} \n {v}')
            else: ### IF FIELD DOES NOT
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
            'func': lambda lapC,diffCoeff : diffCoeff*lapC ,
            'com': 'uniform diffcoeff',
            'definition': 'Concentration',
            'initial':1,
        },
    },
    'statevar': {
        'gradCx': {
            'func': lambda C,nabla : Rmatmul(C,nabla),
            'definition': '1d gradient of C',
            'com': 'calculated with nabla matrix multiplication'},
        'lapC': {
            'func': lambda gradCx,nabla : Rmatmul(gradCx,nabla),
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

preset_basis = {
    'nr':N,
    'dt':0.1,
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