

import os
import importlib
import warnings

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


# #############################################################################
# #############################################################################
#                   Core reproducing routine
# #############################################################################


def reproduce_article(
    # key of the article to reproduce
    article=None,
    # list of figures to reproduce
    fig=None,
    # parameters
    darticles=_DARTICLES,
    verb=None,
    # save output to... (False to not save)
    save=None,
    save_path=None,
    fmt=None,
):

    # ------------
    # check inputs

    if article not in darticles.keys():
        msg = (
            "Arg article must be an available article for reproduction!\n"
            f"Provided: {article}"
        )
        get_available_articles(verb=True, returnas=False)
        raise Exception(msg)

    dfig = darticles[article]['dfigures']
    if fig is None:
        fig = sorted(dfig.keys())
    if np.isscalar(fig):
        fig = [int(fig)]
    fig_out = [ff for ff in fig if ff not in dfig.keys()]
    if len(fig_out) > 0:
        msg = f"The follonwing figure keys are not reckognized: {fig_out}"
        warnings.warn(msg)
        fig = [ff for ff in fig if ff not in fig_out]

    if save is None:
        save = False
    if not isinstance(save, bool):
        msg = "Arg save must be a bool!"
        raise Exception(msg)

    if save_path is None:
        save_path = os.path.abspath('./')
    if save is True and not os.path.isdir(save_path):
        msg = (
            "Arg save_path must be a valid path for saving!\n"
            f"Provided: {save_path}"
        )
        raise Exception(msg)

    if fmt is None:
        fmt = 'png'

    # ---------
    # Reproduce

    for k0, v0 in darticles[article]['dmodel_preset'].items():

        # if no relevant figure => skip
        if not any([ff in v0['fig'] for ff in fig]):
            continue

        # load and run
        hub = _core.Hub(
            model=v0['model'],
            preset=v0['preset'],
            from_user=False,
            verb=verb,
        )

        hub.run(
            solver=v0.get('solver', 'eRK4-scipy'),
            verb=verb,
        )

        for ff in v0['fig']:

            # if not relevant => skip
            if ff not in fig:
                continue

            dax = darticles[article]['dfigures'][ff]['func'](hub)

            # optinal saving
            if save is True:
                name = f'Article_{article}_fig{ff}_reproduced'
                pfe = os.path.join(save_path, name + f'.{fmt}')
                figure = list(dax.values())[0].figure
                figure.savefig(pfe, format=fmt)
                msg = f"Saved in:\n\t{pfe}"
                print(msg)

    return
