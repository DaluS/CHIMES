# -*- coding: utf-8 -*-
#rootfold='/home/ejp/Desktop/Goodwin-Keen/simulations'
rootfold='D:\\Georgetown\\Simulation-Goodwin\\'

### WELCOME MESSAGE ################################################################################
"""
GOODWIN-TYPE RESOLUTION ALGORITHM 

This python code has been created to simulate Goodwin-Keen simulations, with all the variants to it. 
Do not worry about the number of section : the architecture is thought to be user-friendly and coder-friendly

WHAT ARE THE SPECIFICITIES OF THIS CODE ? 
* The algorithm solve p['Nx'] system in parrallel : the idea is that later we will couple the systems altogether ("spatial/network properties").
* For now, there is no much coupling, but you can use it to test many initial conditions and array of parameters values 
* The steps are :
    - Creation of the parameters dictionnary p ( in Parameters.py for initial values)
    - Creation of initial conditions in the dictionnary ic
    - Translation into machine friendly variable y
    - Calculation of all the dynamics variable Y_s (the temporal loop)
    - Translation into user-friendly result in the dictionnary r 
    - Additional analysis (period, slow enveloppe mouvement...)
    - Plot of variables and analysis through r

HOW TO IMPLEMENT YOUR TOY-MODEL ? 
 * Add the parameters in Parameters.py (check if it isn't already, or if the name isn't already taken)
 * Add the temporal component in FG.preparedT for dt selection
 * Add the related quantity in the dictionnary of initial condition ic
 * Add a section to prepareY
 * Add the equations in a f_THENAMEOFTHEFUNCTION
 * Add the redevelopment in FG.expand
 * have fun !
 
WHAT I AM (Paul) LOOKING FOR IN FURTHER DEVELOPMENT 
* Check the functions in FunctionGoodwin, I've done some mistakes in more complex models (typically coping with collapse)
* Add spatial operators which are non unstable ( I have implicit scheme elsewhere but it's a different kind of resolution, and much more work when you change a model)
* Have a list of all models existing in this framework (copingwithcollapse, Harmoney, predatory-prey...) and code them
* The plots are UGLY ! Let's do something nicer
* As Iloveclim and Dymends are not in python, prepare some bindings 
"""

### INITIALISATION LIBRAIRIES ######################################################################
####################################################################################################
for _ in range(1):
    """
    The code is importing some other libraries so that we can use their functions. 
    """
    import time                     # Time (run speed) printing
 
    """
    These libraries are local code fragments we use later
    """
    import Parameters as Par      # All the parameters of the system
    import ClassesGoodwin as C # Core of models
    import Miscfunc as M          # All miscellaneous functions

    ### MATPLOTLIB INTERACTIVITY ####
    '''
    Matplotlib allow in-line (in terminal) output or interactive output. Select one here.
    You can change it in the jupyter (interactive terminal) of your IDE also 
    %matplotlib # Allow interactive output
    %matplotlib inline # plot in terminal
    '''
    #%matplotlib inline 

#print('List of existing set of equations  :')
#for f in [ f for f in dir(FG) if 'f_' in f] : print(f)
#print(3*'\n')

### PARAMETERS INITIALISATION ######################################################################
####################################################################################################    
for _ in range(1):
    """
    This part create 'p' (parameters dic) and 'op' (operators dic) depending of the system size and properties
    Typically, p contains the "default parameters" values and should be open in another windows, 
    I edit them after p initialisation if I want to do some original runs 
    """
    
    SYS = C.GK_Reduced()       # SYSTEM SOLVED 
    pN= Par.parnum()           # Value of numerical parameters 
    p = Par.initparams()       # Value of "Physical" parameters    
    ic= Par.initCond(p,pN)     # Values of the initial parameters 
    op= M.prepareOperators(pN)  # Spatial operators initialisation

    p['Nx']=pN['Nx']
### initial conditions #############################################################################
####################################################################################################
"""
The initial state vector at t=0 of the system in a "readable" language.
Depending of the equation set you use, all of them will not necessary be used. 
(example, a reduced set will read ic['d'], a complete set will read ic['D']) 
"""
tim=time.time();print('Start simulation...',end='')

y        = SYS.initializeY(ic,pN)            ### The vector y containing all the state of a time t.
Y_s, t_s = M.TemporalLoop(y,SYS,op,pN,p)### Calculation of all timesteps

print('done ! elapsed time :', time.time()-tim,'s')        

#if p['Save'] : FG.savedata(rootfold,t,Y_s,p,op) # Save the data as a pickle file in a new folder
### Results interpretation #########################################################################
####################################################################################################
"""
Now that the simulation is done, we can translate its results in a more readable fashion. 
r is the expansion of Y_s into all the relevant variables we are looking for, stored as a dictionnary.
Then, the other parts are simply plots of the result
"""

r = SYS.expandY_simple(Y_s,t_s,op,p)  # Result dictionnary 
#r = M.getperiods(r,p,op)      # Period measurements 


### PLOTS ##########################################################################################
#################################################################################################### 
SYS.plotlitst_simple(r,p)
#plts.PhilAndInvest(p,)             # Show behavior functions 
#plts.GoodwinKeenTypical(r,p,)      # Typical 3-Dimension phase-plot
#plts.omegalambdacycles(r,p,)       # 2-D omega-lambda phase portrait
#plts.GraphesIntensive(r,p)    
#plts.GraphesExtensive(r,p) 
#plts.PhasewithG(r,p,op,)           # Phase diagram with growth
#plts.PeriodPlots(r,p,op,)          # Study stability-period
#plts.map2DLambdaT(r,op,)
#plts.MesoMeanSTD(r,p,op,)
