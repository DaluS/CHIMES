# -*- coding: utf-8 -*-
"""
PARAMETERS FOR GOODWIN-KEEN LIKE MODELS
"""

import numpy as np


def Modifications(params,parnum):
    """
    FOR THE MOMENT DOES NOTHING ! """
    return params


def parnum():
    '''
    Contains all numerical parameters needed for temporal and spatial resolution
    '''

    parNum={
        'Tmax' : 100,       # Duration of simulation    
        'Nx'   : 1,         # Number of similar systems evolving in parrallel
        'dt'   : 0.01,        # Timestep (fixed timestep method)  
        'verb' : True,      # Printing elements
    }

    ### INTERMEDIARY VALUES 
    parNum['Tstore']     = parNum['dt']                         # Time between two storage (if StorageMode=full, it goes to dt)
    parNum['Nt']         = int(parNum['Tmax']/parNum['dt'])         # Number of temporal iteration          
    parNum['Ns']         = int(parNum['Tmax']/parNum['Tstore'])+1   # Number of elements stored
    return parNum

def initCond(p,parNum):
    '''
    Determine the initial conditions that are used by the system to iterate on
    '''

    v1 = np.ones(parNum['Nx']) ### Pratical notation for more readable code : 
                           ### an array with 1 everywhere
    ic = {
        ### INTENSIVE VARIABLES 
        'd'      : v1*0.1,           # relative debt
        'omega'  : v1*p['omega0'],   # wage share
        'lambda' : v1*p['lambdamax'],# employement
        't'      : v1*0,             # initial time 

        ### INITIAL EXTENSIVE VARIABLES 
        'N' : v1*1 ,                # Population
        'a' : v1*1 ,                # productivity
        'p' : v1*1 ,                # Price
    }
    
    
    ### GREGOIRE 
    ic['Xh']= v1*1000
    ic['a2']= ic['a']
    
    ### DEDUCED FROM PREVIOUS ONES 
    ic['L'] = ic['lambda']*ic['N']  # Labor 
    ic['K'] = ic['a2']*ic['L']      # Capital 
    ic['Y'] = ic['K']/p['nu']      # Output 
    ic['D'] = ic['d']*ic['Y']       # Debt 
    ic['W'] = ic['omega']*ic['a']   # Salary
 
 

    
    return ic

def BasicParameters():
    """
    Create a dictionnary containing all the "phyiscal" parameters necessary 
    for the simulation. Their description is in comment here. 
    """
    params = {
        # Population evolution 
        'beta'   : 0.025,                      # Rate of population growth     (y^-1)
        'PopSat' : 10000,                      # Ratio between initial and maximal population 
        'alpha'  : 0.02,                       # Rate of productivity increase (y^-1)

        # Capital properties
        'delta' : 0.005,                      # Rate of WORKING capital depletion (y^-1)

        # Production 
        'nu'    : 3,                           # Kapital to output ratio as in Leontiev. CAREFUL IN CES this is 1/A
        'eta'   : 1000,                        # CES Only eta =1/(1+substituability)
        'b'     : .5,                          # CES parameter : capital part of the production 
        'z'     : 1,                           # Markup on salary estimation

        # INTEREST / Price
        'r'        : .03,                      # Interest at the bank
        'etaP'     : .192,                     # Typical rate for inflation
        'muP'      : 1.3,                      # Mark-up of price
        'gammaP'   : 1,                        # Money-illusion 

        ### FUNCTIONS AND THEIR PARAMETERS ########################################
        # PHILIPS CURVE (employement-salary increase)
        'phinul'   : 0.04,                     # Unemployement rate at which there is no salary increase with no inflation

        # KEEN INVESTMENT FUNCTION (profit-investment function)
        'k0'       : -0.0065,
        'k1'       : np.exp(-5),
        'k2'       : 20,

        # LINEAR DIVIDENT PROFITS 
        'div0'     : 0.138, # Part of GDP as dividends when pi=0
        'div1'     : 0.473, # Slope 

        # Coupling Effets (EDP) ##################################################
        'g1'  : .0    ,                       # GLOBAL         EFFECTS OF LAMBDA (Mean field)
        'g2'  : .00   ,                       # WITH NEIGHBORS EFFECTS OF LAMBDA (field)
        'muI' : 0     ,                       # 
        'muN' : 0     ,                       #

        # RELAXATION-BUFFER DYNAMICS #############################################
        'tauR'   : 2.0,                       # Typical time for recruitement (y)
        'tauF'   : 0.1,                       # Typical time for firing       (y)
        'tauLam' : 2. ,                       # Typical time for employement information 
        'tauK'   : 2  ,                       # Typical time on new capital integration

        #### GEMMES PARAMETERS ###################################################
        'theta'  : 2.6,                   # Convexity on abattement cost function
        'dsigma' : - 0.001,               # Variation rate of the growth of emission intensity 
        'dPBS'   : - 0.005,               # Growth rate of back-stop technology price   
        'dPc'    : 0, #[CORRECT]          # Growth rate of back-stop technology price 
        'dEland' : - 0.022,               # Growth rate of land use change in CO2 emission

        # Damage function (on GDP)
        'pi1' : 0         ,                # Linear temperature impact
        'pi2' : .00236    ,                # Quadratic temperature impact
        'pi3' : .00000507 ,                # Weitzmann Damage temperature impact 
        'zeta': 6.754     ,                # Weitzmann impact 
        
        'fk'  : 1/3       ,                # Fraction of environmental damage 
                                           # allocated to the stock of capital
  

        'C'     : 1/.098 ,# Heat capacity of fast-paced climate
        'C0'    : 3.52   ,# Heat capacity of inertial component of climate
        'gamma' : 0.0176 ,# Heat exchange coefficient between layer
        'Tsens' : 3.1    ,# Climate sensibility

        'dFexo'   : 0,
        'FexoMax' : 0 ,
        'F2CO2'   : 3.681, # W/M2, doubling CO2 impact on forced radiations
     
        # GREGOIRE'S MODEL        
        'z0'  : 1 ,
        'c'   : 1 ,
        'mu0' : 0.01 ,
        'RT'  : 2479 ,
        'Xsh' : 10**5 ,
        'chi' : 1/75
     }  
    
    params['omega0']     = 1-params['nu']*(params['alpha']+
                                           params['beta']+
                                           params['delta'])  # Solow point of a classic goodwin system          
    params['phi0']       = params['phinul']    / (1- params['phinul']**2)          # Based on Phinul value
    params['phi1']       = params['phinul']**(3) / (1- params['phinul']**2)        # Based on Phinul value
    params['lambdamin']  = 1- np.sqrt( params['phi1']/(params['alpha']+
                                                       params['phi0'])) # Same
    params['lambdamax']  = .98
    return params
