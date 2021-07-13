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


# library-specific
sys.path.insert(0, _PATH_PCK)   # ensure Main comes from .. => add PYTHONPATH
import _class
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
        cls.dsolver = {}

    @classmethod
    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test01_init_from_all_models(self):
        """ Make sure the main function runs from a python console """
        lmodel = _class._class_checks.models.get_available_models(
            returnas=list,
        )
        for model in lmodel:
            self.dsolver[model] = _class.Solver(model)

    def test02_get_dparam(self):
        pass


    def test02_run_all_models(self):
        """ Make sure the main function runs as executable from terminal """

        # list of entry parameters to try
        for model in self.dsolver.keys():
            self.dsolver[model].run()
