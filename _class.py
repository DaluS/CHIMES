# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
import _utils
import _class_checks


class Solver():
    """ Generic class
    """

    _PARAMSET = 'v0'

    def __init__(self):
        self.__dinput = {}

    def set_dinput(self, dinput=None, key=None, value=None):
        """ Set the dict of input parameters (dinput) or a single param """

        # If all None => set to self._PARAMSET
        c0 = dinput is None and key is None and value is None
        if c0 is True:
            dinput = self._PARAMSET

        # Check input: dinput xor (key, value)
        lc = [
            dinput is not None,
            key is not None and value is not None,
        ]
        if np.sum(lc) != 1:
            lstr = [
                '\t- {}: {}'.format(kk, vv)
                for kk, vv in [
                    ('dinput', dinput), ('key', key), ('value', value)
                ]
            ]
            msg = (
                "Please provide dinput xor (key, value)!\n"
                + "You provided:\n"
                + "\n".format(lstr)
            )
            raise Exception(msg)

        # set dinput or update desired key
        if dinput is not None:
            self.__dinput = _class_checks.check_dinput(dinput=dinput)
        else:
            if key not in self.__dinput.keys():
                msg = (
                    "key {} is not identified!\n".format(key)
                    + "See get_dinput() method"
                )
                raise Exception(msg)
            self.__dinput[key]['value'] = value

        # Update to check consistency
        _class_checks.update_dinput(dinput=self.__dinput)

    def get_dinput(self, verb=None, returnas=None):
        """ Return a copy of the input parameters dict

        Return as:
            - False: do not return
            - dict: dict
            - str: message to be printed
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays

        if verb = True the message is automatically printed

        """

        lcol = ['key', 'value', 'units', 'group', 'comment']
        lar = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0['group'],
                v0['com'],
            ])
            for k0, v0 in self.__dinput.items()
        ]
        msg = _utils._get_summary(
            lar=[lar],
            lcol=[lcol],
            verb=verb,
            returnas=str,
        )
        if returnas is str:
            return msg
        elif returnas is dict:
            # return a copy of the dict
            return {k0: dict(v0) for k0, v0 in self.__dinput.items()}
        elif returnas in [np.ndarray, 'DataFrame']:
            lk = list(self.__dinput.keys())
            out = {
                'key': np.array(lk, dtype=str),
                'value': np.array([
                    np.nan if self.__dinput[k0]['value'] is None
                    else self.__dinput[k0]['value']
                    for k0 in lk
                ]),
                'com': np.array([self.__dinput[k0]['com'] for k0 in lk]),
                'units': np.array([
                    str(self.__dinput[k0]['units']) for k0 in lk
                ]),
            }
            if returnas == 'DataFrame':
                import pandas as pd
                return pd.DataFrame.from_dict(out)

    def initialize(self):
        pass













