# -*- coding: utf-8 -*-

# %% Importations ###########

# built-in
import time


# Common
import numpy as np


# Library-specific
from utilities import _utils, _class_checks, _class_utility
from utilities import _solvers, _saveload
import _plots as plots


class Hub():
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
    # %% Setting / getting parameters
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
                + "{}\n".format(lstr)
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
        
        if verb is None and returnas is None:
            print("")

        return _class_utility._get_dict_subset(
            indict=self.__dparam,
            verb=verb,
            returnas=returnas,
            lcrit=lcrit,
            lprint=lprint,
            **kwdargs,
        )

    # ##############################
    # %% Read-only properties
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
        # Define shape of model system
        sys_shape = [self.__dparam['nt']['value'],
                     self.__dparam['nx']['value']]
        lode = self.get_dparam(eqtype='ode', returnas=list)
        lpde = self.get_dparam(eqtype='pde', returnas=list)
        linter = self.__dmisc['func_order']
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        # Create and initialize evolving variables
        for k0 in lode + lpde:
            var_shape = ([] if self.__dparam[k0]['eqtype'] == 'ode'
                         else list(self.__dparam[k0]['initial'].shape))
            self.__dparam[k0]['value'] = np.full(sys_shape + var_shape, np.nan)
            self.__dparam[k0]['value'][0] = self.__dparam[k0]['initial']

        # Add references in dict of arguments to newly initialized values
        # handling any lambda exception here rather than at each time step
        self.__dargs = {
            k0: {
                'lamb' if k1 == 'lambda' else k1: self.__dparam[k1]['value']
                for k1 in (self.__dparam[k0]['args']['ode']
                           + self.__dparam[k0]['args']['pde'])
            }
            for k0 in lode + lpde + linter + laux
        }

        # Create and initialize intermediary variables and auxiliary variables
        for k0 in linter + laux:
            # prepare dict of args
            kwdargs = {k1: v1[0] for k1, v1 in self.__dargs[k0].items()}
            # calculate inital value and use it to initialize the value array
            initial_value = self.__dparam[k0]['func'](**kwdargs)
            is_scalar = np.isscalar(initial_value) or initial_value.size == 1
            var_shape = [] if is_scalar else list(initial_value.shape)
            self.__dparam[k0]['value'] = np.full(sys_shape + var_shape, np.nan)
            self.__dparam[k0]['value'][0] = initial_value
            # Add references in dict of arguments to newly initialized values,
            # handling any lambda exception here rather than at each time step
            ref = 'lamb' if k0 == 'lambda' else k0
            for k1 in lode + lpde + linter + laux:
                if k0 in (self.__dparam[k1]['args']['ode']
                          + self.__dparam[k1]['args']['pde']
                          + self.__dparam[k1]['args']['intermediary']
                          + self.__dparam[k1]['args']['auxiliary']):
                    self.__dargs[k1][ref] = self.__dparam[k0]['value']

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
        leqtype = ['ode', 'pde', 'intermediary', 'auxiliary']
        if eqtype is None:
            eqtype = ['ode', 'pde', 'intermediary']
        if isinstance(eqtype, str):
            eqtype = [eqtype]
            if any([ss not in leqtype for ss in eqtype]):
                msg = (
                    f"eqtype must be in {leqtype}\n"
                    f"You provided: {eqtype}"
                )
                raise Exception(msg)

        # Define shape of model system
        sys_shape = [self.__dparam['nt']['value'],
                     self.__dparam['nx']['value']]

        # list of keys of variables
        keys = np.hstack([
            np.repeat(k0, np.prod(v0['value'].shape[len(sys_shape):]))
            for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') in leqtype
        ])

        # Get compact variable array
        variables = np.concatenate([
            v0['value'].reshape(sys_shape + [-1])
            for k0, v0 in self.__dparam.items()
            if v0.get('eqtype') in leqtype
        ], axis=len(sys_shape))

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
        value_str = (lambda value, fmt="{}":
                     fmt.format(value) if np.isscalar(value)
                     else f"{value.shape} array")

        # ----------
        # Numerical parameters
        col0 = ['Numerical param.', 'value', 'units', 'comment']
        ar0 = [
            [
                k0,
                value_str(v0['value']),
                str(v0['units']),
                v0['com'],
            ]
            for k0, v0 in self.__dparam.items() if v0['group'] == 'Numerical'
        ]
        ar0.append(['run', str(self.__dmisc['run']), '', ''])

        larr = [f"{k0}:\n"
                f"    {v0['value']}" for k0, v0 in self.__dparam.items()
                if v0['group'] == 'Numerical' and not np.isscalar(v0['value'])]
        if len(larr) > 0:
            ps0 = ("\n"
                   "Numerical param. array values:\n"
                   "-----------------------------\n"
                   + '\n'.join(larr))
        else:
            ps0 = ""

        # ----------
        # parameters
        col1 = ['Model param.', 'value', 'units', 'group', 'comment']
        ar1 = [
            [
                k0,
                value_str(v0['value']),
                str(v0['units']),
                v0['group'],
                v0['com'],
            ]
            for k0, v0 in self.__dparam.items()
            if v0['group'] != 'Numerical'
            and v0.get('func') is None
        ]

        larr = [f"{k0}:\n"
                f"    {v0['value']}" for k0, v0 in self.__dparam.items()
                if v0['group'] != 'Numerical'
                and v0.get('func') is None
                and not np.isscalar(v0['value'])]
        if len(larr) > 0:
            ps1 = ("\n\n\n"
                   "Model param. array values:\n"
                   "-------------------------\n"
                   + '\n'.join(larr))
        else:
            ps1 = ""

        # ----------
        # functions
        col2 = ['function', 'source', 'initial',
                'units', 'eqtype', 'comment']
        ar2 = [
            [
                k0,
                'See below' if 'return' in v0['source_exp']
                else v0['source_exp'],
                value_str(v0['value'][0, idx], fmt="{:.2e}"),
                str(v0['units']),
                v0['eqtype'].replace('intermediary', 'inter').replace(
                    'auxiliary', 'aux',
                ),
                v0['com'],
            ]
            for k0, v0 in self.__dparam.items()
            if v0.get('func') is not None
        ]

        lexp = [(f"def d_t {k0}:" if v0['eqtype'] == 'ode' else
                 f"def \\partial_t {k0}:" if v0['eqtype'] == 'pde' else
                 f"def {k0}:")
                + v0['source_exp']
                for k0, v0 in self.__dparam.items()
                if v0.get('func') is not None
                and 'return' in v0['source_exp']]
        if len(lexp) > 0:
            ps2 = ("\n\n"
                   "Multi-line functions:\n"
                   "--------------------\n"
                   + '\n'.join(lexp))
        else:
            ps2 = ""
        larr = [f"{k0}:\n"
                f"    {v0['value'][0, idx]}"
                for k0, v0 in self.__dparam.items()
                if v0['group'] != 'Numerical'
                and v0.get('func') is not None
                and not np.isscalar(v0['value'][0, idx])]
        if len(larr) > 0:
            ps2 += ("\n"
                    "Initial array values:\n"
                    "--------------------\n"
                    + '\n'.join(larr))

        # --------------------------
        # Add solver and final value if has run
        if self.__dmisc['run'] is True:

            # add solver
            ar0.append(['solver', self.__dmisc['solver'], '', ''])

            # add column title
            col2.insert(3, 'final')

            # add value to each variable
            ii = 0
            for k0, v0 in self.__dparam.items():
                if v0.get('func') is not None:
                    ar2[ii].insert(
                        3,
                        value_str(v0.get('value')[-1, idx], fmt="{:.2e}"),
                    )
                    ii += 1

            # add final values to postscript
            larr = [f"{k0}:\n"
                    f"    {v0['value'][0, idx]}"
                    for k0, v0 in self.__dparam.items()
                    if v0['group'] != 'Numerical'
                    and v0.get('func') is not None
                    and not np.isscalar(v0['value'][-1, idx])]
            if len(larr) > 0:
                ps2 += ("\n\n"
                        "Final array values:\n"
                        "------------------\n"
                        + '\n'.join(larr))

        # ----------
        # format output
        return _utils._get_summary(
            lar=[ar0, ar1, ar2],
            lcol=[col0, col1, col2],
            lps=[ps0, ps1, ps2],
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
        lpde = self.get_dparam(eqtype='pde', returnas=list)
        linter = self.__dmisc['func_order']
        laux = self.get_dparam(eqtype='auxiliary', returnas=list)

        # ------------
        # start time loop
        if solver == 'eRK4-homemade':

            _solvers._eRK4_homemade(
                dparam=self.__dparam,
                lode=lode,
                lpde=lpde,
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
    #       Deep analysis methods
    # ##############################

    def FillCyclesForAll(self, ref=None):
        '''
        This function is a wrap-up on GetCycle to do it on all variables.

        For each variables, it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself
        '''

        for var, dic1 in self.__dparam.items():
            if 'func' in dic1.keys():
                if ref is None:
                    self.FillCycles(var, var)
                else:
                    self.FillCycles(var, ref)

    def FillCycles(self, var, ref='lambda'):
        '''
        it calculates the cycles properties
        ref is the reference variable on which the time of cycles is determined
        by default the variable detect cycles in itself

        var : name of the variable we are working on
        ref : reference for the oscillations detections
        '''

        # Check if the run did occur

        # Get the new dictionnary to edit
        dic = self.__dparam[var]
        if 'cycles' not in dic.keys():
            dic['cycles'] = {'reference': ref}
            '''
'period_indexes': [],  # [[idx1,idx2],[idx2,idx3],] index of borders
# for each period
'period_T_intervals': [],  # [t[idx1,t[idx2]],..] time of borders
't_mean_cycle': [],  # [(t[idx1+t[idx2])/2.],..]
# time of the middle of the cycle
'period_T': [],  # duration of the cycle
'meanval': [],  # mean value during the interval
'stdval': [],   # standard deviation during the interval
'minval': [],   # minimal value in the interval
'maxval': [],   # maximal value in the interval
'reference': ref,  # the variable that has been used to detect cycle
}
            '''

        # check if reference has already calculated its period
        # the reference has cycle and this cycle has been calculated on itself
        dic1 = dic['cycles']
        ready = False
        if 'cycles' in self.__dparam[ref].keys():
            dic2 = self.__dparam[ref]['cycles']
            if (dic2['reference'] == ref and 'period_indexes' in dic2):
                # We can take the reference as the base
                ready = True
        # If there is no good reference
        # We calculate it and put
        if not ready:
            self.findCycles(ref)
            dic2 = self.__dparam[ref]['cycles']

        for key in ['period_indexes', 'period_T_intervals',
                    't_mean_cycle', 'period_T']:
            dic1[key] = dic2[key]

        tim = self.__dparam['time']['value']
        dic1['period_T_intervals'] = [[tim[idx[0], 0], tim[idx[1], 0]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]

        # Fill for each the characteristics
        values = dic['value']
        dic1['meanval'] = [np.mean(values[idx[0]:idx[1]])
                           for idx in dic1['period_indexes']]
        dic1['medval'] = [np.median(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['stdval'] = [np.std(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['minval'] = [np.amin(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]
        dic1['maxval'] = [np.amax(values[idx[0]:idx[1]])
                          for idx in dic1['period_indexes']]

    def findCycles(self, refval):
        '''
        Detect all positions of local maximums and the time that is linked
        '''
        # initialisation
        periods = []
        id1 = 1

        self.__dparam[refval]['cycles'] = {}

        dic1 = self.__dparam[refval]['cycles']
        val = self.__dparam[refval]['value']

        # identification loop
        while id1 < len(val) - 2:
            if (val[id1] > val[id1 - 1] and
                    val[id1] > val[id1 + 1]):
                periods.append(1 * id1)
            id1 += 1

        # Fill the formalism
        self.__dparam[refval]['cycles']['period_indexes'] = [
            [periods[i], periods[i + 1]] for i in range(len(periods) - 1)
        ]
        tim = self.__dparam['time']['value']
        dic1 = self.__dparam[refval]['cycles']
        dic1['period_T_intervals'] = [[tim[idx[0]], tim[idx[1]]]
                                      for idx in dic1['period_indexes']]
        dic1['t_mean_cycle'] = [
            (t[0] + t[1]) / 2 for t in dic1['period_T_intervals']]
        dic1['period_T'] = [
            (t[1] - t[0]) for t in dic1['period_T_intervals']]
        dic1['reference'] = refval

        # ##############################
        #       plotting methods
        # ##############################

    def plot(self):
        """
        Launch all the basic plots
        """

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
