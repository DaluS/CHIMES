

import os
import importlib


import numpy as np


from .. import _core


_PATH_HERE = os.path.dirname(__file__)


# ####################################################
# ####################################################
#       Automatically load all available articles
# ####################################################


_LART = [
    ff for ff in os.listdir(_PATH_HERE)
    if os.path.isdir(os.path.join(_PATH_HERE, ff))
    and 'pycache' not in ff
]


_DARTICLES = {}
for aa in _LART:
    pfe = os.path.join(_PATH_HERE, aa, '_article.py')
    spec = importlib.util.spec_from_file_location('_article', pfe)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    _DARTICLES[aa] = dict(foo._DARTICLE)

    # for each unique (models, preset), get list of figures
    unique = list(set([
        (v0['model'], v0['preset'])
        for k0, v0 in _DARTICLES[aa]['dfigures'].items()
    ]))

    # sort by min figure number
    lfig = [
        [
            k0 for k0 in _DARTICLES[aa]['dfigures'].keys()
            if _DARTICLES[aa]['dfigures'][k0]['model'] == uu[0]
            and _DARTICLES[aa]['dfigures'][k0]['preset'] == uu[1]
        ]
        for uu in unique
    ]
    lminfig = [min(ff) for ff in lfig]
    argsort = sorted(range(len(lminfig)), key=lminfig.__getitem__)

    # complete _DARTICLES[aa]
    _DARTICLES[aa]['dmodel_preset'] = {
        f'dmodpre{ii}': {
            'model': unique[ii][0],
            'preset': unique[ii][1],
            'fig': [
                k0 for k0 in _DARTICLES[aa]['dfigures'].keys()
                if _DARTICLES[aa]['dfigures'][k0]['model'] == unique[ii][0]
                and _DARTICLES[aa]['dfigures'][k0]['preset'] == unique[ii][1]
            ],
        }
        for ii in argsort
    }


# #############################################################################
# #############################################################################
#                   get_available_articles
# #############################################################################


def get_available_articles(
    article=None,
    details=None,
    returnas=None,
    verb=None,
):

    # -----------------
    # check inputs

    if article is None:
        article = sorted(_DARTICLES.keys())
    if isinstance(article, str):
        article = [article]
    if returnas is None:
        returnas = False
    if verb is None:
        verb = returnas is False
    if details is None:
        details = False

    # -----------------
    # get available models

    darticles = {
        k0: dict(v0)
        for k0, v0 in _DARTICLES.items()
        if k0 in article
    }

    # -----------------
    # print

    if verb is True or returnas is str:

        if details:
            # To be done later in a dedicated PR depending on observed usage
            msg = None

        else:
            # compact message

            head = ['key', 'short ref', 'model', 'preset', 'figures']

            lcol = []
            for k0, v0 in darticles.items():
                for ii, (k1, v1) in enumerate(v0['dmodel_preset'].items()):
                    add = ['', '', '', '', '']
                    if ii == 0:
                        add[0] = k0
                        add[1] = v0['ref_short']
                    add[2] = v1['model']
                    add[3] = v1['preset']
                    add[4] = str(v1['fig'])
                    lcol.append(add)

            # justify for pretty-printing
            nmax = np.char.str_len([head] + lcol).max(axis=0)

            head = ' '.join([hh.ljust(nmax[ii]) for ii, hh in enumerate(head)])
            sep = ' '.join(['-'*ii for ii in nmax])
            lcol = [
                ' '.join([
                    ci.ljust(nmax[ii])
                    for ii, ci in enumerate(cc)
                ])
                for cc in lcol
            ]
            msg = (
                "The following articles can currently be reproduced:\n"
                + "\n".join([head] + [sep] + lcol)
            )

        if verb is True:
            print(msg)

    # -----------------
    # return

    if returnas is list:
        return article
    elif returnas is dict:
        return darticle
    elif returnas is str:
        return msg


