# -*- coding: utf-8 -*-


# Common
import numpy as np


# Library-specific
from utilities import _utils, _class_checks


class Solver():
    """ Generic class
    """

    _MODEL = 'GK'

    def __init__(self, model=None):
        self.__dparam = {}
        self.__func_order = None
        if model is not None:
            self.set_dparam(dparam=model)
        self.__run = False

    # ##############
    # parameters

    def set_dparam(
        self,
        dparam=None,
        key=None, value=None,
        func_order=None,
        method=None,
    ):
        """ Set the dict of input parameters (dparam) or a single param """

        # If all None => set to self._PARAMSET
        c0 = dparam is None and key is None and value is None
        if c0 is True:
            dparam = self._MODEL

        # Check input: dparam xor (key, value)
        lc = [
            dparam is not None or func_order is not None,
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
                "Please provide dparam/func_order xor (key, value)!\n"
                + "You provided:\n"
                + "\n".format(lstr)
            )
            raise Exception(msg)

        # set dparam or update desired key
        if dparam is None:
            if func_order is not None:
                dparam = self.__dparam
            elif key not in self.__dparam.keys():
                msg = (
                    "key {} is not identified!\n".format(key)
                    + "See get_dparam() method"
                )
                raise Exception(msg)
            dparam = dict(self.__dparam)
            dparam[key]['value'] = value

        # func_order as previous if not provided
        if func_order is None:
            func_order = self.__func_order

        # Update to check consistency
        (
            self.__dparam,
            self.__model,
            self.__func_order,
        ) = _class_checks.check_dparam(
            dparam=dparam, func_order=func_order, method=method,
        )

        # reset variable
        self.reset()

    # #############
    # Read-only properties

    @property
    def lfunc(self):
        return [
            k0 for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') is not None
        ]

    @property
    def func_order(self):
        return self.__func_order

    # #############
    # reset

    def reset(self):
        """ Re-initializes all variables

        Only the first time step (initial values) is preserved
        All other time steps are set to nan
        """

        # reset ode variables
        for k0 in self.lfunc:
            if self.__dparam[k0]['eqtype'] == 'ode':
                self.__dparam[k0]['value'][0, :] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:, :] = np.nan
            else:
                self.__dparam[k0]['value'][:, :] = np.nan
        self.__run = False

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

        # ----------------------
        # check input

        if returnas is None:
            returnas = dict
        if verb is None:
            verb = returnas is False

        # ----------------------
        # select relevant parameters

        if len(kwdargs) > 0:
            # isolate relevant criteria
            dcrit = {
                k0: v0 for k0, v0 in kwdargs.items()
                if k0 in ['dimension', 'units', 'type', 'group', 'eqtype']
            }

            # select param keys matching all critera
            lk = [
                k0 for k0 in self.__dparam.keys()
                if all([
                    self.__dparam[k0].get(k1) == dcrit[k1]
                    for k1 in dcrit.keys()
                ])
            ]
        else:
            lk = list(self.__dparam.keys())

        # ----------------------
        # Optional print

        if verb is True:
            col0 = [
                'parameter', 'value', 'units', 'dim.', 'symbol',
                'type', 'group', 'comment',
            ]
            ar0 = [
                tuple([
                    k0,
                    str(self.__dparam[k0]['value'].shape)
                    if self.__dparam[k0].get('func') is not None
                    else str(self.__dparam[k0]['value']),
                    str(self.__dparam[k0]['units']),
                    str(self.__dparam[k0]['dimension']),
                    str(self.__dparam[k0]['symbol']),
                    str(self.__dparam[k0]['type']),
                    self.__dparam[k0]['group'],
                    self.__dparam[k0]['com'],
                ])
                for k0 in lk
            ]
            _utils._get_summary(
                lar=[ar0],
                lcol=[col0],
                verb=True,
                returnas=False,
            )

        # ----------------------
        # return as dict or array

        if returnas is dict:
            # return a copy of the dict
            return {k0: dict(self.__dparam[k0]) for k0 in lk}

        elif returnas in [np.ndarray, 'DataFrame']:
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

    def get_variables_compact(self, eqtype=None):
        """ Return a compact numpy arrays containing all variable

        Return
            - compact np.ndarray of all variables
            - list of variable names, in the same order
            - array of indices
        """
        # check inputs
        leqtype = ['ode', 'intermediary', 'auxiliary']
        if eqtype is None:
            eqtype = ['ode', 'intermediary']
        if isinstance(eqtype, str):
            eqtype = [eqtype]
            if any([ss not in leqtype for ss in eqtype]):
                msg = (
                    f"eqtype must be in {leqtype}\n"
                    f"You provided: {eqtype}"
                )
                raise Exception(msg)

        # list of keys of variables
        keys = np.array([
            k0 for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') in leqtype
        ], dtype=str)

        # get compact variable array
        variables = np.swapaxes([
            self.__dparam[k0]['value'] for k0 in keys
        ], 0, 1)

        return keys, variables

    # ##############
    # show summary

    def __repr__(self):
        col0 = ['model', 'source', 'nb. model param', 'nb. functions', 'run']
        ar0 = [
            list(self.__model.keys())[0],
            list(self.__model.values())[0],
            len([
                k0 for k0, v0 in self.__dparam.items()
                if v0.get('func') is None
            ]),
            len(self.lfunc),
            self.__run,
        ]
        return _utils._get_summary(
            lar=[ar0],
            lcol=[col0],
            verb=False,
            returnas=str,
        )

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
            for k0, v0 in self.__dparam.items()
            if v0['group'] != 'Numerical'
            and v0.get('func') is None
        ]

        # ----------
        # functions
        col2 = ['function', 'source', 'shape', 'units', 'eqtype', 'comment']
        ar2 = [
            tuple([
                k0,
                v0['source'].split(':')[-1].replace('\n', '').replace(',', ''),
                str(v0['value'].shape),
                str(v0['units']),
                v0['eqtype'],
                v0['com'],
            ])
            for k0, v0 in self.__dparam.items()
            if v0.get('func') is not None
        ]

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2],
            lcol=[col0, col1, col2],
            verb=True,
            returnas=False,
        )

    # ----------
    # run simulation

    def run(self, verb=None):
        """ Run the simulation

        Compute each time step from the previous one using:
            - parameters
            - differentials (ode)
            - intermediary functions in specified func_order

        """
        # ------------
        # check inputs
        if verb in [None, True]:
            verb = 1
        if verb == 1:
            end = '\r'
            flush = True
        elif verb == 2:
            end = '\n'
            flush = False

        # ------------
        # reset variables
        self.reset()

        # time vector
        nt = self.__dparam['nt']['value']

        # ------------
        # temporary dict of input
        lode = list(self.get_dparam(eqtype='ode').keys())
        linter = self.__func_order
        dargs = {
            k0: (
                self.__dparam[k0]['args']['ode']
                + self.__dparam[k0]['args']['intermediary']
            )
            for k0 in lode + linter
        }

        # ------------
        # start time loop
        for ii in range(nt):

            # log if verb > 0
            if verb > 0:
                if ii == nt - 1:
                    end = '\n'
                msg = (
                    f'time step {ii+1} / {nt}'
                )
                print(msg, end=end, flush=flush)

            # compute intermediary functions, in good order
            for k0 in linter:
                kwdargs = {
                    k1: self.__dparam[k1]['value'][ii, :]
                    for k1 in dargs[k0]
                }
                if 'lambda' in dargs[k0]:
                    kwdargs['lamb'] = kwdargs['lambda']
                    del kwdargs['lambda']
                self.__dparam[k0]['value'][ii, :] = (
                    self.__dparam[k0]['func'](
                        **kwdargs
                    )
                )

            # no need to compute ode of next step if already at last time step
            if ii == nt - 1:
                break

            # compute ode variables from ii-1, using rk4
            for k0 in lode:
                kwdargs = {
                    k1: self.__dparam[k1]['value'][ii, :] for k1 in dargs[k0]
                }
                if 'lambda' in dargs[k0]:
                    kwdargs['lamb'] = kwdargs['lambda']
                    del kwdargs['lambda']

                self.__dparam[k0]['value'][ii+1, :] = (
                    self.__dparam[k0]['value'][ii, :]
                    + self._rk4(
                        k0=k0,
                        y=self.__dparam[k0]['value'][ii, :],
                        kwdargs=kwdargs,
                    )
                )
        self.__run = True

    def _rk4(self, k0=None, y=None, kwdargs=None):
        """
        a traditional RK4 scheme, with:
            - y = array of all variables
            - p = parameter dictionnary
        dt is contained within p
        """
        if 'itself' in self.__dparam[k0]['kargs']:
            dy1 = self.__dparam[k0]['func'](itself=y, **kwdargs)
            dy2 = self.__dparam[k0]['func'](itself=y+dy1/2., **kwdargs)
            dy3 = self.__dparam[k0]['func'](itself=y+dy2/2., **kwdargs)
            dy4 = self.__dparam[k0]['func'](itself=y+dy3, **kwdargs)
        else:
            dy1 = self.__dparam[k0]['func'](**kwdargs)
            dy2 = self.__dparam[k0]['func'](**kwdargs)
            dy3 = self.__dparam[k0]['func'](**kwdargs)
            dy4 = self.__dparam[k0]['func'](**kwdargs)
        return (dy1 + 2*dy2 + 2*dy3 + dy4) * self.__dparam['dt']['value']/6.

    # ##############################
    #       plotting methods
    # ##############################

    def plot(self):
        """ To be done (Paul?)

        Advice: put all plotting functions in a dedicated _plot.py module
        """
        pass

    # ##############################
    #       saving methods
    # ##############################

    def save(self):
        """ To be done (me) """
        pass
