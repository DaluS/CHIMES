# -*- coding: utf-8 -*-


import os
import shutil


_PATH_HERE = os.path.dirname(__file__)
_PATH_USER_HOME = os.path.expanduser('~')


def create_private_pygemmes(
    path_user_home=_PATH_USER_HOME,
    reset=None,
    reset_hard=None,
):
    """ Create the private .pygemmes folder in user's home

    This pivate folder contains user-customizable:
        - _models/:
            - _def_fields.py: for customizing _LIBRARY
            - _model_....py: for customizing existing models or adding new ones

    Options:
    --------
    reset:      bool
        will overwrite existing files but will preserve added files
    reset_hard: bool
        will remove the whole .pygemmes/ folder and re-create it

    """

    # -----------
    # check input

    if not os.path.isdir(path_user_home):
        msg = (
            "Arg path_user_home must be a valid path!\n"
            f"Provided: {path_user_home}"
        )
        raise Exception(msg)

    if reset is None:
        reset = False
    if not isinstance(reset, bool):
        msg = (
            f"Arg reset must be a bool!\nProvided: {reset}"
        )
        raise Exception(msg)

    if reset_hard is None:
        reset_hard = False
    if not isinstance(reset_hard, bool):
        msg = (
            f"Arg reset_hard must be a bool!\nProvided: {reset_hard}"
        )
        raise Exception(msg)

    # ---------------------------------
    # Check pre-existing private folder

    path_private_pgm = os.path.join(path_user_home, '.pygemmes')

    if os.path.isdir(path_private_pgm):
        if reset_hard is True:
            # remove
            shutil.rmtree(path_private_pgm)
        elif reset is False:
            # do nothing
            return

    # ---------------------
    # Create private folder

    if not os.path.isdir(path_private_pgm):
        os.mkdir(path_private_pgm)

    # -----------------------------------
    # Populate private folder with models

    # models folder
    path_source = os.path.join(_PATH_HERE, '_models')
    path_target = os.path.join(path_private_pgm, '_models')
    if not os.path.isdir(path_target):
        os.mkdir(path_target)

    # create / overwrite models _LIBRARY
    #pfe_source = os.path.join(path_source, '_def_fields.py')
    #pfe_target = os.path.join(path_target, '_def_fields.py')
    #shutil.copy(pfe_source, pfe_target)

    # create / overwrite all existing models
    lf = [
        ff for ff in os.listdir(path_source)
        if ff.startswith('_model_') and ff.endswith('.py')
    ]
    for ff in lf:
        shutil.copy(
            os.path.join(path_source, ff),
            os.path.join(path_target, ff),
        )

    # ------------------------------------------
    # Populate private folder with output folder

    path_target = os.path.join(path_private_pgm, 'output')
    if not os.path.isdir(path_target):
        os.mkdir(path_target)

    return
