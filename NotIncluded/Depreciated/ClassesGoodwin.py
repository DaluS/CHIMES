# -*- coding: utf-8 -*-
import numpy as np
import plots as plts          # Already written plot functions

"""
Class version of GEMMES
"""

class GK_NOINFLATION():
    """
    MODEL : GOODWIN-KEEN NO INFLATION
    
    Extensive variable dynamics of a simple Goodwin-Keen model.  
    Ingredients :
        * Leontiev Function
        * Instant labor optimization 
        * Philips curve negociation 
        * Instant capital creation 
        * No-behavior bank, investment of profit
        * Say's Law 
        * Exogeneous population growth
        * Exogeneous worker productivity
    """
    
    def __init__(self):     
        ## DEFINE ALL THE DYNAMICALLY-DEFINED VARIABLES 
        self.variables  = {'a' : self.da, # growth of productivity
                           'N' : self.dN, # growth of population
                           'K' : self.dK, # growth of capital
                           'W' : self.dW, # growth of salary
                           'D' : self.dD, # growth of debt
                           }
           
        ## LIST ALL NECESSARY PARAMETERS FOR THE selfTEM
        self.parameters = ['r','k0','k1','k2',     # investment-debt parameters
                           'alpha','delta','beta', # time-rate parameters
                           'nu',                   # UnEfficiency of capital
                           'phi0','phi1']          # Salary negociation
        
        self.intermediaryfuncs = {  'Y'      : self.GDP    ,   # GDP Leontiev optimized
                                    'L'      : self.worker ,   # Workers
                                    'Pi'     : self.Pi     ,   # Extensive profit 
                                    'lambda' : self.lambd  ,   # employement rate 
                                    'omega'  : self.omega  ,   # wage share in GDP
                                    'philips': self.philips,   # Rate of salary growth
                                    'kappa'  : self.kappa  ,   # percent of production going into investment
                                    'I'      : self.invest ,   # Investment in new capital  
                                }
      
        ## BE CAREFUL IN THE ORDER OF THE INTERMEDIARYFUNCS
        ## THE VARIABLES WILL BE CALCULATED IN THAT ORDER 
        ## CHECK THAT THEY ONLY NEED PREVIOUS CALCULATION AND DYNAMICALLY-DEFINED VARIABLES
        #self.OrderOfIntermediaryFuncs = [ k for k in self.intermediaryfuncs.keys()] #Automatic mode if you trust the order
        #self.OrderOfIntermediaryFuncs = ['Y','L','Pi','lambda','omega','philips','kappa']

        self.auxiliaryfuncs = {    'g'      : self.g      ,   # Growth rate
                                   'd'      : self.d      ,   # relative debt
                                   'pi'     : self.pi     ,   # Relative profit
                                   'i'      : self.i      ,   # INFLATION IS 0 here 
                              }
                

    ### DIFFERENTIAL DEFINITIONS 
    def dN     (self, y, p): return p['beta'] *y['N']
    def da     (self, y, p): return p['alpha']*y['a']
    def dK     (self, y, p): return y['I'] - y['K']*p['delta']
    def dW     (self, y, p): return y['W'] * ( y['philips']  )
    def dD     (self, y, p): return y['I'] - y['Pi']  
    
    ### SPECIFIC FUNCTIONS INSIDE 
    def GDP    (self, y, p): return y['K'] / p['nu']
    def worker (self, y, p): return y['K'] / (y['a'] * p['nu'])
    def Pi     (self, y, p): return y['Y'] - y['W']*y['L'] - p['r']*y['D']    
    def lambd  (self, y, p): return y['L'] / y['N']
    def philips(self, y, p): return - p['phi0'] + p['phi1']/ (1-y['lambda'])**2 
    def omega  (self, y, p): return y['W'] * y['L'] / y['Y']
    def kappa  (self, y, p): return p['k0'] + p['k1'] * np.exp(p['k2']*y['Pi']/y['Y'])
    def invest (self, y, p): return y['Y'] * y['kappa']     
    
    ### AUXILIARY VALUES THAT ARE PRACTICAL
    def pi     (self, y, p): return 1 - y['omega'] - p['r']*y['d']
    def g      (self, y, p): return (1-y['omega']) / p['nu'] - p['delta']
    def d      (self, y, p): return y['D'] / y['Y']
    def i      (self, y, p): return y['Y']*0                                 # NOT CODED 

    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        #plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        #plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        plts.GraphesIntensive  (r, p)      
        #plts.GraphesExtensive  (r, p) 


    ##### THIS SECTION SHOULD NEED NO CHANGES #################################
    ##### WE CAN INCLUDE THIS INSIDE _Class ? #################################
    ###########################################################################
    def f(self,inputt,op,p):
        '''
        Dynamic core of the selftem, makes the step for y between t and t+dt
        '''
        #0#### y allocation for faster calculation
        #y = {k0 : np.zeros(len(inputt[0])) for k0 in self.Uvarlist.keys()}
        y = {}
        #I#### GET VARIABLES FROM Y AS A DIC SO THAT IT'S MORE PRACTICAL
        for i, k0,  in enumerate(self.variables.keys()) : y[k0] = inputt[i]   
               
        #II### CALCULATE SOME INTERMEDIATE VALUE IN THE RIGHT ORDER 
        for k0 in self.OrderOfIntermediaryFuncs : 
            y[k0]=self.intermediaryfuncs[k0](y,p)
        
        #III## CALCULATE EVOLUTION OF DYNAMIC VARIABLES  
        dy = {k0: v0(y,p) for k0, v0 in self.variables.items() } 

        return np.array([dy[j]*p['dt'] for j in self.variables])
        
    def intermediatevariables(self):
        ''' A FEW VARIABLES THAT CAN BE CALCULATED AFTER INIT '''
        self.Nvar       = len(self.variables) 
        self.varlist    =  {**{**self.variables,          #list of all variables
                               **self.intermediaryfuncs}, #And their expression
                            **self.auxiliaryfuncs}
        self.Uvarlist   = {**self.variables,              #list of all variables
                           **self.intermediaryfuncs}    
        return self
    
    def initializeY(self,ic,pN):
        '''Rewrite the initial conditions in a machine-friendly style'''
        y= np.zeros((self.Nvar,pN['Nx']))
        for i,ids in enumerate(self.variables): y[i,:] = ic[ids]
        return(y)
    
    def expandY_simple(self,Y_s,t_s,op,p):
        ''' Get all relevant instant variables that one can extract from the selftem'''
        r={'t' : t_s}    
        for i,ids in enumerate(self.variables): r[ids] = Y_s[i,:,:]     # Expand calculated variables
        for name,fs in self.intermediaryfuncs.items() : r[name]=fs(r,p) # Back to intermediary variables
        for name,fs in self.auxiliaryfuncs   .items() : r[name]=fs(r,p) # Simple variables to plot
        return r

    def printParameters(self,p):
        '''Print all physical parameters that are in the selftem'''
        print('#################################')
        print("Physical parameters value ######")
        for name in self.parameters:
            print(name+(15-len(name))*' ',p[name])   
        print(33*'#')

    def keepUsefulParams(self,p):
        '''Clean all parameters values'''
        newParams = {}
        for key in self.parameters:
            newParams[key] = p[key]
        return newParams

    def Findtherightorder(self,p,parNum):
        '''
        This function find an order that allow the model to compute all the intermediary variables
        '''
        if parNum['verb']: 
            print(33*'#')
            print('Finding the right order to compute the intermediary variables...') 
            
        y = { k : 1 for k in self.variables.keys()}                            # Dummy y just for calls
        OrderOfIntermediaryFuncs = []                                          # The list of the variable order 
        VariablesStillInTheList = [ k for k in self.intermediaryfuncs.keys()]  # The list of variable still to find 
        for i in range(len(self.intermediaryfuncs)):                           # For each variable that has to be placed in order
            for j in range(len(VariablesStillInTheList)):                      # We select one which has not been calculated
                Templist = OrderOfIntermediaryFuncs+[VariablesStillInTheList[j]] # We add it to the list
                try :                                                          # We try to go through calculations
                    for k0 in Templist : y[k0]=self.intermediaryfuncs[k0](y,p) # We calculate each variable in order
                    if parNum['verb']: print('element',i, 'found ! it is :',VariablesStillInTheList[j])
                    OrderOfIntermediaryFuncs = Templist.copy()                 # Templist is a good begining
                    del VariablesStillInTheList[j]                             # We removeitfromthelist
                    break                                                      # We go to the next i element
                except BaseException :                                         # If it didn't work
                    y = { k : 1 for k in self.variables.keys()}                # We reinitialise y to be sure we don't keep error
        self.OrderOfIntermediaryFuncs = OrderOfIntermediaryFuncs


