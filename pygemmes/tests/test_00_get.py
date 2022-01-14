# -*- coding: utf-8 -*-
"""
This module contains tests for tofu.geom in its structured version
"""

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

    def test01_get_available_models(self):
        """ Make sure the main function runs from a python console """

        ldetails = [False, True]
        lverb = [False, True]
        lreturn = [False, list, dict, str]

        for comb in itt.product(ldetails, lverb, lreturn):
            out = pgm.get_available_models(
                details=comb[0],
                verb=comb[1],
                returnas=lreturn[2],
                from_user=False,
            )

    def test02_get_available_solvers(self):
        """ Make sure the main function runs from a python console """

        lverb = [False, True]
        lreturn = [False, list, dict]

        for comb in itt.product(lverb, lreturn):
            out = pgm.get_available_solvers(
            )

    def test03_get_available_output(self):
        """ Make sure the main function runs from a python console """

        lverb = [False, True]
        lreturn = [False, list, dict]

        lmodel = [None, 'GK']
        lsolver = [None, 'eRK4-homemade']

        for comb in itt.product(lverb, lreturn, lmodel, lsolver):
            out = pgm.get_available_output(
                path=_PATH_OUTPUT_REF,
                model=comb[2],
                user=None,
                solver=comb[3],
                name=None,
                fmt=None,
                verb=comb[0],
                returnas=comb[1],
            )
