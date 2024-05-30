# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations
import numpy as np
import matplotlib.pyplot as plt
import chimes as chm

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

    def testC_01a_Megatestatonce(self):
        '''Sensitivity is working as intended in minimal version'''

        hub = chm.Hub('E-CHIMES')
        ########################################################
        Nsect = 3    # Number of sectors

        gamma0 = 0.1   # Mean intermediate consumption
        sigmagamma = .2    # standard deviation on intermediate consumption

        xi0 = 1.5     # Mean capital size
        sigmaxi = .2    # standard deviation on capital size

        apondscale = .05
        wpondscale = .05

        ########################################################

        ### GENERATION #########################################
        dfields0 = hub.supplements['generateNgoodwin'](Nsect)  # Basic N Goodwin dictionnary

        # vector equivalent for wage and productivity
        dfields0['apond'] = np.random.normal(1, scale=apondscale, size=Nsect)
        dfields0['z'] = np.random.normal(1, scale=wpondscale, size=Nsect)

        dfields0['a'] = dfields0['a0']*dfields0['apond']
        dfields0['w'] = dfields0['w0']*dfields0['z']

        ### MATRICES AND CONSUMPTION VECTOR (HERE RANDOM) ######
        dfields0['Gamma'] = np.random.lognormal(size=(Nsect, Nsect))
        dfields0['Gamma'] *= gamma0/np.sum(dfields0['Gamma'], axis=1)[:, np.newaxis]
        dfields0['Gamma'] *= (1+np.random.normal(scale=sigmagamma, size=Nsect))[:, np.newaxis]

        dfields0['Xi'] = np.random.lognormal(size=(Nsect, Nsect))
        dfields0['Xi'] *= xi0/np.sum(dfields0['Xi'], axis=1)[:, np.newaxis]
        dfields0['Xi'] *= (1+np.random.normal(scale=sigmaxi, size=Nsect))[:, np.newaxis]

        dfields0['Cpond'] = np.random.lognormal(size=Nsect)
        dfields0['Cpond'] /= np.sum(dfields0['Cpond'])

        dfields0['p'] = hub.supplements['pForROC'](dfields0)

        K = hub.supplements['Kfor0dotV'](dfields0)
        K *= dfields0['employment']*dfields0['N']/np.sum(K/dfields0['a'])  # homotetic scaling for employment and N
        dfields0['K'] = K

        hub.set_fields(**dfields0, verb=True)
        hub.set_fields('Tsim', 3, verb=False)

        hub.run()
        hub.get_summary()

        # F = chm.Plots.SankeyCHIMES(hub, t=50, returnFig=True)
        # chm.Plots.nyaxis(hub, [[['employment', sect] for sect in dfields0['Nprod']],
        #                            [['omega', sect] for sect in dfields0['Nprod']]])
        F = hub.supplements['PiRepartition'](hub, returnFig=True)
        F = hub.supplements['MonetaryFluxes'](hub, returnFig=True)
        F = hub.supplements['PhysicalFluxes'](hub, returnFig=True)

    def testC_02_Multisectoral_set_params(self):
        # Multisectoral

        hub = chm.Hub('E-CHIMES', preset='2Goodwin', verb=False)
        hub.set_fields('Gamma', [[0, 1], [1, 0]])  # will put [[0,1],[1,0]] for all parrallel all regions
        hub = chm.Hub('E-CHIMES', preset='2Goodwin', verb=False)
        hub.set_fields(Nprod=['Consumption', 'Capital'])
        hub.set_fields(**{'Gamma': {'first': ['Consumption', 'Capital'],
                                    'nr': 0,
                                    'value': [0.5, 0.22]}})
