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
import Main
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
        pass

    @classmethod
    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test01_run(self):
        """ Make sure the main function runs from a python console """

        # list of entry parameters to try
        lplot = [True, False]
        lsave = ['None', True, False]

        # loop to test all combinations
        for comb in itt.product(lplot, lsave):
            Main.run(
                plot=comb[0],
                save=comb[1],
            )

        # Close figures
        plt.close('all')

    def test02_run_as_exec(self):
        """ Make sure the main function runs as executable from terminal """

        # list of entry parameters to try
        dpar = {
            'plot': [False],
            'timeit': [True, False],
            'save': [False],
        }

        # Invoke via the shell for windows only
        shell = True if sys.platform.lower().startswith('win') else False

        # loop to test all combinations
        lpar = list(dpar.keys())
        lcomb = [dpar[kk] for kk in lpar]
        for ii, comb in enumerate(itt.product(*lcomb)):
            cmd = [
                os.path.join(_PATH_PCK, 'Main.py'),
                '--plot', str(comb[0]),
                '--timeit', str(comb[1]),
                "--save", str(comb[2]),
            ]
            assert comb[0] is False, "Only plot = False allowed here!"
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=shell,
            )

            # Catch error if any
            out, err = process.communicate()
            if err != '':
                lstr = [
                    '-\t {}: {}'.format(lpar[jj], comb[jj])
                    for jj in range(len(lpar))
                ]
                msg = (
                    str(err)
                    + "\n\nInput comb. {} failed (see above):\n".format(ii)
                    + '\n'.join(lstr)
                )
                raise Exception(msg)
            process.wait()

