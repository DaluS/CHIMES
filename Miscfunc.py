# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import diags
import shutil
from datetime import datetime
import os

###############################################################################
### SYSTEM INITIALISATION ###############################################
###############################################################################
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


###############################################################################
### NUMERICAL CORE ############################################################
###############################################################################
def rk4(f,y,op,p):
    """
    a traditional RK4 scheme, with y the vector values, and p the parameter dictionnary
    dt is contained within p
    """
    dy1 =  f(y       ,op,p  )
    dy2 =  f(y+dy1/2 ,op,p  )
    dy3 =  f(y+dy2/2 ,op,p  )
    dy4 =  f(y+dy3   ,op,p  )
    return (dy1 + 2*dy2 + 2*dy3 + dy4)/6 

def TemporalLoop(y,SYS,op,pN,p):
    Y_s = np.zeros((SYS.Nvar,pN['Ns'],pN['Nx']))     # stock dynamics
    Y_s[:,0,:]= 1*y                                 # first stock
    t_s       = np.zeros(pN['Ns'])                   # stock time
    p['dt']=pN['dt']
    t=0 
    
    for i in range(pN['Nt']+1):
        y += rk4(SYS.f,y,op,p)                       # The vector y is dynamically updated 
        t += pN['dt']
        Y_s[:,i,:] = np.copy(y)             # we write it in the "book" Y_s
        t_s[i]     = t*1                    # we write the time 
    return Y_s, t_s


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

################## MISCELLANEOUS ##############################################
###############################################################################    
def savedata(rootfold,t,Y_s,p,op):  
    date = str(datetime.now()).split(' ')[0]
    try : os.mkdir(rootfold+date)
    except BaseException : print('Folder of the day already created')
    Nfolder = os.listdir(rootfold+date+'/')
    Fold    = rootfold+date+'/Expe_'+str(len(Nfolder))
    os.mkdir(Fold)   
    #pickle.dump(t  ,      open(Fold+'/t.p'      ,"wb"))
    print("THIS SHOULD BE WRITTEN WITH THE RELEVANT VARIABLES AGAIN")
    
    codefolder = os.getcwd()
    shutil.copyfile(codefolder+'/FunctionsGoodwin.py'     ,Fold+'/FunctionsGoodwin.py' )
    shutil.copyfile(codefolder+'/Main.py'                 ,Fold+'/Main.py' )
    print('data saved in :',Fold)

def PrintNumericalparameters(p):
    print("Numerical parameters ############")
    for n,v in p.items():
        print(n+(15-len(n))*' ',v)   
    print(34*'#')
