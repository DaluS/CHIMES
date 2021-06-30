# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
import _utils
import _class_checks


class Solver():
    """ Generic class
    """

    _MODEL = 'v0'
    _PARAMSET = _MODEL
    _VARSET = 'GK'

    def __init__(self):
        self.__dparam = {}
        self.__dvar = {}
        self.__dfunc = {}

    # ##############
    # parameters

    def set_dparam(self, dparam=None, key=None, value=None):
        """ Set the dict of input parameters (dparam) or a single param """

        # If all None => set to self._PARAMSET
        c0 = dparam is None and key is None and value is None
        if c0 is True:
            dparam = self._PARAMSET

        # Check input: dparam xor (key, value)
        lc = [
            dparam is not None,
            key is not None and value is not None,
        ]
        if np.sum(lc) != 1:
            lstr = [
                '\t- {}: {}'.format(kk, vv)
                for kk, vv in [
                    ('dparam', dparam), ('key', key), ('value', value)
                ]
            ]
            msg = (
                "Please provide dparam xor (key, value)!\n"
                + "You provided:\n"
                + "\n".format(lstr)
            )
            raise Exception(msg)

        # set dparam or update desired key
        if dparam is not None:
            self.__dparam, self.__paramset = _class_checks.check_dparam(
                dparam=dparam,
            )
        else:
            if key not in self.__dparam.keys():
                msg = (
                    "key {} is not identified!\n".format(key)
                    + "See get_dparam() method"
                )
                raise Exception(msg)
            self.__dparam[key]['value'] = value
            self.__paramset = None

        # Update to check consistency
        _class_checks.update_dparam(dparam=self.__dparam)

    def get_dparam(self, returnas=None):
        """ Return a copy of the input parameters dict

        Return as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
        """

        # check input
        if returnas is None:
            returnas = dict

        # return
        if returnas is dict:
            # return a copy of the dict
            return {k0: dict(v0) for k0, v0 in self.__dparam.items()}

        elif returnas in [np.ndarray, 'DataFrame']:
            lk = list(self.__dparam.keys())
            out = {
                'key': np.array(lk, dtype=str),
                'value': np.array([
                    np.nan if self.__dparam[k0]['value'] is None
                    else self.__dparam[k0]['value']
                    for k0 in lk
                ]),
                'com': np.array([self.__dparam[k0]['com'] for k0 in lk]),
                'units': np.array([
                    str(self.__dparam[k0]['units']) for k0 in lk
                ]),
            }
            if returnas == 'DataFrame':
                import pandas as pd
                return pd.DataFrame.from_dict(out)
            else:
                return out


    # ##############
    # variables

    def set_dvar(self, dvar=None):
        """ Set the dict of variables """
        if dvar is None:
            dvar = self._VARSET
        self.__dvar, self.__varset = _class_checks.check_dvar(dvar=dvar)
        self._initialize_var()

    def _initialize_var(self):
        """ Create numpy arrays for each variable, full of nans """
        nt = self.__dparam['Nt']['value']
        nx = self.__dparam['Nx']['value']
        for k0 in self.__dvar.keys():
            self.__dvar[k0]['value'] = np.full((nt, nx), np.nan)

    # ##############
    # functions


    # ##############
    # show summary

    def get_summary(self):
        """
        Print a str summary of the solver

        """

        # ----------
        # parameters
        col0 = ['parameter', 'value', 'units', 'group', 'comment']
        ar0 = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0['group'],
                v0['com'],
            ])
            for k0, v0 in self.__dparam.items()
        ]

        # ----------
        # variables
        col1 = ['variable', 'shape', 'units', 'comment']
        ar1 = [
            tuple([
                k0,
                'None' if v0['value'] is None else str(v0['value'].shape),
                str(v0['units']),
                v0['com'],
            ])
            for k0, v0 in self.__dvar.items()
        ]

        # ----------
        # functions
        col2 = ['function', 'comment']
        ar2 = [
            tuple([
                k0,
                v0['com'],
            ])
            for k0, v0 in self.__dfunc.items()
        ]

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2],
            lcol=[col0, col1, col2],
            verb=True,
            returnas=False,
        )




