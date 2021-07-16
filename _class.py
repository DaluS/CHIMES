# -*- coding: utf-8 -*-


# Common
import numpy as np
import time

# Library-specific
from utilities import _utils, _class_checks, _class_utility


class Solver():
    """ Generic class
    """

    _MODEL = 'GK'

    def __init__(self, model=None):
        self.__dparam = {}
        self.__func_order = None
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
            func_order = self.__func_order

        # Update to check consistency
        (
            self.__dparam,
            self.__model,
            self.__func_order,
        ) = _class_checks.check_dparam(
            dparam=dparam, func_order=func_order, method=method,
        )

        # store a simplified dict of variable arguments
        # used in reset() and run()
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.__func_order
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
        return self.__func_order

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
            if self.__dparam[k0]['eqtype'] == 'ode':
                self.__dparam[k0]['value'][0, :] = self.__dparam[k0]['initial']
                self.__dparam[k0]['value'][1:, :] = np.nan
            else:
                self.__dparam[k0]['value'][:, :] = np.nan

        # reset intermediary variables and auxiliary variables
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)
        linter_aux = self.__func_order + laux
        for k0 in linter_aux:
            # prepare dict of args
            kwdargs = {
                k1: v1[ii, :]
                for k1, v1 in self.__dargs[k0].items()
            }
            # run function
            self.__dparam[k0]['value'][0, :] = (
                self.__dparam[k0]['func'](**kwdargs)
            )
            # set other time steps to nan
            self.__dparam[k0]['value'][1:, :] = np.nan

        # set run to False
        self.__run = False

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
                v0['source'].split(':')[-1].replace('\n', '').replace(',', ''),
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

    def run(self, compute_auxiliary=None, verb=None):
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
            timewait = False
        elif verb == 2:
            end = '\n'
            flush = False
            timewait = False
        elif type(verb) is float:   # if timewait is a float, then it is the
            end = '\n'              # delta of real time between print
            flush = False
            timewait = True         # will check real time between iteratiions
        else:
            timewait = False

        if compute_auxiliary is None:
            compute_auxiliary = True

        # ------------
        # reset variables
        self.reset()

        # time vector
        nt = self.__dparam['nt']['value']

        # ------------
        # temporary dict of input
        lode = self.get_dparam(eqtype='ode', returnas=list)
        linter = self.__func_order
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        # ------------
        # start time loop
        if timewait:
            t0 = time.time()    # We look at the time between two iterations
            # We removed 2 verb to be sure that we print the first iteration

        for ii in range(1, nt):

            # log if verb > 0
            if verb > 0:
                if not timewait:
                    if ii == nt - 1:
                        end = '\n'
                    msg = (
                        f'time step {ii+1} / {nt}'
                    )
                    print(msg, end=end, flush=flush)
                if timewait:
                    if time.time() - t0 > verb:
                        msg = (
                            f'time step {ii+1} / {nt}'
                        )
                        print(msg, end=end, flush=flush)
                        t0 = time.time()
                    elif (ii == nt - 1 or ii == 1):
                        end = '\n'
                        msg = (
                            f'time step {ii+1} / {nt}'
                        )
                        print(msg, end=end, flush=flush)

            # compute ode variables from ii-1, using rk4
            for k0 in lode:
                kwdargs = {
                    k1: v1[ii-1, :]
                    for k1, v1 in self.__dargs[k0].items()
                }
                self.__dparam[k0]['value'][ii, :] = (
                    self.__dparam[k0]['value'][ii-1, :]
                    + self._rk4(
                        k0=k0,
                        y=self.__dparam[k0]['value'][ii-1, :],
                        kwdargs=kwdargs,
                    )
                )

            # compute intermediary functions, in good order
            # Now that inermediary functions are computed at t=0 in reset()
            # we have to reverse the order of resolution:
            # first ode then intermediary
            for k0 in linter:
                kwdargs = {
                    k1: v1[ii-1, :]
                    for k1, v1 in self.__dargs[k0].items()
                }
                self.__dparam[k0]['value'][ii, :] = (
                    self.__dparam[k0]['func'](
                        **kwdargs
                    )
                )

            # Since the computation is fast we can also compute auxiliary
            if compute_auxiliary:
                for k0 in laux:
                    kwdargs = {
                        k1: v1[ii-1, :]
                        for k1, v1 in self.__dargs[k0].items()
                    }
                    self.__dparam[k0]['value'][ii, :] = (
                        self.__dparam[k0]['func'](
                            **kwdargs
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
        """ To be done (Didier) """
        pass
