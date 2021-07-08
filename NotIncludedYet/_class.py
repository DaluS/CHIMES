# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
import _utils
import _class_checks
import _class_utility


# #############################################################################
# #############################################################################
#                       Main class
# #############################################################################


class Solver():
    """ Generic class
    """

    _MODEL = 'GK'

    def __init__(self, model=None):
        self.__dparam = {}
        self.__dvar = {}
        self.__dfunc = {}
        if model is not None:
            self.set_model(model)

    # ##############
    # model

    def set_model(self, model=None):
        """ Set the parameters, variables and functions for desired model """

        # Set to default if None
        if model is None:
            model = self._MODEL

        # set parameters, variables and functions
        self.set_dparam(model)
        self.set_dvar(model)
        self.set_dfunc(model)

    # ##############
    # parameters

    def set_dparam(self, dparam=None, key=None, value=None):
        """ Set the dict of input parameters (dparam) or a single param """

        # If all None => set to self._PARAMSET
        c0 = dparam is None and key is None and value is None
        if c0 is True:
            dparam = self._MODEL

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

    def get_dparam(self, verb=None, returnas=None, **kwdargs):
        """ Return a copy of the input parameters dict

        Return as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)

        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing
        """

        # list of criteria on which the user can discriminate
        lcrit = ['dimension', 'units', 'type', 'group']

        # list of fields to be printed if verb = True
        lprint = [
            'value', 'units', 'dimension', 'symbol',
            'type', 'group', 'com',
        ]

        return _class_utility._get_dict_subset(
            indict=self.__dparam,
            verb=verb,
            returnas=returnas,
            lcrit=lcrit,
            lprint=lprint,
            keyname='parameter key',
            **kwdargs,
        )

    # ##############
    # variables

    def set_dvar(self, dvar=None):
        """ Set the dict of variables """
        if dvar is None:
            dvar = self._MODEL
        self.__dvar, self.__varset = _class_checks.check_dvar(dvar=dvar)
        self._initialize_var()

    def _initialize_var(self):
        """ Create numpy arrays for each variable, full of nans """

        # Check parameters are set
        if any([ss not in self.__dparam.keys() for ss in ['Nt', 'Nx']]):
            msg = "Variables cannot be initialized => set parameters first"
            raise Exception(msg)

        # initialize variables
        nt = self.__dparam['Nt']['value']
        nx = self.__dparam['Nx']['value']
        for k0 in self.__dvar.keys():
            self.__dvar[k0]['value'] = np.full((nt, nx), np.nan)

    def get_dvar(self, verb=None, returnas=None, **kwdargs):
        """ Return a copy of the variables dict

        Return as:
            - dict: dict
            - 'DataGFrame': a pandas DataFrame
            - np.ndarray: a dict of np.ndarrays
            - False: return nothing (useful of verb=True)

        verb:
            - True: pretty-print the chosen parameters
            - False: print nothing
        """

        # list of criteria on which the user can discriminate
        lcrit = ['shape', 'units', 'dimension']

        # list of fields to be printed if verb = True
        lprint = ['shape', 'units', 'dimension', 'symbol', 'type', 'com']

        return _class_utility._get_dict_subset(
            indict=self.__dvar,
            verb=verb,
            returnas=returnas,
            lcrit=lcrit,
            lprint=lprint,
            keyname='variable key',
            **kwdargs,
        )

    # ##############
    # functions

    def set_dfunc(self, dfunc=None):
        """ Set the dict of functions """
        if dfunc is None:
            dfunc = self._MODEL
        self.__dfunc, self.__funcset = _class_checks.check_dfunc(
            dfunc=dfunc, dparam=self.__dparam, dvar=self.__dvar,
        )

    # ##############
    # show summary

    def get_summary(self):
        """
        Print a str summary of the solver

        """

        # ----------
        # Numerical parameters
        col0 = ['Numerical param.', 'value', 'units', 'comment']
        ar0 = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0['com'],
            ])
            for k0, v0 in self.__dparam.items() if v0['group'] == 'Numerical'
        ]

        # ----------
        # parameters
        col1 = ['Model param.', 'value', 'units', 'group', 'comment']
        ar1 = [
            tuple([
                k0,
                str(v0['value']),
                str(v0['units']),
                v0['group'],
                v0['com'],
            ])
            for k0, v0 in self.__dparam.items() if v0['group'] != 'Numerical'
        ]

        # ----------
        # variables
        col2 = ['variable', 'shape', 'units', 'comment']
        ar2 = [
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
        col3 = ['function', 'args', 'units', 'comment']
        ar3 = [
            tuple([
                k0,
                'f(({}), ({}), ({}))'.format(
                    ', '.join(v0['args_param']),
                    ', '.join(v0['args_var']),
                    ', '.join(v0['args_func']),
                ),
                v0['units'],
                v0['com'],
            ])
            for k0, v0 in self.__dfunc.items()
        ]

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2, ar3],
            lcol=[col0, col1, col2, col3],
            verb=True,
            returnas=False,
        )
