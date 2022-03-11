# -*- coding: utf-8 -*-
"""
This module contains tests for tofu.geom in its structured version
"""

# Built-in
import os
import sys
import itertools as itt     # for iterating on parameters combinations
import subprocess           # for handling bash commands
import warnings


# Standard
import numpy as np
import matplotlib.pyplot as plt


# Make sure the figures do not block the execution => allow interactivity
plt.ion()


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_PCK = os.path.dirname(os.path.dirname(_PATH_HERE))
_PATH_OUTPUT = os.path.join(_PATH_HERE, 'output_temp')
_PATH_OUTPUT_REF = os.path.join(_PATH_HERE, 'output_ref')

# unit tests => only official models, not private
_PATH_MODELS = os.path.join(_PATH_PCK, 'pygemmes', '_models')


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
#######################################################
#     Creating Hub and testing methods
#           single system
#######################################################


class Test01_Hub():

    @classmethod
    def setup_class(cls):
        cls.dhub = {}
        cls.lsolvers = [
            'eRK4-homemade',
            'eRK4-scipy',  # 'eRK8-scipy', 'eRK2-scipy',
        ]

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
        dmodel = pgm.get_available_models(
            returnas=dict,
            from_user=False,
        )
        for model in dmodel.keys():
            lpresets = [None] + dmodel[model]['presets']
            self.dhub[model] = dict.fromkeys(lpresets)
            for preset in lpresets:
                self.dhub[model][preset] = pgm.Hub(
                    model,
                    preset=preset,
                    from_user=False,
                )

    def test02_get_summary_repr(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                print(self.dhub[model][preset])
                self.dhub[model][preset].get_summary()

    def test03_get_dparam(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                out = self.dhub[model][preset].get_dparam(group='Numerical')
                out = self.dhub[model][preset].get_dparam(
                    eqtype=['ode', 'param'], group='CORE',
                )
                out = self.dhub[model][preset].get_dparam(
                    eqtype=('ode',), group=['CORE', 'Debt'], key=('lambda'),
                )

    def test04_get_dparam_as_reverse_dict(self):
        for model in self.dhub.keys():
            for preset, hub in self.dhub[model].items():
                out = hub.get_dparam_as_reverse_dict(
                    crit='units',
                )
                out = hub.get_dparam_as_reverse_dict(
                    crit='units', group='CORE', key=('time',),
                )
                out = hub.get_dparam_as_reverse_dict(
                    crit='units', verb=True,
                )
    '''
    DEPRECIATED TEST : FUNCTION REMOVED BECAUSE USELESS

    def test05_get_variables_compact(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                out = self.dhub[model][preset].get_variables_compact()
    '''

    def test06_set_single_param(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                self.dhub[model][preset].set_dparam(key='Tmax', value=20)

    def test07_run_all_models_all_solvers(self):
        """ Make sure the main function runs as executable from terminal """

        # list of entry parameters to try
        dfail = {}
        for ii, model in enumerate(self.dhub.keys()):
            for jj, preset in enumerate(self.dhub[model].keys()):
                self.dhub[model][preset] = {
                    solver: pgm.Hub(
                        model,
                        preset=preset,
                        from_user=False,
                    )
                    for solver in self.lsolvers
                }
                for kk, solver in enumerate(self.lsolvers):

                    try:
                        self.dhub[model][preset][solver].set_dparam(Tmax=10)
                        self.dhub[model][preset][solver].run(
                            solver=solver,
                            verb=0,
                            rtol=1,
                            atol=1
                        )
                    except Exception as err:
                        dfail[f'{model} {preset} {solver}'] = str(err)

        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following solvers failed:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    def test08_get_summary_repr_after_run(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                for solver in self.lsolvers:
                    print(self.dhub[model][preset][solver])
                    self.dhub[model][preset][solver].get_summary()

    def test09_save(self):
        # list of entry parameters to try
        for ii, model in enumerate(self.dhub.keys()):
            for jj, preset in enumerate(self.dhub[model].keys()):
                for kk, solver in enumerate(self.lsolvers):
                    self.dhub[model][preset][solver].save(
                        path=_PATH_OUTPUT,  # _PATH_OUTPUT_REF to update ref
                    )

    '''

    def test10_load_and_equal(self):
        df = pgm.get_available_output(
            path=_PATH_OUTPUT,
            returnas=dict,
        )
        for ii, (ff, vv) in enumerate(df.items()):
            model0 = vv['model']
            preset0 = vv['preset']
            solver0 = vv['solver']
            if ii % 2 == 0:
                model_file = os.path.join(_PATH_MODELS, f'_model_{model0}.py')
            else:
                model_file = None
            obj = pgm.load(ff, model_file=model_file)[0]
            model = obj.dmodel['name']
            preset = obj.dmodel['preset']
            solver = obj.dmisc['solver']
            #assert model == model0
            assert str(preset) == preset0
            assert solver == solver0
            assert obj == self.dhub[model][preset][solver]
    '''

    def test11_copy(self):
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                for solver in self.lsolvers:
                    obj = self.dhub[model][preset][solver].copy()
                    assert obj == self.dhub[model][preset][solver]
                    assert obj is not self.dhub[model][preset][solver]

    def test12_nonregression_output(self):

        # load reference files
        df_ref = pgm.get_available_output(
            path=_PATH_OUTPUT_REF,
            returnas=dict,
        )
        lobj_ref = pgm.load(list(df_ref.keys()))

        # if no non-regression tests => warning
        if len(df_ref) == 0:
            msg = "No non-regression reference output found!"
            warnings.warn(msg)

        # tolerated errors
        lexcept = [
            'LorenzSystem_Canonical_eRK8-scipy',
            'LorenzSystem_Canonical_eRK4-scipy',
            'LorenzSystem_Canonical_eRK2-scipy',
        ]

        # compare to current output
        dfail = {}
        for ii, (ff, v0) in enumerate(df_ref.items()):
            model = lobj_ref[ii].dmodel['name']
            preset = lobj_ref[ii].dmodel['preset']
            solver = lobj_ref[ii].dmisc['solver']
            obj = self.dhub[model][preset][solver]

            isok, dfaili = obj.__eq__(
                lobj_ref[ii],
                verb=False,
                return_dfail=True,
            )

            if isok is False:

                # tolerate well-identified exceptions, but warn
                kkk = f'{model}_{preset}_{solver}'
                if kkk in lexcept:
                    dfaili = {}
                    isok = True
                    msg = f"Regression {kkk} tolerated!"
                    warnings.warn(msg)

                # only tolerated error: different absolute path to model file
                keyok = "dmodel['file']"
                if keyok in dfaili.keys():
                    del dfaili[keyok]

                # record any remaining error
                if len(dfaili) > 0:
                    lstr = [f"\t\t. {k0}: {v0}" for k0, v0 in dfaili.items()]
                    msg = (
                        "Differs from reference for:\n"
                        + "\n".join(lstr)
                    )
                    dfail[kkk] = msg

        if len(dfail) > 0:
            lstr = [f'\t- {k0}: {v0}' for k0, v0 in dfail.items()]
            msg = (
                "The following output regressions have been detected:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    def test13_plot(self):
        lcol = ['k', 'r', 'g', 'b', 'c', 'm']
        dcolor = {
            k0: lcol[ii] for ii, k0 in enumerate(self.lsolvers)
        }
        for model in self.dhub.keys():
            for preset in self.dhub[model].keys():
                dax = None
                units = None if preset is None else 'undefined'
                key = ('phillips',) if preset is None else None
                lab = None if preset is None else 'test'
                for solver, hub in self.dhub[model][preset].items():
                    dax = hub.plot(
                        dax=dax,
                        color=dcolor[solver],
                        label=lab,
                        units=units,
                        key=key,
                    )
                plt.close('all')
