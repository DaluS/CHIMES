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

        print('TESTS ARE EMPTY !')