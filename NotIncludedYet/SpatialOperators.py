# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import diags

def prepareOperators(p):
    """
    Creation of few spatial operators :
    *    3diag is a local meaning on both neighbors and centered value 
    *    diff_cent is a centered difference operator 
    *    laplacian is a classical laplacian operator
    """
    operator={}
    if p['Nx']>=3:
        operator['3diag']    =diags([1/3*np.ones(p['Nx']-1), 1/3*np.ones(p['Nx']-1),np.ones(p['Nx'])*1/3,1/3,1/3], [1, -1, 0,p['Nx'],-p['Nx']])    
        operator['diff_cent']=diags([0.5*np.ones(p['Nx']-1),-0.5*np.ones(p['Nx']-1),-0.5,0.5]                 , [1, -1   ,p['Nx'],-p['Nx']])
        operator['laplacian']=diags([1*np.ones(p['Nx']-1), -1*np.ones(p['Nx']-1),-2*np.ones(p['Nx'])*1/3,1,1], [1, -1, 0,p['Nx'],-p['Nx']])
        operator['Mean']  = np.ones((p['Nx'],p['Nx']))/(p['Nx'])
    return operator

