# -*- coding: utf-8 -*-
"""
This module is an adaptation of tests for tofu.geom in its structured version,
for pygemmes
"""

# Built-in

import os
import sys
import itertools as itt     # for iterating on parameters combinations
import subprocess           # for handling bash commands


# Standard
import numpy as np
import matplotlib.pyplot as plt


# Make sure the figures do not block the execution => allow interactivity
plt.ion()


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_PCK = os.path.dirname(os.path.dirname(_PATH_HERE))
_PATH_OUTPUT = os.path.join(_PATH_HERE, 'output_temp')
_PATH_OUTPUT_REF = os.path.join(_PATH_HERE, 'output_ref')


# library-specific
sys.path.insert(0, _PATH_PCK)   # ensure Main comes from .. => add PYTHONPATH
import pygemmes as pgm
sys.path.pop(0)                 # clean PYTHONPATH


_DPRESETS = {
    'multi1': {
        'fields': {
            'phinull': [0.1, 0.11],
        },
        'com': (
            'test multiple values for parameter'
        ),
    },
    'multi2': {
        'fields': {
            'alpha': [0.01, 0.02, 0.03],
        },
        'com': (
            'test multiple values for ode initial value'
        ),
    },
    'multi3': {
        'fields': {
            'phinull': [0.1, 0.11, 0.12],
            'alpha': [0.01, 0.02, 0.03],
        },
        'com': (
            'test multiple values for parameter and ode initial value'
        ),
    },
    'multi4': {
        'fields': {
            'phinull': {'value': [0.1, 0.11]},
        },
        'com': (
            'test multiple values for parameter'
        ),
    },
    'multi5': {
        'fields': {
            'a': {'initial': [0.96, 0.966, 0.966], 'grid': True},
        },
        'com': (
            'test multiple values for ode initial value'
        ),
    },
    'multi6': {
        'fields': {
            'phinull': [0.1, 0.11],
            'a': {'value': [0.96, 0.966, 0.966], 'grid': True},
        },
        'com': (
            'test multiple values for parameter and ode initial value'
        ),
    },
}


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
#######################################################
#     Creating Hub and testing methods
#           multiple systems
#######################################################


class Test01_Hub_MultipleSystems():

    lsolvers = ['eRK4-homemade', 'eRK4-scipy']
    lmodels = pgm.get_available_models(returnas=list, from_user=False)
    lgrid = [True, False]

    @classmethod
    def setup_class(cls):
        cls.dhub = {
            k0: {
                k1: dict.fromkeys(cls.lgrid)
                for k1 in cls.lsolvers
            }
            for k0 in cls.lmodels
        }

    @classmethod
    def teardown_class(cls):
        """ Clean-up the saved files """
        lf = [
            os.path.join(_PATH_OUTPUT, ff) for ff in os.listdir(_PATH_OUTPUT)
            if ff.endswith('.npz')
        ]
        for ff in lf:
            os.remove(ff)

    def setup(self):
        """ Load all models / presets / solvers """
        # list of entry parameters to try
        for model in self.lmodels:
            for solver in self.lsolvers:
                for grid in self.lgrid:

                    hub = pgm.Hub(model, from_user=False)
                    self.dhub[model][solver][grid] = hub

                    # set k0, v0
                    lpar = hub.get_dparam(
                        eqtype=None,
                        group=('Numerical',),
                        returnas=list,
                    )
                    if len(lpar) >= 2:
                        k0 = lpar[0]
                        v0 = hub.dparam[k0]['value'] * np.r_[0.9, 1, 1.1]
                        k1 = lpar[1]
                        v1_grid = hub.dparam[k1]['value'] * np.r_[1, 1.1]
                        v1_nogrid = hub.dparam[k1]['value'] * np.r_[0.9, 1, 1.1]

                        self.dhub[model][solver][grid].set_dparam(
                            key=k0, value=v0, grid=grid,
                        )
                        if grid:
                            self.dhub[model][solver][grid].set_dparam(
                                key=k1, value=v1_nogrid, grid=grid,
                            )
                        else:
                            iserr = False
                            try:
                                self.dhub[model][solver][grid].set_dparam(
                                    key=k1, value=v1_grid, grid=grid,
                                )
                            except Exception as err:
                                iserr = True
                            assert iserr
                            self.dhub[model][solver][grid].set_dparam(
                                key=k1, value=v1_nogrid, grid=grid,
                            )

    def test01_get_summary(self):
        for model in self.lmodels:
            for solver in self.lsolvers:
                for grid in self.lgrid:
                    hub = self.dhub[model][solver][grid]
                    for idx in [None, True]:
                        if idx is True:
                            if grid in [False, 'multi2']:
                                idx = 0
                            else:
                                idx = tuple([
                                    0 for ii in hub.dmisc['dmulti']['shape']
                                ])
                        hub.get_summary(idx=idx)

    def test02_run(self):
        for model in self.lmodels:
            for solver in self.lsolvers:
                for grid in self.lgrid:
                    self.dhub[model][solver][grid].set_dparam(Tmax=1)
                    self.dhub[model][solver][grid].run(solver=solver)

    def test03_plot(self):
        for model in self.lmodels:
            for solver in self.lsolvers:
                for grid in self.lgrid:
                    hub = self.dhub[model][solver][grid]
                    if grid in [False, 'multi3']:
                        idx = 0
                    else:
                        idx = tuple([
                            0 for ii in hub.dmisc['dmulti']['shape']
                        ])
                    dax = hub.plot(idx=idx)
            plt.close('all')

    def test04_save_load_equal(self):

        # save
        for model in self.lmodels:
            for solver in self.lsolvers:
                for grid in self.lgrid:
                    pfe = self.dhub[model][solver][grid].save(
                        path=_PATH_OUTPUT,
                        returnas=str,
                        verb=False,
                    )
                    obj = pgm.load(pfe)[0]
                    assert obj == self.dhub[model][solver][grid]


class Test02_Hub_FromPresets(Test01_Hub_MultipleSystems):

    lmodels = ['G']
    lgrid = list(_DPRESETS.keys())

    def setup(self):
        """ Load all models / presets / solvers """
        # list of entry parameters to try
        for model in self.lmodels:
            for solver in self.lsolvers:
                for preset in self.lgrid:
                    self.dhub[model][solver][preset] = pgm.Hub(
                        model,
                        preset=preset,
                        dpresets=_DPRESETS,
                        from_user=False,
                        verb=False,
                    )
