# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 14:48:22 2021

@author: Paul Valcke
"""

import numpy as np

###############################################################################

def getperiods(r,p,op):
    '''
    calculate period index values (index of the local maximal position on lambda)
    '''
    r['PeriodID']=[]
    
    for j in np.arange(p['Nx']): 
        r['PeriodID'].append([])
        id1=1
        while id1<p['Nt']-2:
            if ( r['lambda'][id1,j]>r['lambda'][id1-1,j] and 
                 r['lambda'][id1,j]>r['lambda'][id1+1,j] ):
                r['PeriodID'][j].append(1*id1)  
            id1+=1    
    return r        
            
def sumexp(f,valini,p,pN,r):
    y=np.zeros((p['Nt'],pN['Nx']))
    y[0]=1 
    if type(f)==float :
        for i in range(p['Nt']-1): y[i+1,:]=y[i,:]*(1+f   *(r['t'][i+1]-r['t'][i]))      
    else :
        for i in range(p['Nt']-1): y[i+1,:]=y[i,:]+(1+f[i]*(r['t'][i+1]-r['t'][i]))
    return y