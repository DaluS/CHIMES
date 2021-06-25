# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:23:59 2021

@author: Paul
"""

import matplotlib.pyplot as plt
import numpy as np
import FunctionsGoodwin as FG
import Miscfunc as M



def PhilAndInvest(p):
    '''
    Show behavior functions 
    '''
    plt.figure('Behaviors Function')
    ax1=plt.subplot(121)
    ax2=plt.subplot(122)
    plt.title('Behavior functions')
    x = np.arange(0,1,0.01)
    ax1.plot(x,M.philips(x,p));ax1.set_xlabel('$\lambda$');ax1.set_ylabel('$\Phi(\lambda)$')
    ax2.semilogy(x,M.fk(x,p)     );ax2.set_xlabel('$\pi$');ax2.set_ylabel('$\kappa(\pi)$')
    plt.show()
    
    
def GoodwinKeenTypical(r,p,title=''):  
    '''
    Typical 3-Dimension phase-plot
    '''
    cm = plt.cm.jet(np.linspace(0,1,p['Nx']))
    
    plt.figure('GraphesTemporels2',figsize=(10,5))
    ax1=plt.subplot(131)
    ax2=plt.subplot(132)
    ax3=plt.subplot(133)
    for j in range(p['Nx']):
        ax1.plot(r['t'],r['lambda'][:,j],c=cm[j,:])
        ax2.plot(r['t'],r['omega'][:,j] ,c=cm[j,:])
        ax3.plot(r['t'],r['d'][:,j]     ,c=cm[j,:])
        
    
    ax1.set_ylabel('$\lambda$')
    ax2.set_ylabel('$\omega$')
    ax3.set_ylabel('d')
    #ax2.plot(r['t'],r['d']    [:,j] ,c='k',label='d')
    plt.legend()
    plt.title(title)
    plt.show()
    
def omegalambdacycles(r,p,title=''):   
    '''
    2-D omega-lambda phase portrait
    '''
    cm = plt.cm.jet(np.linspace(0,1,p['Nx']))
    plt.figure('Cycles Goodwin2')

    for j in range(p['Nx']): plt.plot(r['omega'][:,j],r['lambda'][:,j],c=cm[j,:])
    plt.plot(r['omega'][0,0],r['lambda'][0,0],'*')
    plt.axis('scaled')
    plt.title(title)
    plt.show()
    
def GraphesIntensive(r,p):
    plt.figure('IntensiveVariable',figsize=(15,10))
    plt.subplot(321);plt.plot(r['t'],r['omega'] ,);plt.xlabel('time');plt.ylabel('wage share')
    plt.subplot(322);plt.plot(r['t'],r['lambda'],);plt.xlabel('time');plt.ylabel('employement')
    plt.subplot(323);plt.plot(r['t'],r['d']     ,);plt.xlabel('time');plt.ylabel('rel debt')
    plt.subplot(324);plt.plot(r['t'],r['pi']    ,);plt.xlabel('time');plt.ylabel('rel profit')
    plt.subplot(325);plt.plot(r['t'],r['i']    ,);plt.xlabel('time');plt.ylabel('inflation')    
    plt.subplot(326);plt.plot(r['t'],r['g']    ,);plt.xlabel('time');plt.ylabel('growth')
    plt.show()


def GraphesExtensive(r,p,j=0):   
    plt.figure('IntensiveVariable',figsize=(10,5))
    
    plt.subplot(121)
    plt.semilogy(r['t'],r['Y'][:,j]             ,label='GDP')
    plt.plot(    r['t'],r['K'][:,j]             ,label='Kapital')
    plt.plot(    r['t'],r['p'][:,j]             ,label='Price')
    plt.plot(    r['t'],r['Pi'][:,j]            ,label='Profit')
    plt.plot(    r['t'],r['D'][:,j]             ,label='Debt')
    plt.plot(    r['t'],r['I'][:,j]             ,label='Investment')  
    plt.xlabel('time');plt.ylabel('Money')
    plt.legend()
    
    plt.subplot(122)
    plt.semilogy(r['t'],r['N'][:,j],label='Population');
    plt.plot    (r['t'],r['L'][:,j],label='Labor');
    plt.xlabel('time');plt.ylabel('Humans')
    plt.legend()
        
    plt.show()

 
def PhasewithG(r,p,op,title='skp'):
    '''
    Phase diagram with growth
    '''    
    
    if title=='skp': title='$\eta=$'+str(p['eta'])+'\n, $b =$'+str(p['b'])+'\n r='+str(p['r'])

    cm = plt.cm.jet(np.linspace(0,1,p['Nx']))   
    plt.figure('Osc2')
    ax1=plt.subplot(231)
    ax2=plt.subplot(232)
    ax3=plt.subplot(233)
    ax4=plt.subplot(212)
    for j in range(p['Nx']):
        ax1.plot(r['omega'] [:,j],r['g']     [:,j],c=cm[j,:])
        ax2.plot(r['lambda'][:,j],r['g']     [:,j],c=cm[j,:])
        ax3.plot(r['omega'] [:,j],r['lambda'][:,j],c=cm[j,:],)
        ax4.plot(r['t']             ,r['g']     [:,j],c=cm[j,:],)
    ax1.set_xlabel('$\omega$')
    ax1.set_ylabel('g')    
    
    ax2.set_xlabel('$\lambda$')
    ax2.set_ylabel('g')   
    
    ax3.set_xlabel('$\omega$')
    ax3.set_ylabel('$\lambda$')     
    
    ax4.set_xlabel('$t$')
    ax4.set_ylabel('$g$') 
    
    plt.suptitle(title)
    plt.show()

    

def PeriodPlots(r,p,op,title='skp'):
    if title=='skp':title='$b =$'+str(p['b'])+'\n r='+str(p['r'])     
    cm = plt.cm.jet(np.linspace(0,1,p['Nx']))
    plt.figure('PeriodMeasures')
    ax1=plt.subplot(231)
    ax2=plt.subplot(232)
    ax3=plt.subplot(233)
    ax4=plt.subplot(234)
    ax5=plt.subplot(235)
    ax6=plt.subplot(236)
    for j in range(p['Nx']):
        
        Tv=[]
        gv=[]
        tv=[]
        lm=[]
        deltalamb=[]
        for z in range(len(r['PeriodID'][j])-1):
            id1 = r['PeriodID'][j][z]
            id2 = r['PeriodID'][j][z+1]
            
            t2 = r['t'][id2]
            t1 = r['t'][id1]
    
            T   =t2-t1        
            gmoy=(np.sum(r['g'][id1:id2])*p['dt'])/T
    
            Tv.append(T)
            gv.append(gmoy)
            tv.append((t1+t2)/2)
            lm.append(r['lambda'][id1,j])
            deltalamb.append(r['lambda'][id1,j]-r['lambda'][id2,j])
            #plt.plot((t1+t2)/2,T,'*')
    
            #plt.plot(T,gmoy,'*')
        ax1.plot(Tv,gv       ,c=cm[j,:])
        ax2.plot(tv,Tv       ,c=cm[j,:])
        ax3.plot(tv,gv       ,c=cm[j,:])
        ax4.plot(lm,Tv       ,c=cm[j,:])
        ax5.plot(lm,gv       ,c=cm[j,:])
        ax6.semilogy(tv,np.array(deltalamb)/np.array(Tv),c=cm[j,:])
    
    #    ax6.plot(lm,gv,'-*',c=cm[j,:])
    ax1.set_xlabel('Period of a cycle')
    ax1.set_ylabel('Mean growth speed')    
    
    ax2.set_xlabel('time evolution')
    ax2.set_ylabel('Period of a cycle')   
    
    ax3.set_xlabel('time')
    ax3.set_ylabel('Mean growth speed')     
    
    ax4.set_xlabel('maximum $\lambda$ in cycle')
    ax4.set_ylabel('Period')   
    
    ax5.set_xlabel('maximum $\lambda$ in cycle')
    ax5.set_ylabel('Mean growth speed')   
    
    ax6.set_xlabel('time')
    ax6.set_ylabel('deltalamb/t')
    #ax6.legend()
    #ax6.set_axis_off()  
    
    plt.suptitle(title)
    plt.show() 
    

def map2DLambdaT(r,op,title='skp'):
    """
    if title='skp': 
        title='Superposed "synchronisation" with meso Philips ,'+ 
              '$N_x$ ='+str(p['Nx'])+
              ',   $\lambda_s =$'     +"{0:.2f}".format(p['lambdamin']) +
              ',   $\Delta \lambda =$'+"{0:.2f}".format(p['lambdamax']-p['lambdamin']))
    """ 
    plt.figure('2DLambdaT',figsize=(20,10))
    OO,LL   = np.meshgrid(r['t'],r['lambda'][0,:]) 
    
    plt.pcolormesh(OO,LL,r['lambda'].T,cmap='inferno')
    plt.xlabel('time')
    plt.ylabel('$\lambda(t=0)$')
    plt.colorbar()
    plt.title(title)
    plt.show()


def MesoMeanSTD(r,p,op,title='skp'):
    '''
    if title=='skp': title = 'Leontiev r='+str(p['r'])+
             ', Nx ='+str(p['Nx'])+
             ' \n $\mu_{\lambda}=$'+str(lmmoy)+
             ', $\Delta_{\lambda}=$'+str(deltalamb)+
             '\n $g_{global}$='+str(p['g1'])
    '''
    ls='-'
    lw=.5
    cm = plt.cm.jet(np.linspace(0,1,p['Nx']))
    
    meanlambd= np.mean(r['lambda'],axis=1)
    stdlambd = np.std( r['lambda'],axis=1)
    meanomega= np.mean(r['omega'] ,axis=1)
    stdomega = np.std( r['omega'] ,axis=1)
    meand    = np.mean(r['d']     ,axis=1)
    stdd     = np.std( r['d']     ,axis=1)
    
    plt.figure('GraphesTemporels2'+str(int(100*p['g1'])),figsize=(15,20))
    ax0=plt.subplot(231)
    ax1=plt.subplot(232)
    ax2=plt.subplot(233)
    ax3=plt.subplot(234)
    ax4=plt.subplot(235)
    ax5=plt.subplot(236)
    for j in range(p['Nx']):
        ax1.plot(r['t'],r['lambda'][:,j],c=cm[j,:],ls=ls,lw=lw)
        ax2.plot(r['t'],r['omega'][:,j] ,c=cm[j,:],ls=ls,lw=lw)    
        ax3.plot(r['t'],r['d'][:,j]     ,c=cm[j,:],ls=ls,lw=lw)
        ax0.plot(r['omega'][:,j],r['lambda'][:,j],c=cm[j,:],lw=0.3)
    
    ax1.plot(r['t'],meanlambd       ,c='k'    ,lw=1)  
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$\lambda$')
    ax2.plot(r['t'],meanomega       ,c='k'    ,lw=1)  
    ax2.set_xlabel('t')
    ax2.set_ylabel('$\omega$')
    ax3.plot(r['t'],meand           ,c='k'    ,lw=1) 
    ax3.set_xlabel('t')
    ax3.set_ylabel('d')
    ax4.plot(r['t'],stdlambd       ,lw=1,c='b',label='$\sigma_{\lambda}$')  
    ax4.plot(r['t'],stdd           ,lw=1,c='r',label='$\sigma_{d}$')   
    ax4.plot(r['t'],stdomega       ,lw=1,c='g',label='$\sigma_{\omega}$')   
    ax4.legend()
    
    OO,LL   = np.meshgrid(r['t'],r['lambda'][0,:])       
    ax5.pcolormesh(OO,LL,r['lambda'].T,cmap='gist_ncar')
    ax5.set_xlabel('time')
    ax5.set_ylabel('$\lambda_0$')
    ax5.set_title('$\lambda$ map')
      
    #plt.suptitle()
    plt.show()


















