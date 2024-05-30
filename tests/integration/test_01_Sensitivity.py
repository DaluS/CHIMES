# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations
import numpy as np
import matplotlib.pyplot as plt
import chimes as chm

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


class Test01_Sensitivity():

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

    def testB_01a_Sensitivity(self):
        '''Sensitivity is working as intended in minimal version'''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity()

        # Check keys
        # Check input distributions

    def testB_01b_Sensitivity(self):
        """Sensitivity is only done on variable a"""
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys=['a'])
        assert 'a' in list(OUT.keys())
        assert 'alpha' not in list(OUT.keys())

    def testB_01b2_Sensitivity(self):
        """Sensitivity is only done on variable a by a string"""
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys='a')
        assert 'a' in list(OUT.keys())
        assert 'alpha' not in list(OUT.keys())

    def testB_01c_Sensitivity(self):
        '''Check that there is everything but a'''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys=('a',))
        assert 'a' not in list(OUT.keys())
        assert 'alpha' in list(OUT.keys())

    def testB_01d_Sensitivity(self):
        '''Check that there is two value with correct STD '''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys={'a': 0.1,
                                        'alpha': 0.01})
        assert 'a' in list(OUT.keys())
        assert 'alpha' in list(OUT.keys())
        assert 'K' not in list(OUT.keys())

    def testB_01e_Sensitivity(self):
        ''' Check that other types of distributions are correctly covered'''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys='a',
                                  distribution='normal')
        OUT = hub.run_sensitivity(keys='a',
                                  distribution='uniform')
        F = chm.Plots.Showsensitivity(OUT, ['employment', 'omega'], returnFig=True)

    def testB_01f_Sensitivity(self):
        '''# Check that number of value in distribution is respected'''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys='a',
                                  distribution='normal',
                                  N=3)
        R = OUT['a'].get_dfields()
        assert len(R['alpha']['value'][:, 0, 0, 0]) == 3

    def testB_01g_Sensitivity(self):
        '''Check that combined_run is responding to `independant, additive, true, error`'''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys='a', combined_run='independant')
        assert 'a' in list(OUT.keys())
        assert '_COMBINED_' not in list(OUT.keys())

        OUT = hub.run_sensitivity(keys='a', combined_run='additive')
        assert 'a' not in list(OUT.keys())
        assert '_COMBINED_' in list(OUT.keys())

    def testB_01h_Sensitivity(self):
        '''# Check that the output can be reinterpolated '''
        hub = chm.Hub('Goodwin_example', verb=False)
        hub.set_fields('Tsim', 1)
        OUT = hub.run_sensitivity(keys='a', combined_run='independant', Noutput=100)
        R = OUT['a'].get_dfields()
        assert len(R['a']['value'][:, 0, 0, 0, 0] == 100)

    def testB_01i_Sensitivity(self):
        '''# Check that verbose is working as intended'''

        hub = chm.Hub('Goodwin_example', verb=False)
        OUT = hub.run_sensitivity(std=0.01,
                                  distribution='lognormal',
                                  keys={'a': 0.1, 'nu': 0.2},
                                  stdmode='relative',
                                  N=10,
                                  combined_run=True,
                                  Noutput=500,
                                  verb=True)
        F = chm.Plots.Showsensitivity(OUT, ['employment', 'omega'], returnFig=True)
