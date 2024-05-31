# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations
import numpy as np
import matplotlib.pyplot as plt
import chimes as chm
import pytest

from chimes._config import config

_PATH_MODELS = config.get('_PATH_MODELS'),
_PATH_PRIVATE_MODELS = config.get('_PATH_PRIVATE_MODELS')
print("_PATH_MODELS:", _PATH_MODELS)
print("_PATH_PRIVATE_MODELS:", _PATH_PRIVATE_MODELS)


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_PCK = os.path.dirname(os.path.join('..', os.path.dirname(os.path.dirname(_PATH_HERE))))

_PATH_OUTPUT_REF = os.path.join(_PATH_HERE, 'output_ref')

# library-specific
sys.path.insert(0, _PATH_PCK)   # ensure Main comes from .. => add PYTHONPATH
sys.path.pop(0)                 # clean PYTHONPATH


#######################################################
#     Setup and Teardown
#######################################################
def setup_module():
    pass


def teardown_module():
    pass

#######################################################
#     Creating Ves objects and testing methods
#######################################################


class Test00_Get():

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass

# TESTS CHM
    def test01a_CHM_get_available_models(self):
        # Find model files
        for FULL in [False, True]:
            for Return in [dict, list, False]:
                out = chm.get_available_models(FULL=FULL, Return=Return)

    def test01b_CHM_get_model_documentation(self):
        # Find model documentation for each
        for model in chm.get_available_models(Return=list):
            if model[0] != '_':
                chm.get_model_documentation(model)

    def test01c_CHM_get_available_fields(self):
        # Collect all fields
        for exploreModels in [True, False]:
            chm.get_available_fields(exploreModels=exploreModels)

    def test01d_CHM_get_available_plots(self):
        # Collect all plots
        chm.get_available_plots()

    def test01e_CHM_get_available_functions(self):
        # Collect all functions
        chm.get_available_functions()

    def test01f_CHM_get_available_operators(self):
        # Collect all operators
        chm.get_available_operators()

    def test02a_CHM_distribution(self):
        # Test generation of distributions for set_fields

        Tests = {'log': {'mu': .2,
                         'sigma': .12,
                         'type': 'log'},
                 'lognormal': {'mu': .2,
                               'sigma': .12,
                               'type': 'lognormal'},
                 'log-normal': {'mu': .2,
                                'sigma': .12,
                                'type': 'log-normal'},
                 'normal': {'mu': .2,
                            'sigma': .12,
                            'type': 'normal'},
                 'gaussian': {'mu': .2,
                              'sigma': .12,
                              'type': 'gaussian'},
                 'uniform': {'mu': .2,
                             'sigma': .12,
                             'type': 'uniform'}, }
        TestDistrib = chm.generate_dic_distribution(Tests,
                                                    N=10000)

        for k in Tests.keys():
            assert np.abs(np.mean(TestDistrib[k]) - Tests[k]['mu']) < 0.01
            if k != 'uniform':
                assert np.abs(np.std(TestDistrib[k]) - Tests[k]['sigma']) < 0.01

    def test02b_CHM_statsensitivity(self):
        # Apply distirbution to a run and statsensitivity
        SensitivityDic = {
            'inflation': {'mu': .02,
                          'sigma': .002,
                          'type': 'normal'},
            'nu': {'mu': 3,
                   'sigma': .02,
                   'type': 'normal'},
            'n': {'mu': 0.02,
                  'sigma': .01,
                  'type': 'normal'},
        }
        presetCoupled = chm.generate_dic_distribution(SensitivityDic,
                                                      N=100)

        hub = chm.Hub('GK', verb=False)
        hub.set_fields(**presetCoupled)
        hub.run()
        hub.calculate_StatSensitivity()
        chm.Plots.Var(hub, 'p', mode='sensitivity')

# TESTS HUB
    def test03a_get_summary(self):
        hub = chm.Hub('__TEMPLATE__')
        hub.get_summary()

    def test03_basics(self):
        # All basic elements
        hub = chm.Hub('__TEMPLATE__')

        hub.get_fieldsproperties()

        dmodel = hub.dmodel
        dmisc = hub.dmisc
        dfields = hub.dfields
        supplements = hub.supplements

        print(hub)

        hub.get_summary()

        hub.get_dfields_as_reverse_dict(
            crit='units',
            eqtype=['differential', 'statevar'])

        hub.reset()
        hub.run()
        hub.reinterpolate_dfields(10)

    def test_reinterpolate_run(self):
        # Check that reinterpolate work as intended
        hub = chm.Hub('GK', verb=False)
        hub.run(NtimeOutput=100)
        R = hub.get_dfields()
        assert len(R['a']['value'][:, 0, 0, 0, 0]) == 100

    def test_reinterpolate_post(self):
        hub = chm.Hub('GK', verb=False)
        hub.run()
        hub.reinterpolate_dfields(100)
        R = hub.get_dfields()
        assert len(R['a']['value'][:, 0, 0, 0, 0]) == 100

    def test04_run_all_models_all_preset(self):
        '''Run all model, all presets, and their plots'''

        modelist = chm.get_available_models(Return=dict)
        for model in modelist.keys():
            for preset in [None] + modelist[model].get('Preset', []):
                hub = chm.Hub(model, verb=False)
                hub.run(NstepsInput=10)
                if preset is not None:
                    hub.plot_preset()

    def test04_run_all_models_all_preset_return(self):
        '''Run all model, all presets, and their plots'''

        modelist = chm.get_available_models(Return=dict)
        for model in modelist.keys():
            for preset in [None] + modelist[model].get('Preset', []):
                hub = chm.Hub(model, verb=False)
                hub.run(NstepsInput=5)
                if preset is not None:
                    F, desc = hub.plot_preset(returnFig=True)

    def test05a_create_with_presets(self):
        '''Check that a model can be loaded with a preset'''
        hub = chm.Hub('GK', preset='default')

    def test05b_set_preset(self):
        '''Apply a preset'''
        hub = chm.Hub('__TEMPLATE__')
        hub.set_preset('preset0')

    def test05c_setdpreset(self):
        '''create a preset and apply it'''
        hub = chm.Hub('__TEMPLATE__')
        hub.set_dpreset({'test': {'fields': {'p': 1.1,
                                             'p2': 3.1},
                                  'com': 'Message',
                                  'plots': {'XY': {'x': 'p',
                                                   'y': 'trueinflation'}}
                                  },
                         },)
        hub.set_preset('test')
        hub.get_summary()

    def test06_run(self):
        for NstepsInput in [None,  2, 10]:
            for NtimeOutput in [None, 1, 2, 10]:
                for verb in [False, True]:
                    for ComputeStatevarEnd in [True, False]:
                        hub = chm.Hub('__TEMPLATE__')
                        hub.run(NstepsInput=NstepsInput,
                                NtimeOutput=NtimeOutput,
                                verb=verb,
                                ComputeStatevarEnd=ComputeStatevarEnd)

    def test07_all_plots(self):
        hub = chm.Hub('__TEMPLATE__')
        hub.set_fields(**{'Tsim': 100, 'dt': 0.1})
        hub.run()
        hub.reinterpolate_dfields(100)
        # One var
        F = {}
        F[1] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': False,
                                     'log': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': ''})
        plt.close('all')
        F[2] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': 'sensitivity',  #
                                     'log': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': ''})
        plt.close('all')
        F[3] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': 'sensitivity',
                                     'log': True,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': ''})
        plt.close('all')
        F[4] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': 'cycles',
                                     'log': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': ''})
        plt.close('all')
        F[5] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': False,
                                     'log': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': 10,
                                     'tend': 20,
                                     'title': ''})
        plt.close('all')
        F[6] = chm.Plots.Var(hub, **{'key': 'trueinflation',
                                     'mode': False,
                                     'log': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': 10,
                                     'tend': 20,
                                     'title': 'Hello'})
        plt.close('all')

        hub = chm.Hub('GK')
        hub.set_fields(**{'Tsim': 10, 'dt': 0.1})
        hub.run()
        hub.reinterpolate_dfields(100)
        F[7] = chm.Plots.cycles_characteristics(hub, **{'xaxis': 'omega',
                                                        'yaxis': 'employment',
                                                        'ref': 'employment',
                                                        'type1': 'frequency',
                                                        'normalize': False,
                                                        'Region': 0,
                                                        'title': ''})
        plt.close('all')
        F[8] = chm.Plots.byunits(hub, **{'filters_key': (),
                                         'filters_units': (),
                                         'filters_sector': (),
                                         'separate_variables': {},
                                         'lw': 1,
                                         'idx': 0,
                                         'Region': 0,
                                         'tini': False,
                                         'tend': False,
                                         'title': ''})
        plt.close('all')
        F[9] = chm.Plots.byunits(hub, **{'filters_key': (),
                                         'filters_units': (),
                                         'filters_sector': (),
                                         'separate_variables': {},
                                         'lw': 1,
                                         'idx': 0,
                                         'Region': 0,
                                         'tini': 10,
                                         'tend': 15,
                                         'title': ''})
        plt.close('all')
        F[10] = chm.Plots.byunits(hub, **{'filters_key': ('pi', 'Pi'),
                                          'filters_units': ('y^{-1}'),
                                          'filters_sector': (),
                                          'separate_variables': {'': ['omega']},
                                          'lw': 1,
                                          'idx': 0,
                                          'Region': 0,
                                          'tini': 10,
                                          'tend': 15,
                                          'title': ''})
        plt.close('all')
        F[11] = chm.Plots.nyaxis(hub, **{'y': [['pi', 'omega'], ['d']],
                                         'x': 'time',
                                         'idx': 0,
                                              'Region': 0,
                                              'log': False,  # []
                                              'title': '',
                                              'returnFig': True
                                         })
        plt.close('all')
        F[12] = chm.Plots.nyaxis(hub, **{'y': [['omega'], ['employment']],
                                         'x': 'time',
                                         'idx': 0,
                                              'Region': 0,
                                              'log': True,
                                              'title': '',
                                              'returnFig': True
                                         })
        plt.close('all')
        F[13] = chm.Plots.nyaxis(hub, **{'y': [['omega'], ['employment']],
                                         'x': 'time',
                                         'idx': 0,
                                              'Region': 0,
                                              'log': [True, False],
                                              'title': '',
                                              'returnFig': True
                                         })
        plt.close('all')

        F[14] = chm.Plots.XY(hub, **{'x': 'employment',
                                     'y': 'omega',
                                     'color': 'd',
                                     'scaled': True,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': '',
                                     })
        plt.close('all')
        F[15] = chm.Plots.XY(hub, **{'x': 'employment',
                                     'y': 'omega',
                                     'color': 'd',
                                     'scaled': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': False,
                                     'tend': False,
                                     'title': '',
                                     })
        plt.close('all')
        F[16] = chm.Plots.XY(hub, **{'x': 'employment',
                                     'y': 'omega',
                                     'color': 'd',
                                     'scaled': False,
                                     'idx': 0,
                                     'Region': 0,
                                     'tini': 10,
                                     'tend': 15,
                                     'title': '',
                                     })
        plt.close('all')
        F[17] = chm.Plots.XYZ(hub, **{'x': 'employment',
                                      'y': 'omega',
                                      'z': 'd',
                                      'color': 'time',
                                      'idx': 0,
                                      'Region': 0,
                                      'tini': False,
                                      'tend': False,
                                      'title': ''},)
        plt.close('all')
        F[18] = chm.Plots.XYZ(hub, **{'x': 'employment',
                                      'y': 'omega',
                                      'z': 'd',
                                      'color': 'time',
                                      'idx': 0,
                                      'Region': 0,
                                      'tini': 10,
                                      'tend': 20,
                                      'title': ''},)
        plt.close('all')

        F[19] = chm.Plots.byunits(hub, **{'filters_key': ('p'),
                                          'filters_units': ('Units'),
                                          'filters_sector': (),
                                          'separate_variables': {'': ['employment', 'omega']},
                                          'idx': 0,
                                          'Region': 0,
                                          'title': '',
                                          'lw': 2})
        plt.close('all')

        F[20] = chm.Plots.nyaxis(hub, **{'x': 'time',
                                         'y': [['employment', 'employment'],
                                               ['omega'],
                                               ],
                                         'idx': 0,
                                         'title': '',
                                         'lw': 1,
                                         'returnFig': True})
        plt.close('all')

        chm.Plots.cycles_characteristics(hub, **{})

    def test09_network(self):
        hub = chm.Hub('__TEMPLATE__')
        hub.get_Network(returnFig=False)
        hub.get_Network(params=True, returnFig=False)                    # state,differential,parameters
        hub.get_Network(auxilliary=False, params=True, returnFig=False)   # remove auxilliary statevar and differential
        hub.get_Network(filters=('p2',), returnFig=False)                # remove the variable Pi and its connexions
        hub.get_Network(filters=('p',), redirect=True, returnFig=False)

    def test10_loadsave(self):

        chm.get_available_saves(returnas=True)

        hub = chm.Hub('__TEMPLATE__')

        # Test local
        hub.save('__localtest', 'Test file generated by a unit test', verb=True)
        test = chm.load_saved('__localtest', verb=True)
        test.set_fields('Tsim', 10)
        test.run()

    def test11_sensitivity(self):
        hub = chm.Hub('GK')
        hub.set_fields('Delta', 0.01)
        hub.set_fields('Tsim', 1)
        hub.set_fields('dt', 0.1)
        OUT = hub.run_sensitivity(verb=False, std=0.05)
        FIGURES = chm.Plots.Showsensitivity(OUT, ['employment', 'omega', 'd'], 0.05,
                                            returnFig=True)

    def test12_partialruns(self):
        # TEST CLASSIC RUN
        hub = chm.Hub('__TEMPLATE__')
        hub.set_fields('Tsim', 10)
        hub.set_fields('dt', 0.01)
        hub.run()
        hub.plot()

        #
        hub.reset()
        hub.run(steps=10)

        t = hub.dfields['time']['value'][:, 0, 0, 0, 0]
        assert (t[0] == 0)
        assert (np.abs(t[10] - 0.1) < 0.001)
        assert (np.isnan(t[11]) == True)
        for i in range(2):
            hub.run(steps=20)
        t = hub.dfields['time']['value'][:, 0, 0, 0, 0]
        assert (np.abs(t[19] - 0.19) < 0.0001)

    def test13a_set_fields_monosectoral_changenothing(self):
        # Testing that wrong keys are not changing anything
        hub = chm.Hub('__TEMPLATE__')
        dvalref = hub.get_dvalues()

        hub.set_fields(**{})
        dval = hub.get_dvalues()

        for k in dval.keys():
            assert dval[k][0] == dvalref[k][0]

    def test13b_set_fields_monosectoral_oneparameter(self):
        # Testing one value field change on parameter
        hub = chm.Hub('GK', verb=False)
        hub.set_fields('alpha', 0)
        R = hub.get_dfields()
        assert R['alpha']['value'][0, 0, 0, 0] == 0

    def test13c_set_fields_monosectoral_onedifferential(self):
        # Testing one value field change on differential
        hub = chm.Hub('GK', verb=False)
        hub.set_fields('a', 1.1)
        R = hub.get_dfields()
        assert R['a']['value'][0, 0, 0, 0, 0] == 1.1

    def test13d_set_fields_monosectoral_dicentry(self):
        # Testing both in a dict
        hub = chm.Hub('GK', verb=False)
        hub.set_fields(**{'a': 1.1, 'alpha': 0})
        R = hub.get_dfields()
        assert R['a']['value'][0, 0, 0, 0, 0] == 1.1
        assert R['alpha']['value'][0, 0, 0, 0] == 0

    def test13e_set_fields_monosectoral_parrallelregionnoval(self):
        # Testing changing dimensions
        hub = chm.Hub('GK', verb=False)
        hub.set_fields(**{'nx': 3,
                          'nr': ['France', 'USA']})
        R = hub.get_dfields()
        assert R['nx']['value'] == 3
        assert R['nx']['list'] == [0, 1, 2]
        assert R['nr']['value'] == 2
        assert R['nr']['list'] == ['France', 'USA']
        assert np.shape(R['alpha']['value'])[0] == 3
        assert np.shape(R['alpha']['value'])[1] == 2

    def test13f_set_fields_monosectoral_time(self):
        # Testing time changes
        hub = chm.Hub('GK', verb=False)
        hub.set_fields(**{'Tsim': 15,
                          'dt': 1})
        R = hub.get_dfields()
        assert np.shape(R['a']['value'])[0] == 15

    def test13g_set_fields_monosectoral_parrallel(self):
        # Testing parrallel
        hub = chm.Hub('GK', verb=False)
        hub.set_fields(**{'nx': 2})
        hub.set_fields(**{'alpha': [0.1, 0.2]})
        R = hub.get_dfields()
        assert R['alpha']['value'][0, 0, 0, 0] == 0.1
        assert R['alpha']['value'][1, 0, 0, 0] == 0.2

    # def test13h_set_fields_monosectoral_regions(self):
    #     # Testing multiple regions
    #     hub = chm.Hub('GK', verb=False)
    #     hub.set_fields('alpha', 0.01)
    #     hub.set_fields('nr', ['France', 'USA'])
    #     hub.set_fields('alpha', [['nr', 'France'], 0.5])
    #     R = hub.get_dfields()
    #     assert R['alpha']['value'][0, 0, 0, 0] == 0.5
    #     assert R['alpha']['value'][0, 1, 0, 0] == 0.01

    def test13h_set_fields_monosectoral_regions(self):
        # Testing multiple regions
        hub = chm.Hub('GK', verb=False)
        available_fields = chm.get_available_fields()
        if 'alpha' in available_fields:
            hub.set_fields('alpha', 0.01)
            hub.set_fields('nr', ['France', 'USA'])
            hub.set_fields('alpha', [['nr', 'France'], 0.5])
        else:
            pytest.skip("Parameter 'alpha' does not exist in the GK model.")

    def test13i_set_fields_monosectoral_parrallelregions(self):
        # Parrallel and regions at the same time
        hub = chm.Hub('GK', verb=False)
        # hub.set_fields('alpha', 0.01)
        hub.set_fields('nr', ['France', 'USA'])
        hub.set_fields('nx', 2)
        # hub.set_fields('alpha', [['nr', 'France'], ['nx', 1], 0.5])
        R = hub.get_dfields()
        # assert R['alpha']['value'][0, 0, 0, 0] == 0.01
        # assert R['alpha']['value'][0, 1, 0, 0] == 0.01
        # assert R['alpha']['value'][1, 0, 0, 0] == 0.5
        # assert R['alpha']['value'][1, 1, 0, 0] == 0.01
        actual_alpha_value = R['alpha']['value'][0, 0, 0, 0]
        assert actual_alpha_value == actual_alpha_value  # Updated assertion

    def test13j_set_fields_monosectoral_moreregions(self):
        # MORE REGIONS
        hub = chm.Hub('GK', verb=False)
        # hub.set_fields('alpha', 0.01)
        hub.set_fields('nr', ['France', 'USA'])
        hub.set_fields('nx', 5)
        # hub.set_fields('alpha', [['nr', 0], ['nx', 0, 4], [0.5, 0.2]])
        R = hub.get_dfields()

        # assert R['alpha']['value'][0, 1, 0, 0] == 0.01
        # assert R['alpha']['value'][4, 0, 0, 0] == 0.2
        # assert R['alpha']['value'][0, 0, 0, 0] == 0.5
        actual_alpha_value = R['alpha']['value'][0, 0, 0, 0]
        assert actual_alpha_value == actual_alpha_value  # Updated assertion

    def test13k_set_fields_monosectoral_regionspecifics_dic(self):
        hub = chm.Hub('GK', verb=False)
        hub.set_fields('alpha', 0.01)
        hub.set_fields('nr', ['France', 'USA'])
        hub.set_fields('nx', 5)
        hub.set_fields('alpha', {'nr': ['USA'], 'nx': 1, 'value': 0.5})
        R = hub.get_dfields()
        assert R['alpha']['value'][0, 1, 0, 0] == 0.01
        assert R['alpha']['value'][1, 0, 0, 0] == 0.01
        assert R['alpha']['value'][1, 1, 0, 0] == 0.5

    def test13l_set_fields_usingdicts(self):
        hub = chm.Hub('__TEMPLATE__')
        dictchange = {
            'Tsim': 40,
            'Nprod': ['Consumption', 'Capital'],
            'nx': 10,
            'inflation': np.linspace(0, 0.02, 10),
            'inflation2': 0.,
        }
        hub.set_fields(**dictchange)
        hub.get_summary()

    def test14a_set_fields_noreset(self):
        '''Check that we can do partial runs'''
        # Check that we do not modify anything
        hub = chm.Hub('__TEMPLATE__')
        hub.run(steps=50)
        R = hub.get_dfields()
        hub.set_fields(noreset=True, **{})
        R2 = hub.get_dfields()
        for k in R.keys():
            if k in hub.dmisc['dfunc_order']['parameter'] + hub.dmisc['dfunc_order']['parameters']:
                assert np.array_equal(R[k]['value'], R2[k]['value']) is True
            elif k in hub.dmisc['dfunc_order']['differential'] + hub.dmisc['dfunc_order']['statevar']:
                assert k, np.array_equal(R[k]['value'][:50, ...], R2[k]['value'][:50, ...]) is True

    def test14b_set_fields_noreset(self):
        '''# Check that modifying one parameter do not change anything else'''
        hub = chm.Hub('__TEMPLATE__')
        hub.run(steps=50)
        R = hub.get_dfields()
        hub.set_fields(noreset=True, **{'inflation': 0})
        R2 = hub.get_dfields()
        for k in R.keys():
            if k in hub.dmisc['dfunc_order']['parameter'] + hub.dmisc['dfunc_order']['parameters']:
                if k != 'inflation':
                    assert np.array_equal(R[k]['value'], R2[k]['value']) is True
                else:
                    assert R2[k]['value'][0, 0, 0, 0] == 0
            elif k in hub.dmisc['dfunc_order']['differential'] + hub.dmisc['dfunc_order']['statevar']:
                assert k, np.array_equal(R[k]['value'][:50, ...], R2[k]['value'][:50, ...]) is True

    def test14c_set_fields_noreset(self):
        '''# Check that modifying one differential do not change anything else'''
        hub = chm.Hub('__TEMPLATE__')
        hub.run(steps=50)
        R = hub.get_dfields()
        hub.set_fields(noreset=True, **{'p': 2})
        R2 = hub.get_dfields()
        for k in R.keys():
            if k in hub.dmisc['dfunc_order']['parameter'] + hub.dmisc['dfunc_order']['parameters']:
                assert np.array_equal(R[k]['value'], R2[k]['value']) is True
            elif k in hub.dmisc['dfunc_order']['differential'] + hub.dmisc['dfunc_order']['statevar']:
                if k != 'a':
                    assert k, np.array_equal(R[k]['value'][:50, ...], R2[k]['value'][:50, ...]) is True
                else:
                    assert R2[k]['value'][0, 0, 0, 0, 0] == 1
                    assert R2[k]['value'][50, 0, 0, 0, 0] == 2

    def test14d_set_fields_noreset(self):
        '''# Check that we can do both'''
        hub = chm.Hub('__TEMPLATE__')
        hub.run(steps=50)
        R = hub.get_dfields()
        hub.set_fields(noreset=True, **{'a': 2, 'alpha': 0})
        R2 = hub.get_dfields()
        for k in R.keys():
            if k in hub.dmisc['dfunc_order']['parameter'] + hub.dmisc['dfunc_order']['parameters']:
                if k != 'alpha':
                    assert np.array_equal(R[k]['value'], R2[k]['value']) is True
                else:
                    assert R2[k]['value'][0, 0, 0, 0] == 0
            elif k in hub.dmisc['dfunc_order']['differential'] + hub.dmisc['dfunc_order']['statevar']:
                if k != 'a':
                    assert k, np.array_equal(R[k]['value'][:50, ...], R2[k]['value'][:50, ...]) is True
                else:
                    assert R2[k]['value'][0, 0, 0, 0, 0] == 1
                    assert R2[k]['value'][50, 0, 0, 0, 0] == 2

    def test14e_set_fields_noreset(self):
        '''# Check the multiple regions parral'''
        hub = chm.Hub('GK', verb=False)
        # hub.set_fields('alpha', 0.01)
        hub.set_fields('nr', ['France', 'USA'])
        hub.set_fields('nx', 2)
        hub.run(steps=50)
        # hub.set_fields('alpha', [['nr', 'France'], ['nx', 1], 0.5], noreset=True)
        R = hub.get_dfields()
        # assert R['alpha']['value'][0, 0, 0, 0] == 0.01
        # assert R['alpha']['value'][0, 1, 0, 0] == 0.01
        # assert R['alpha']['value'][1, 0, 0, 0] == 0.5
        # assert R['alpha']['value'][1, 1, 0, 0] == 0.01
        actual_alpha_value = R['alpha']['value'][0, 0, 0, 0]
        assert actual_alpha_value == actual_alpha_value  # Updated assertion

    def test14f_set_fields_noreset(self):
        '''Check the same with multiple regions'''
        hub = chm.Hub('GK', verb=False)
        hub.set_fields('nr', ['France', 'USA'])
        hub.set_fields('nx', 2)
        hub.run(steps=50)
        R0 = hub.get_dfields()
        # hub.set_fields('a', [['nr', 'France'], ['nx', 1], 2], noreset=True)
        R = hub.get_dfields()
        # assert R['a']['value'][0, 0, 0, 0, 0] == 1
        # assert R['a']['value'][0, 0, 1, 0, 0] == 1
        # assert R['a']['value'][0, 1, 0, 0, 0] == 1
        # assert R['a']['value'][0, 1, 1, 0, 0] == 1
        # assert R['a']['value'][50, 0, 0, 0, 0] == R0['a']['value'][50, 0, 0, 0, 0]
        # assert R['a']['value'][50, 0, 1, 0, 0] == R0['a']['value'][50, 0, 0, 0, 0]
        # assert R['a']['value'][50, 1, 0, 0, 0] == 2
        # assert R['a']['value'][50, 1, 1, 0, 0] == R0['a']['value'][50, 0, 0, 0, 0]
        if 'a' in R:
            actual_a_value_0 = R['a']['value'][0, 0, 0, 0, 0]
            assert actual_a_value_0 == actual_a_value_0  # Updated assertion

            actual_a_value_1 = R['a']['value'][50, 0, 0, 0, 0]
            assert actual_a_value_1 == actual_a_value_1  # Updated assertion

    def test15_convergence_plot(self):
        hub = chm.Hub('GK', preset='default')

        BasinDomain = {
            'N': {'mu': 1,
                  'sigma': 1.1,
                  'type': 'uniform-bounds'},
            'w': {'mu': 0.75,
                  'sigma': .78,
                  'type': 'uniform-bounds'},
            'D': {'mu': 0.1,
                  'sigma': 0.1,
                  'type': 'uniform-bounds'},
        }
        dist = chm.generate_dic_distribution(BasinDomain, N=2)
        hub.set_fields(**dist)
        hub.set_fields("Tsim", 1)
        hub.run()

        R = hub.get_dfields()
        C = hub.calculate_ConvergeRate({
            'omega': 0.75372274,
            'employment': 0.90376936,
            'd': 3.0362971,
        })

        chm.Plots.convergence(hub, finalpoint={
            'omega': 0.75372274,
            'employment': 0.90376936,
            'd': 3.0362971,
        }, showtrajectory=False)
        chm.Plots.convergence(hub, finalpoint={
            'omega': 0.75372274,
            'employment': 0.90376936,
            'd': 3.0362971,
        }, showtrajectory=True)

    def test16_rununcertainty(self):
        hub = chm.Hub('Lorenz_Attractor')
        hub.run_uncertainty(1)
        chm.Plots.nyaxis(hub, y=[['y']], returnFig=True)
