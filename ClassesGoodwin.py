# -*- coding: utf-8 -*-
import numpy as np
import plots as plts          # Already written plot functions

"""
Class version of GEMMESCORE

######## HOW TO USE ONE ? 

######## HOW TO CREATE YOUR OWN ? 
    1 Copy one version that looks alike (typically choose between intensive and extensive type)
    2 Change the name
    3 Change the list of hypothesis in the class description\
    4 Create your list of variables, parameters
    5 Code intermediary functions ( combination of variable and parameters that are practical)
    6 Add them in intermediaryfuncs 
    7 Change the core ( self.f ) of the dynamics 
    8 Change the list of plots 
"""


class GK_Reduced():
    """3 intensive variable dynamic of simple GoodwinKeen model. Ingredients : 
        * Leontiev Function
        * Instant labor optimization 
        * Philips curve negociation 
        * Instant capital creation 
        * No-behavior bank, investment on relative profit 
        * Say's Law 
        * Exogeneous population growth
        * Exogeneous worker productivity
    """
    
    def __init__(self):
        self.type = 'intensive' 
        self.variables  = ['omega',
                           'lambda',
                           'd']
        self.Nvar       = len(self.variables)    
        self.parameters = ['r',
                           'alpha','delta1','beta',
                           'nu',
                           'eta','mu','gamma',
                           'k0','k1','k2',
                           'phi0','phi1']        
        
        self.intermediaryfuncs = {'pi' : self.pi,
                                  'i'  : self.i,
                                  'g'  : self.g,
                                  'philips': self.philips,
                                  'kappa'  : self.kappa}
    def f(self,inputt,op,p):
        '''
        Dynamic core of the system, makes the step for y between t and t+dt
        '''
        #I#### GET VARIABLES FROM Y AS A DIC SO THAT IT'S MORE PRACTICAL        
        y  = {}
        dy = {}
        for i,ids in enumerate(self.variables): y[ids] = inputt[i]
            
        #II### CALCULATE SOME INTERMEDIATE VALUE 
        y['pi']      = self.pi(y,p)      # Relative profit
        y['i']       = self.i (y,p)      # Rate of Inflation 
        y['philips'] = self.philips(y,p) # Rate of salary growth
        y['kappa']   = self.kappa(y,p)   # percent of production going into investment
    
        #III## CALCULATE EVOLUTION OF DYNAMIC VARIABLES  
        dy['omega' ] = y['omega'] * (y['philips']-p['alpha']-p['gamma']*y['i'])
        dy['lambda'] = y['lambda'] * (y['kappa']/p['nu'] - p['alpha'] - p['alpha'] - p['beta'] )
        dy['d'     ] = y['kappa'] - y['pi'] - y['d']*  (y['kappa']/p['nu'] - p['delta1'] + y['i'])
        
        #IV## RETURN ITERATED VECTOR 
        return np.array([dy[j]*p['dt'] for j in self.variables])

    def pi(     self,y,p): return 1 - y['omega'] - p['r']*y['d']
    def i(      self,y,p): return p['eta']*(y['omega']*p['mu']-1)
    def g(      self,y,p): return (1-y['omega'])/p['nu'] - p['delta1']
    def philips(self,y,p): return - p['phi0'] + p['phi1']/ (1-y['lambda'])**2 
    def kappa(  self,y,p): return p['k0']+p['k1']*np.exp(p['k2']*y['pi'])
 
    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        plts.GoodwinKeenTypical(r,p,)      # Typical 3-Dimension phase-plot
        plts.omegalambdacycles(r,p,)       # 2-D omega-lambda phase portrait
        plts.GraphesIntensive(r,p)      
        

    ##### THIS SECTION SHOULD NEED NO CHANGES !
    def initializeY(self,ic,pN):
        '''Rewrite the initial conditions in a machine-friendly style'''
        y= np.zeros((self.Nvar,pN['Nx']))
        for i,ids in enumerate(self.variables): y[i,:] = ic[ids]

        return(y)
    
    def expandY_simple(self,Y_s,t_s,op,p):
        ''' Get all relevant instant variables that one can extract from the system'''
        r={'t' : t_s}    
        for i,ids in enumerate(self.variables): r[ids] = Y_s[i,:,:]     # Expand calculated variables
        for name,fs in self.intermediaryfuncs.items() : r[name]=fs(r,p) # Back to intermediary variables
        return r

    def printParameters(self,p):
        '''Print all physical parameters that are in the system'''
        print("Physical parameters value")
        for name in self.parameters:
            print(name+(30-len(name)*' '),p['name'])        

