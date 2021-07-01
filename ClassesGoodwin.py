# -*- coding: utf-8 -*-
import numpy as np
import plots as plts          # Already written plot functions

"""
Class version of GEMMES
"""
class GK_FULL():
    """
    Extensive variable dynamics of a simple GoodwinKeen model. 
    Should give the same result as GK_Reduced. 
    Ingredients :
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
        self.variables  = ['a',
                           'N',
                           'K',
                           'W',
                           'D']
        
        self.Nvar       = len(self.variables)    
        self.parameters = ['r',
                           'alpha','delta','beta',
                           'nu',
                           'etaP','muP','gammaP',
                           'k0','k1','k2',
                           'phi0','phi1']        
        
        self.intermediaryfuncs = {  'Y'      : self.GDP    ,   # GDP Leontiev optimized
                                    'L'      : self.worker ,   # Workers
                                    'Pi'     : self.Pi     ,   # Extensive profit 
                                    'lambda' : self.lambd  ,   # employement rate 
                                    'omega'  : self.omega  ,   # wage share in GDP
                                    'd'      : self.d      ,   # relative debt
                                    'pi'     : self.pi     ,   # Relative profit
                                    'i'      : self.i      ,   # Rate of Inflation 
                                    'philips': self.philips,   # Rate of salary growth
                                    'kappa'  : self.kappa  ,   # percent of production going into investment
                                    'I'      : self.invest ,   # Investment in new capital 
                                    'g'      : self.g      ,   # Growth rate 
                                }
        
        self.description =  (
        "Extensive variable dynamics of a simple GoodwinKeen model." +'\n'+
        "Should give the same result as GK_Reduced." +'\n'+
        "Ingredients :" +'\n'+
            "* Leontiev Function"+'\n'+
            "* Instant labor optimization "+'\n'+
            "* Philips curve negociation "+'\n'+
            "* Instant capital creation "+'\n'+
            "* No-behavior bank, investment on relative profit" +'\n'+
            "* Say's Law "+'\n'+
            "* Exogeneous population growth"+'\n'+
            "* Exogeneous worker productivity ")
        
    def f(self,inputt,op,p):
        '''
        Dynamic core of the system, makes the step for y between t and t+dt
        '''
        #I#### GET VARIABLES FROM Y AS A DIC SO THAT IT'S MORE PRACTICAL        
        y  = {}
        dy = {}
        for i,ids in enumerate(self.variables): y[ids] = inputt[i]
            
        #II### CALCULATE SOME INTERMEDIATE VALUE 
        y['Y']       = self.GDP    (y, p)   # GDP Leontiev optimized
        y['L']       = self.worker (y, p)   # Workers
        y['Pi']      = self.Pi     (y, p)   # Extensive profit 
        y['lambda']  = self.lambd  (y, p)   # employement rate 
        y['omega']   = self.omega  (y, p)   # wage share in GDP
        y['d']       = self.d      (y, p)   # relative debt
        y['pi']      = self.pi     (y, p)   # Relative profit
        y['i']       = self.i      (y, p)   # Rate of Inflation 
        y['philips'] = self.philips(y, p)   # Rate of salary growth
        y['kappa']   = self.kappa  (y, p)   # percent of production going into investment
        y['I']       = self.invest (y, p)   # Investment in new capital 
        
        #III## CALCULATE EVOLUTION OF DYNAMIC VARIABLES  
        dy['a'] = p['alpha']*y['a']
        dy['N'] = p['beta'] *y['N']
        dy['K'] = y['I'] - y['K']*p['delta']
        dy['W'] = y['W'] * ( y['philips'] + p['gammaP'] * y['i'] )
        dy['D'] = y['I'] - y['Pi']
        
        #IV## RETURN ITERATED VECTOR 
        return np.array([dy[j]*p['dt'] for j in self.variables])
        
    
    
    ### SPECIFIC FUNCTIONS INSIDE 
    def pi     (self, y, p): return 1 - y['omega'] - p['r']*y['d']
    def Pi     (self, y, p): return y['Y'] - y['W']*y['L'] - p['r']*y['D']
    def i      (self, y, p): return p['etaP'] * (y['omega']*p['muP']-1)
    def g      (self, y, p): return (1-y['omega']) / p['nu'] - p['delta']
    def philips(self, y, p): return - p['phi0'] + p['phi1']/ (1-y['lambda'])**2 
    def kappa  (self, y, p): return p['k0'] + p['k1'] * np.exp(p['k2']*y['pi'])
    def worker (self, y, p): return y['K'] / (y['a'] * p['nu'])
    def lambd  (self, y, p): return y['L'] / y['N']
    def omega  (self, y, p): return y['W'] * y['L'] / y['Y']
    def d      (self, y, p): return y['D'] / y['Y']
    def GDP    (self, y, p): return y['K'] / p['nu']
    def invest (self, y, p): return y['Y'] * y['kappa']

    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        plts.GraphesIntensive  (r, p)      
        plts.GraphesExtensive  (r, p) 


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


class G_GREGOIRE():
    """
    Extensive variable dynamics of a simple Goodwin with ressources. 
   [MORE TO COME]
    """
    def __init__(self):       
        self.variables  = ['a2',
                           'N',
                           'K',
                           'W',
                           'Xh']
        
        self.Nvar       = len(self.variables)    
        self.parameters = ['alpha','delta','beta',
                           'phi0','phi1',
                           'z0','c',                # parametres gregoire 1
                           'mu0','RT','Xsh',        # parametres gregoire 2
                           'chi']                   # Chaisson
        
        self.intermediaryfuncs = {  'J'       : self.J ,     
                                    'muH'     : self.muH ,   
                                    'muL'     : self.muL ,   
                                    'Deltamu' : self.Deltamu,
                                    'G'       : self.G      ,      
                                    'PsiH'    : self.PsiH   ,      
                                    'Y'       : self.Y      ,   # GDP Leontiev optimized
                                    'L'       : self.L      ,   # Workers
                                    'Pi'      : self.Pi     ,   # Extensive profit 
                                    'lambda'  : self.lambd  ,   # employement rate 
                                    'omega'   : self.omega  ,   # wage share in GDP
                                    'pi'      : self.pi     ,   # Relative profit
                                    'philips' : self.philips,   # Rate of salary growth
                                    'I'       : self.invest }   # Investment in new capital }
        
        self.description =  ("C'EST LE SYSTEME DE GREGOOOOOOOOOOOIRE")
 
    ### SPECIFIC FUNCTIONS INSIDE 
    def pi     (self, y, p): return 1 - y['omega'] 
    def Pi     (self, y, p): return y['Y'] - y['W']*y['L']
    def philips(self, y, p): return - p['phi0'] + p['phi1']/ (1-y['lambda'])**2 
    def L      (self, y, p): return y['K'] / y['a2'] 
    def lambd  (self, y, p): return y['L'] / y['N']
    def omega  (self, y, p): return y['W'] / y['a2'] 
    def invest (self, y, p): return y['Pi'] 
    
    def G      (self, y, p): return (y['Deltamu'] - p['z0'] * p['chi'] )*p['chi']*p['c']*y['K']
    def Y      (self, y, p): return y['G']/p['c']
    def muH    (self, y, p): return p['mu0']-p['RT'] * np.log(1-y['Xh']/(y['Xh']+p['Xsh']))  # Reservoir potential 
    def muL    (self, y, p): return p['mu0']                                                 # Sink potential  
    def Deltamu(self, y, p): return y['muH']-y['muL']  # Difference of potential 
    def nu     (self, y, p): return y['K']/y['Y']
    def J      (self, y, p): return p['chi']*p['c']*y['K']
    def PsiH   (self, y, p): return y['Deltamu']*y['J']
    def PsiL   (self, y, p): return p['z0']*p['chi']**2 * p['c']*y['K']
    
    def f(self,inputt,op,p):
        '''
        Dynamic core of the system, makes the step for y between t and t+dt
        '''
        #I#### GET VARIABLES FROM Y AS A DIC SO THAT IT'S MORE PRACTICAL        
        y  = {}
        dy = {}
        for i,ids in enumerate(self.variables): y[ids] = inputt[i]
            
        #II### CALCULATE SOME INTERMEDIATE VALUE 
        y['J']       = self.J      (y, p)
        y['muH']     = self.muH    (y, p)
        y['muL']     = self.muL    (y, p)
        y['Deltamu'] = self.Deltamu(y, p)
        y['G']       = self.G      (y, p)      
        y['PsiH']    = self.PsiH   (y, p)      
        
        y['Y']       = self.Y      (y, p)   # GDP Leontiev optimized
        y['L']       = self.L      (y, p)   # Workers
        y['Pi']      = self.Pi     (y, p)   # Extensive profit 
        y['lambda']  = self.lambd  (y, p)   # employement rate 
        y['omega']   = self.omega  (y, p)   # wage share in GDP
        y['pi']      = self.pi     (y, p)   # Relative profit
        y['philips'] = self.philips(y, p)   # Rate of salary growth
        y['I']       = self.invest (y, p)   # Investment in new capital 


        #III## CALCULATE EVOLUTION OF DYNAMIC VARIABLES  
        dy['a2'] = p['alpha']*y['a2']
        dy['N']  = p['beta'] *y['N']
        dy['K']  = y['I'] - y['K']*p['delta']
        dy['W']  = y['W'] * y['philips'] 
        dy['Xh'] = -y['PsiH'] 
        
        #IV## RETURN ITERATED VECTOR 
        return np.array([dy[j]*p['dt'] for j in self.variables])
        
    
    

    
    
    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        plts.GraphesIntensive  (r, p)      
        plts.GraphesExtensive  (r, p) 


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


###############################################################################
###############################################################################

class GK_Reduced():    
    """
    3 intensive variable dynamic of simple GoodwinKeen model. Ingredients :
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
        self.variables  = ['omega',
                           'lambda',
                           'd']
        
        self.Nvar       = len(self.variables) 
        
        self.parameters = ['r',
                           'alpha','delta','beta',
                           'nu',
                           'etaP','muP','gammaP',
                           'k0','k1','k2',
                           'phi0','phi1']        
        
        self.intermediaryfuncs = {'pi' : self.pi,
                                  'i'  : self.i,
                                  'g'  : self.g,
                                  'philips': self.philips,
                                  'kappa'  : self.kappa}
        
        self.description = ("3 intensive variable dynamic of simple GoodwinKeen model. Ingredients :" +'\n'+
            "* Leontiev Function"+'\n'+
            "* Instant labor optimization "+'\n'+
            "* Philips curve negociation "+'\n'+
            "* Instant capital creation "+'\n'+
            "* No-behavior bank, investment on relative profit" +'\n'+
            "* Say's Law "+'\n'+
            "* Exogeneous population growth"+'\n'+
            "* Exogeneous worker productivity ")
        
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
        dy['omega' ] = y['omega'] * (y['philips']-p['alpha']-p['gammaP']*y['i'])
        dy['lambda'] = y['lambda'] * (y['kappa']/p['nu'] - p['alpha'] - p['alpha'] - p['beta'] )
        dy['d'     ] = y['kappa'] - y['pi'] - y['d']*  (y['kappa']/p['nu'] - p['delta'] + y['i'])
        
        #IV## RETURN ITERATED VECTOR 
        return np.array([dy[j]*p['dt'] for j in self.variables])

    def pi(     self,y,p): return 1 - y['omega'] - p['r']*y['d']
    def i(      self,y,p): return p['etaP']*(y['omega']*p['muP']-1)
    def g(      self,y,p): return (1-y['omega'])/p['nu'] - p['delta']
    def philips(self,y,p): return - p['phi0'] + p['phi1']/ (1-y['lambda'])**2 
    def kappa(  self,y,p): return p['k0']+p['k1']*np.exp(p['k2']*y['pi'])
 
    def plotlitst_simple(self,r,p):
        '''Launch all plots that don't need further understanding'''
        plts.GoodwinKeenTypical(r, p,)      # Typical 3-Dimension phase-plot
        plts.omegalambdacycles (r, p,)       # 2-D omega-lambda phase portrait
        plts.GraphesIntensive  (r, p)      
        plts.PhasewithG        (r, p,[],)        
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


