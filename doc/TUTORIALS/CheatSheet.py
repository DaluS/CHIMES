##################################################################
#################### PYGEMMES CHEATSHEET #########################
##################################################################
Tab for autocompletion
? for docstring 

##################################################################

### LOADING PYGEMMES 
import sys 
path = "YOURPATHTOTHELIBRARY" 
sys.path.insert(0, path)
import pygemmes as pgm

### LOOKING AT AVAILABLE MODELS
pgm.get_available_models()
lmodel = pgm.get_available_models(Return=dict).keys()

### LOADING MODEL
hub=pgm.Hub('GK',preset=False,verb=False)

### INTROSPECTION 
hub.get_summary()
hub.get_fieldsproperties()
hub.get_dataframe(t0=0,t1=0).transpose()
hub.get_Network(params=True)      
groupsoffields = hub.get_dparam_as_reverse_dict(
    crit='units',
    eqtype=['differential', 'statevar',None])

### MINIMAL RUN AND PLOT 
hub.run(N=100)
hub.plot()
hub.plot(filters_units=['','y'],
         filters_key=('kappa'),
         separate_variables={'':['employment','omega']},
         title='basic GK') ### Everything but the dimensionless units

### FIELDS INTROSPECTION 
R=hub.get_dparam()
hub.dparam 
R['employment']['value'][:,0,0,0,0]

