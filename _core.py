# -*- coding: utf-8 -*-


# built-in
import time


# Common
import numpy as np


# Library-specific
from utilities import _utils, _class_checks, _class_utility
from utilities import _solvers, _saveload


class Solver():
    """ Generic class
    """

    _MODEL = 'GK'

    def __init__(self, model=None):
        self.__dparam = {}
        self.__dmisc = dict.fromkeys(['model', 'func_order', 'run', 'solver'])
        self.__dargs = {}
        if model is not False:
            self.set_dparam(dparam=model)

    # ##############################
    #  Setting / getting parameters
    # ##############################

    def set_dparam(
        self,
        dparam=None,
        key=None, value=None,
        func_order=None,
        method=None,
    ):
        """ Set the dict of input parameters (dparam) or a single param

        dparam is the large dictionary that contains:
            - fixed-value parameters
            - functions of different types (equations)

        You can provide:
            - dparam as a dict
            - dparam as a str refering to an existing pre-defined model
            - only a key, value pair to change the value of a single parameter

        """

        # If all None => set to self._MODEL
        c0 = dparam is None and key is None and value is None

        if c0 is True:
            print()
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
            func_order = self.__dmisc['func_order']

        # Update to check consistency
        (
            self.__dparam,
            self.__dmisc['model'],
            self.__dmisc['func_order'],
        ) = _class_checks.check_dparam(
            dparam=dparam, func_order=func_order, method=method,
            model=self.__dmisc.get('model')
        )

        # store a simplified dict of variable arguments
        # used in reset() and run()
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.__dmisc['func_order']
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        self.__dargs = {
            k0: {
                k1: self.__dparam[k1]['value']
                for k1 in (
                    self.__dparam[k0]['args']['ode']
                    + self.__dparam[k0]['args']['intermediary']
                    + self.__dparam[k0]['args']['auxiliary']
                )
                if k1 != 'lambda'
            }
            for k0 in lode + linter + laux
        }

        # Handle the lambda exception here to avoid test at every time step
        # if lambda exists and is a function
        c0 = (
            'lambda' in self.__dparam.keys()
            and self.__dparam['lambda'].get('func') is not None
        )
        # then handle the exception
        for k0, v0 in self.__dargs.items():
            if c0 and 'lambda' in self.__dparam[k0]['kargs']:
                self.__dargs[k0]['lamb'] = self.__dparam['lambda']['value']

        # reset all variables
        self.reset()

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
        lcrit = ['dimension', 'units', 'type', 'group', 'eqtype']
        lprint = [
            'parameter', 'value', 'units', 'dimension', 'symbol',
            'type', 'eqtype', 'group', 'comment',
        ]

        return _class_utility._get_dict_subset(
            indict=self.__dparam,
            verb=verb,
            returnas=returnas,
            lcrit=lcrit,
            lprint=lprint,
            **kwdargs,
        )

    # ##############################
    # Read-only properties
    # ##############################

    @property
    def lfunc(self):
        """ List of parameters names that are actually functions """
        return [
            k0 for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') is not None
        ]

    @property
    def func_order(self):
        """ The ordered list of intermediary function names """
        return self.__dmisc['func_order']

    @property
    def model(self):
        """ The model identifier """
        return self.__dmisc['model']

    @property
    def dargs(self):
        return self.__dargs

    @property
    def dmisc(self):
        return self.__dmisc

    @property
    def dparam(self):
        return self.get_dparam(returnas=dict, verb=False)

    # ##############################
    # reset
    # ##############################

    def reset(self):
        """ Re-initializes all variables

        Only the first time step (initial values) is preserved
        All other time steps are set to nan
        """

        # reset ode variables
        for k0 in self.lfunc:
            if k0 == 'time':
                self.__dparam[k0]['value'][0] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:] = np.nan
            elif self.__dparam[k0]['eqtype'] == 'ode':
                self.__dparam[k0]['value'][0, :] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:, :] = np.nan
            else:
                self.__dparam[k0]['value'][:, :] = np.nan

        # reset intermediary variables and auxiliary variables
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)
        linter_aux = self.__dmisc['func_order'] + laux
        for k0 in linter_aux:
            # prepare dict of args
            kwdargs = {
                k1: v1[0, :]
                for k1, v1 in self.__dargs[k0].items()
            }
            # run function
            self.__dparam[k0]['value'][0, :] = (
                self.__dparam[k0]['func'](**kwdargs)
            )
            # set other time steps to nan
            self.__dparam[k0]['value'][1:, :] = np.nan

        # set run to False
        self.__dmisc['run'] = False

    # ##############################
    # variables
    # ##############################

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

    # ##############################
    #  Introspection
    # ##############################

    def __repr__(self):
        """ This is automatically called when only the instance is entered """
        col0 = ['model', 'source', 'nb. model param', 'nb. functions', 'run']
        ar0 = [
            list(self.__dmisc['model'].keys())[0],
            list(self.__dmisc['model'].values())[0],
            len([
                k0 for k0, v0 in self.__dparam.items()
                if v0.get('func') is None
            ]),
            len(self.lfunc),
            self.__dmisc['run'],
        ]
        return _utils._get_summary(
            lar=[ar0],
            lcol=[col0],
            verb=False,
            returnas=str,
        )

    def get_summary(self, idx=0):
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
        col2 = ['function', 'source', 'initial', 'units', 'eqtype', 'comment']
        ar2 = [
            tuple([
                k0,
                v0['source_exp'],
                "{:.2e}".format(v0.get('value')[0, idx]),
                str(v0['units']),
                v0['eqtype'].replace('intermediary', 'inter').replace(
                    'auxiliary', 'aux',
                ),
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

    # ##############################
    # run simulation
    # ##############################

    def run(
        self,
        compute_auxiliary=None,
        solver=None,
        verb=None,
        rtol=None,
        atol=None,
        max_time_step=None,
    ):
        """ Run the simulation

        Compute each time step from the previous one using:
            - parameters
            - differentials (ode)
            - intermediary functions in specified func_order

        """
        # ------------
        # check inputs
        (
            verb, end, flush, timewait,
            compute_auxiliary, solver, solver_scipy,
        ) = _class_checks._run_check(
            verb=verb, compute_auxiliary=compute_auxiliary, solver=solver,
        )

        # ------------
        # reset variables
        self.reset()

        # time vector
        nt = self.__dparam['nt']['value']

        # ------------
        # temporary dict of input
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.__dmisc['func_order']
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        # ------------
        # start time loop
        if timewait:
            t0 = time.time()    # We look at the time between two iterations

        if solver == 'eRK4-homemade':

            _solvers._eRK4_homemade(
                dparam=self.__dparam,
                lode=lode,
                linter=linter,
                laux=laux,
                dargs=self.__dargs,
                nt=nt,
                verb=verb,
                timewait=timewait,
                end=end,
                flush=flush,
                compute_auxiliary=compute_auxiliary,
            )

        elif 'scipy' in solver:
            sol = _solvers._solver_scipy(
                dparam=self.__dparam,
                lode=lode,
                linter=linter,
                dargs=self.__dargs,
                verb=verb,
                rtol=rtol,
                atol=atol,
                max_time_step=max_time_step,
                solver_scipy=solver_scipy,
            )

        self.__dmisc['run'] = True
        self.__dmisc['solver'] = solver

    # ##############################
    #       plotting methods
    # ##############################

    def plot(self):
        """ To be done (Paul?)

        Advice: put all plotting functions in a dedicated _plot.py module
        """
        pass

    # ##############################
    #       data conversion
    # ##############################

    def _to_dict(self):
        """ Convert instance to dict """

        dout = {
            'dparam': self.get_dparam(returnas=dict, verb=False),
            'dmisc': dict(self.__dmisc),
            'dargs': dict(self.__dargs),
        }
        return dout

    @classmethod
    def _from_dict(cls, dout=None):
        """ Create an instance from a dict """

        # --------------
        # check inputs
        c0 = (
            isinstance(dout, dict)
            and sorted(dout.keys()) == ['dargs', 'dmisc', 'dparam']
            and all([isinstance(dd, dict) for dd in dout.values()])
        )
        if not c0:
            msg = (
                "Arg dout must be a dict of the form:\n"
                "{'dargs': dict, 'dmisc': dict, 'dparams': dict}\n"
                f"You provided:\n{dout}"
            )
            raise Exception(msg)

        # -------------
        # reformat func from source
        for k0, v0 in dout['dparam'].items():
            if dout['dparam'][k0].get('func') is not None:
                dout['dparam'][k0]['func'] = eval(
                    f"lambda {dout['dparam'][k0]['source_kargs']}: "
                    f"{dout['dparam'][k0]['source_exp']}"
                )[0]

        # -------------------
        # create instance
        obj = cls(model=False)
        obj.__dparam = {k0: dict(v0) for k0, v0 in dout['dparam'].items()}
        obj.__dmisc = dict(dout['dmisc'])
        obj.__dargs = dict(dout['dargs'])

        return obj

    # ##############################
    #       saving methods
    # ##############################

    def save(self, path=None, name=None, fmt=None, verb=None):
        """ Save the instance

        Saved files are stored in path/fullname.ext
        The extension (ext) depends on the format (fmt) chosen for saving
        The file full name (fullname) is the concatenation of a base default
        name and a user-defined name.
            ex.: Output_MODELNAME_USERDEFINEDNAME.ext
        where MODELNAME is the model's name

        By default path is set to 'output/', but the user can overload it

        """

        return _saveload.save(
            self,
            path=path,
            name=name,
            fmt=fmt,
            verb=verb,
        )

    # ##############################
    #       replication methods
    # ##############################

    def copy(self):
        """ Return a copy of the instance """

        dout = self._to_dict()
        return self.__class__._from_dict(dout=dout)

    # ##############################
    #       comparison methods
    # ##############################

    def __eq__(self, other, verb=None, return_dfail=None):
        """ Automatically called when testing obj1 == obj2 """
        return _class_utility._equal(
            self, other,
            verb=verb,
            return_dfail=return_dfail,
        )
