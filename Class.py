# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np
import plots as plts          # Already written plot functions

"""
Class version of GEMMES
"""

class CORE():
    '''
THE CORE OF THE RESOLUTION FOR THE MODEL

HAS AS ELEMENTS ##################
- self.parNum            : dic{name : value}    the numerical parameters the system use
- self.parameters        : dic{name : value}    the ensemble of parameters the system use
- self.EQUATIONS         : dic{name : function} the ensemble of equations the system has 

- self.description       : string               the description of the system of equations 

- self.variables         : list of strings      the variables dynamically defined in the coupled 
                                                system (through differential equations)
                                                
- self.intermediaryfuncs : list of strings      the intermediary values (calculated through the 
                                                state of the system) useful to compute our 
                                                differential equations
                                                
- self.auxiliaryfuncs    : list of strings      the intermediary values (calculated through the 
                                                state of the system) which are not needed for the 

- self.auxiliarydiff     : list of strings      variables dynamically defined useful for user but 
                                                not impacting the system NOT IMPLEMENTED YET  
                                                
- self.Nvar              : integer              Number of dynamically defined variables 
          
- self.Uvarlist          : All variables defined in the system 

- self.OrderOfIntermediaryFuncs : list of strings The order in which the system should solve the system
                                                  of equations before computing differential equations  
 
HAS A METHOD #######################    
- Findtherightorder : From the list of intermediary function find the order of execution

- initializeY       : Create the initial Y vector 

- printParameters   : 

- f                 : from y(t) to dy(t)*dt  
- rk4               : from y(t) to y(t+dt)
- TemporalLoop      : from y(t=0) to y(tmax)

- expandY_simple    : from dynamically defined variable to all useful variables

- self.plot         : Plot all the things written by the modeler
  
    '''
    
    def __init__(self,syseq,p,parNum):     
        # LOADING THE SYSTEM WE WANT TO SOLVE
        self.EQUATIONS         = syseq.EQUATIONS        
        self.description       = syseq.__doc__          
        self.variables         = { k:v['f'] for k,v in syseq.EQUATIONS.items() if v['type']=='differential'  }
        self.intermediaryfuncs = { k:v['f'] for k,v in syseq.EQUATIONS.items() if v['type']=='intermediary'  }  
        self.auxiliaryfuncs    = { k:v['f'] for k,v in syseq.EQUATIONS.items() if v['type']=='auxilliary'    } 
        self.Nvar       = len(self.variables) 
        self.Uvarlist   = {**self.variables,              
                           **self.intermediaryfuncs}            
        self.plot = syseq.plotlitst_simple

        # LOADING THE PARAMETERS WE ARE GOING TO USE 
        self.parNum            = parNum                                 # FOR THE COMPUTER
        self.parameters        = { k : p[k] for k in syseq.parameters}  # FOR THE COMPUTER
        

        self.VariableDescription   = None                               # FOR USER AND PLOT
        self.ParametersDescription = None                               # FOR USER AND PLOT
        
        # FINDING THE ORDER OF THE EQUATIONS TO SOLVE
        if hasattr(syseq, 'OrderOfIntermediaryFuncs'):
            self.OrderOfIntermediaryFuncs = syseq.OrderOfIntermediaryFuncs 
        else:
            self.OrderOfIntermediaryFuncs = self.Findtherightorder()

        
    ########## FUNCTIONS TO ASSIST INITIALISATION ######
    def Findtherightorder(self):
        '''
        This function find an order that allow the model 
        to compute all the intermediary variables
        #!#!#!#! SHOULD BE PLACED ELSEWHERE AND ONLY ACCEPT MODELS THAT HAVE THIS MANUALY ADDED
        '''
        
        if self.parNum['verb']: 
            print('System has no order of calculation for intermediaryFunctions')
            print('Finding one that works...') 
            
        y = { k : 1 for k in self.variables.keys()}                            # Dummy y just for calls
        OrderOfIntermediaryFuncs = []                                          # The list of the variable order 
        VariablesStillInTheList = [ k for k in self.intermediaryfuncs.keys()]  # The list of variable still to find 
        for i in range(len(self.intermediaryfuncs)):                           # For each variable that has to be placed in order
            for j in range(len(VariablesStillInTheList)):                      # We select one which has not been calculated
                Templist = OrderOfIntermediaryFuncs+[VariablesStillInTheList[j]] # We add it to the list
                try :                                                          # We try to go through calculations
                    for k0 in Templist : 
                        y[k0]=self.intermediaryfuncs[k0](y,self.parameters)   # We calculate each variable in order
                    OrderOfIntermediaryFuncs = Templist.copy()                 # Templist is a good begining
                    del VariablesStillInTheList[j]                             # We removeitfromthelist
                    break                                                      # We go to the next i element
                except BaseException :                                         # If it didn't work
                    y = { k : 1 for k in self.variables.keys()}                # We reinitialise y to be sure we don't keep error
                    #if j == len(VariablesStillInTheList)-1:
                    #    raise Exception("NO ORDER OF RESOLUTION FOUND")
                    
        if self.parNum['verb']: 
            print('Order found :',OrderOfIntermediaryFuncs)                    
        return OrderOfIntermediaryFuncs

    def initializeY(self,ic):
        '''Rewrite the initial conditions in a machine-friendly style'''
        y= np.zeros((self.Nvar,self.parNum['Nx']))
        for i,ids in enumerate(self.variables): y[i,:] = ic[ids]
        return(y)
    

    ########### CORE OF DYNAMIC SYSTEM RESOLUTION ######        
    def f(self,inputt,p):
        '''
        Dynamic core of the system, makes the step for y between t and t+dt
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
 
    
    def rk4(self,y):
        """
        a traditional RK4 scheme, with y the vector values, and p the parameter dictionnary
        dt is contained within p
        """
        dy1 = self.f( y       , self.parameters  )
        dy2 = self.f( y+dy1/2 , self.parameters  )
        dy3 = self.f( y+dy2/2 , self.parameters  )
        dy4 = self.f( y+dy3   , self.parameters  )
        return (dy1 + 2*dy2 + 2*dy3 + dy4)/6 

    def TemporalLoop(self,y):
        Y_s = np.zeros((self.Nvar,self.parNum['Ns'],self.parNum['Nx']))     # stock dynamics
        Y_s[:,0,:]= 1*y                                 # first stock
        t_s       = np.zeros(self.parNum['Ns'])                   # stock time
        self.parameters['dt']=self.parNum['dt']
        t=0 
        
        for i in range(self.parNum['Nt']+1):
            y += self.rk4(y)                       # The vector y is dynamically updated 
            t += self.parNum['dt']
            Y_s[:,i,:] = np.copy(y)             # we write it in the "book" Y_s
            t_s[i]     = t*1                    # we write the time 
        return Y_s, t_s     
    
    
    ########### MORE PRACTICAL OUTPUT ######  
    def expandY_simple(self,Y_s,t_s):
        ''' Get all relevant instant variables that one can extract from the system'''
        r={'t' : t_s}    
        for i,ids in enumerate(self.variables): r[ids] = Y_s[i,:,:]     # Expand calculated variables
        for name,fs in self.intermediaryfuncs.items() : r[name]=fs(r,self.parameters) # Back to intermediary variables
        for name,fs in self.auxiliaryfuncs   .items() : r[name]=fs(r,self.parameters) # Simple variables to plot
        return r


    def printParameters(self):
        '''Print all physical parameters that are in the selftem
        #!#!#!#!#! SHOULD BE DEPRECIATED BY DIDIER'S FUNCTIONS'''
        print('#################################')
        print("Physical parameters value ######")
        for name in self.parameters:
            print(name+(15-len(name))*' ',self.parameters[name])   
        print(33*'#')



