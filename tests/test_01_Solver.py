# -*- coding: utf-8 -*-
"""
This module contains tests for tofu.geom in its structured version
"""

# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations
import subprocess           # for handling bash commands


# Standard
import matplotlib.pyplot as plt


# Make sure the figures do not block the execution => allow interactivity
plt.ion()


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_PCK = os.path.dirname(_PATH_HERE)
_PATH_OUTPUT = os.path.join(_PATH_HERE, 'output_temp')
_PATH_OUTPUT_REF = os.path.join(_PATH_HERE, 'output_ref')


# library-specific
sys.path.insert(0, _PATH_PCK)   # ensure Main comes from .. => add PYTHONPATH
import _core
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


class Test01_Run():

    @classmethod
    def setup_class(cls):
        cls.dmodel = {}
        cls.lsolvers = [
            'eRK4-homemade',
            'eRK2-scipy', 'eRK4-scipy', 'eRK8-scipy',
        ]

    @classmethod
    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def teardown_class(cls):
        """ Clean-up the saved files """
        lf = [
            os.path.join(_PATH_OUTPUT, ff) for ff in os.listdir(_PATH_OUTPUT)
            if ff.endswith('.npz')
        ]
        for ff in lf:
            os.remove(ff)

    def test01_init_from_all_models(self):
        """ Make sure the main function runs from a python console """
        lmodel = _core._class_checks.models.get_available_models(
            returnas=list,
        )
        for model in lmodel:
            self.dmodel[model] = _core.Solver(model)

    def test02_get_summary_repr(self):
        for model in self.dmodel.keys():
            print(self.dmodel[model])
            self.dmodel[model].get_summary()

    def test03_get_dparam(self):
        for model in self.dmodel.keys():
            out = self.dmodel[model].get_dparam(group='Numerical')
            out = self.dmodel[model].get_dparam(eqtype='ode')

    def test04_get_variables_compact(self):
        for model in self.dmodel.keys():
            out = self.dmodel[model].get_variables_compact()

    def test05_set_single_param(self):
        for model in self.dmodel.keys():
            self.dmodel[model].set_dparam(key='Tmax', value=20)

    def test06_run_all_models_all_solvers(self):
        """ Make sure the main function runs as executable from terminal """

        # list of entry parameters to try
        for model in self.dmodel.keys():
            self.dmodel[model] = {
                solver: _core.Solver(model) for solver in self.lsolvers
            }
            for solver in self.lsolvers:
                self.dmodel[model][solver].run(solver=solver)

    def test07_save(self):
        # list of entry parameters to try
        for ii, model in enumerate(self.dmodel.keys()):
            for jj, solver in enumerate(self.lsolvers):
                self.dmodel[model][solver].save(
                    name=str(ii * 10 + jj),
                    path=_PATH_OUTPUT,
                )

    def test08_load_and_equal(self):
        lf = [
            os.path.join(_PATH_OUTPUT, ff)
            for ff in os.listdir(_PATH_OUTPUT)
            if ff.endswith('.npz')
        ]
        for ff in lf:
            obj = _core._saveload.load(ff)[0]
            model = list(obj.model.keys())[0]
            solver = obj.dmisc['solver']
            assert obj == self.dmodel[model][solver]

    def test09_copy(self):
        for model in self.dmodel.keys():
            for solver in self.lsolvers:
                obj = self.dmodel[model][solver].copy()
                assert obj == self.dmodel[model][solver]
                assert obj is not self.dmodel[model][solver]

    def test10_get_available_output(self):
        # verb
        _core._saveload.get_available_output(path=_PATH_OUTPUT)
        # list
        _core._saveload.get_available_output(path=_PATH_OUTPUT, returnas=list)
        # dict, with filters
        _core._saveload.get_available_output(
            path=_PATH_OUTPUT,
            model='GK',
            name='2',
            returnas=dict,
        )

    def test11_nonregression_output(self):

        # load reference files
        df_ref = _core._saveload.get_available_output(
            path=_PATH_OUTPUT_REF,
            returnas=dict,
        )
        lobj_ref = _core._saveload.load(list(df_ref.keys()))

        # compare to current output
        dfail = {}
        for ii, (ff, v0) in enumerate(df_ref.items()):
            model = list(lobj_ref[ii].dmisc['model'].keys())[0]
            solver = lobj_ref[ii].dmisc['solver']
            obj = self.dmodel[model][solver]
            if not obj == lobj_ref[ii]:
                msg = (
                    "Difference with reference output!"
                )
                dfail[f'{model}_{solver}'] = msg

        if len(dfail) > 0:
            lstr = [f'\t- {k0}: v0' for k0, v0 in dfail.items()]
            msg = (
                "The following output regressions have been detected:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)
