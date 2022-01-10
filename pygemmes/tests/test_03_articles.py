# -*- coding: utf-8 -*-
"""
This module tests that pygemmes' article-reproducing routines work
"""

# Built-in
import os
import sys


# Standard
import matplotlib.pyplot as plt


# Make sure the figures do not block the execution => allow interactivity
plt.ion()


_PATH_HERE = os.path.dirname(__file__)
_PATH_PCK = os.path.dirname(os.path.dirname(_PATH_HERE))


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
#           multiple systems
#######################################################


class Test01_Articles():

    lart = pgm.get_available_articles(returnas=list)

    @classmethod
    def setup_class(cls):
        cls.lart = pgm.get_available_articles(returnas=list, verb=False)

    def test01_reproduce(self):

        # Try reproducing all articles
        dfail = {}
        for art in self.lart:
            try:
                pgm.reproduce_article(article=art, save=False)
            except Exception as err:
                dfail[art] = str(err)

            # close all produced figures (to avoid overloading)
            plt.close('all')

        # If any fail => raise err with informative message
        if len(dfail) > 0:
            lstr = [f"{k0}: {v0}" for k0, v0 in dfail.items()]
            msg = (
                "The following articles could not be reproduced:\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)
