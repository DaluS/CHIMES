# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_PCK = os.path.dirname(os.path.dirname(_PATH_HERE))
_PATH_OUTPUT_REF = os.path.join(_PATH_HERE, 'output_ref')


# library-specific
sys.path.insert(0, _PATH_PCK)   # ensure Main comes from .. => add PYTHONPATH
import pygemmes as pgm
sys.path.pop(0)                 # clean PYTHONPATH


#######################################################
#
#     Setup and Teardown
#
#######################################################


def setup_module():
    pass


def teardown_module():
    pass

#######################################################
#
#     Creating Ves objects and testing methods
#
#######################################################


class Test00_Get():

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test01_test_get(self):
        """ Make sure the main function runs from a python console """

        pgm.get_available_fields(exploreModels=True)
        pgm.get_available_functions()
        pgm.get_available_models(details=True)
        pgm.get_available_plots()

    def test02_run_all_models(self):
        dmodel = pgm.get_available_models(Return=dict)
        for k in dmodel.keys():
            if k!='__EMPTY__':
                for v in [None]+dmodel['Presets'][k]:
                    print(k,v)
                    hub=pgm.Hub(k,preset=v)
                    hub.set_dparam('Tmax',1)
                    hub.set_dparam('dt',0.01)
                    hub.run()
                    if v:
                        hub.plot_preset()

    def test03_generate_distribution(self):
        out =pgm.generate_dic_distribution(
                                      { 'alpha': {'mu': .02,
                                                  'sigma': .2,
                                                  'type': 'normal'},
                                        'k2': {'mu': 20,
                                               'sigma': .2,
                                               'type': 'log'},
                                        'mu': {'mu': 1.3,
                                               'sigma': .2,
                                               'type': 'uniform'},
                                            })

    def test04_all_plots(self):
        hub=pgm.Hub('GK')
        hub.set_dparam(**{'Tmax':100,'dt':0.1})
        hub.run()
        hub.reinterpolate_dparam(100)
        ### One var 
        pgm.plots.Var(hub,**{'key':'employment', 
                'mode':False, 
                'log':False,
                'idx':0, 
                'Region':0, 
                'tini':False, 
                'tend':False, 
                'title':''})
        pgm.plots.Var(hub,**{'key':'employment',
                'mode':'sensitivity',  #
                'log':False,
                'idx':0, 
                'Region':0, 
                'tini':False, 
                'tend':False, 
                'title':''})
        pgm.plots.Var(hub,**{'key':'employment',
                'mode':'sensitivity', 
                'log':True, #
                'idx':0, 
                'Region':0, 
                'tini':False, 
                'tend':False, 
                'title':''})
        pgm.plots.Var(hub,**{'key':'employment',
                'mode':'cycles', #
                'log':False,
                'idx':0, 
                'Region':0, 
                'tini':False, 
                'tend':False, 
                'title':''})
        pgm.plots.Var(hub,**{'key':'employment',
                'mode':False, 
                'log':False,
                'idx':0, 
                'Region':0, 
                'tini':10, #
                'tend':20, #
                'title':''})
        pgm.plots.Var(hub,**{'key':'employment',
                'mode':False, 
                'log':False,
                'idx':0, 
                'Region':0, 
                'tini':10, #
                'tend':20, #
                'title':'Hello'})


        pgm.plots.cycles_characteristics(hub,**{'xaxis':'omega', 
                                              'yaxis':'employment', 
                                              'ref':'employment', 
                                              'type1':'frequency', 
                                              'normalize':False, 
                                              'Region':0, 
                                              'title':''})
        pgm.plots.plotbyunits(hub,**{'filters_key':(),
                               'filters_units':(),
                               'filters_sector':(),
                               'separate_variables':{}, 
                               'lw':1, 
                               'idx':0, 
                               'Region':0, 
                               'tini':False, 
                               'tend':False, 
                               'title':''})
        pgm.plots.plotbyunits(hub,**{'filters_key':(),
                               'filters_units':(),
                               'filters_sector':(),
                               'separate_variables':{}, 
                               'lw':1, 
                               'idx':0, 
                               'Region':0, 
                               'tini':10, 
                               'tend':15, 
                               'title':''})
        pgm.plots.plotbyunits(hub,**{'filters_key':('pi','Pi'),
                               'filters_units':('y^{-1}'),
                               'filters_sector':(),
                               'separate_variables':{'':['omega']}, 
                               'lw':1, 
                               'idx':0, 
                               'Region':0, 
                               'tini':10, 
                               'tend':15, 
                               'title':''})
        pgm.plots.plotnyaxis(hub,**{'y':[['pi','omega'],['d']],
                                   'x':'time', 
                                   'idx':0,
                                   'Region':0,
                                   'log':False,# []
                                   'title':'', 
                                   })
        pgm.plots.plotnyaxis(hub,**{'y':[['omega'],['employment']],
                                   'x':'time', 
                                   'idx':0,
                                   'Region':0,
                                   'log':True,
                                   'title':'', 
                                   })
        pgm.plots.plotnyaxis(hub,**{   'y':[['omega'],['employment']],
                                   'x':'time', 
                                   'idx':0,
                                   'Region':0,
                                   'log':[True,False],
                                   'title':'', 
                                   })
        #pgm.plots.repartition()

        pgm.plots.XY(hub,**{    'x':'employment',
                            'y':'omega',
                            'color':'d', 
                            'scaled':True,
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':'', 
                            })
        pgm.plots.XY(hub,**{    'x':'employment',
                            'y':'omega',
                            'color':'d', 
                            'scaled':False,
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':'', 
                            })
        pgm.plots.XY(hub,**{    'x':'employment',
                            'y':'omega',
                            'color':'d', 
                            'scaled':False,
                            'idx':0, 
                            'Region':0, 
                            'tini':10, 
                            'tend':15, 
                            'title':'', 
                            })
        pgm.plots.XYZ(hub,**{   'x':'employment',
                            'y':'omega',
                            'z':'d', 
                            'color':'time', 
                            'idx':0, 
                            'Region':0, 
                            'tini':False, 
                            'tend':False, 
                            'title':''},)
        pgm.plots.XYZ(hub,*{   'x':'employment',
                            'y':'omega',
                            'z':'d', 
                            'color':'time', 
                            'idx':0, 
                            'Region':0, 
                            'tini':10, 
                            'tend':20, 
                            'title':''},)

    def test05_set_params(self):
        hub=pgm.Hub('GK')
        dpreset = {'test': {'fields': {'philinConst': -0.55465958},
                           'com': '',
                           'plots': {}},}
        hub.set_dpreset(dpreset,preset='test')
        
        hub=pgm.Hub('GK')
        hub.set_preset('test')

        # Monosectoral 
        hub=pgm.Hub('GK',verb=False); hub.set_dparam('a',1           ,verb=False)
        hub=pgm.Hub('GK',verb=False); hub.set_dparam('alpha',0.01    ,verb=False)  
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'alpha':0.01},verb=False)      

        # Dimensions nr and nx 
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'Tmax':10,
                                                        'dt':0.01},verb=False)
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nx':10,
                                                        'nr':5},verb=False)
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nx':['one','two'],
                                                        'nr':['here','there','test']},verb=False)

        # Multiple values 
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nx':3,
                                                        'alpha':[0.01,0.02,0.03]})
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nr':['France','USA'],
                                                        'alpha':[['nr','France'],0.01]})    
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nr':['France','USA'],
                                                        'nx': 3,    
                                                        'alpha':[['nr','France'],['nx',1],0.01]})
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nr':['France','USA'],
                                                        'nx': 6,    
                                                        'alpha':[['nr',0],['nx',0,4],[0.5,0.2]]}) 
        hub=pgm.Hub('GK',verb=False); hub.set_dparam(**{'nr':['France','USA'],
                                                        'nx': 6, 
                                                        'alpha':{'nr':['France','USA'],
                                                                 'nx':1,
                                                                 'value':0.5}})

        # Multisectoral        
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam('p',[0.1,1])                      #will put [0,1] for all parrallel all regions
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam('p',[['nr',0],[0.1,1]])            #will put [0,1] for all parrallel in region 0
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam('p',[['nr',0,1],[0.1,1]])          #will put [0,1] for all parrallel in region 0 and 1
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam('p',[['nx',0],['nr',0,1],[0.1,1]]) #will put [0,1] for parrallel system 0, in region 0 and 1
                                                                                                 
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam('Gamma',[[0,1],[1,0]])  #will put [[0,1],[1,0]] for all parrallel all regions
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam(**{'Gamma': {'first':['Consumption','Capital'],
                                                                                        'second':['Consumption','Consumption'],
                                                                                        'nr':0,
                                                                                        'value':[0.5,0.22]}})
        hub=pgm.Hub('CHIMES',preset='SimpleBi',verb=False);hub.set_dparam(**{'Gamma': {'first':['Consumption','Capital'],
                                                                                       'nr':0,
                                                                                       'value':[0.5,0.22]}})

                                                                            
    def test06_network(self):
        hub=pgm.GK()
        hub.get_network()
        hub.get_Network(params=True)                    # state,differential,parameters
        hub.get_Network(auxilliary=False,params=True)   # remove auxilliary statevar and differential
        hub.get_Network(filters=('Pi',))                # remove the variable Pi and its connexions
        hub.get_Network(filters=('Pi',),redirect=True) 

    def test07_description(self):
        hub=pgm.GK()
        hub.get_equations_description()
        hub.get_summary()
        _=hub.dmodel
        _=hub.dmisc
        _=hub.dparam
        print(hub)
        hub.get_dparam_as_reverse_dict(
    crit='units',
    eqtype=['differential', 'statevar'])

    def test08_distributions(self):
        import numpy as np
        print(np.linspace(0,0.1,3))
        hub=pgm.Hub('GK',verb=False)
        hub.set_dparam(**{
            'nx':3,
            'alpha':np.linspace(0,0.1,3),})
        hub.run()
        pgm.plots.Var(hub,'employment',mode='sensitivity')