## Random matrices at equilibrium

We determine randomly :
* the content of the intermediate consumption matrix $\Gamma$
* the content of the capital composition matrix $\Xi$
* the structure of the consumption vector $C^{pond}$ (summing to 1)
* the local wage ponderation $w$
* the local productivity per worker $a$












hub=pgm.Hub('CHIMES0',verb=False)

########################################################
Nsect       = 3     # Number of sectors

gamma0      = 0.1   # Mean intermediate consumption
sigmagamma  = .1    # standard deviation on intermediate consumption

xi0         = 1     # Mean capital size 
sigmaxi     = .1    # standard deviation on capital size

apondscale = .05
wpondscale = .05
########################################################

### GENERATION #########################################
dparam0 = hub.supplements['generateNgoodwin'](Nsect) #Basic N Goodwin dictionnary 

# vector equivalent for wage and productivity 
dparam0['apond'] = np.random.normal(1,scale=apondscale,size=Nsect)
dparam0['z']     = np.random.normal(1,scale=wpondscale,size=Nsect)

dparam0['a'] = dparam0['a0']*dparam0['apond']
dparam0['w'] = dparam0['w0']*dparam0['z']

### MATRICES AND CONSUMPTION VECTOR (HERE RANDOM) ######
dparam0['Gamma'] = np.random.lognormal(size=(Nsect,Nsect))   
dparam0['Gamma']*= gamma0/np.sum(dparam0['Gamma'],axis=1)[:, np.newaxis]
dparam0['Gamma']*= (1+np.random.normal(scale=sigmagamma,size=Nsect ))[:, np.newaxis]

dparam0['Xi'] = np.random.lognormal(size=(Nsect,Nsect)) 
dparam0['Xi']*= xi0/np.sum(dparam0['Xi'],axis=1)[:, np.newaxis]
dparam0['Xi']*= (1+np.random.normal(scale=sigmaxi,size=Nsect ))[:, np.newaxis]

dparam0['Cpond'] = np.random.lognormal(size=Nsect) 
dparam0['Cpond']/= np.sum(dparam0['Cpond'])

########################################################
### Employment to no wage share change through Philips curve
dparam0['employment']= (dparam0['alpha']-dparam0['philinConst'])/dparam0['philinSlope'] # Linear Philips
#dparam0['employment']= 1 - np.sqrt(dparam0['phi1']/(dparam0['phi0']+dparam0['alpha'])) # Divergent Philips

### Price to ensuire ROC to be the natural growth rate of society
dparam0['p'] = hub.supplements['pForROC'](dparam0)
#dparam0['p']*=1.1
### Capital composition to be sure that dotV=0 then scaling for employment and N 
K= hub.supplements['Kfor0dotV'](dparam0)
K*=dparam0['employment']*dparam0['N']/np.sum(K/dparam0['a']) # homotetic scaling for employment and N
dparam0['K']= K
#dparam0['V']=dparam0['K']*dparam0['A']*dparam0['epsilonV']*1000000

dparam0['CESexp']= 10000
# RUN AND PLOT ######################################## 
hub.set_dparam(**dparam0,verb=True) 
hub.set_dparam('Tmax',200,verb=False) 

hub.run()

pgm.plots.plotnyaxis(hub,[
                         ['employmentAGG'],
                          ])
                          

pgm.plots.plotnyaxis(hub,[
                         [['V',sect] for sect in dparam0['Nprod']],
                          ])
                          #[[#['employment',dparam0['Nprod'][1]],
                          #['employment',dparam0['Nprod'][2]]]])

pgm.plots.plotnyaxis(hub,[
                         [['employment',sect] for sect in dparam0['Nprod']],
                         [['ROC',sect] for sect in dparam0['Nprod']],  
                         #[['omega',sect] for sect in dparam0['Nprod']],
                         #[['pi',sect] for sect in dparam0['Nprod']],
                         [['omegacarac',sect] for sect in dparam0['Nprod']],
                         [['l',sect] for sect in dparam0['Nprod']],  
                          ])
                          #[[#['employment',dparam0['Nprod'][1]],
                          #['employment',dparam0['Nprod'][2]]]])
"""
pgm.plots.plotnyaxis(hub,[
                         [['AcY',sect] for sect in dparam0['Nprod']],
                         [['AcI',sect] for sect in dparam0['Nprod']],
                         [['AcC',sect] for sect in dparam0['Nprod']], 
                          ])
                          #[[#['employment',dparam0['Nprod'][1]],
                          #['employment',dparam0['Nprod'][2]]]])
"""
for i,sect in enumerate(dparam0['Nprod']):
    title = sect +f"Gamma :{dparam0['Gamma'][i,:]}, Gamma :{dparam0['Xi'][i,:]}. Cpond :{dparam0['Cpond'][i]}"
    pgm.plots.plotnyaxis(hub,[[[var,sect]] for var in ['ROC','inflation','dotV','v','V']],title=title)#,tend=20)

pgm.plots.Sankey(hub,t=60)