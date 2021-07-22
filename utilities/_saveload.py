# -*- coding: utf-8 -*-


# Built-in
import os
import inspect
import itertools as itt
import getpass
import datetime as dtm
import warnings


# common
import numpy as np


_PATH_HERE = os.path.dirname(__file__)
_PATH_OUTPUT = os.path.join(os.path.dirname(_PATH_HERE), 'output')


# #############################################################################
# #############################################################################
#                               save
# #############################################################################


def _save_check_inputs(
    path=None,
    name=None,
    fmt=None,
    verb=None,
):

    # path
    if path is None:
        path = _PATH_OUTPUT
    if not os.path.isdir(path):
        msg = (
            "Arg path must be a valid path!\n"
            f"Provided: {path}"
        )
        raise Exception(msg)
    path = os.path.abspath(path)

    # name
    if name is None:
        name = 'placeholder'
    if not isinstance(name, str):
        msg = (
            "Arg name must be a str!\n"
            f"Provided: {name}"
        )
        raise Exception(msg)
    name = name.replace('_', '-').replace(' ', '-')

    # fmt
    if fmt is None:
        fmt = 'npz'
    lfmt = ['npz']
    if fmt not in lfmt:
        msg = (
            "Arg fmt must be a valid format!\n"
            f"\t- provided: {fmt}\n"
            f"\t- allowed: {lfmt}"
        )
        raise Exception(msg)

    # verb
    if verb is None:
        verb = True
    if not isinstance(verb, bool):
        msg = (
            "Arg verb must be a bool!\n"
            f"\t- provided: {verb}"
        )
        raise Exception(msg)

    return path, name, fmt, verb


def save(
    obj,
    path=None,
    name=None,
    fmt=None,
    verb=None,
):

    # ------------
    # check inputs
    path, name, fmt, verb = _save_check_inputs(
        path=path,
        name=name,
        fmt=fmt,
        verb=verb,
    )

    # -------------
    # set extension
    if fmt == 'npz':
        ext = 'npz'

    # --------------
    # Make full name
    model = list(obj.model.keys())[0].replace('_', '-').replace(' ', '-')
    user = getpass.getuser()
    date = dtm.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    fullname = f'Output_{model}_{name}_{user}_{date}.{ext}'

    # --------------
    # convert data for saving

    if fmt == 'npz':
        # convert obj to dict
        dout = obj._to_dict()

        # delete lambda functions
        # they can't be saved, and will be reloaded from the model file
        for k0 in dout['dparam'].keys():
            if dout['dparam'][k0].get('func') is not None:
                dout['dparam'][k0]['func'] = True

        # the model source file stored in self.model

        # full saving pfe (Path-File-Extension)
        pfe = os.path.join(path, fullname)
        np.savez(pfe, **dout)

    # --------------
    # verb and return
    if verb is True:
        msg = (f"Saved in:\n\t{pfe}")
        print(msg)


# #############################################################################
# #############################################################################
#                              load
# #############################################################################


def _load_check_input(pfe):
    c0 = (
        isinstance(pfe, str)
        and pfe.endswith('.npz')
    )
    if not c0:
        msg = (
            "Arg pfe must be a str pointing to a valid file!\n"
            + f"Provided: {pfe}"
        )
        raise Exception(msg)

    if not os.path.isfile(pfe):
        if not os.path.isfile(os.path.join(_PATH_OUTPUT, pfe)):
            msg = (
                "Arg pfe must be a str pointing to a valid file!\n"
                + f"Provided: {pfe}"
            )
            raise Exception(msg)
        pfe = os.path.join(_PATH_OUTPUT, pfe)
    return pfe


def load(pfe):
    """ Load a save output file """

    # --------------
    # check inputs
    pfe = _load_check_input(pfe)

    # --------------
    # load
    dout = {
        k0: v0.tolist()
        for k0, v0 in dict(np.load(pfe, allow_pickle=True)).items()
    }

    # --------------
    # create instance from dict
    import _core
    return _core.Solver._from_dict(dout)
